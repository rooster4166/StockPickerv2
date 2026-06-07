"""rNPV and NAV engine arithmetic."""

from __future__ import annotations

import math

import pytest

from microcap_engine.schemas.assumptions import (
    AssetLine,
    NAVAssumptions,
    RNPVAssumptions,
    Scenario,
)
from microcap_engine.valuation.engines.nav import compute as nav_compute
from microcap_engine.valuation.engines.rnpv import compute as rnpv_compute


def test_rnpv_probability_weighted():
    a = RNPVAssumptions(scenarios=[
        Scenario(name="approval", probability=0.3, value_per_share=30.0),
        Scenario(name="crl", probability=0.7, value_per_share=2.0),
    ])
    res = rnpv_compute(a)
    # 0.3*30 + 0.7*2 = 9 + 1.4 = 10.4
    assert math.isclose(res.fair_value_per_share, 10.4, abs_tol=1e-6)
    assert res.fair_value_p10 == 2.0
    assert res.fair_value_p90 == 30.0


def test_rnpv_discounts_to_present_value():
    # success $30/sh realized in 3 years; failure $2/sh now; 12% systematic rate.
    a = RNPVAssumptions(discount_rate=0.12, scenarios=[
        Scenario(name="approval", probability=0.4, value_per_share=30.0,
                 years_to_realization=3),
        Scenario(name="fail", probability=0.6, value_per_share=2.0, years_to_realization=0),
    ])
    res = rnpv_compute(a)
    # PV(success) = 30 / 1.12^3 = 21.3534; expected = 0.4*21.3534 + 0.6*2 = 9.7414
    assert math.isclose(res.fair_value_per_share, 9.7414, abs_tol=1e-3)
    assert math.isclose(res.fair_value_p90, 21.3534, abs_tol=1e-3)  # PV, not the raw 30
    assert res.fair_value_p10 == 2.0


def test_rnpv_probs_must_sum_to_one():
    with pytest.raises(Exception):
        RNPVAssumptions(scenarios=[
            Scenario(name="a", probability=0.3, value_per_share=10),
            Scenario(name="b", probability=0.3, value_per_share=2),
        ])


def test_nav_haircuts_and_liabilities():
    a = NAVAssumptions(
        assets=[
            AssetLine(name="cash", fair_value=100, realization_haircut=0.0),
            AssetLine(name="real estate", fair_value=200, realization_haircut=0.25),
        ],
        total_liabilities=50.0,
        shares_outstanding=10.0,
    )
    # assets = 100 + 200*0.75 = 250; equity = 250 - 50 = 200; /10 = 20
    res = nav_compute(a)
    assert math.isclose(res.equity_value, 200.0)
    assert math.isclose(res.fair_value_per_share, 20.0)
