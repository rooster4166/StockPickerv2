"""PersistentAgent — a context-holding conversation with one specialist role.

The PM keeps a reference to each phase's agent so it can re-query the *same*
context later (follow-up questions land in the accumulated history). A "fresh"
agent (see ``fresh_agent.spawn_fresh``) is just one constructed with no seeded
history — used for the red-team and ensemble members where we want an unanchored
opinion.

Context isolation: each agent reasons in its own window. Only the distilled,
validated brief (a Pydantic object) is passed on to the next phase — never the
raw transcript.
"""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

from microcap_engine.llm.client import LLMClient, Message
from microcap_engine.utils.ids import new_agent_id

T = TypeVar("T", bound=BaseModel)


class PersistentAgent:
    def __init__(
        self,
        *,
        client: LLMClient,
        system: str,
        model: str,
        role: str,
        ticker: str,
        agent_id: str | None = None,
        thinking: bool = True,
    ):
        self.client = client
        self.system = system
        self.model = model
        self.role = role
        self.ticker = ticker
        self.agent_id = agent_id or new_agent_id(role)
        self.thinking = thinking
        self._history: list[Message] = []

    # ── interaction ────────────────────────────────────────────────────────
    def ask_structured(
        self,
        user_message: str | list[dict],
        *,
        output_schema: type[T],
        phase: str,
        max_tokens: int | None = None,
    ) -> T:
        """Send a message and force a validated ``output_schema`` back.

        The user message and a JSON rendering of the structured reply are
        appended to history so later follow-ups see the full thread.
        """
        content = self._as_content(user_message)
        self._history.append({"role": "user", "content": content})
        parsed, _usage = self.client.parse(
            model=self.model,
            system=self.system,
            messages=self._history,
            output_schema=output_schema,
            ticker=self.ticker,
            phase=phase,
            label=f"{self.role}:{phase}",
            max_tokens=max_tokens,
            thinking=self.thinking,
        )
        # Record the assistant's structured answer as text so history stays valid.
        self._history.append(
            {"role": "assistant", "content": parsed.model_dump_json()}
        )
        return parsed

    # ── utilities ──────────────────────────────────────────────────────────
    @property
    def history(self) -> list[Message]:
        return self._history

    @staticmethod
    def _as_content(user_message: str | list[dict]) -> Any:
        return user_message
