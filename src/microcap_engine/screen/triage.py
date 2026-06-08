"""Stage 2 — Sonnet edge triage on the Stage-1 survivors.

The deterministic prior is coarse (a 'Software - Infrastructure' label hides a quantum
company; a heavily-covered insurtech may still be hype-mispriced). A cheap Sonnet read
of the actual business — with the cheap signals in hand — judges the real complexity
BARRIER and the coverage-understanding GAP, and recommends whether the name earns the
expensive deep dive. Runs only on the top-of-prior slice, so it is cheap.
"""

from __future__ import annotations

from microcap_engine.config import settings
from microcap_engine.llm.client import LLMClient
from microcap_engine.llm.fresh_agent import spawn_fresh
from microcap_engine.schemas.edge import EdgePrior, EdgeSignals, EdgeTriage
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)

_TRIAGE_SYSTEM = (
    "You triage micro-cap stocks for an AI equity-research engine whose EDGE is that it can "
    "absorb the entire public record and genuinely understand hard domains (biology, quantum/"
    "deep-tech, insurance cycles, complex structures) that thinly-staffed human coverage cannot. "
    "The engine's expensive deep dive is worth spending ONLY where its DIFFERENTIAL edge is "
    "large = (the business is genuinely complex to value, needing specialist domain knowledge) "
    "AND (coverage is thin / promotional / hype-driven, so the price is likely wrong). A complex "
    "but competently-covered name (efficient price) is NOT worth it; a thinly-covered but SIMPLE "
    "business (any generalist can value it) is NOT worth it — the mispricing must be PROTECTED by "
    "a complexity barrier the engine uniquely crosses. Judge THIS business from its description "
    "and the coverage signals; score complexity_barrier, coverage_understanding_gap, "
    "differential_edge (≈ their product), and recommend_deep_dive. Be decisive and calibrated."
)


def triage(client: LLMClient, signals: EdgeSignals, prior: EdgePrior,
           description: str, company_name: str) -> EdgeTriage:
    agent = spawn_fresh(
        client=client, role="edge_triage", system=_TRIAGE_SYSTEM,
        ticker=signals.ticker, model=settings.edge_triage_model, thinking=False)
    msg = (
        f"COMPANY: {company_name} ({signals.ticker})\n"
        f"Sector / industry: {signals.sector} / {signals.industry}\n"
        f"Market cap: {signals.market_cap}\n"
        f"COVERAGE SIGNALS: {signals.n_analysts} sell-side analysts, "
        f"{signals.n_institutions} institutional (13F) holders"
        + (", PRE-REVENUE / negative-margin" if signals.is_pre_revenue else "")
        + f". EV/Sales={signals.ev_to_sales}, net margin TTM={signals.net_margin_ttm}.\n"
        f"(Deterministic prior edge: {prior.edge_prior} — complexity {prior.complexity_prior}, "
        f"coverage_gap {prior.coverage_gap}.)\n\n"
        f"BUSINESS DESCRIPTION:\n{(description or '(none)')[:1500]}\n\n"
        "Score the edge for THIS business and recommend whether it earns the deep dive."
    )
    try:
        return agent.ask_structured(msg, output_schema=EdgeTriage,
                                    phase="edge_triage", max_tokens=1500)
    except Exception as e:  # pragma: no cover - never let triage kill the screen
        log.warning("edge triage failed for %s: %s", signals.ticker, e)
        # Fail OPEN (recall-safe): keep the name in contention at its prior level.
        return EdgeTriage(
            complexity_barrier=prior.complexity_prior,
            coverage_understanding_gap=prior.coverage_gap,
            plausible_mispricing=True, differential_edge=min(prior.edge_prior, 1.0),
            recommend_deep_dive=prior.edge_prior >= 0.2,
            reasoning="triage unavailable; carried prior forward (recall-safe).")
