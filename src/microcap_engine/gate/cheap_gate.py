"""Cheap reject-gate — a single LLM call to triage obvious passes.

Fires only on unambiguous, high-confidence rejects. "When in doubt, keep going."
No filings, no quote — just a compact fundamentals snapshot. The asymmetry is
brutal (dropping a future 28x costs the 28x; a needless deep dive costs cents),
so the bar to drop is deliberately high.
"""

from __future__ import annotations

from microcap_engine.config import settings
from microcap_engine.llm.client import LLMClient
from microcap_engine.llm.fresh_agent import spawn_fresh
from microcap_engine.orchestrator import digest
from microcap_engine.orchestrator.phases import prompts
from microcap_engine.schemas.name_result import GateVerdict, NameData


def cheap_gate(data: NameData, client: LLMClient, model: str | None = None) -> GateVerdict:
    agent = spawn_fresh(
        client=client,
        role="cheap_gate",
        system=prompts.CHEAP_GATE,
        ticker=data.ticker,
        model=model or settings.cheap_gate_model,
        thinking=False,  # fast triage; conservative keep-bias doesn't need deep thinking
    )
    msg = (
        "Is there any plausible case this stock is materially undervalued and worth a "
        "full deep dive? Be conservative about rejecting.\n\n"
        + digest.profile_block(data)
        + "\n\n"
        + digest.financials_block(data)
    )
    return agent.ask_structured(
        msg, output_schema=GateVerdict, phase="cheap_gate", max_tokens=4000
    )


def has_asset_floor(data: NameData) -> bool:
    """True if the company has a balance-sheet floor it could be undervalued against.

    Price-free (uses only the company's own financials, never the market quote), so
    it's safe inside the price-blinded path. A name with positive net cash OR positive
    book equity cannot be a "no asset value" reject — these are exactly the deep-value
    / cash-shell / turnaround plays we cannot afford to drop.
    """
    latest = _latest_annual(data)
    if latest is None:
        return False
    cash = latest.cash_and_equivalents or 0.0
    debt = latest.total_debt or 0.0
    equity = latest.total_equity or 0.0
    return (cash - debt) > 0 or equity > 0


def _latest_annual(data: NameData):
    annuals = [f for f in data.financials if str(f.fiscal_period).upper().startswith("FY")]
    pool = annuals or data.financials
    return max(pool, key=lambda f: f.period_end, default=None)


def should_drop(verdict: GateVerdict, data: NameData) -> bool:
    """Drop ONLY a high-confidence obvious_no that ALSO has no asset floor.

    The code floor overrides the LLM: a cash-rich or book-positive name is never
    dropped even if the model says obvious_no. False positives (junk we keep) cost a
    deep dive; false negatives (a winner we drop) are unrecoverable — so we bias hard
    toward keeping.
    """
    if has_asset_floor(data):
        return False
    return verdict.verdict == "obvious_no" and verdict.confidence >= settings.gate_drop_confidence
