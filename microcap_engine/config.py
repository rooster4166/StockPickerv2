"""Central configuration for the Micro-Cap Value Engine.

Every tunable lives here so the strategy parameters from the design spec
(universe bounds, margin of safety, ensemble width, model choices) have a single
source of truth. Values can be overridden via ``MCE_*`` environment variables,
which keeps secrets and per-deployment knobs out of the code.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from typing import Any


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    return float(raw) if raw not in (None, "") else default


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    return int(raw) if raw not in (None, "") else default


def _env_str(name: str, default: str) -> str:
    raw = os.environ.get(name)
    return raw if raw not in (None, "") else default


@dataclass(frozen=True)
class Settings:
    # --- Universe (strategy params A.4) -------------------------------------
    mcap_min: float = field(default_factory=lambda: _env_float("MCE_MCAP_MIN", 50_000_000))
    mcap_max: float = field(default_factory=lambda: _env_float("MCE_MCAP_MAX", 300_000_000))

    # --- Selection / sizing ------------------------------------------------
    # Required undervaluation vs. fair value before a name is bought (B.5 / B.8).
    margin_of_safety: float = field(default_factory=lambda: _env_float("MCE_MARGIN_OF_SAFETY", 0.30))
    # Single position may not exceed this fraction of average daily $ volume (B.5).
    adv_fraction: float = field(default_factory=lambda: _env_float("MCE_ADV_FRACTION", 0.10))
    # Hard cap on any single name as a fraction of total capital.
    max_position_fraction: float = field(default_factory=lambda: _env_float("MCE_MAX_POSITION_FRACTION", 0.05))

    # --- Cheap reject-gate (B.2) -------------------------------------------
    # Drop a name ONLY on an unambiguous, high-confidence "obvious_no". The
    # asymmetry is brutal (a dropped 28x costs the 28x), so this bar is high.
    gate_drop_confidence: float = field(default_factory=lambda: _env_float("MCE_GATE_DROP_CONFIDENCE", 0.85))

    # --- Ensemble for confidence (B.4) -------------------------------------
    ensemble_n: int = field(default_factory=lambda: _env_int("MCE_ENSEMBLE_N", 3))
    # Coefficient of variation that maps to ~zero confidence. Confidence feeds
    # SIZING only — it never filters a flagged-undervalued name.
    dispersion_norm: float = field(default_factory=lambda: _env_float("MCE_DISPERSION_NORM", 0.5))

    # --- Models ------------------------------------------------------------
    # Opus for the deep reasoning; Sonnet as the decorrelated red-team so the
    # disconfirming pass is not the same model politely arguing with itself.
    deep_model: str = field(default_factory=lambda: _env_str("MCE_DEEP_MODEL", "claude-opus-4-8"))
    redteam_model: str = field(default_factory=lambda: _env_str("MCE_REDTEAM_MODEL", "claude-sonnet-4-6"))
    gate_model: str = field(default_factory=lambda: _env_str("MCE_GATE_MODEL", "claude-sonnet-4-6"))
    baseline_model: str = field(default_factory=lambda: _env_str("MCE_BASELINE_MODEL", "claude-opus-4-8"))
    effort: str = field(default_factory=lambda: _env_str("MCE_EFFORT", "high"))

    # --- Data --------------------------------------------------------------
    sec_user_agent: str = field(
        default_factory=lambda: _env_str("SEC_USER_AGENT", "microcap-value-engine contact@example.com")
    )
    # Per-filing character cap; full filings are huge and we keep the most
    # recent few so multi-period trends are visible without blowing the budget.
    max_filing_chars: int = field(default_factory=lambda: _env_int("MCE_MAX_FILING_CHARS", 60_000))
    max_filings: int = field(default_factory=lambda: _env_int("MCE_MAX_FILINGS", 6))

    output_dir: str = field(default_factory=lambda: _env_str("MCE_OUTPUT_DIR", "output"))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# A module-level default; callers may construct their own Settings for tests.
SETTINGS = Settings()
