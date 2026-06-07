"""The persistent Agent — a context-holding conversational session.

Carried over from the design spec's engine properties (B.3):

  * **Context isolation** — each Agent owns its own message window and returns
    distilled, cited briefs to the orchestrator rather than dumping raw context.
  * **Persistent sessions** — the PM re-queries the *same* Agent for follow-ups
    (``ask`` appends to the running transcript), so the specialist keeps the full
    context it already built.
  * **Fresh agents** — when the PM wants an *unanchored* opinion it spawns a new
    Agent (``fork``-free construction), which starts clean with only the shared,
    cached system context.

The Agent is model-agnostic: pass any object exposing ``complete`` /
``complete_json`` (the real ``AnthropicLLM`` or a test fake).
"""

from __future__ import annotations

from typing import Any, Optional

from .client import Messages, SystemPrompt


class Agent:
    def __init__(
        self,
        llm: Any,
        *,
        system: SystemPrompt,
        model: Optional[str] = None,
        effort: Optional[str] = None,
        name: str = "agent",
    ):
        self.llm = llm
        self.system = system
        self.model = model
        self.effort = effort
        self.name = name
        self.messages: Messages = []

    # ------------------------------------------------------------------ text
    def ask(self, prompt: str, *, max_tokens: int = 16000) -> str:
        self.messages.append({"role": "user", "content": prompt})
        reply = self.llm.complete(
            system=self.system,
            messages=self.messages,
            model=self.model,
            effort=self.effort,
            max_tokens=max_tokens,
        )
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    # ------------------------------------------------------------------ json
    def ask_json(
        self, prompt: str, schema: Optional[dict] = None, *, max_tokens: int = 16000
    ) -> dict:
        self.messages.append({"role": "user", "content": prompt})
        result = self.llm.complete_json(
            system=self.system,
            messages=self.messages,
            schema=schema,
            model=self.model,
            effort=self.effort,
            max_tokens=max_tokens,
        )
        # Record a compact textual echo so follow-ups see prior structured turns.
        import json as _json

        self.messages.append({"role": "assistant", "content": _json.dumps(result)})
        return result

    def fresh(self, *, system: Optional[SystemPrompt] = None, name: Optional[str] = None) -> "Agent":
        """Spawn an unanchored sibling sharing the LLM and (by default) context."""
        return Agent(
            self.llm,
            system=system if system is not None else self.system,
            model=self.model,
            effort=self.effort,
            name=name or f"{self.name}-fresh",
        )
