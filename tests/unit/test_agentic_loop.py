"""The agentic loop's terminal control flow, offline (scripted fake client).

Locks the user's key requirement: submit_final triggers a red-team gate, and an
unresolved valuation-changing concern FORCES the PM back into the loop until the
submission survives. reject_early drops. Real valuation gate (compute_valuation)
runs the real engine.
"""

from __future__ import annotations

from microcap_engine.data.models import CompanyProfile
from microcap_engine.orchestrator.agentic import AgenticOrchestrator
from microcap_engine.schemas.judge import JudgeReport
from microcap_engine.schemas.name_result import NameData
from microcap_engine.schemas.redteam import Concern, RedTeamReport


class _Block:
    def __init__(self, type, **kw):
        self.type = type
        for k, v in kw.items():
            setattr(self, k, v)


class _Resp:
    def __init__(self, content, stop_reason="tool_use"):
        self.content = content
        self.stop_reason = stop_reason
        self.usage = None
        self._request_id = "req_fake"


class _Audit:
    run_id = "fake"

    def summary(self, ticker):
        return {"cost_usd": 0.0, "total_tokens": 0, "n_calls": 0}

    def record(self, *a, **k):
        pass


_GOOD_ASSUMPTION = {
    "method": "worked", "rationale": "insurer P/TBV x ROE",
    "citations": [{"source_kind": "filing", "quote": "tbv"}],
    "worked": {"framework": "P/TBV x ROE", "key_inputs": {"tbvps": 20.0, "pb": 1.5},
               "formula": "tbvps * pb"},
}


def _tool(name, inp, tid="t1"):
    return _Block("tool_use", id=tid, name=name, input=inp)


class _FakeClient:
    """Scripts PM turns + tool-using reviewer verdicts (red-team / judge) by phase.

    Reviewers (ToolReviewer) emit their verdict via an emit_<schema> tool call, so
    the fake returns that tool_use directly for the reviewer phases.
    """

    def __init__(self, turns, redteam_reports, judge_reports=None):
        self.audit = _Audit()
        self._turns = list(turns)
        self._reds = list(redteam_reports)
        self._judges = list(judge_reports or [])

    def tool_turn(self, *, phase, **kw):
        if phase == "redteam_gate":
            r = self._reds.pop(0)
            return _Resp([_Block("tool_use", id="er", name="emit_redteamreport",
                                 input=r.model_dump())])
        if phase == "judge":
            j = self._judges.pop(0)
            return _Resp([_Block("tool_use", id="ej", name="emit_judgereport",
                                 input=j.model_dump())])
        return self._turns.pop(0)  # PM turn


def _data():
    return NameData(ticker="TST",
                    profile=CompanyProfile(ticker="TST", name="Test Co", description="x"))


def _orch(client):
    return AgenticOrchestrator(_data(), client, "fake", max_steps=10, max_red_rounds=3)


def test_submit_blocked_by_redteam_then_accepted():
    submit_input = {
        "markdown_memo": "# Memo\nDetailed.",
        "dossier": {"fair_value_per_share": 30.0, "fair_value_low": 20.0,
                    "fair_value_high": 40.0, "valuation_method": "P/TBV x ROE",
                    "confidence": 0.7, "thesis_summary": "cheap vs book"},
    }
    turns = [
        _Resp([_tool("compute_valuation", _GOOD_ASSUMPTION)]),
        _Resp([_tool("submit_final", submit_input, "s1")]),   # round 1 -> blocked
        _Resp([_tool("submit_final", submit_input, "s2")]),   # round 2 -> accepted
    ]
    reports = [
        RedTeamReport(would_break_thesis=True, summary="dilution",
                      concerns=[Concern(category="dilution", severity="high",
                                        description="ignored converts", evidence="proxy",
                                        would_change_valuation=True)]),
        RedTeamReport(would_break_thesis=False, summary="ok", concerns=[]),
    ]
    # Round 1: red-team blocks (no judge). Round 2: red-team clean -> judge approves.
    judges = [JudgeReport(best_in_existence=True, overall_score=92, verdict="excellent")]
    out = _orch(_FakeClient(turns, reports, judges)).analyze()
    assert out.action == "evaluated"
    assert out.dossier is not None
    assert out.judge_approved is True
    assert out.judge_score == 92
    assert out.red_team_rounds == 1  # one rejection before acceptance
    assert out.dossier.fair_value_per_share == 30.0
    assert out.memo_markdown.startswith("# Memo")


def test_reject_early_drops():
    turns = [_Resp([_tool("reject_early", {"reason": "shell, no assets"})])]
    out = _orch(_FakeClient(turns, [])).analyze()
    assert out.action == "drop"
    assert "shell" in out.reject_reason


def test_compute_valuation_runs_real_engine():
    # The compute_valuation tool must actually run the code engine (worked formula).
    turns = [
        _Resp([_tool("compute_valuation", _GOOD_ASSUMPTION)]),
        _Resp([_tool("reject_early", {"reason": "done testing"})]),
    ]
    orch = _orch(_FakeClient(turns, []))
    orch.analyze()
    assert orch.ctx.last_valuation is not None
    assert orch.ctx.last_valuation.fair_value_per_share == 30.0  # 20 * 1.5
