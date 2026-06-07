"""The seven deep-dive phases, in strict dependency order.

Each phase reasons in its own agent (context isolation) and returns a distilled,
cited brief. Only briefs pass between phases — never raw transcripts. Phase 6 is
the only phase with no LLM call: it runs the code-executed, price-blinded
valuation through the consolidation gate.
"""

from __future__ import annotations

from microcap_engine.llm.client import LLMClient
from microcap_engine.llm.fresh_agent import spawn_fresh
from microcap_engine.llm.persistent_agent import PersistentAgent
from microcap_engine.orchestrator import digest
from microcap_engine.orchestrator.phases import prompts
from microcap_engine.orchestrator.state import OrchestratorState
from microcap_engine.schemas.assumptions import AssumptionSet
from microcap_engine.schemas.briefs import (
    BusinessBrief,
    FinancialsBrief,
    IndustryBrief,
    NewsBrief,
    TranscriptBrief,
)
from microcap_engine.schemas.name_result import NameData
from microcap_engine.schemas.redteam import RedTeamReport
from microcap_engine.schemas.valuation import ValuationResult
from microcap_engine.valuation.dispatch import run_valuation


def _agent(client: LLMClient, system: str, state: OrchestratorState, role: str) -> PersistentAgent:
    return PersistentAgent(
        client=client,
        system=system + prompts.variant_suffix(state.config.prompt_variant),
        model=state.config.model,
        role=role,
        ticker=state.ticker,
        thinking=state.config.thinking,
    )


def _transcripts_addendum(state: OrchestratorState) -> str:
    """A compact transcript-signal block to append to downstream phase prompts."""
    if state.transcripts is None:
        return ""
    return (
        "\n\nEARNINGS-CALL SIGNAL (distilled by the transcript analyst):\n"
        + state.transcripts.model_dump_json(indent=2)
    )


def run_phase0_transcripts(
    data: NameData, state: OrchestratorState, client: LLMClient
) -> TranscriptBrief | None:
    """Dedicated distiller (Sonnet): read the raw calls, return only signal.

    Runs first so its brief can inform every downstream phase. Returns None when
    no transcripts are available (common for the smallest micro-caps)."""
    if not data.transcripts:
        return None
    agent = spawn_fresh(
        client=client,
        role="transcripts",
        system=prompts.TRANSCRIPT_DISTILL,
        ticker=state.ticker,
        model=state.config.extract_model,  # Sonnet — extraction, not deep reasoning
        thinking=False,  # extraction doesn't need adaptive thinking; keep it fast
    )
    msg = (
        "Extract the value-relevant signal from these earnings calls.\n\n"
        + digest.profile_block(data)
        + "\n\n"
        + digest.transcripts_block(data)
    )
    return agent.ask_structured(
        msg, output_schema=TranscriptBrief, phase="phase0_transcripts", max_tokens=8000
    )


def run_phase1_financials(
    data: NameData, state: OrchestratorState, client: LLMClient
) -> FinancialsBrief:
    agent = _agent(client, prompts.PHASE1_FINANCIALS, state, "financials")
    msg = (
        "Analyze the financial trajectory of this company across all periods and "
        "filings.\n\n"
        + digest.profile_block(data)
        + "\n\n"
        + digest.financials_block(data)
        + "\n\n"
        + digest.filings_block(data)
    )
    return agent.ask_structured(msg, output_schema=FinancialsBrief, phase="phase1_financials")


def run_phase2_business(
    data: NameData, state: OrchestratorState, client: LLMClient
) -> BusinessBrief:
    agent = _agent(client, prompts.PHASE2_BUSINESS, state, "business")
    msg = (
        "Using the financial brief and filings, explain how this company makes money.\n\n"
        + digest.profile_block(data)
        + "\n\nFINANCIAL BRIEF (from the financial analyst):\n"
        + state.financials.model_dump_json(indent=2)
        + _transcripts_addendum(state)
        + "\n\n"
        + digest.filings_block(data)
    )
    return agent.ask_structured(msg, output_schema=BusinessBrief, phase="phase2_business")


