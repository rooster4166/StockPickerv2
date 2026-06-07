"""The orchestrator / PM (design spec B.3).

A single deep dive, one configuration. The PM delegates to context-isolated
specialist subagents in strict dependency order, fuses their cited briefs at a
**code-enforced consolidation gate** (valuation literally cannot run until the
assumption set exists), runs the adaptive code-executed valuation price-blinded,
then hands the thesis to a decorrelated red-team.

``Orchestrator(...).analyze()`` returns one run's result; ``ensemble.py`` runs
several decorrelated configurations to derive a confidence signal.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Optional

from ..config import SETTINGS, Settings
from ..data.types import CompanyData
from ..llm.agent import Agent
from . import valuation as val
from .phases import ORDERED_PHASES, SPECIALIST_SYSTEM
from .redteam import red_team
from .schemas import CONSOLIDATION_SCHEMA

log = logging.getLogger(__name__)


@dataclass
class OrchestratorConfig:
    """One decorrelated configuration of the deep-dive engine."""

    model: Optional[str] = None
    redteam_model: Optional[str] = None
    effort: Optional[str] = None
    # A short framing nudge appended to phase prompts to decorrelate runs without
    # relying on sampling temperature (removed on Opus 4.8).
    framing: str = ""


_CONSOLIDATION_PROMPT = """You are the portfolio manager. Below are four cited \
specialist briefs on a price-blinded micro-cap. Fuse them into ONE grounded \
assumption set and choose the valuation method that best fits this business \
(dcf for stable cash generators, rnpv for binary-catalyst names, nav for \
asset-heavy names, comps where peers are clean). Return the required JSON.

=== FINANCIAL TRENDS ===
{financials}

=== BUSINESS MODEL ===
{business}

=== INDUSTRY + ADJACENT EXPOSURE ===
{industry}

=== NEWS + CATALYSTS ===
{news}
"""

_VALUATION_PROMPT = """Using the consolidated assumption set, produce the inputs \
for a CODE-EXECUTED valuation. You reason to the assumptions; arithmetic is done \
deterministically downstream, so be precise and numeric. You are PRICE-BLINDED — \
do not infer or anchor to a market price.

Chosen method: {method}
Assumption summary: {summary}
Key drivers: {drivers}

Return JSON with this exact shape:
{{
  "method": "{method}",
  "scenario_sets": {{
    "bear": {{ ...assumptions... }},
    "base": {{ ...assumptions... }},
    "bull": {{ ...assumptions... }}
  }},
  "valuation_notes": "one short paragraph"
}}

Each of bear/base/bull is a FULL assumption set for method "{method}". Required \
fields by method (all figures in $M unless noted):
  dcf:   fcf_base_m, stage1_growth (decimal), stage1_years (int), \
terminal_growth (decimal), discount_rate (decimal), net_debt_m
  rnpv:  discount_rate (decimal), scenarios: [ {{ "probability" (decimal), \
"payoff_equity_m", "years" }} ]
  nav:   assets: [ {{ "name", "value_m" }} ], liabilities_m
  comps: metric_name, metric_value_m, peer_multiple, is_enterprise_multiple \
(bool), net_debt_m

