"""Central configuration. The only place env vars are read.

Loads `.env` via pydantic-settings and exposes a singleton ``settings`` object.
Strategy constants (margin of safety, dispersion normalizer, model picks) live
here so they can be tuned in one place after backtest.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Repo root = three parents up from this file (src/microcap_engine/config.py).
REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
AUDIT_DIR = DATA_DIR / "audit"
CACHE_DIR = DATA_DIR / "cache"


class Settings(BaseSettings):
    """Runtime settings, sourced from environment / `.env`."""

    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Secrets ────────────────────────────────────────────────────────────
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    fmp_api_key: str = Field(default="", alias="FMP_API_KEY")
    sec_user_agent: str = Field(
        default="Micro-Cap Value Engine contact@example.com",
        alias="SEC_USER_AGENT",
    )

    # ── Model picks (per-task) ─────────────────────────────────────────────
    # Opus for reasoning/judgment; Sonnet for extraction/triage. The red-team is
    # Opus for maximum adversarial strength — decorrelated by fresh context +
    # adversarial framing, not by a weaker model.
    main_model: str = "claude-opus-4-8"        # reasoning phases 1-5
    reasoning_model: str = "claude-opus-4-8"   # alias, explicit
    redteam_model: str = "claude-opus-4-8"     # phase 7 (strong adversary)
    extract_model: str = "claude-sonnet-4-6"   # transcript distillation
    cheap_gate_model: str = "claude-sonnet-4-6"  # fast triage gate

    # ── Strategy constants ─────────────────────────────────────────────────
    # "agentic" (tool-using PM, default) or "phased" (the older fixed cascade).
    engine_mode: str = "agentic"
    agentic_max_steps: int = 60
    # Generous ceiling so a deep investigation is never force-submitted mid-analysis;
    # quality-over-cost for research/validation. Lower it for cost-sensitive batch runs.
    agentic_max_cost_usd: float = 75.0

    margin_of_safety: float = 0.30  # required (FV - price)/price to enter the pool
    dispersion_norm: float = 0.40  # confidence = max(0, 1 - dispersion/DISP_NORM)
    gate_drop_confidence: float = 0.85  # only drop on obvious_no AND conf >= this
    adv_liquidity_cap: float = 0.10  # max position = this fraction of $ ADV
    ensemble_n: int = 3  # decorrelated runs per surviving name

    # ── Universe bounds (USD) ──────────────────────────────────────────────
    min_market_cap: int = 50_000_000
    max_market_cap: int = 300_000_000

    # ── LLM call defaults ──────────────────────────────────────────────────
    # With summarized thinking, thinking + output share this budget, so keep it
    # generous; the structured-output path escalates further on truncation.
    max_tokens: int = 16000
    max_tokens_ceiling: int = 28000  # escalation cap (stays under SDK non-stream guard)
    schema_repair_retries: int = 2  # structured-output validation retries
    call_timeout_s: float = 300.0  # per-call wall-clock cap (SDK retries within)
    capture_thinking: bool = True  # record summarized thinking traces in the audit log

    @property
    def has_anthropic(self) -> bool:
        return bool(self.anthropic_api_key)

    @property
    def has_fmp(self) -> bool:
        return bool(self.fmp_api_key)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached singleton accessor."""
    return Settings()


settings = get_settings()
