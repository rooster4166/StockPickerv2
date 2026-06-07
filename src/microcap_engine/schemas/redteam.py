"""Red-team output — a decorrelated model hunting disconfirming evidence."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from microcap_engine.schemas.briefs import Citation


class Concern(BaseModel):
    category: Literal[
        "going_concern",
        "accounting",
        "litigation",
        "competition",
        "governance",
        "dilution",
        "valuation_assumption",
        "valuation_method",
        "liquidity",
        "data_error",
        "other",
    ]
    description: str
    severity: Literal["low", "medium", "high"]
    evidence: str = Field(description="The specific disconfirming fact found.")
    would_change_valuation: bool = Field(
        default=False,
        description="True if, were this correct, the fair value would materially change.",
    )


class RedTeamReport(BaseModel):
    concerns: list[Concern] = Field(default_factory=list)
    would_break_thesis: bool = Field(
        description="True if any concern, if accurate, invalidates the undervaluation thesis."
    )
    most_severe: Literal["none", "low", "medium", "high"] = "none"
    summary: str
    citations: list[Citation] = Field(default_factory=list)