bear must be conservative, bull optimistic, base your central case — vary the \
key drivers, not just one number."""


class Orchestrator:
    def __init__(
        self,
        company: CompanyData,
        llm: Any,
        config: Optional[OrchestratorConfig] = None,
        settings: Settings = SETTINGS,
    ):
        self.company = company
        self.llm = llm
        self.settings = settings
        self.config = config or OrchestratorConfig()
        self._system = SPECIALIST_SYSTEM.format(data=company.blinded_text())

    # ------------------------------------------------------------------- run
    def analyze(self) -> dict:
        briefs = self._run_phases()
        consolidation = self._consolidate(briefs)
        valuation = self._valuation_phase(consolidation)
        redteam = red_team(
            self.company,
            consolidation,
            valuation if valuation else {"method": consolidation["recommended_method"]},
            self.llm,
            self.settings,
            model=self.config.redteam_model or self.settings.redteam_model,
        )
        final = self._apply_red_team(valuation, redteam)
        return {
            "ticker": self.company.ticker,
            "fair_value": final,  # post-red-team per-share {low,median,high} or None
            "fair_value_pre_red_team": valuation.get("fair_value_per_share") if valuation else None,
            "method": (valuation or {}).get("method", consolidation["recommended_method"]),
            "p_catalyst": float(consolidation.get("catalyst", {}).get("probability", 0.0)),
            "catalyst_within_year": bool(
                consolidation.get("catalyst", {}).get("within_holding_year", False)
            ),
            "consolidation": consolidation,
            "redteam": redteam,
            "valuation_detail": valuation,
            "briefs": briefs,
            "config": {
                "model": self.config.model or self.settings.deep_model,
                "redteam_model": self.config.redteam_model or self.settings.redteam_model,
                "effort": self.config.effort or self.settings.effort,
                "framing": self.config.framing,
            },
        }

    # -------------------------------------------------------------- internals
    def _run_phases(self) -> dict[str, str]:
        """Run specialists in dependency order; each is its own context window."""
        briefs: dict[str, str] = {}
        for phase in ORDERED_PHASES:
            agent = Agent(
                self.llm,
                system=self._system,
                model=self.config.model or self.settings.deep_model,
                effort=self.config.effort or self.settings.effort,
                name=f"{self.company.ticker}:{phase.key}",
            )
            prompt = phase.prompt
            if self.config.framing:
                prompt = f"{prompt}\n\nAnalytical lens for this pass: {self.config.framing}"
            # Feed the financial brief forward as grounding for later phases.
            if phase.key != "financials" and "financials" in briefs:
                prompt += f"\n\nFor reference, the financial-trends brief found:\n{briefs['financials']}"
            briefs[phase.key] = agent.ask(prompt)
        return briefs

    def _consolidate(self, briefs: dict[str, str]) -> dict:
        """The code-enforced consolidation gate -> grounded assumption set."""
        pm = Agent(
            self.llm,
            system=self._system,
            model=self.config.model or self.settings.deep_model,
            effort=self.config.effort or self.settings.effort,
            name=f"{self.company.ticker}:pm",
        )
        result = pm.ask_json(
            _CONSOLIDATION_PROMPT.format(
                financials=briefs.get("financials", ""),
                business=briefs.get("business", ""),
                industry=briefs.get("industry", ""),
                news=briefs.get("news", ""),
            ),
            schema=CONSOLIDATION_SCHEMA,
        )
        return result

    def _valuation_phase(self, consolidation: dict) -> Optional[dict]:
        """Code-enforced: valuation requires a consolidation result first."""
        if not consolidation or "recommended_method" not in consolidation:
            raise RuntimeError("consolidation gate not satisfied; valuation cannot run")

        method = consolidation["recommended_method"]
        shares_m = self.company.price.shares_outstanding_m
        if not shares_m or shares_m <= 0:
            log.warning("%s: no shares outstanding; cannot derive per-share value", self.company.ticker)
            return None

        pm = Agent(
            self.llm,
            system=self._system,
            model=self.config.model or self.settings.deep_model,
            effort=self.config.effort or self.settings.effort,
            name=f"{self.company.ticker}:valuation",
        )
        raw = pm.ask_json(
            _VALUATION_PROMPT.format(
                method=method,
                summary=consolidation.get("assumption_summary", ""),
                drivers=", ".join(consolidation.get("key_drivers", [])),
            ),
            schema=None,  # heterogeneous, method-specific assumptions
        )
        chosen = raw.get("method", method)
        scenario_sets = raw.get("scenario_sets", {})
        try:
            result = val.run_valuation(chosen, scenario_sets, shares_m)
        except val.ValuationError as exc:
            log.warning("%s: valuation compute failed: %s", self.company.ticker, exc)
            return None
        out = result.to_dict()
        out["valuation_notes"] = raw.get("valuation_notes", "")
        out["assumptions"] = scenario_sets
        return out

    @staticmethod
    def _apply_red_team(valuation: Optional[dict], redteam: dict) -> Optional[dict]:
        if not valuation:
            return None
        adj = float(redteam.get("fair_value_adjustment", 1.0))
        fv = valuation["fair_value_per_share"]
        return {
            "low": fv["low"] * adj,
            "median": fv["median"] * adj,
            "high": fv["high"] * adj,
            "red_team_adjustment": adj,
        }
