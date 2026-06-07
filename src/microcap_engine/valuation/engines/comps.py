"""Comparables valuation — apply a peer-justified multiple to a company metric.

EV-based multiples (ev_ebitda, ev_sales) yield enterprise value, bridged to
equity via net debt. Equity-based multiples (p_e, p_b) yield equity value
directly. ``metric_value`` is the company-level metric the multiple applies to.
"""

from __future__ import annotations

from microcap_engine.schemas.assumptions import CompsAssumptions, ValuationMethod
from microcap_engine.schemas.valuation import ValuationResult

_EV_BASED = {"ev_ebitda", "ev_sales"}


def compute(a: CompsAssumptions) -> ValuationResult:
    mtype = a.multiple_type.lower()
    # A multiple on a negative denominator is economically meaningless (e.g. EV/EBITDA
    # on negative EBITDA, or P/E on negative earnings) — it produces a spurious negative
    # "fair value". The PM must value loss-makers on a different metric (sales/book/DCF).
    if a.metric_value <= 0:
        raise ValueError(
            f"comps: multiple_type '{a.multiple_type}' applied to a non-positive metric "
            f"({a.metric_value}) is meaningless; value this company on a positive metric "
            "(ev_sales, p_b) or a cash-flow method instead.")
    gross = a.target_multiple * a.metric_value
    if mtype in _EV_BASED:
        enterprise_value = gross
        equity_value = enterprise_value - a.net_debt
    else:  # p_e, p_b, or any equity-level multiple
        enterprise_value = None
        equity_value = gross
    per_share = equity_value / a.shares_outstanding

    return ValuationResult(
        method=ValuationMethod.COMPS,
        fair_value_per_share=round(per_share, 4),
        fair_value_median=round(per_share, 4),
        enterprise_value=round(enterprise_value, 2) if enterprise_value is not None else None,
        equity_value=round(equity_value, 2),
        intermediate={
            "multiple_type": a.multiple_type,
            "target_multiple": a.target_multiple,
            "metric_value": a.metric_value,
            "peer_set": a.peer_set,
            "net_debt": a.net_debt,
            "shares_outstanding": a.shares_outstanding,
        },
        notes=f"Comps: {a.target_multiple}x {a.multiple_type} on {len(a.peer_set)} peers.",
    )
