"""Independent quality judge — the best-in-existence acceptance gate.

Distinct from the red-team (which hunts valuation-changing FLAWS): the judge asks
whether the final report is the single most rigorous, complete, and accurate
valuation of this company that could exist — better than any sell-side initiation
or firm report — and independently verifies the headline facts. The engine is not
done until the judge approves.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class FactCheck(BaseModel):
    claim: str = Field(description="A headline number/claim from the memo.")
    verified: bool = Field(description="True if it matches the actual filing/source.")
    note: str = Field(default="", description="Correct value or discrepancy if not verified.")


class JudgeReport(BaseModel):
    best_in_existence: bool = Field(
        description="True ONLY if this is genuinely the best, most complete and accurate "
        "valuation report that exists for this company AND its argument is compelling enough that "
        "you would personally act on the conclusion."
    )
    would_act_on_it: bool = Field(
        default=False,
        description="Would YOU — a skeptical elite investor — stake your reputation acting on this "
        "report's conclusion? (Extraordinary claimed mispricings require airtight support.)",
    )
    consensus_summary: str = Field(
        default="", description="What the market / analyst consensus believes about this name and "
        "WHY (researched via web search).",
    )
    more_convincing_than_consensus: bool = Field(
        default=False,
        description="Is this report's analysis at least as compelling and better-reasoned than the "
        "market consensus — i.e. you'd back it over the crowd? (Exact alignment counts as yes.)",
    )
    conviction_reasoning: str = Field(
        default="", description="Why you are (or are not) convinced enough to act on the thesis."
    )
    overall_score: int = Field(ge=0, le=100, description="Quality vs the ideal report (0-100).")
    fact_checks: list[FactCheck] = Field(default_factory=list)
    factual_errors: list[str] = Field(
        default_factory=list, description="Material factual/numeric errors vs the filings."
    )
    gaps_vs_best_in_class: list[str] = Field(
        default_factory=list,
        description="Concrete things a best-in-class report would add or do better.",
    )
    strengths: list[str] = Field(default_factory=list)
    verdict: str = Field(description="The reasoned overall judgment.")
