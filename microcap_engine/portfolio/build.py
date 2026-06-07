"""Assemble the final book from analysis results (design spec B.8 build_portfolio)."""

from __future__ import annotations

from typing import Optional

from ..config import SETTINGS, Settings
from .ranking import Candidate, rank_candidates
from .sizing import Position, size_book


def build_book(
    results: list[dict],
    prices: dict[str, Optional[float]],
    adv_dollar: dict[str, Optional[float]],
    capital: float,
    settings: Settings = SETTINGS,
) -> dict:
    """Rank the undervalued pool, size it, and report deployment.

    Returns a dict with the ranked candidates, the sized positions, and summary
    deployment stats (long-only, many names, liquidity-capped).
    """
    candidates: list[Candidate] = rank_candidates(results, prices, settings)
    positions: list[Position] = size_book(candidates, capital, adv_dollar, settings)
    deployed = sum(p.dollars for p in positions)
    return {
        "capital": capital,
        "n_candidates": len(candidates),
        "n_positions": len([p for p in positions if p.shares > 0]),
        "deployed": round(deployed, 2),
        "cash_remaining": round(capital - deployed, 2),
        "candidates": [c.to_dict() for c in candidates],
        "positions": [p.to_dict() for p in positions],
    }
