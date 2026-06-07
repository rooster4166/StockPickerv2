"""The decorrelated red-team (design spec B.3, phase 7).

A *different* model from the one that built the thesis seeks disconfirming
evidence — short theses, going-concern language, litigation, auditor changes —
rather than the same model politely arguing with itself. Its output adjusts the
fair value (a haircut in [0,1]) and flags thesis-breakers; it never sees the
price either.
"""

from __future__ import annotations

import logging
from typing import Any

from ..config import SETTINGS, Settings
from ..data.types import CompanyData
from .schemas import REDTEAM_SCHEMA

log = logging.getLogger(__name__)

_REDTEAM_SYSTEM = """You are an adversarial short-seller and forensic skeptic, \
brought in to DESTROY an investment thesis built by another analyst on a \
neglected micro-cap. You are a different mind than the one that wrote it — your \
job is to find what they missed or rationalized away. Hunt for disconfirming \
evidence in the public record: deteriorating fundamentals, going-concern or \
liquidity risk, dilution, related-party dealings, litigation, auditor changes, \
aggressive accounting, value-trap dynamics (cheap for a real reason), and \
catalysts that will never actually fire. You are PRICE-BLINDED.

=== PRICE-BLINDED COMPANY DATA ===
{data}
=== END DATA ==="""

_REDTEAM_PROMPT = """The thesis to attack:

Recommended valuation method: {method}
Assumption summary: {assumptions}
Key drivers: {drivers}
Catalyst: {catalyst}
Estimated fair value per share (pre-red-team): low {low:.2f} / median \
{median:.2f} / high {high:.2f}

Attack it. Then return the required JSON:
- disconfirming_findings: concrete, cited problems
- thesis_breakers: issues that would invalidate the thesis entirely
- fair_value_adjustment: a multiplicative haircut in [0,1] to apply to the \
median fair value (1.0 = thesis intact, 0.7 = cut 30%, etc.)
- verdict: "thesis_intact" | "weakened" | "broken"
- summary: one paragraph."""


def red_team(
    company: CompanyData,
    consolidation: dict,
    valuation: dict,
    llm: Any,
    settings: Settings = SETTINGS,
    model: str | None = None,
) -> dict:
    fv = valuation.get("fair_value_per_share", {})
    cat = consolidation.get("catalyst", {})
    prompt = _REDTEAM_PROMPT.format(
        method=valuation.get("method", consolidation.get("recommended_method", "")),
        assumptions=consolidation.get("assumption_summary", ""),
        drivers=", ".join(consolidation.get("key_drivers", [])),
        catalyst=cat.get("description", "none"),
        low=float(fv.get("low", 0.0)),
        median=float(fv.get("median", 0.0)),
        high=float(fv.get("high", 0.0)),
    )
    try:
        result = llm.complete_json(
            system=_REDTEAM_SYSTEM.format(data=company.blinded_text()),
            messages=[{"role": "user", "content": prompt}],
            schema=REDTEAM_SCHEMA,
            model=model or settings.redteam_model,  # DECORRELATED model
            effort=settings.effort,
        )
        adj = float(result.get("fair_value_adjustment", 1.0))
        result["fair_value_adjustment"] = max(0.0, min(1.0, adj))
        return result
    except Exception as exc:  # noqa: BLE001
        log.warning("red-team failed for %s: %s", company.ticker, exc)
        return {
            "disconfirming_findings": [],
            "thesis_breakers": [],
            "fair_value_adjustment": 1.0,
            "verdict": "thesis_intact",
            "summary": f"red-team error: {exc}",
        }
