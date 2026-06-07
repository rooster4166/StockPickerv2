"""The cheap reject-gate (design spec B.2).

A quick screen asking only: "is there any plausible case this is undervalued?"
The calibration is deliberately lopsided — drop a name ONLY on an unambiguous,
high-confidence ``obvious_no`` (no viable business; imminent insolvency with no
asset value). Cost is not the constraint; missing the next 28x is. The rule is
"when in doubt, keep going."
"""

from __future__ import annotations

import logging
from typing import Any

from ..config import SETTINGS, Settings
from ..data.types import CompanyData
from .schemas import GATE_SCHEMA

log = logging.getLogger(__name__)

_GATE_SYSTEM = """You are a fast triage analyst for a deep value research desk \
that reads neglected $50-300M micro-caps. You see price-blinded fundamentals: \
business description, multi-period financials, recent filings, and news. You do \
NOT see the stock price.

Your ONLY job is to decide whether this name deserves a full, expensive deep \
dive. Return "obvious_no" ONLY when you are highly confident the name is \
disqualified on the fundamentals alone — e.g. no viable ongoing business, \
imminent insolvency with no asset value behind it, or a structure that cannot \
hold equity value. Everything plausible OR ambiguous returns "plausible".

The asymmetry is brutal: wrongly dropping a name that would have been a huge \
winner costs the winner; running a deep dive on a dud costs a few dollars. When \
in doubt, return "plausible". Reserve "obvious_no" with confidence >= 0.85 for \
truly unambiguous rejects."""

_GATE_PROMPT = """Price-blinded company data:

{data}

Decide whether this name warrants a full deep dive. Respond with the required \
JSON: verdict ("plausible" or "obvious_no"), confidence in [0,1], and a one- \
sentence reason."""


def cheap_gate(company: CompanyData, llm: Any, settings: Settings = SETTINGS) -> dict:
    """Return ``{"verdict", "confidence", "reason"}``. Never raises on model error
    in a way that would silently drop a name — on failure it returns 'plausible'."""
    try:
        result = llm.complete_json(
            system=_GATE_SYSTEM,
            messages=[{"role": "user", "content": _GATE_PROMPT.format(data=company.blinded_text())}],
            schema=GATE_SCHEMA,
            model=settings.gate_model,
            effort="low",  # triage is cheap by design
        )
        # Normalize / clamp.
        verdict = result.get("verdict", "plausible")
        conf = float(result.get("confidence", 0.0))
        conf = max(0.0, min(1.0, conf))
        return {"verdict": verdict, "confidence": conf, "reason": result.get("reason", "")}
    except Exception as exc:  # noqa: BLE001 - fail OPEN, never drop on an error
        log.warning("gate failed for %s, defaulting to plausible: %s", company.ticker, exc)
        return {"verdict": "plausible", "confidence": 0.0, "reason": f"gate error: {exc}"}


def should_drop(gate_result: dict, settings: Settings = SETTINGS) -> bool:
    return (
        gate_result.get("verdict") == "obvious_no"
        and gate_result.get("confidence", 0.0) >= settings.gate_drop_confidence
    )
