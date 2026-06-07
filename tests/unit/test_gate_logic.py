"""The reject-gate drop rule: drop ONLY a high-confidence obvious_no that also has
NO balance-sheet floor. The code floor overrides the LLM (recall safety)."""

from __future__ import annotations

from datetime import date

from microcap_engine.data.models import CompanyProfile, FinancialPeriod
from microcap_engine.gate.cheap_gate import has_asset_floor, should_drop
from microcap_engine.schemas.name_result import GateVerdict, NameData


def _data(cash=0.0, debt=0.0, equity=0.0) -> NameData:
    return NameData(
        ticker="T",
        profile=CompanyProfile(ticker="T", name="T", description=""),
        financials=[FinancialPeriod(
            ticker="T", period="FY2024", period_end=date(2024, 12, 31), fiscal_period="FY",
            cash_and_equivalents=cash, total_debt=debt, total_equity=equity,
        )],
    )


_NO_FLOOR = _data(cash=1.0, debt=10.0, equity=-5.0)  # net debt, negative equity
_OBVIOUS_NO = GateVerdict(verdict="obvious_no", confidence=0.95, reason="insolvent shell")


def test_drops_insolvent_obvious_no_with_no_floor():
    assert should_drop(_OBVIOUS_NO, _NO_FLOOR)


def test_never_drops_when_net_cash_positive():
    # Cash-rich name: never dropped even on a confident obvious_no.
    assert has_asset_floor(_data(cash=100.0, debt=10.0, equity=-5.0))
    assert not should_drop(_OBVIOUS_NO, _data(cash=100.0, debt=10.0, equity=-5.0))


def test_never_drops_when_book_equity_positive():
    assert has_asset_floor(_data(cash=0.0, debt=50.0, equity=80.0))
    assert not should_drop(_OBVIOUS_NO, _data(cash=0.0, debt=50.0, equity=80.0))


def test_keeps_low_confidence_no():
    assert not should_drop(GateVerdict(verdict="obvious_no", confidence=0.5, reason="x"), _NO_FLOOR)


def test_never_drops_plausible_or_ambiguous():
    assert not should_drop(GateVerdict(verdict="plausible", confidence=0.99, reason="x"), _NO_FLOOR)
    assert not should_drop(GateVerdict(verdict="ambiguous", confidence=0.99, reason="x"), _NO_FLOOR)
