"""Orchestrator config + mutable per-run state.

The state object threads through the seven phases in strict order. Phase 6
(valuation) asserts ``assumption_set`` exists before it runs — the gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from microcap_engine.config import settings
from microcap_engine.schemas.assumptions import AssumptionSet
from microcap_engine.schemas.briefs import (
    BusinessBrief,
    FinancialsBrief,
    IndustryBrief,
    NewsBrief,
    TranscriptBrief,
)
from microcap_engine.schemas.redteam import RedTeamReport
from microcap_engine.schemas.valuation import ValuationResult


@dataclass
class OrchestratorConfig:
    """One decorrelated configuration. Decorrelation is by model + prompt
    variant (NOT temperature — Opus 4.8 rejects it)."""

    label: str = "base"
    model: str = field(default_factory=lambda: settings.main_model)  # reasoning (Opus)
    redteam_model: str = field(default_factory=lambda: settings.redteam_model)
    extract_model: str = field(default_factory=lambda: settings.extract_model)  # Sonnet
    prompt_variant: str = "a"  # selects a framing in the phase prompts
    thinking: bool = True


@dataclass
class OrchestratorState:
    run_id: str
    ticker: str
    config: OrchestratorConfig
    transcripts: TranscriptBrief | None = None
    financials: FinancialsBrief | None = None
    business: BusinessBrief | None = None
    industry: IndustryBrief | None = None
    news: NewsBrief | None = None
    assumption_set: AssumptionSet | None = None
    valuation: ValuationResult | None = None
    redteam: RedTeamReport | None = None
