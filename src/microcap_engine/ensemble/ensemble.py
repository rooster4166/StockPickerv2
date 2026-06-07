"""Ensemble for confidence — N decorrelated runs, dispersion sizes (never filters).

Split into ``run_members`` (do K deep dives) and ``blend_runs`` (fuse them into a
NameResult) so the universe runner can TIER ensemble depth: one full deep dive on
every survivor, then extra members only on the undervalued pool — cutting cost
without ever dropping a name. ``ensemble_deepdive`` is the all-at-once convenience.
"""

from __future__ import annotations

import statistics

from microcap_engine.config import settings
from microcap_engine.ensemble.configs import decorrelated_configs
from microcap_engine.llm.client import LLMClient
from microcap_engine.orchestrator.orchestrator import Orchestrator
from microcap_engine.orchestrator.state import OrchestratorConfig
from microcap_engine.schemas.name_result import (
    BlendedFairValue,
    DeepDiveResult,
    NameData,
    NameResult,
)
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)


def run_members(
    data: NameData, client: LLMClient, run_id: str, configs: list[OrchestratorConfig]
) -> list[DeepDiveResult]:
    runs: list[DeepDiveResult] = []
    for cfg in configs:
        try:
            runs.append(Orchestrator(data, cfg, client, run_id).analyze())
        except Exception as e:  # one member failing is tolerable in an ensemble
            log.warning("[%s] ensemble member %s failed: %s", data.ticker, cfg.label, e)
    return runs


def blend_runs(ticker: str, runs: list[DeepDiveResult]) -> NameResult:
    if not runs:
        raise RuntimeError(f"No successful deep-dive runs for {ticker}.")
    medians = [r.valuation.fair_value_median for r in runs]
    mean_fv = statistics.mean(medians)
    spread = len(medians) > 1 and mean_fv > 0
    dispersion = (statistics.pstdev(medians) / mean_fv) if spread else 0.0
    confidence = max(0.0, 1.0 - dispersion / settings.dispersion_norm)
    thesis_breakers = [
        c.description
        for r in runs
        for c in r.redteam.concerns
        if r.redteam.would_break_thesis and c.severity == "high"
    ]
    return NameResult(
        ticker=ticker,
        action="evaluated",
        runs=runs,
        fair_value=BlendedFairValue(
            median=round(statistics.median(medians), 4),
            p10=round(min(medians), 4),
            p90=round(max(medians), 4),
            n_runs=len(runs),
        ),
        confidence=round(confidence, 4),
        thesis_breakers=thesis_breakers,
    )


def ensemble_deepdive(
    data: NameData, client: LLMClient, run_id: str, n: int | None = None
) -> NameResult:
    n = n or settings.ensemble_n
    runs = run_members(data, client, run_id, decorrelated_configs(n))
    if not runs:
        raise RuntimeError(f"All ensemble members failed for {data.ticker}.")
    return blend_runs(data.ticker, runs)


def deepen(
    result: NameResult, data: NameData, client: LLMClient, run_id: str, target_n: int
) -> NameResult:
    """Add ensemble members up to ``target_n`` total, then re-blend (for sizing).

    Used on the undervalued pool only: the cheap members beyond the first exist to
    measure dispersion -> confidence -> position size, which only matters once a name
    is a buy candidate."""
    have = len(result.runs)
    if have >= target_n:
        return result
    extra_cfgs = decorrelated_configs(target_n)[have:target_n]
    more = run_members(data, client, run_id, extra_cfgs)
    if not more:
        return result
    combined = blend_runs(data.ticker, result.runs + more)
    combined.gate = result.gate
    return combined
