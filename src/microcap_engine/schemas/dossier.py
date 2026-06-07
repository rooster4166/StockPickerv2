"""Final output of the agentic PM: a structured dossier + a full markdown memo.

The PM submits BOTH: an extremely in-depth markdown investment memo (the full
justification, start to finish) and this structured object holding the discrete
parts we consume programmatically (fair value, method, conviction, drivers, risks).
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from microcap_engine.schemas.briefs import Citation


class FinalDossier(BaseModel):
    fair_value_per_share: float = Field(
        description="HEADLINE: fair market value per share — PV of probability-weighted future "
        "cash incl. growth/optionality (max a rational buyer pays today)."
    )
    intrinsic_value_floor: float = Field(
        default=0.0,
        description="Conservative floor: value on current/normalized earnings power, NO heroic "
        "growth (earnings-power / asset / book value). The margin-of-safety anchor.",
    )
    fair_value_low: float = Field(
        description="Low end of the FMV CONFIDENCE BAND (uncertainty around the expected value, "
        "≈ a lower percentile of the outcome distribution) — NOT a 'bear case' story."
    )
    fair_value_high: float = Field(
        description="High end of the FMV CONFIDENCE BAND (≈ an upper percentile) — NOT a 'bull "
        "case' story."
    )
    valuation_method: str = Field(
        description="The framework actually used, justified for THIS business "
        "(e.g. 'P/TBV x through-cycle ROE', 'multi-stage DCF', 'NAV on 2P reserves')."
    )
    confidence: float = Field(ge=0, le=1, description="Conviction in the fair value estimate.")
    thesis_summary: str = Field(description="2-4 sentence core thesis.")
    key_value_drivers: list[str] = Field(default_factory=list)
    key_risks: list[str] = Field(default_factory=list)
    what_would_change_my_mind: list[str] = Field(default_factory=list)
    diluted_shares_used: float | None = Field(
        default=None, description="Fully-diluted share count used in the valuation."
    )
    citations: list[Citation] = Field(default_factory=list)


class AgenticOutcome(BaseModel):
    """What the agentic orchestrator returns for one name."""

    ticker: str
    action: str  # "evaluated" | "drop"
    reject_reason: str = ""
    dossier: FinalDossier | None = None
    memo_markdown: str = ""
    red_team_rounds: int = 0
    unresolved_concerns: list[str] = Field(default_factory=list)
    judge_approved: bool = False
    judge_score: int = 0
    judge_gaps: list[str] = Field(default_factory=list)
    tool_calls: int = 0
    transcript_path: str = ""
