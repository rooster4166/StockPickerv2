"""LLM access layer.

A thin wrapper over the Anthropic SDK that the rest of the engine depends on
through a small interface (``complete`` / ``complete_json``). Keeping the surface
narrow means the deep-dive code never touches SDK specifics, and tests can inject
a fake implementing the same two methods to run the whole pipeline offline.

Conventions baked in (per the claude-api guidance):
  * Default model is ``claude-opus-4-8`` with **adaptive thinking** and an
    ``effort`` set in ``output_config``.
  * Requests **stream** and use ``get_final_message()`` so large outputs don't
    hit HTTP timeouts.
  * Large, reused context (price-blinded company data) is passed as a cached
    system block so the N ensemble runs share the prefix instead of re-paying.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Optional, Sequence, Union

from ..config import SETTINGS, Settings

log = logging.getLogger(__name__)

SystemPrompt = Union[str, Sequence[dict]]
Messages = list[dict]


class LLMError(RuntimeError):
    pass


def _system_blocks(system: SystemPrompt, cache: bool) -> list[dict]:
    if isinstance(system, str):
        block = {"type": "text", "text": system}
        if cache:
            block["cache_control"] = {"type": "ephemeral"}
        return [block]
    blocks = [dict(b) for b in system]
    if cache and blocks:
        blocks[-1] = {**blocks[-1], "cache_control": {"type": "ephemeral"}}
    return blocks


def _extract_text(message) -> str:
    return "".join(b.text for b in message.content if getattr(b, "type", None) == "text")


def _loads_lenient(text: str) -> dict:
    """Parse JSON, tolerating code fences or leading prose from the model."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Last resort: grab the outermost {...} span.
        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise


class AnthropicLLM:
    """Concrete LLM client backed by the Anthropic Messages API."""

    def __init__(self, settings: Settings = SETTINGS, client: Any = None, max_retries: int = 4):
        self.settings = settings
        if client is None:
            import anthropic

            client = anthropic.Anthropic(max_retries=max_retries)
        self._client = client

    # ------------------------------------------------------------------ text
    def complete(
        self,
        *,
        system: SystemPrompt,
        messages: Messages,
        model: Optional[str] = None,
        effort: Optional[str] = None,
        max_tokens: int = 16000,
        thinking: bool = True,
        cache_system: bool = True,
    ) -> str:
        model = model or self.settings.deep_model
        output_config: dict[str, Any] = {"effort": effort or self.settings.effort}
        kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "system": _system_blocks(system, cache_system),
            "messages": messages,
            "output_config": output_config,
        }
        if thinking:
            kwargs["thinking"] = {"type": "adaptive"}
        try:
            with self._client.messages.stream(**kwargs) as stream:
                final = stream.get_final_message()
        except Exception as exc:  # noqa: BLE001 - surface a uniform error type
            raise LLMError(f"completion failed ({model}): {exc}") from exc
        return _extract_text(final)

    # ------------------------------------------------------------------ json
    def complete_json(
        self,
        *,
        system: SystemPrompt,
        messages: Messages,
        schema: Optional[dict] = None,
        model: Optional[str] = None,
        effort: Optional[str] = None,
        max_tokens: int = 16000,
        thinking: bool = True,
        cache_system: bool = True,
    ) -> dict:
        """Return parsed JSON.

        When ``schema`` is provided, the response is constrained via
        ``output_config.format`` (structured outputs). For heterogeneous outputs
        (e.g. method-specific valuation assumptions) pass ``schema=None`` and the
        result is parsed leniently from the model's text.
        """
        model = model or self.settings.deep_model
        output_config: dict[str, Any] = {"effort": effort or self.settings.effort}
        if schema is not None:
            output_config["format"] = {"type": "json_schema", "schema": schema}
        kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "system": _system_blocks(system, cache_system),
            "messages": messages,
            "output_config": output_config,
        }
        if thinking:
            kwargs["thinking"] = {"type": "adaptive"}
        try:
            with self._client.messages.stream(**kwargs) as stream:
                final = stream.get_final_message()
        except Exception as exc:  # noqa: BLE001
            raise LLMError(f"json completion failed ({model}): {exc}") from exc
        text = _extract_text(final)
        try:
            return _loads_lenient(text)
        except json.JSONDecodeError as exc:
            raise LLMError(f"model did not return valid JSON ({model}): {text[:400]}") from exc
