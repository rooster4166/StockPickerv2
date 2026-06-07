"""Cross-sectional ranking of the undervalued pool (design spec B.5).

Names are ranked *against each other* by margin of safety (fair value vs price).
Ranking relatively cancels uniform model bias: if the engine is systematically
optimistic, every estimate inflates together and the ordering is preserved. The
rank metric is ``gap * confidence`` so dispersion across ensemble runs tilts
sizing without ever filtering a name out.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..config import SETTINGS, Settings


@dataclass
class Candidate:
    ticker: str
    price: float
    fair_value_median: float
    gap: float  # (fair_value - price) / price
    confidence: float
    p_catalyst: float
    score: float  # rank metric = gap * confidence

    def to_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "price": self.price,
            "fair_value_median": self.fair_value_median,
            "gap": self.gap,
            "confidence": self.confidence,
            "p_catalyst": self.p_catalyst,
            "score": self.score,
        }


def rank_candidates(
    results: list[dict],
    prices: dict[str, Optional[float]],
    settings: Settings = SETTINGS,
) -> list[Candidate]:
    """Filter to names with sufficient margin of safety, then rank by score."""
    pool: list[Candidate] = []
    for r in results:
        if r.get("action") == "drop":
            continue
        fv = r.get("fair_value")
        if not fv or fv.get("median") is None:
            continue
        ticker = r["ticker"]
        price = prices.get(ticker)
        if not price or price <= 0:
            continue  # cannot compute a margin of safety without a price
        median = float(fv["median"])
        gap = (median - price) / price
        if gap < settings.margin_of_safety:
            continue  # require a margin of safety (B.5)
        confidence = float(r.get("confidence", 0.0))
        pool.append(
            Candidate(
                ticker=ticker,
                price=price,
                fair_value_median=median,
                gap=gap,
                confidence=confidence,
                p_catalyst=float(r.get("p_catalyst", 0.0)),
                score=gap * confidence,
            )
        )
    pool.sort(key=lambda c: c.score, reverse=True)
    return pool
