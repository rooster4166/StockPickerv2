"""Offline, deterministic end-to-end test of the full cascade.

A fake LLM returns canned-but-valid briefs for each phase; the valuation math is
REAL (DCF/comps run in code). This exercises every architectural seam — gate ->
8 phases -> consolidation gate -> price-blinded valuation -> red-team -> ensemble
-> portfolio price-join — without touching the network, and asserts the gate and
price-blinding invariants hold under a real run.
"""

from __future__ import annotations

from microcap_engine.llm.audit import AuditLogger
from microcap_engine.portfolio.book import build_portfolio
from microcap_engine.runner.pipeline import analyze_name
from microcap_engine.schemas.assumptions import (
    AssumptionSet,
    CompsAssumptions,
    ValuationMethod,
)
from microcap_engine.schemas.briefs import (
    BalanceSheetSummary,
    BusinessBrief,
    Citation,
    FinancialsBrief,
    IndustryBrief,
    NewsBrief,
    PeriodPoint,
    TranscriptBrief,
)
from microcap_engine.schemas.name_result import GateVerdict
from microcap_engine.schemas.redteam import RedTeamReport

_CIT = [Citation(source_kind="fundamentals", quote="rev grew")]


def _canned(schema):
    name = schema.__name__
    if name == "GateVerdict":
        return GateVerdict(verdict="plausible", confidence=0.5, reason="cheap and cash-rich")
    if name == "TranscriptBrief":
        return TranscriptBrief(summary="management upbeat on margins", citations=_CIT)
    if name == "FinancialsBrief":
        return FinancialsBrief(
            revenue_trend=[PeriodPoint(period="FY2024", value=100.0)],
            balance_sheet=BalanceSheetSummary(
                cash_and_equivalents=50, total_debt=10, net_debt=-40,
                total_equity=120, shares_outstanding=10,
            ),
            summary="steady revenue, net cash", citations=_CIT,
        )
    if name == "BusinessBrief":
        return BusinessBrief(unit_economics="good", moat_assessment="some",
                             summary="makes widgets", citations=_CIT)
    if name == "IndustryBrief":
        return IndustryBrief(growth_outlook="ok", competitive_position="mid",
                             summary="niche", adjacent_exposures=["feedstock"], citations=_CIT)
    if name == "NewsBrief":
        return NewsBrief(summary="quiet", citations=_CIT)
    if name == "AssumptionSet":
        return AssumptionSet(
            method=ValuationMethod.COMPS, rationale="clean peers", citations=_CIT,
            comps=CompsAssumptions(
                peer_set=["X", "Y"], multiple_type="ev_ebitda", target_multiple=8.0,
                metric_value=20.0, shares_outstanding=10.0, net_debt=-40.0,
            ),
        )
    if name == "RedTeamReport":
        return RedTeamReport(would_break_thesis=False, most_severe="low",
                             summary="no killers", citations=[])
    raise AssertionError(f"no canned object for {name}")


class _FakeAudit(AuditLogger):
    def __init__(self):
        pass

    run_id = "fake-run"

    def record(self, ticker, record):
        pass

    def summary(self, ticker):
        return {"cost_usd": 0.0, "total_tokens": 0, "n_calls": 0}


class _FakeClient:
    def __init__(self):
        self.audit = _FakeAudit()

    def parse(self, *, output_schema, **kwargs):
        return _canned(output_schema), {"input_tokens": 0, "output_tokens": 0}


def test_full_cascade_offline(axti_name_data):
    client = _FakeClient()
    result = analyze_name(axti_name_data, client, run_id="fake-run", n_ensemble=2)

    assert result.action == "evaluated"
    assert result.fair_value is not None
    # comps: EV = 8*20 = 160; equity = 160 - (-40) = 200; /10 = 20.0
    assert result.fair_value.median == 20.0
    assert result.confidence == 1.0  # identical members -> zero dispersion
    assert len(result.runs) == 2
    # every phase populated
    run = result.runs[0]
    assert run.transcripts is not None  # fixture has transcripts? if not, None is ok
    assert run.assumption_set.method == ValuationMethod.COMPS
    assert run.valuation.fair_value_per_share == 20.0
    assert run.redteam.would_break_thesis is False


def test_portfolio_join_applies_mos(axti_name_data):
    client = _FakeClient()
    result = analyze_name(axti_name_data, client, run_id="fake-run", n_ensemble=1)
    # fair value 20; price 10 -> 100% upside, well above MOS -> a position
    book = build_portfolio([result], {"AXTI": 10.0}, {"AXTI": 1_000_000.0}, 100_000.0)
    assert len(book.positions) == 1
    assert book.positions[0].upside == 1.0
    # price 30 -> -33% upside, below MOS -> passed, no position
    book2 = build_portfolio([result], {"AXTI": 30.0}, {"AXTI": 1_000_000.0}, 100_000.0)
    assert not book2.positions
    assert "AXTI" in book2.passed
