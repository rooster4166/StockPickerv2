"""Distilled, cited briefs returned by each deep-dive phase.

Each phase reasons in its own context window and returns one of these — a
compact, grounded summary, never its raw transcript. Citations are required so
every downstream assumption can be traced to a filing, news item, or datapoint.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """A grounding reference. ``quote`` is the actual snippet relied upon."""

    source_kind: Literal["filing", "news", "fundamentals", "price", "profile"]
    quote: str = Field(description="The exact snippet of text or datapoint relied upon.")
    accession: str | None = Field(default=None, description="SEC accession number, if a filing.")
    section: str | None = Field(default=None, description="Filing section, e.g. 'Item 7'.")
    url: str | None = None


class PeriodPoint(BaseModel):
    """One time-series observation, e.g. a year's revenue."""

    period: str = Field(description="Fiscal period label, e.g. 'FY2024' or 'Q3-2024'.")
    value: float


class BalanceSheetSummary(BaseModel):
    cash_and_equivalents: float
    total_debt: float
    net_debt: float
    total_equity: float
    shares_outstanding: float


class FinancialsBrief(BaseModel):
    """Phase 1 — multi-period financial trends across ALL available filings."""

    revenue_trend: list[PeriodPoint]
    gross_margin_trend: list[PeriodPoint] = Field(default_factory=list)
    operating_margin_trend: list[PeriodPoint] = Field(default_factory=list)
    free_cash_flow_trend: list[PeriodPoint] = Field(default_factory=list)
    balance_sheet: BalanceSheetSummary
    dilution_history: list[PeriodPoint] = Field(
        default_factory=list, description="Shares outstanding over time."
    )
    anomalies: list[str] = Field(
        default_factory=list, description="Restatements, one-offs, accounting flags."
    )
    summary: str = Field(description="2-4 sentence narrative of the financial trajectory.")
    citations: list[Citation] = Field(min_length=1)


class Segment(BaseModel):
    name: str
    revenue_share: float | None = Field(default=None, description="Fraction of revenue, 0-1.")
    notes: str = ""


class BusinessBrief(BaseModel):
    """Phase 2 — how the company makes money."""

    segments: list[Segment] = Field(default_factory=list)
    unit_economics: str = Field(description="Drivers of revenue and cost per unit.")
    revenue_drivers: list[str] = Field(default_factory=list)
    moat_assessment: str
    summary: str
    citations: list[Citation] = Field(min_length=1)


class Catalyst(BaseModel):
    description: str
    expected_timing: str = Field(description="When convergence might occur, e.g. 'within 12mo'.")
    probability_note: str = Field(default="", description="Qualitative likelihood commentary.")


class IndustryBrief(BaseModel):
    """Phase 3 — industry position + the adjacent exposures a human would skip."""

    tam_estimate: float | None = Field(default=None, description="Total addressable market, USD.")
    growth_outlook: str
    competitive_position: str
    direct_comps: list[str] = Field(default_factory=list, description="Peer tickers.")
    adjacent_exposures: list[str] = Field(
        default_factory=list,
        description="Indirect dependencies (e.g. an oil-feedstock cost link).",
    )
    summary: str
    citations: list[Citation] = Field(min_length=1)


class NewsBrief(BaseModel):
    """Phase 4 — recent developments and catalysts that could force convergence."""

    recent_developments: list[str] = Field(default_factory=list)
    catalysts: list[Catalyst] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    summary: str
    citations: list[Citation] = Field(min_length=1)


class TranscriptBrief(BaseModel):
    """Distilled signal from earnings-call transcripts — only what matters.

    A dedicated agent reads the (long) transcripts in its own window and returns
    this compact extract so the orchestrator gets signal, not the raw calls.
    """

    guidance_signals: list[str] = Field(
        default_factory=list, description="Forward guidance, targets, or walk-backs."
    )
    capital_allocation: list[str] = Field(
        default_factory=list, description="Buybacks, dilution, capex, M&A, debt commentary."
    )
    tone_and_changes: list[str] = Field(
        default_factory=list,
        description="Notable shifts in management tone or narrative across quarters.",
    )
    red_flags: list[str] = Field(
        default_factory=list, description="Evasive answers, missed targets, churn, dependencies."
    )
    catalysts: list[str] = Field(default_factory=list)
    summary: str = ""
    citations: list[Citation] = Field(default_factory=list)
