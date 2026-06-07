"""Ensemble for confidence — NOT for pruning (design spec B.4).

Run each surviving name a few times with decorrelated configurations. The
dispersion of the per-share fair-value medians becomes a **confidence signal
that feeds position sizing**. It is never a filter: a flagged-undervalued name is
never discarded because runs disagreed — disagreement shrinks its size, it does
not kill it. This preserves the breadth and convexity behind the proof of
concept's returns.
"""

from __future__ import annotations

import logging
import statistics
from typing import Any, Optional

from ..config import SETTINGS, Settings
from ..data.types import CompanyData
from .orchestrator import Orchestrator, OrchestratorConfig

log = logging.getLogger(__name__)


def decorrelated_configs(n: int, settings: Settings = SETTINGS) -> list[OrchestratorConfig]:
    """Build n decorrelated configurations.

    Decorrelation comes from rotating the deep/red-team model pairing, the effort
    level, and an analytical framing nudge — not from sampling temperature, which
    is removed on Opus 4.8.
    """
    deep, red = settings.deep_model, settings.redteam_model
    palette = [
        OrchestratorConfig(model=deep, redteam_model=red, effort="high",
                           framing="Lead with downside protection and balance-sheet safety."),
        OrchestratorConfig(model=red, redteam_model=deep, effort="high",
                           framing="Lead with normalized earning power and cash generation."),
        OrchestratorConfig(model=deep, redteam_model=red, effort="medium",
                           framing="Lead with catalysts and asset value realizable within a year."),
        OrchestratorConfig(model=red, redteam_model=deep, effort="medium",
                           framing="Lead with competitive position and through-cycle margins."),
    ]
    out = []
    for i in range(max(1, n)):
        out.append(palette[i % len(palette)])
    return out


def _median_fv(run: dict) -> Optional[float]:
    fv = run.get("fair_value")
    if fv and fv.get("median") is not None:
        return float(fv["median"])
    return None


def blend(runs: list[dict]) -> Optional[dict]:
    """Blend per-share fair values across runs (median of each band)."""
    lows = [r["fair_value"]["low"] for r in runs if r.get("fair_value")]
    meds = [r["fair_value"]["median"] for r in runs if r.get("fair_value")]
    highs = [r["fair_value"]["high"] for r in runs if r.get("fair_value")]
    if not meds:
        return None
    return {
        "low": statistics.median(lows),
        "median": statistics.median(meds),
        "high": statistics.median(highs),
    }


def confidence_from_dispersion(medians: list[float], settings: Settings = SETTINGS) -> float:
    """Map coefficient-of-variation of the medians to a confidence in [0,1]."""
    medians = [m for m in medians if m is not None]
    if len(medians) < 2:
        return 0.5  # single usable run: neutral confidence, never a filter
    mean = statistics.mean(medians)
    if mean == 0:
        return 0.0
    dispersion = statistics.pstdev(medians) / abs(mean)
    return max(0.0, 1.0 - dispersion / settings.dispersion_norm)


def ensemble_deepdive(
    company: CompanyData,
    llm: Any,
    n: Optional[int] = None,
    settings: Settings = SETTINGS,
) -> dict:
    """Run the deep dive n times (decorrelated) and produce value + confidence."""
    n = n or settings.ensemble_n
    runs: list[dict] = []
    for cfg in decorrelated_configs(n, settings):
        try:
            runs.append(Orchestrator(company, llm, cfg, settings).analyze())
        except Exception as exc:  # noqa: BLE001 - one run failing must not sink the name
            log.warning("ensemble run failed for %s: %s", company.ticker, exc)

    usable = [r for r in runs if r.get("fair_value")]
    medians = [_median_fv(r) for r in usable]
    confidence = confidence_from_dispersion(medians, settings)
    fair_value = blend(usable)

    # Catalyst probability blended across runs (informational / sizing tilt).
    p_cats = [float(r.get("p_catalyst", 0.0)) for r in runs]
    p_catalyst = statistics.median(p_cats) if p_cats else 0.0

    return {
        "ticker": company.ticker,
        "action": "analyzed",
        "fair_value": fair_value,  # per-share {low,median,high} or None
        "confidence": confidence,
        "p_catalyst": p_catalyst,
        "n_runs": len(runs),
        "n_usable": len(usable),
        "runs": runs,
    }
