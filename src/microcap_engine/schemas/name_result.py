"""Top-level per-name structures.

``NameData`` is the bundle handed to the orchestrator. It deliberately contains
**no ``Quote``** — the orchestrator is price-blinded by construction. The market
price is joined only later, in the portfolio layer.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from microcap_engine.data.models import (
    CompanyProfile,
    FilingDocument,
    FinancialPeriod,
    KeyMetrics,
    NewsItem,
    TranscriptItem,
)
from microcap_engine.schemas.assumptions import AssumptionSet
from microcap_engine.schemas.briefs import (
    BusinessBrief,
    Citation,
    FinancialsBrief,
    IndustryBrief,
    NewsBrief,
    TranscriptBrief,
)
from microcap_engine.schemas.dossier import FinalDossier
from microcap_engine.schemas.redteam import RedTeamReport
from microcap_engine.schemas.valuation import ValuationResult


class NameData(BaseModel):
    """Everything the engine reads about a name — EXCEPT the market price."""

    ticker: str
    profile: CompanyProfile
    financials: list[FinancialPeriod] = Field(default_factory=list)
    key_metrics: list[KeyMetrics] = Field(default_factory=list)
    filings: list[FilingDocument] = Field(default_factory=list)
    news: list[NewsItem] = Field(default_factory=list)
    transcripts: list[TranscriptItem] = Field(default_factory=list)


class GateVerdict(BaseModel):
    """Cheap reject-gate output. Drop only on obvious_no with high confidence."""

    verdict: Literal["obvious_no", "plausible", "ambiguous"]
    confidence: float = Field(ge=0, le=1)
    reason: str
    citations: list[Citation] = Field(default_factory=list)


class BlendedFairValue(BaseModel):
    median: float
    p10: float | None = None
    p90: float | None = None
    n_runs: int = 1


class DeepDiveResult(BaseModel):
    """The full output of one orchestrator run (one ensemble member)."""

    ticker: str
    config_label: str
    transcripts: TranscriptBrief | None = None
    financials: FinancialsBrief
    business: BusinessBrief
    industry: IndustryBrief
    news: NewsBrief
    assumption_set: AssumptionSet
    valuation: ValuationResult
    redteam: RedTeamReport


class NameResult(BaseModel):
    """The unit the portfolio layer consumes. Either dropped at the gate, or a
    full ensemble-blended evaluation. Still carries no price."""

    ticker: str
    action: Literal["drop", "evaluated"]
    gate: GateVerdict | None = None
    reason: str = ""

    # populated when action == "evaluated"
    runs: list[DeepDiveResult] = Field(default_factory=list)
    fair_value: BlendedFairValue | None = None
    confidence: float | None = None
    thesis_breakers: list[str] = Field(default_factory=list)

    # agentic output (the in-depth memo + structured dossier)
    memo_markdown: str | None = None
    dossier: FinalDossier | None = None
    red_team_rounds: int | None = None
    unresolved_concerns: list[str] = Field(default_factory=list)
    judge_approved: bool | None = None
    judge_score: int | None = None
    judge_gaps: list[str] = Field(default_factory=list)
    transcript_path: str | None = None

    # cost accounting (filled from the audit log after analysis)
    cost_usd: float | None = None
    total_tokens: int | None = None
    n_calls: int | None = None
