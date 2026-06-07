"""Deterministic valuation math — the code-executed half of the engine."""

import math

import pytest

from microcap_engine.engine import valuation as val


def test_dcf_known_value():
    a = {"fcf_base_m": 10.0, "stage1_growth": 0.05, "stage1_years": 5,
         "terminal_growth": 0.02, "discount_rate": 0.10, "net_debt_m": 0.0}
    equity = val.dcf(a)
    # Hand-computed: ~144.6 (see conftest derivation)
    assert equity == pytest.approx(144.6, rel=0.02)


def test_dcf_net_debt_subtracts():
    base = {"fcf_base_m": 10.0, "stage1_growth": 0.05, "stage1_years": 5,
            "terminal_growth": 0.02, "discount_rate": 0.10, "net_debt_m": 0.0}
    with_debt = {**base, "net_debt_m": 50.0}
    assert val.dcf(base) - val.dcf(with_debt) == pytest.approx(50.0)


def test_dcf_rejects_discount_below_terminal():
    with pytest.raises(val.ValuationError):
        val.dcf({"fcf_base_m": 10, "stage1_growth": 0.05, "stage1_years": 5,
                 "terminal_growth": 0.10, "discount_rate": 0.08})


def test_rnpv_probability_weighted():
    a = {"discount_rate": 0.10, "scenarios": [
        {"probability": 0.5, "payoff_equity_m": 100.0, "years": 0},
        {"probability": 0.5, "payoff_equity_m": 0.0, "years": 0},
    ]}
    assert val.rnpv(a) == pytest.approx(50.0)


def test_rnpv_discounts_future_payoff():
    a = {"discount_rate": 0.10, "scenarios": [
        {"probability": 1.0, "payoff_equity_m": 110.0, "years": 1}]}
    assert val.rnpv(a) == pytest.approx(100.0)


def test_nav_assets_minus_liabilities():
    a = {"assets": [{"name": "RE", "value_m": 80}, {"name": "cash", "value_m": 20}],
         "liabilities_m": 30}
    assert val.nav(a) == pytest.approx(70.0)


def test_comps_equity_and_enterprise():
    assert val.comps({"metric_value_m": 10, "peer_multiple": 12}) == pytest.approx(120.0)
    ev = val.comps({"metric_value_m": 10, "peer_multiple": 12,
                    "is_enterprise_multiple": True, "net_debt_m": 20})
    assert ev == pytest.approx(100.0)


def test_run_valuation_orders_low_median_high():
    sets = {
        "bear": {"fcf_base_m": 8, "stage1_growth": 0.02, "stage1_years": 5,
                 "terminal_growth": 0.02, "discount_rate": 0.12, "net_debt_m": 0},
        "base": {"fcf_base_m": 10, "stage1_growth": 0.05, "stage1_years": 5,
                 "terminal_growth": 0.02, "discount_rate": 0.10, "net_debt_m": 0},
        "bull": {"fcf_base_m": 12, "stage1_growth": 0.08, "stage1_years": 5,
                 "terminal_growth": 0.02, "discount_rate": 0.09, "net_debt_m": 0},
    }
    res = val.run_valuation("dcf", sets, shares_outstanding_m=10.0)
    assert res.low <= res.median <= res.high
    assert res.median == pytest.approx(14.46, rel=0.03)


def test_run_valuation_requires_positive_shares():
    sets = {"bear": {}, "base": {}, "bull": {}}
    with pytest.raises(val.ValuationError):
        val.run_valuation("dcf", sets, shares_outstanding_m=0)


def test_run_valuation_missing_scenarios():
    with pytest.raises(val.ValuationError):
        val.run_valuation("dcf", {"base": {}}, shares_outstanding_m=10.0)


def test_unknown_method():
    with pytest.raises(val.ValuationError):
        val.equity_value("voodoo", {})
