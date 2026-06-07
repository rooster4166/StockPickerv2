"""Net asset value / sum-of-the-parts for asset-heavy names.

Sum of fair values (net of realization haircuts) minus liabilities, per share.
"""

from __future__ import annotations

from microcap_engine.schemas.assumptions import NAVAssumptions, ValuationMethod
from microcap_engine.schemas.valuation import ValuationResult


def compute(a: NAVAssumptions) -> ValuationResult:
    gross_assets = sum(line.fair_value * (1.0 - line.realization_haircut) for line in a.assets)
    equity_value = gross_assets - a.total_liabilities
    per_share = equity_value / a.shares_outstanding
    return ValuationResult(
        method=ValuationMethod.NAV,
        fair_value_per_share=round(per_share, 4),
        fair_value_median=round(per_share, 4),
        equity_value=round(equity_value, 2),
        intermediate={
            "assets": [
                {
                    "name": ln.name,
                    "fair_value": ln.fair_value,
                    "realization_haircut": ln.realization_haircut,
                }
                for ln in a.assets
            ],
            "total_liabilities": a.total_liabilities,
            "shares_outstanding": a.shares_outstanding,
        },
        notes=f"NAV/SOTP over {len(a.assets)} asset lines.",
    )
