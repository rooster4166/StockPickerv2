"""Multi-stage discounted cash flow — pure, deterministic arithmetic.

This is the "math in code" half of judgment-in-LLM / math-in-code: the LLM
produces a ``DCFAssumptions`` block; this function turns it into a fair value
with no model involvement and full intermediate working for the audit log.
"""

from __future__ import annotations

from microcap_engine.schemas.assumptions import DCFAssumptions, ValuationMethod
from microcap_engine.schemas.valuation import ValuationResult


def compute(a: DCFAssumptions) -> ValuationResult:
    n = len(a.revenue_growth)
    rev = []
    prev = a.base_revenue
    for g in a.revenue_growth:
        prev = prev * (1.0 + g)
        rev.append(prev)

    years = []
    pv_fcf_total = 0.0
    for t in range(n):
        r = rev[t]
        ebit = r * a.ebit_margin[t]
        nopat = ebit * (1.0 - a.tax_rate)
        da = r * a.da_pct_revenue[t]
        capex = r * a.capex_pct_revenue[t]
        nwc_change = r * a.nwc_pct_revenue[t]
        fcf = nopat + da - capex - nwc_change
        discount = 1.0 / ((1.0 + a.wacc) ** (t + 1))
        pv = fcf * discount
        pv_fcf_total += pv
        years.append(
            {
                "year": t + 1,
                "revenue": round(r, 2),
                "ebit": round(ebit, 2),
                "nopat": round(nopat, 2),
                "da": round(da, 2),
                "capex": round(capex, 2),
                "nwc_change": round(nwc_change, 2),
                "fcf": round(fcf, 2),
                "discount_factor": round(discount, 6),
                "pv_fcf": round(pv, 2),
            }
        )

    terminal_fcf = years[-1]["fcf"]
    tv = terminal_fcf * (1.0 + a.terminal_growth) / (a.wacc - a.terminal_growth)
    pv_tv = tv / ((1.0 + a.wacc) ** n)

    enterprise_value = pv_fcf_total + pv_tv
    equity_value = enterprise_value - a.net_debt
    per_share = equity_value / a.shares_outstanding

    return ValuationResult(
        method=ValuationMethod.DCF,
        fair_value_per_share=round(per_share, 4),
        fair_value_median=round(per_share, 4),
        enterprise_value=round(enterprise_value, 2),
        equity_value=round(equity_value, 2),
        intermediate={
            "years": years,
            "pv_fcf_total": round(pv_fcf_total, 2),
            "terminal_value": round(tv, 2),
            "pv_terminal_value": round(pv_tv, 2),
            "net_debt": a.net_debt,
            "shares_outstanding": a.shares_outstanding,
        },
        notes=f"{n}-stage DCF, WACC {a.wacc:.1%}, terminal g {a.terminal_growth:.1%}.",
    )
