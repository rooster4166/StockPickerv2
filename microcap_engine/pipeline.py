"""End-to-end pipeline: per-name cascade + full-universe run (design spec B.1/B.8).

``analyze_name`` is the conservative early-stop cascade: a cheap reject-gate that
fires ONLY on unambiguous, high-confidence rejects, with everything plausible or
ambiguous proceeding to the ensemble deep dive. ``run_pipeline`` walks a ticker
list through either the heavy engine or the Phase-0 baseline, then hands the
results to the shared ranking/sizing/execution layer to build the book.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from .baseline.sweep import baseline_value
from .config import SETTINGS, Settings
from .data.types import CompanyData, PriceData
from .engine.ensemble import ensemble_deepdive
from .engine.gate import cheap_gate, should_drop
from .portfolio.build import build_book

log = logging.getLogger(__name__)


def analyze_name(
    company: CompanyData,
    llm: Any,
    settings: Settings = SETTINGS,
) -> dict:
    """Cheap reject-gate, then ensemble deep dive for everything that survives."""
    gate = cheap_gate(company, llm, settings)
    if should_drop(gate, settings):
        return {
            "ticker": company.ticker,
            "action": "drop",
            "reason": gate.get("reason", ""),
            "gate": gate,
            "fair_value": None,
        }
    result = ensemble_deepdive(company, llm, settings.ensemble_n, settings)
    result["gate"] = gate
    return result


def run_pipeline(
    tickers: list[str],
    provider: Any,
    llm: Any,
    capital: float,
    mode: str = "heavy",
    settings: Settings = SETTINGS,
) -> dict:
    """Run the engine over ``tickers`` and build a sized, ranked book.

    mode: "heavy" (full deep-dive engine) or "baseline" (Phase-0 single prompt).
    """
    if mode not in ("heavy", "baseline"):
        raise ValueError("mode must be 'heavy' or 'baseline'")

    results: list[dict] = []
    prices: dict[str, Optional[float]] = {}
    adv: dict[str, Optional[float]] = {}

    for i, ticker in enumerate(tickers, 1):
        log.info("[%d/%d] %s (%s)", i, len(tickers), ticker, mode)
        try:
            company = provider.get_company_data(ticker)
        except Exception as exc:  # noqa: BLE001 - never let one name kill the run
            log.warning("data fetch failed for %s: %s", ticker, exc)
            company = CompanyData(ticker=ticker, price=PriceData(ticker=ticker))
            company.notes.append(f"data fetch failed: {exc}")

        prices[ticker] = company.price.price
        adv[ticker] = company.price.avg_dollar_volume

        if mode == "baseline":
            results.append(baseline_value(company, llm, settings))
        else:
            results.append(analyze_name(company, llm, settings))

    book = build_book(results, prices, adv, capital, settings)
    return {
        "mode": mode,
        "n_analyzed": len(tickers),
        "n_dropped": len([r for r in results if r.get("action") == "drop"]),
        "results": results,
        "book": book,
    }
