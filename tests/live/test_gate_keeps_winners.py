"""Recall calibration (opt-in: `pytest -m live`).

The catastrophic error is dropping a good name. This hits the REAL gate (Anthropic
+ FMP) on a basket of names that should always survive triage — known value
winners and asset-rich names — and asserts the gate keeps every one. If this ever
fails, the gate has become too aggressive and will silently delete opportunities.

Costs a few cents/name. Skipped by default (see pyproject `addopts = -m 'not live'`).
"""

from __future__ import annotations

import pytest

# Names that must survive triage: spec-cited POC winners + cash/asset-rich value
# names. Add resolved winners here over time (the spec's "resolved-case library").
MUST_KEEP = ["AXTI", "ZUMZ", "BBW", "ICCC", "CIX", "NL"]


@pytest.mark.live
@pytest.mark.parametrize("ticker", MUST_KEEP)
def test_gate_keeps_known_value_names(ticker):
    from microcap_engine.data.universe import load_name_data
    from microcap_engine.gate.cheap_gate import cheap_gate, should_drop
    from microcap_engine.llm.audit import AuditLogger
    from microcap_engine.llm.client import LLMClient
    from microcap_engine.utils.ids import new_run_id

    client = LLMClient(AuditLogger(new_run_id()))
    data = load_name_data(ticker)
    verdict = cheap_gate(data, client)
    assert not should_drop(verdict, data), (
        f"Gate would DROP {ticker} (verdict={verdict.verdict} "
        f"conf={verdict.confidence}) — recall failure: {verdict.reason}"
    )
