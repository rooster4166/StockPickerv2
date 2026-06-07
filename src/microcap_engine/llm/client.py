"""The single chokepoint to the Anthropic Messages API.

Every LLM call in the engine goes through ``LLMClient``. Nothing else imports
``anthropic``. Each call:
  1. stamps a call_id,
  2. records the full request,
  3. invokes Anthropic (SDK auto-retries 429/5xx),
  4. records usage / latency / request_id / estimated cost,
  5. writes one JSONL audit record,
  6. returns the result.

Structured output uses ``messages.parse(output_format=PydanticModel)`` — the
recommended path. Per the Anthropic API, Opus 4.8 / Sonnet 4.6 reject
``temperature``/``top_p``/``top_k`` (400), so we never send them; decorrelation
is by model + prompt-variant + effort. Large, stable context (filing text, role
instructions) goes in the system prompt with ``cache_control`` so repeated
queries to the same persistent agent hit the cache.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, TypeVar

import anthropic
from pydantic import BaseModel

from microcap_engine.config import settings
from microcap_engine.llm.audit import AuditLogger, estimate_cost_usd
from microcap_engine.utils.ids import new_call_id, utc_now_iso
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)

# Anthropic message dicts; kept loose to avoid over-coupling to SDK types.
Message = dict[str, Any]


class LLMError(RuntimeError):
    """Raised when a call fails terminally or the model refuses."""


@dataclass
class TextReply:
    text: str
    usage: dict
    request_id: str | None
    stop_reason: str | None


def _as_cached_system(system: str | list[dict]) -> list[dict]:
    """Render a system prompt as blocks with a cache breakpoint on the last block.

    Caching the (stable) system prefix means re-querying the same persistent
    agent, or running many names that share boilerplate, pays ~0.1x for the
    cached portion instead of full price.
    """
    if isinstance(system, str):
        blocks = [{"type": "text", "text": system}]
    else:
        blocks = [dict(b) for b in system]
    if blocks:
        blocks[-1] = {**blocks[-1], "cache_control": {"type": "ephemeral"}}
    return blocks


class LLMClient:
    def __init__(self, audit: AuditLogger, api_key: str | None = None):
        key = api_key or settings.anthropic_api_key
        if not key:
            raise LLMError("ANTHROPIC_API_KEY is not set (see .env).")
        # Explicit per-call timeout so a slow/stuck call fails fast and the
        # structured-output retry loop (or SDK retry) can recover, instead of
        # blocking on the SDK's 10-minute default.
        self._client = anthropic.Anthropic(
            api_key=key, timeout=settings.call_timeout_s, max_retries=2
        )
        self.audit = audit

    # ── structured output ──────────────────────────────────────────────────
    def parse(
        self,
        *,
        model: str,
        system: str | list[dict],
        messages: list[Message],
        output_schema: type[T],
        ticker: str,
        phase: str,
        label: str,
        max_tokens: int | None = None,
        thinking: bool = True,
    ) -> tuple[T, dict]:
        """Force a validated ``output_schema`` instance out of the model.

        Returns (parsed_object, usage_dict). Raises LLMError on refusal.
        """
        base_max = max_tokens or settings.max_tokens
        cur_max = max(base_max, 12000)
        last_err: Exception | None = None
        working: list[Message] = list(messages)
        use_tool = False  # start on the fast strict path; fall back if grammar too big

        # Extra attempts so a fallback switch doesn't consume the repair budget.
        for attempt in range(settings.schema_repair_retries + 2):
            call_id = new_call_id()
            started = time.monotonic()
            try:
                if use_tool:
                    resp, parsed, kwargs = self._tool_invoke(
                        model, system, working, output_schema, cur_max, thinking)
                else:
                    resp, parsed, kwargs = self._format_invoke(
                        model, system, working, output_schema, cur_max, thinking)
            except anthropic.AuthenticationError as e:
                self._audit_failure(ticker, call_id, model, phase, f"{label}#auth", e)
                raise LLMError(f"{label}: auth error: {e}") from e
            except anthropic.BadRequestError as e:
                last_err = e
                msg = str(e).lower()
                if not use_tool and any(k in msg for k in
                                        ("grammar", "strict", "compiled", "schema too")):
                    # Schema too complex for strict structured output -> tool-use.
                    use_tool = True
                    self._audit_failure(ticker, call_id, model, phase,
                                        f"{label}#fmt->tool", e)
                elif "max_tokens" in msg or "length" in msg:
                    cur_max = min(cur_max * 2, settings.max_tokens_ceiling)
                    self._audit_failure(ticker, call_id, model, phase,
                                        f"{label}#badreq(len)", e)
                else:
                    self._audit_failure(ticker, call_id, model, phase,
                                        f"{label}#badreq", e)
                continue
            except Exception as e:
                last_err = e
                msg = str(e).lower()
                truncated = any(k in msg for k in
                                ("max_tokens", "length", "truncat", "finish_reason"))
                self._audit_failure(ticker, call_id, model, phase,
                                    f"{label}#try{attempt}"
                                    f"({'truncated' if truncated else 'error'}@{cur_max})", e)
                if truncated:
                    cur_max = min(cur_max * 2, settings.max_tokens_ceiling)
                else:
                    working = list(messages) + [self._repair_msg(output_schema, e)]
                continue
            latency = time.monotonic() - started

            usage = self._usage_dict(resp)
            self._audit_success(
                ticker, call_id, model, phase, label, kwargs, resp, usage, latency,
                structured=True,
            )
            if getattr(resp, "stop_reason", None) == "refusal":
                last_err = LLMError("model refused")
                continue
            if parsed is None:
                last_err = LLMError(f"no parsed output (stop={resp.stop_reason})")
                if getattr(resp, "stop_reason", None) == "max_tokens":
                    cur_max = min(cur_max * 2, settings.max_tokens_ceiling)
                elif use_tool:
                    working = list(messages) + [{
                        "role": "user",
                        "content": f"You did not call the emit tool. Call "
                                   f"emit_{output_schema.__name__.lower()} now with the "
                                   f"complete, schema-valid object.",
                    }]
                continue
            return parsed, usage

        raise LLMError(
            f"{label}: structured output failed after {attempt + 1} attempts: {last_err}"
        ) from last_err

    def _thinking_cfg(self, thinking: bool) -> dict | None:
        if not thinking:
            return None
        disp = "summarized" if settings.capture_thinking else "omitted"
        return {"type": "adaptive", "display": disp}

    def _format_invoke(self, model, system, messages, schema, max_tokens, thinking):
        """Strict structured output via output_format (fast, grammar-limited)."""
        kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "system": _as_cached_system(system),
            "messages": messages,
            "output_format": schema,
        }
        tc = self._thinking_cfg(thinking)
        if tc:
            kwargs["thinking"] = tc
        resp = self._client.messages.parse(**kwargs)
        return resp, getattr(resp, "parsed_output", None), kwargs

    def _tool_invoke(self, model, system, messages, schema, max_tokens, thinking):
        """Non-strict tool-use fallback — no grammar compilation, so it handles
        arbitrarily complex schemas. tool_choice must be 'auto' when thinking is on
        (forced tool + thinking is a 400), so we instruct the model to call it."""
        tname = f"emit_{schema.__name__.lower()}"
        tool = {
            "name": tname,
            "description": f"Return the {schema.__name__} as structured data.",
            "input_schema": schema.model_json_schema(),
        }
        msgs = list(messages) + [{
            "role": "user",
            "content": f"Respond by calling the {tname} tool with the complete, "
                       f"schema-valid object. Do not write a text answer.",
        }]
        kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "system": _as_cached_system(system),
            "messages": msgs,
            "tools": [tool],
            "tool_choice": {"type": "auto"},
        }
        tc = self._thinking_cfg(thinking)
        if tc:
            kwargs["thinking"] = tc
        resp = self._client.messages.create(**kwargs)
        block = next((b for b in resp.content
                      if getattr(b, "type", None) == "tool_use"
                      and getattr(b, "name", None) == tname), None)
        parsed = schema.model_validate(block.input) if block is not None else None
        return resp, parsed, kwargs

    def tool_turn(
        self,
        *,
        model: str,
        system: str | list[dict],
        messages: list[Message],
        tools: list[dict],
        ticker: str,
        phase: str,
        label: str,
        max_tokens: int | None = None,
        thinking: bool = True,
        tool_choice: dict | None = None,
    ):
        """One audited turn of an agentic tool-use loop. Returns the raw response
        (which may contain tool_use blocks). The caller runs the loop, executes
        tools, and feeds results back. Server tools (e.g. web_search) are allowed."""
        kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens or settings.max_tokens,
            "system": _as_cached_system(system),
            "messages": messages,
            "tools": tools,
            "tool_choice": tool_choice or {"type": "auto"},
            # Auto-cache the growing conversation prefix: in the agentic loop the
            # prior turns are stable, so each turn reads the cache instead of
            # re-paying full price for the whole transcript.
            "cache_control": {"type": "ephemeral"},
        }
        # Forced tool_choice + thinking is a 400; only enable thinking with auto.
        if thinking and kwargs["tool_choice"].get("type") == "auto":
            tc = self._thinking_cfg(thinking)
            if tc:
                kwargs["thinking"] = tc
        call_id = new_call_id()
        started = time.monotonic()
        try:
            resp = self._client.messages.create(**kwargs)
        except anthropic.APIError as e:  # pragma: no cover - network
            self._audit_failure(ticker, call_id, model, phase, label, e)
            raise LLMError(f"{label}: tool turn failed: {e}") from e
        latency = time.monotonic() - started
        usage = self._usage_dict(resp)
        # Audit without echoing the (large) tool list each turn.
        self._audit_success(
            ticker, call_id, model, phase, label,
            {"messages": messages[-2:], "max_tokens": kwargs["max_tokens"],
             "thinking": kwargs.get("thinking"), "n_tools": len(tools)},
            resp, usage, latency, structured=False,
        )
        return resp

    @staticmethod
    def _repair_msg(schema, err: Exception) -> Message:
        return {
            "role": "user",
            "content": f"Your previous response did not satisfy the {schema.__name__} "
                       f"schema/constraints. Error:\n{str(err)[:1500]}\nReturn a "
                       f"corrected object that fully satisfies the schema and all "
                       f"stated constraints.",
        }

    # ── free text ──────────────────────────────────────────────────────────
    def complete_text(
        self,
        *,
        model: str,
        system: str | list[dict],
        messages: list[Message],
        ticker: str,
        phase: str,
        label: str,
        max_tokens: int | None = None,
        thinking: bool = True,
    ) -> TextReply:
        call_id = new_call_id()
        kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens or settings.max_tokens,
            "system": _as_cached_system(system),
            "messages": messages,
        }
        if thinking:
            # display=summarized so thinking text is populated (default is omitted
            # on Opus 4.8/4.7) and we can capture it in the audit trace.
            disp = "summarized" if settings.capture_thinking else "omitted"
            kwargs["thinking"] = {"type": "adaptive", "display": disp}

        started = time.monotonic()
        try:
            resp = self._client.messages.create(**kwargs)
        except anthropic.APIError as e:  # pragma: no cover - network
            self._audit_failure(ticker, call_id, model, phase, label, e)
            raise LLMError(f"{label}: Anthropic call failed: {e}") from e
        latency = time.monotonic() - started

        usage = self._usage_dict(resp)
        self._audit_success(
            ticker, call_id, model, phase, label, kwargs, resp, usage, latency,
            structured=False,
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
        return TextReply(
            text=text,
            usage=usage,
            request_id=getattr(resp, "_request_id", None),
            stop_reason=getattr(resp, "stop_reason", None),
        )

    # ── audit helpers ──────────────────────────────────────────────────────
    @staticmethod
    def _usage_dict(resp: Any) -> dict:
        u = getattr(resp, "usage", None)
        if u is None:
            return {}
        return {
            "input_tokens": getattr(u, "input_tokens", 0),
            "output_tokens": getattr(u, "output_tokens", 0),
            "cache_creation_input_tokens": getattr(u, "cache_creation_input_tokens", 0) or 0,
            "cache_read_input_tokens": getattr(u, "cache_read_input_tokens", 0) or 0,
        }

    def _audit_success(
        self, ticker, call_id, model, phase, label, kwargs, resp, usage, latency, structured
    ) -> None:
        stop = getattr(resp, "stop_reason", None)
        record = {
            "call_id": call_id,
            "ts": utc_now_iso(),
            "run_id": self.audit.run_id,
            "ticker": ticker,
            "phase": phase,
            "label": label,
            "model": model,
            "structured": structured,
            "request": {
                "system": kwargs.get("system"),
                "messages": kwargs.get("messages"),
                "max_tokens": kwargs.get("max_tokens"),
                "thinking": kwargs.get("thinking"),
                "output_schema": getattr(kwargs.get("output_format"), "__name__", None),
            },
            # Full per-phase trace: thinking + text + tool calls (untruncated up
            # to a large safety cap), so nothing is hidden for debugging/audit.
            "response_blocks": self._content_blocks(resp),
            "response_text": self._response_preview(resp),
            "stop_reason": stop,
            "truncated": stop == "max_tokens",  # max_tokens cut the response off
            "request_id": getattr(resp, "_request_id", None),
            "usage": usage,
            "latency_s": round(latency, 3),
            "cost_usd": estimate_cost_usd(model, usage),
        }
        self.audit.record(ticker, record)

    @staticmethod
    def _content_blocks(resp: Any) -> list[dict]:
        """Full, structured trace of every content block returned."""
        blocks: list[dict] = []
        for b in getattr(resp, "content", []) or []:
            t = getattr(b, "type", None)
            if t == "thinking":
                blocks.append({"type": "thinking",
                               "thinking": (getattr(b, "thinking", "") or "")[:40000]})
            elif t == "redacted_thinking":
                blocks.append({"type": "redacted_thinking"})
            elif t == "text":
                blocks.append({"type": "text", "text": (getattr(b, "text", "") or "")[:60000]})
            elif t == "tool_use":
                blocks.append({"type": "tool_use", "name": getattr(b, "name", None),
                               "input": getattr(b, "input", None)})
            else:
                blocks.append({"type": str(t)})
        return blocks

    def _audit_failure(self, ticker, call_id, model, phase, label, err) -> None:
        self.audit.record(
            ticker,
            {
                "call_id": call_id,
                "ts": utc_now_iso(),
                "run_id": self.audit.run_id,
                "ticker": ticker,
                "phase": phase,
                "label": label,
                "model": model,
                "error": str(err),
                "cost_usd": 0.0,
            },
        )

    @staticmethod
    def _response_preview(resp: Any) -> str:
        parts = []
        for b in getattr(resp, "content", []) or []:
            t = getattr(b, "type", None)
            if t == "text":
                parts.append(getattr(b, "text", ""))
            elif t == "tool_use":
                parts.append(f"[tool_use:{getattr(b, 'name', '')}] "
                             + str(getattr(b, "input", "")))
        return "".join(parts)[:24000]
