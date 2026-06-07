"""Comps arithmetic: EV-based bridges via net debt; equity-based does not."""

from __future__ import annotations

import math

from microcap_engine.schemas.assumptions import CompsAssumptions
from microcap_engine.valuation.engines.comps import compute


def test_ev_ebitda_bridges_net_debt():
    a = CompsAssumptions(
        peer_set=["A", "B"], multiple_type="ev_ebitda", target_multiple=8.0,
        metric_value=100.0, shares_outstanding=10.0, net_debt=200.0,
    )
    # EV = 8*100 = 800; equity = 800 - 200 = 600; /10 = 60
    res = compute(a)
    assert math.isclose(res.enterprise_value, 800.0)
    assert math.isclose(res.equity_value, 600.0)
    assert math.isclose(res.fair_value_per_share, 60.0)


def test_pe_is_equity_level():
    a = CompsAssumptions(
        peer_set=["A"], multiple_type="p_e", target_multiple=12.0,
        metric_value=50.0, shares_outstanding=10.0, net_debt=200.0,
    )
    # equity = 12*50 = 600 (net debt NOT subtracted); /10 = 60
    res = compute(a)
    assert res.enterprise_value is None
    assert math.isclose(res.equity_value, 600.0)
    assert math.isclose(res.fair_value_per_share, 60.0)