def run_phase3_industry(
    data: NameData, state: OrchestratorState, client: LLMClient
) -> IndustryBrief:
    agent = _agent(client, prompts.PHASE3_INDUSTRY, state, "industry")
    msg = (
        "Assess the industry position and surface adjacent exposures.\n\n"
        + digest.profile_block(data)
        + "\n\nBUSINESS BRIEF:\n"
        + state.business.model_dump_json(indent=2)
        + "\n\n"
        + digest.filings_block(data)
    )
    return agent.ask_structured(msg, output_schema=IndustryBrief, phase="phase3_industry")


def run_phase4_news(data: NameData, state: OrchestratorState, client: LLMClient) -> NewsBrief:
    agent = _agent(client, prompts.PHASE4_NEWS, state, "news")
    msg = (
        "Identify recent developments and catalysts that could force convergence "
        "within one year.\n\n"
        + digest.profile_block(data)
        + "\n\nBUSINESS BRIEF:\n"
        + state.business.model_dump_json(indent=2)
        + _transcripts_addendum(state)
        + "\n\n"
        + digest.news_text(data)
    )
    return agent.ask_structured(msg, output_schema=NewsBrief, phase="phase4_news")


def run_phase5_consolidate(
    data: NameData, state: OrchestratorState, client: LLMClient
) -> AssumptionSet:
    """Fresh PM agent fuses the four briefs into the gate object."""
    agent = spawn_fresh(
        client=client,
        role="consolidator",
        system=prompts.PHASE5_CONSOLIDATE + prompts.variant_suffix(state.config.prompt_variant),
        ticker=state.ticker,
        model=state.config.model,
        thinking=state.config.thinking,
    )
    msg = (
        "Fuse these four specialist briefs into ONE valuation assumption set. "
        "Choose the method, justify it, and fill the matching block with grounded, "
        "conservative numbers.\n\n"
        + digest.profile_block(data)
        + "\n\n"
        + digest.financials_block(data)
        + "\n\nFINANCIAL BRIEF:\n"
        + state.financials.model_dump_json(indent=2)
        + "\n\nBUSINESS BRIEF:\n"
        + state.business.model_dump_json(indent=2)
        + "\n\nINDUSTRY BRIEF:\n"
        + state.industry.model_dump_json(indent=2)
        + "\n\nNEWS/CATALYST BRIEF:\n"
        + state.news.model_dump_json(indent=2)
        + _transcripts_addendum(state)
    )
    return agent.ask_structured(
        msg, output_schema=AssumptionSet, phase="phase5_consolidate", max_tokens=16000
    )


def run_phase6_valuation(state: OrchestratorState) -> ValuationResult:
    """Code-only. The consolidation gate: refuse to run without an AssumptionSet."""
    if state.assumption_set is None:
        raise RuntimeError("Consolidation gate not crossed: assumption_set is None.")
    return run_valuation(state.assumption_set)


def run_phase7_redteam(
    data: NameData, state: OrchestratorState, client: LLMClient
) -> RedTeamReport:
    """Fresh, decorrelated (different model) skeptic with the full picture."""
    agent = spawn_fresh(
        client=client,
        role="redteam",
        system=prompts.REDTEAM,
        ticker=state.ticker,
        model=state.config.redteam_model,
        thinking=state.config.thinking,
    )
    msg = (
        "Here is a completed long thesis on a micro-cap stock. Try to refute it.\n\n"
        + digest.profile_block(data)
        + "\n\nFINANCIAL BRIEF:\n"
        + state.financials.model_dump_json(indent=2)
        + "\n\nBUSINESS BRIEF:\n"
        + state.business.model_dump_json(indent=2)
        + "\n\nINDUSTRY BRIEF:\n"
        + state.industry.model_dump_json(indent=2)
        + "\n\nNEWS/CATALYST BRIEF:\n"
        + state.news.model_dump_json(indent=2)
        + _transcripts_addendum(state)
        + "\n\nVALUATION ASSUMPTIONS:\n"
        + state.assumption_set.model_dump_json(indent=2)
        + "\n\nCOMPUTED FAIR VALUE (price-blinded):\n"
        + state.valuation.model_dump_json(indent=2)
    )
    return agent.ask_structured(msg, output_schema=RedTeamReport, phase="phase7_redteam")
