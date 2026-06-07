"""DCF arithmetic is deterministic — pin it to a hand-computed golden case."""

from __future__ import annotations

import math

from microcap_engine.schemas.assumptions import DCFAssumptions
from microcap_engine.valuation.engines.dcf import compute


def _golden_assumptions() -> DCFAssumptions:
    return DCFAssumptions(
        base_revenue=100.0,
        revenue_growth=[0.10, 0.10],
        ebit_margin=[0.20, 0.20],
        tax_rate=0.25,
        capex_pct_revenue=[0.05, 0.05],
        nwc_pct_revenue=[0.02, 0.02],
        da_pct_revenue=[0.04, 0.04],
        terminal_growth=0.02,
        wacc=0.10,
        shares_outstanding=10.0,
        net_debt=0.0,
    )


def test_dcf_golden_per_share():
    # Hand calc: Y1 fcf=13.2 (pv 12.0), Y2 fcf=14.52 (pv 12.0), sum=24.0;
    # TV = 14.52*1.02/0.08 = 185.13, pv_tv = 153.0; EV=177.0; equity=177.0; /10 = 17.70
    res = compute(_golden_assumptions())
    assert math.isclose(res.fair_value_per_share, 17.70, abs_tol=0.02)
    assert math.isclose(res.enterprise_value, 177.0, abs_tol=0.1)
    assert math.isclose(res.equity_value, 177.0, abs_tol=0.1)


def test_dcf_net_debt_reduces_equity():
    a = _golden_assumptions()
    a.net_debt = 50.0
    res = compute(a)
    # equity 177 - 50 = 127; /10 = 12.70
    assert math.isclose(res.fair_value_per_share, 12.70, abs_tol=0.02)


def test_dcf_intermediate_audit_trail():
    res = compute(_golden_assumptions())
    years = res.intermediate["years"]
    assert len(years) == 2
    assert math.isclose(years[0]["fcf"], 13.2, abs_tol=0.01)
    assert math.isclose(years[1]["fcf"], 14.52, abs_tol=0.01)
    assert "terminal_value" in res.intermediate
