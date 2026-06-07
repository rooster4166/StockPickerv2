"""Decorrelated ensemble configurations.

Decorrelation sources (Opus 4.8 rejects temperature, so NOT temperature):
  1. prompt variant (different analytical framing per member),
  2. red-team model (a different model family member),
  3. (future) different main models per member.

For the first slice, members differ by prompt variant; bumping to multi-model is
a one-line change here.
"""

from __future__ import annotations

from microcap_engine.config import settings
from microcap_engine.orchestrator.state import OrchestratorConfig

_VARIANTS = ["a", "b", "c"]


def decorrelated_configs(n: int) -> list[OrchestratorConfig]:
    configs: list[OrchestratorConfig] = []
    for i in range(n):
        variant = _VARIANTS[i % len(_VARIANTS)]
        configs.append(
            OrchestratorConfig(
                label=f"ens{i}-{variant}",
                model=settings.main_model,
                redteam_model=settings.redteam_model,
                prompt_variant=variant,
            )
        )
    return configs
