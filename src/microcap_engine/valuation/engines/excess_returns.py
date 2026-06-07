"""Excess-returns / warranted-multiple-of-book valuation.

The correct frame for book-value-and-return businesses (insurers via through-cycle
ROE, banks via ROTE). Warranted P/B = (return - growth)/(cost_of_equity - growth);
equity value = book x warranted P/B. Pure arithmetic — math in code.
"""

from __future__ import annotations

from microcap_engine.schemas.assumptions import ExcessReturnsAssumptions, ValuationMethod
from microcap_engine.schemas.valuation import ValuationResult


def compute(a: ExcessReturnsAssumptions) -> ValuationResult:
    warranted_pb = (a.sustainable_return - a.growth) / (a.cost_of_equity - a.growth)
    equity_value = a.book_value * warranted_pb
    per_share = equity_value / a.shares_outstanding
    return ValuationResult(
        method=ValuationMethod.EXCESS_RETURNS,
        fair_value_per_share=round(per_share, 4),
        fair_value_median=round(per_share, 4),
        equity_value=round(equity_value, 2),
        intermediate={
            "warranted_price_to_book": round(warranted_pb, 4),
            "book_value": a.book_value,
            "sustainable_return": a.sustainable_return,
            "cost_of_equity": a.cost_of_equity,
            "growth": a.growth,
            "shares_outstanding": a.shares_outstanding,
        },
        notes=(
            f"Excess returns: warranted P/B {warranted_pb:.2f}x "
            f"(ROE {a.sustainable_return:.1%}, g {a.growth:.1%}, CoE {a.cost_of_equity:.1%})."
        ),
    )
