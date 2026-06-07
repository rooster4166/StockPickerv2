"""Phase-0 baseline: the proven one-prompt-per-name Buffett sweep (Part D).

This is the deliberately crude version that forward-validated at ~300% on paper:
a single "would Buffett buy this, ignoring that it's too small to bother with?"
prompt per name. It is cheap, proven, and the bar the heavy engine must beat
(the C.1 A/B). It runs price-blinded too so its fair value is independent, then
the same ranking/sizing/execution layer turns it into a book.
"""

from __future__ import annotations

import logging
from typing import Any

from ..config import SETTINGS, Settings
from ..data.types import CompanyData
from ..engine.schemas import BASELINE_SCHEMA

log = logging.getLogger(__name__)

_BASELINE_SYSTEM = """You are Warren Buffett's research analyst. You are handed \
the full public record of a tiny, neglected US company ($50-300M market cap) \
that no fund will ever staff because it is too small to move the needle. Ignore \
that it is too small to bother with. Read everything and reason to an \
independent, conservative estimate of intrinsic value per share with a margin of \
safety. You are PRICE-BLINDED: you never see the market quote and must not \
anchor to one. Favor durable earning power, clean balance sheets, and downside \
protection."""

_BASELINE_PROMPT = """Price-blinded company data:

{data}

Would you buy this business at a sensible price, on a buy-and-hold-one-year \
basis? Return the required JSON: would_buy (bool), fair_value_per_share \
(your conservative intrinsic value, a number), confidence in [0,1], and a short \
thesis."""


def baseline_value(company: CompanyData, llm: Any, settings: Settings = SETTINGS) -> dict:
    """One prompt, one name. Returns an ensemble-shaped result so the same
    portfolio layer (rank/size/execute) consumes it unchanged."""
    try:
        r = llm.complete_json(
            system=_BASELINE_SYSTEM,
            messages=[
                {"role": "user", "content": _BASELINE_PROMPT.format(data=company.blinded_text())}
            ],
            schema=BASELINE_SCHEMA,
            model=settings.baseline_model,
            effort=settings.effort,
        )
    except Exception as exc:  # noqa: BLE001
        log.warning("baseline failed for %s: %s", company.ticker, exc)
        return {"ticker": company.ticker, "action": "analyzed", "fair_value": None,
                "confidence": 0.0, "p_catalyst": 0.0, "error": str(exc)}

    fv = float(r.get("fair_value_per_share", 0.0))
    conf = max(0.0, min(1.0, float(r.get("confidence", 0.0))))
    # If the analyst would not buy, treat fair value as no-signal (None) so it is
    # naturally excluded by the margin-of-safety filter without being "dropped".
    fair_value = {"low": fv, "median": fv, "high": fv} if r.get("would_buy") and fv > 0 else None
    return {
        "ticker": company.ticker,
        "action": "analyzed",
        "fair_value": fair_value,
        "confidence": conf,
        "p_catalyst": 0.0,
        "thesis": r.get("thesis", ""),
        "would_buy": bool(r.get("would_buy", False)),
    }
