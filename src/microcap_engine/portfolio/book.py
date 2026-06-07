"""Cross-sectional ranking + sizing — the ONLY module that joins the price.

This is where price-blinding ends: fair values were computed without ever seeing
the quote; here we finally compare them to price. Ranking is cross-sectional
(margin of safety vs. each other), which cancels uniform model bias. Sizing is
rank x confidence, capped by liquidity. Long-only, many names, right-skew
preserved.

Importing ``Quote`` here is intentional and correct; no module under
``orchestrator/`` may import it (see tests/unit/test_price_blinding.py).
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from microcap_engine.config import settings
from microcap_engine.schemas.name_result import NameResult


class Position(BaseModel):
    ticker: str
    dollars: float
    rank_score: float
    fair_value: float
    price: float
    upside: float
    confidence: float


class Book(BaseModel):
    positions: list[Position] = Field(default_factory=list)
    dropped: list[str] = Field(default_factory=list)
    passed: list[str] = Field(default_factory=list)  # evaluated but below MOS


def build_portfolio(
    results: list[NameResult],
    prices: dict[str, float],
    advs: dict[str, float],
    capital: float,
    mos: float | None = None,
) -> Book:
    mos = settings.margin_of_safety if mos is None else mos
    dropped = [r.ticker for r in results if r.action == "drop"]
    passed: list[str] = []
    pool: list[tuple[float, NameResult, float, float]] = []  # (score, r, price, upside)

    for r in results:
        if r.action != "evaluated" or r.fair_value is None:
            continue
        price = prices.get(r.ticker)
        if not price or price <= 0:
            passed.append(r.ticker)
            continue
        upside = (r.fair_value.median - price) / price
        if upside < mos:
            passed.append(r.ticker)
            continue
        score = upside * (r.confidence or 0.0)
        pool.append((score, r, price, upside))

    pool.sort(key=lambda x: x[0], reverse=True)
    total_score = sum(s for s, _, _, _ in pool) or 1.0

    positions: list[Position] = []
    for score, r, price, upside in pool:
        weight = score / total_score
        target = capital * weight
        liq_cap = settings.adv_liquidity_cap * advs.get(r.ticker, 0.0)
        dollars = min(target, liq_cap) if liq_cap > 0 else target
        positions.append(
            Position(
                ticker=r.ticker,
                dollars=round(dollars, 2),
                rank_score=round(score, 4),
                fair_value=r.fair_value.median,
                price=price,
                upside=round(upside, 4),
                confidence=r.confidence or 0.0,
            )
        )

    return Book(positions=positions, dropped=dropped, passed=passed)
