"""Every LLM call must produce exactly one audit record (with usage + cost)."""

from __future__ import annotations

import json

import pytest

from microcap_engine.llm.audit import AuditLogger, estimate_cost_usd
from microcap_engine.llm.client import LLMClient


class _FakeUsage:
    input_tokens = 1000
    output_tokens = 200
    cache_creation_input_tokens = 0
    cache_read_input_tokens = 500


class _FakeBlock:
    type = "text"
    text = "hello"


class _FakeResp:
    usage = _FakeUsage()
    stop_reason = "end_turn"
    _request_id = "req_test_123"
    content = [_FakeBlock()]


class _FakeMessages:
    def create(self, **kwargs):
        return _FakeResp()

    def parse(self, **kwargs):
        resp = _FakeResp()
        # emulate parsed_output via the requested pydantic schema with dummy-safe data
        resp.parsed_output = _PARSED  # type: ignore[attr-defined]
        return resp


class _FakeAnthropic:
    def __init__(self):
        self.messages = _FakeMessages()


_PARSED = None  # set in test


def _make_client(tmp_path) -> LLMClient:
    audit = AuditLogger("test-run")
    audit._dir = tmp_path / "test-run"  # redirect audit output to tmp
    audit._dir.mkdir(parents=True, exist_ok=True)
    client = LLMClient(audit, api_key="test-key")
    client._client = _FakeAnthropic()  # type: ignore[assignment]
    return client


def test_text_call_writes_one_record(tmp_path):
    client = _make_client(tmp_path)
    reply = client.complete_text(
        model="claude-opus-4-8",
        system="sys",
        messages=[{"role": "user", "content": "hi"}],
        ticker="AXTI",
        phase="test",
        label="t:test",
    )
    assert reply.text == "hello"
    lines = (client.audit.path_for("AXTI")).read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert rec["model"] == "claude-opus-4-8"
    assert rec["usage"]["input_tokens"] == 1000
    assert rec["cost_usd"] > 0
    assert rec["request_id"] == "req_test_123"


def test_three_calls_three_records(tmp_path):
    client = _make_client(tmp_path)
    for _ in range(3):
        client.complete_text(
            model="claude-opus-4-8", system="s",
            messages=[{"role": "user", "content": "hi"}],
            ticker="AXTI", phase="p", label="l",
        )
    lines = client.audit.path_for("AXTI").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3


def test_cost_estimation_uses_cache_discount():
    cheap = estimate_cost_usd("claude-opus-4-8", {"input_tokens": 0, "output_tokens": 0,
                                                  "cache_read_input_tokens": 1_000_000})
    fresh = estimate_cost_usd("claude-opus-4-8", {"input_tokens": 1_000_000, "output_tokens": 0})
    # cache reads are ~0.1x fresh input
    assert cheap == pytest.approx(fresh * 0.10, rel=0.01)
