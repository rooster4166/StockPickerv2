"""Valuation output — produced by code, price-blinded.

A ``ValuationResult`` carries the fair value per share plus the intermediate
arithmetic, so the audit log can show exactly how judgment (the AssumptionSet)
became a number. No market quote appears here.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from microcap_engine.schemas.assumptions import ValuationMethod


class ValuationResult(BaseModel):
    method: ValuationMethod
    fair_value_per_share: float
    # For ensemble dispersion we treat the point estimate as the median; when a
    # distribution is available (Monte Carlo, later) p10/p90 are populated too.
    fair_value_median: float
    fair_value_p10: float | None = None
    fair_value_p90: float | None = None
    enterprise_value: float | None = None
    equity_value: float | None = None
    intermediate: dict = Field(
        default_factory=dict,
        description="Engine-specific working (per-year cash flows, PV factors, etc.).",
    )
    notes: str = ""
