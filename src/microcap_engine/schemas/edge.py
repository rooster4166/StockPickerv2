"""Schemas for the edge pre-screener.

The screener ranks the universe by where the engine's DIFFERENTIAL edge is largest —
complex businesses whose mispricing is *protected by a complexity barrier* that thin /
low-quality coverage fails to cross (validated empirically: biotech/quantum/under-
covered-insurer = high edge; well-covered REIT / simple retail = low). It is a
cost-tiered funnel: a cheap deterministic FMP prior, then a Sonnet triage on the
survivors, so the expensive deep dive is spent only on the highest-edge names.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class EdgeSignals(BaseModel):
    """Cheap, FMP-sourced signals for one name (no LLM)."""

    ticker: str
    sector: str | None = None
    industry: str | None = None
    market_cap: float | None = None
    n_analysts: int = 0  # sum of grades-consensus buckets — coverage thinness
    n_institutions: int = 0  # 13F holders — retail vs institutional
    net_margin_ttm: float | None = None  # extreme negative / ~0 => pre-revenue
    ev_to_sales: float | None = None
    ev_to_ebitda: float | None = None
    revenue_ttm: float | None = None
    beta: float | None = None
    free_float_pct: float | None = None
    is_pre_revenue: bool = False


class EdgePrior(BaseModel):
    """Stage-1 deterministic edge score and its components."""

    ticker: str
    sector: str | None = None
    industry: str | None = None
    complexity_prior: float = Field(ge=0, le=1)  # sector/industry barrier prior
    coverage_gap: float = Field(ge=0, le=1)  # thin/low-quality coverage => high
    dislocation: float = Field(ge=0)  # mild multiplier from pre-revenue/extreme valn
    edge_prior: float = Field(ge=0)  # complexity_prior * coverage_gap * (1+dislocation)
    n_analysts: int = 0
    note: str = ""


class EdgeTriage(BaseModel):
    """Stage-2 Sonnet judgment refining the prior with real business understanding."""

    complexity_barrier: float = Field(
        ge=0, le=1,
        description="How much does valuing THIS business require specialized domain "
                    "knowledge (science, deep-tech, structural/cycle nuance) a generalist "
                    "micro-cap analyst would lack? 1=needs a true specialist, 0=any "
                    "competent generalist can value it.")
    coverage_understanding_gap: float = Field(
        ge=0, le=1,
        description="How likely is the prevailing market/analyst narrative to MISUNDERSTAND "
                    "this business (thin, promotional, or hype-driven coverage), leaving a "
                    "mispricing? 1=clearly under/mis-analyzed, 0=efficiently covered.")
    plausible_mispricing: bool = Field(
        description="Is there a credible case the price is materially wrong (either way)?")
    differential_edge: float = Field(
        ge=0, le=1,
        description="Net judgment: how large is OUR edge (an LLM that can absorb the full "
                    "record and understand the domain) vs the best human who would bother? "
                    "= roughly complexity_barrier x coverage_understanding_gap.")
    recommend_deep_dive: bool = Field(
        description="Should this name get the expensive full deep dive?")
    reasoning: str = Field(description="1-3 sentences justifying the scores.")


class OvervaluationVerdict(BaseModel):
    """Cheap, price-AWARE pre-screen of whether a name is OBVIOUSLY overvalued.

    Lives only in the screener tier (seeing price here is legitimate, like the cheap
    gate) — it never touches the price-blinded engine. Used to keep the deep dive
    spent on plausible BUYS, not on confirming obvious avoids. Recall-safe: only a
    high-confidence obvious case is cut; anything uncertain is kept for the deep dive.
    """

    posture: str = Field(description="cheap | fair | rich | uncertain — the valuation posture.")
    obviously_overvalued: bool = Field(
        description="TRUE only if a deep analysis would CLEARLY conclude 'avoid' without "
                    "needing the work (extreme premium to every plausible floor, no credible "
                    "long). Be conservative — when in doubt, FALSE (we will deep-dive it).")
    plausible_long: bool = Field(
        description="Is there a credible case this could be materially UNDERvalued?")
    reason: str = Field(description="1-2 sentences citing the key multiples/anchors.")


class EdgeCandidate(BaseModel):
    """A fully-scored universe name: prior + (optional) triage -> final rank key."""

    ticker: str
    sector: str | None = None
    industry: str | None = None
    edge_prior: float = 0.0
    triage: EdgeTriage | None = None
    final_edge: float = 0.0  # blended prior + triage; the ranking key
    n_analysts: int = 0
    note: str = ""
