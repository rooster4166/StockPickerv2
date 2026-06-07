"""The consolidation gate: no valuation without a validated AssumptionSet."""

from __future__ import annotations

import pytest

from microcap_engine.schemas.assumptions import (
    AssumptionSet,
    CompsAssumptions,
    DCFAssumptions,
    ValuationMethod,
)
from microcap_engine.schemas.briefs import Citation
from microcap_engine.valuation.dispatch import run_valuation


def _cit():
    return [Citation(source_kind="fundamentals", quote="rev 100")]


def test_dispatch_rejects_non_assumption_set():
    with pytest.raises(TypeError):
        run_valuation(None)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        run_valuation({"method": "dcf"})  # type: ignore[arg-type]


def test_assumption_set_requires_matching_block():
    # method=DCF but a comps block populated -> validation error (gate).
    with pytest.raises(Exception):
        AssumptionSet(
            method=ValuationMethod.DCF,
            rationale="x",
            citations=_cit(),
            comps=CompsAssumptions(
                peer_set=["A"], multiple_type="ev_ebitda", target_multiple=8,
                metric_value=20, shares_outstanding=10,
            ),
        )


def test_assumption_set_requires_some_block():
    # method declared but no block at all -> validation error.
    with pytest.raises(Exception):
        AssumptionSet(method=ValuationMethod.DCF, rationale="x", citations=_cit())


def test_valid_assumption_set_runs():
    aset = AssumptionSet(
        method=ValuationMethod.DCF,
        rationale="stable cash generator",
        citations=_cit(),
        dcf=DCFAssumptions(
            base_revenue=100.0,
            revenue_growth=[0.1, 0.1],
            ebit_margin=[0.2, 0.2],
            tax_rate=0.25,
            capex_pct_revenue=[0.05, 0.05],
            nwc_pct_revenue=[0.02, 0.02],
            da_pct_revenue=[0.04, 0.04],
            terminal_growth=0.02,
            wacc=0.10,
            shares_outstanding=10.0,
            net_debt=0.0,
        ),
    )
    res = run_valuation(aset)
    assert res.method == ValuationMethod.DCF
    assert res.fair_value_per_share > 0
