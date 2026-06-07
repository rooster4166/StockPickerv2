"""Composite valuation: probability-weighted mix of sub-methods across scenarios."""

from __future__ import annotations

import math

import pytest

from microcap_engine.schemas.assumptions import (
    AssumptionSet,
    CompositeAssumptions,
    CompositeScenario,
    DCFAssumptions,
    ValuationMethod,
)
from microcap_engine.schemas.briefs import Citation
from microcap_engine.valuation.dispatch import run_valuation


def _dcf():
    return DCFAssumptions(
        base_revenue=100.0, revenue_growth=[0.1, 0.1], ebit_margin=[0.2, 0.2],
        tax_rate=0.25, capex_pct_revenue=[0.05, 0.05], nwc_pct_revenue=[0.02, 0.02],
        da_pct_revenue=[0.04, 0.04], terminal_growth=0.02, wacc=0.10,
        shares_outstanding=10.0, net_debt=0.0,
    )


def test_composite_weights_branches():
    # Branch A: DCF -> 17.70/share (p=0.6). Branch B: direct 2.00/share (p=0.4 downside).
    # Expected = 0.6*17.70 + 0.4*2.00 = 10.62 + 0.80 = 11.42
    aset = AssumptionSet(
        method=ValuationMethod.COMPOSITE,
        rationale="turnaround vs floor",
        citations=[Citation(source_kind="fundamentals", quote="x")],
        composite=CompositeAssumptions(
            scenarios=[
                CompositeScenario(name="turnaround", probability=0.6, sub_method="dcf", dcf=_dcf()),
                CompositeScenario(name="floor", probability=0.4, sub_method="direct",
                                  value_per_share=2.0),
            ]
        ),
    )
    res = run_valuation(aset)
    assert res.method == ValuationMethod.COMPOSITE
    assert math.isclose(res.fair_value_per_share, 11.42, abs_tol=0.02)
    assert res.fair_value_p10 == 2.0
    assert math.isclose(res.fair_value_p90, 17.70, abs_tol=0.02)


def test_composite_probabilities_must_sum_to_one():
    with pytest.raises(Exception):
        CompositeAssumptions(
            scenarios=[
                CompositeScenario(name="a", probability=0.6, sub_method="direct", value_per_share=5),
                CompositeScenario(name="b", probability=0.6, sub_method="direct", value_per_share=2),
            ]
        )


def test_composite_scenario_requires_its_block():
    with pytest.raises(Exception):
        CompositeScenario(name="a", probability=1.0, sub_method="dcf")  # no dcf block
