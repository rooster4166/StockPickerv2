"""Regression tests for the QM-review fixes (data + valuation correctness).

Locks: (1) common equity does NOT double-subtract minority interest from the
parent-only total; (2) safe_eval bounds exponentiation and rejects non-finite
results instead of crashing / emitting inf; (3) comps normalizes multiple-type
synonyms and refuses a multiple on a non-positive metric.
"""

from __future__ import annotations

import pytest

from microcap_engine.data.fmp import _common_equity
from microcap_engine.schemas.assumptions import CompsAssumptions
from microcap_engine.valuation.engines.comps import compute as comps_compute
from microcap_engine.valuation.safe_eval import FormulaError, safe_eval


# ── _common_equity ──────────────────────────────────────────────────────────
def test_common_equity_parent_total_excludes_minority():
    # FMP totalStockholdersEquity is PARENT-only; minority must NOT be subtracted.
    b = {"totalStockholdersEquity": 437.9e6, "preferredStock": 112e6,
         "minorityInterest": 50e6}
    # ROOT-style: 437.9 - 112 = 325.9 ; the 50 minority is already excluded upstream.
    assert _common_equity(b) == pytest.approx(325.9e6)


def test_common_equity_consolidated_fallback_nets_minority():
    # Only when we fall back to the consolidated totalEquity do we strip NCI.
    b = {"totalEquity": 300e6, "minorityInterest": 40e6, "preferredStock": 10e6}
    assert _common_equity(b) == pytest.approx(250e6)


# ── safe_eval overflow / non-finite ─────────────────────────────────────────
def test_safe_eval_blocks_huge_exponent():
    with pytest.raises(FormulaError):
        safe_eval("2 ** 1000000", {})


def test_safe_eval_rejects_non_finite():
    with pytest.raises(FormulaError):
        safe_eval("a / b", {"a": 1e308, "b": 1e-308})  # overflows to inf


def test_safe_eval_normal_still_works():
    assert safe_eval("tbvps * pb", {"tbvps": 20.0, "pb": 1.5}) == pytest.approx(30.0)


def test_safe_eval_black_scholes_real_option():
    # exp/ln/sqrt/norm_cdf must be available so `worked` can express option payoffs.
    f = ("S*norm_cdf((ln(S/K)+(r+sig*sig/2)*T)/(sig*sqrt(T))) - "
         "K*exp(-r*T)*norm_cdf((ln(S/K)+(r+sig*sig/2)*T)/(sig*sqrt(T)) - sig*sqrt(T))")
    v = safe_eval(f, {"S": 100, "K": 100, "r": 0.05, "sig": 0.2, "T": 1})
    assert v == pytest.approx(10.4506, abs=1e-3)


def test_safe_eval_exp_overflow_guarded():
    with pytest.raises(FormulaError):
        safe_eval("exp(x)", {"x": 1000})


# ── comps multiple-type normalization + metric guard ────────────────────────
def test_comps_normalizes_ev_ebitda_synonym_and_bridges_debt():
    a = CompsAssumptions(peer_set=["X"], multiple_type="EV/EBITDA", target_multiple=10,
                         metric_value=100, shares_outstanding=10, net_debt=50)
    assert a.multiple_type == "ev_ebitda"
    r = comps_compute(a)
    # EV = 1000, equity = 1000 - 50 = 950, /10 = 95
    assert r.fair_value_per_share == pytest.approx(95.0)


def test_comps_rejects_unknown_multiple():
    with pytest.raises(ValueError):
        CompsAssumptions(peer_set=["X"], multiple_type="wibble", target_multiple=10,
                         metric_value=100, shares_outstanding=10)


def test_comps_refuses_negative_metric():
    a = CompsAssumptions(peer_set=["X"], multiple_type="ev_ebitda", target_multiple=10,
                         metric_value=-5, shares_outstanding=10)
    with pytest.raises(ValueError):
        comps_compute(a)


def test_excess_returns_rejects_roe_below_growth():
    # warranted P/B = (ROE-g)/(CoE-g); ROE<=g -> negative fair value -> must be rejected.
    from microcap_engine.schemas.assumptions import ExcessReturnsAssumptions
    with pytest.raises(ValueError):
        ExcessReturnsAssumptions(book_value=100e6, shares_outstanding=10e6,
                                 sustainable_return=0.03, cost_of_equity=0.10, growth=0.05)
    # a healthy spread (ROE 13% > g 4%) is fine:
    ok = ExcessReturnsAssumptions(book_value=100e6, shares_outstanding=10e6,
                                  sustainable_return=0.13, cost_of_equity=0.10, growth=0.04)
    assert ok.sustainable_return > ok.growth


def test_rnpv_rejects_discount_rate_with_no_horizons():
    # discount_rate set but every horizon 0 = silent no-discounting -> reject.
    from microcap_engine.schemas.assumptions import RNPVAssumptions, Scenario
    with pytest.raises(ValueError):
        RNPVAssumptions(discount_rate=0.12, scenarios=[
            Scenario(name="a", probability=0.4, value_per_share=10.0),
            Scenario(name="b", probability=0.6, value_per_share=2.0)])


def test_safe_eval_allows_long_horizon_discounting():
    from microcap_engine.valuation.safe_eval import safe_eval
    # (1+r)^120 (monthly over 10y) must NOT be rejected by the overflow guard.
    v = safe_eval("1 / (1 + r) ** n", {"r": 0.01, "n": 120})
    assert v == pytest.approx(1 / (1.01 ** 120), rel=1e-9)
