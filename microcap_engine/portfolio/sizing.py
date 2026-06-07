"""Position sizing (design spec B.5).

Size each position by rank x confidence (its ``score``), capped by liquidity (a
fraction of average daily $ volume) and by a hard per-name fraction of capital.
Long-only, many names, to preserve breadth and convexity. Liquidity caps mean
the book may not fully deploy capital — the leftover is reported, not forced in.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..config import SETTINGS, Settings
from .ranking import Candidate


@dataclass
class Position:
    ticker: str
    dollars: float
    weight: float  # fraction of total capital
    target_price: float  # limit anchor = current price
    shares: int
    capped_by: str  # "score" | "liquidity" | "max_position"
    score: float
    gap: float
    confidence: float

    def to_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "dollars": round(self.dollars, 2),
            "weight": round(self.weight, 4),
            "target_price": self.target_price,
            "shares": self.shares,
            "capped_by": self.capped_by,
            "score": round(self.score, 4),
            "gap": round(self.gap, 4),
            "confidence": round(self.confidence, 4),
        }


def size_book(
    candidates: list[Candidate],
    capital: float,
    adv_dollar: dict[str, Optional[float]],
    settings: Settings = SETTINGS,
) -> list[Position]:
    """Score-proportional dollars, then liquidity- and concentration-capped."""
    if not candidates or capital <= 0:
        return []
    total_score = sum(c.score for c in candidates)
    if total_score <= 0:
        return []

    positions: list[Position] = []
    for c in candidates:
        raw = capital * (c.score / total_score)
        liq_cap = None
        adv = adv_dollar.get(c.ticker)
        if adv is not None and adv > 0:
            liq_cap = settings.adv_fraction * adv
        pos_cap = settings.max_position_fraction * capital

        dollars = raw
        capped_by = "score"
        if dollars > pos_cap:
            dollars, capped_by = pos_cap, "max_position"
        if liq_cap is not None and dollars > liq_cap:
            dollars, capped_by = liq_cap, "liquidity"

        shares = int(dollars // c.price) if c.price > 0 else 0
        positions.append(
            Position(
                ticker=c.ticker,
                dollars=dollars,
                weight=dollars / capital,
                target_price=c.price,
                shares=shares,
                capped_by=capped_by,
                score=c.score,
                gap=c.gap,
                confidence=c.confidence,
            )
        )
    return positions
