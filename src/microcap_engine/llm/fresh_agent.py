"""Factory for fresh, unanchored agents.

Same class as PersistentAgent — "fresh" simply means no seeded history and a new
identity. Used for the red-team (a decorrelated model seeking disconfirming
evidence), the cheap reject-gate, and each ensemble member's orchestrator.
"""

from __future__ import annotations

from microcap_engine.config import settings
from microcap_engine.llm.client import LLMClient
from microcap_engine.llm.persistent_agent import PersistentAgent


def spawn_fresh(
    *,
    client: LLMClient,
    role: str,
    system: str,
    ticker: str,
    model: str | None = None,
    thinking: bool = True,
) -> PersistentAgent:
    """Create a brand-new agent with no shared context.

    Defaults to the red-team model (a different model family member than the
    main pipeline) to maximize decorrelation when used for the red-team.
    """
    return PersistentAgent(
        client=client,
        system=system,
        model=model or settings.redteam_model,
        role=role,
        ticker=ticker,
        thinking=thinking,
    )
