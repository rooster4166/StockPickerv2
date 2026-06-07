"""Tool-using reviewer — a reviewer that can VERIFY before it judges.

The red-team and the best-in-existence judge get the same read/verify tools the PM
has (financials, ratios, peers, filings, web research) so they can independently
check the memo's stated numbers and claims against the source data — a real
backstop, not just reasoning over the text. The reviewer runs a bounded tool loop,
then emits its structured verdict via an `emit_*` tool (same pattern as the PM's
submit). It is PERSISTENT, so the PM and the same reviewer can debate across rounds.
"""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from microcap_engine.llm.client import LLMClient
from microcap_engine.orchestrator import tools as toolkit
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


def _tr(tool_use_id: str, content: str) -> dict:
    return {"type": "tool_result", "tool_use_id": tool_use_id, "content": content or "(empty)"}


class ToolReviewer:
    def __init__(
        self,
        client: LLMClient,
        ctx: toolkit.ToolContext,
        *,
        system: str,
        output_schema: type[T],
        phase: str,
        model: str,
        max_turns: int = 6,
        default_factory=None,
    ):
        self.client = client
        self.ctx = ctx
        self.system = system
        self.schema = output_schema
        self.phase = phase
        self.model = model
        self.max_turns = max_turns
        self.ticker = ctx.ticker
        self.messages: list[dict] = []  # persistent across rounds (dialogue)
        self.last_trace: list[dict] = []  # reviewer's own verification turns (for transcript)
        self._default_factory = default_factory
        self._emit = f"emit_{output_schema.__name__.lower()}"
        self._tools = toolkit.verification_tool_specs() + [{
            "name": self._emit,
            "description": f"Emit your final {output_schema.__name__} verdict, AFTER you have "
                           f"verified the memo's key numbers/claims with the data and research "
                           f"tools.",
            "input_schema": output_schema.model_json_schema(),
        }]

    def review(self, task_msg: str) -> T:
        self.messages.append({"role": "user", "content": task_msg})
        round_trace: list[dict] = []  # this round's verification turns (for the transcript)
        for turn in range(self.max_turns):
            try:
                resp = self.client.tool_turn(
                    model=self.model, system=self.system, messages=self.messages,
                    tools=self._tools, ticker=self.ticker, phase=self.phase,
                    label=f"{self.phase}:t{turn}", max_tokens=9000, thinking=True)
            except Exception as e:  # pragma: no cover - never block forever
                log.warning("[%s] reviewer %s turn failed: %s", self.ticker, self.phase, e)
                break
            self.messages.append({"role": "assistant", "content": resp.content})
            thinking = "".join(getattr(b, "thinking", "") for b in resp.content
                               if getattr(b, "type", None) == "thinking")
            said = "".join(getattr(b, "text", "") for b in resp.content
                           if getattr(b, "type", None) == "text")
            tool_uses = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
            turn_rec: dict = {"thinking": thinking, "said": said, "checks": []}
            if not tool_uses:
                self.messages.append({"role": "user", "content":
                                      f"Call {self._emit} now with your verdict."})
                round_trace.append(turn_rec)
                continue
            results: list[dict] = []
            verdict = None
            for tu in tool_uses:
                if tu.name == self._emit:
                    try:
                        verdict = self.schema.model_validate(dict(tu.input or {}))
                        results.append(_tr(tu.id, "Verdict recorded."))
                    except Exception as e:
                        results.append(_tr(tu.id, f"Invalid verdict: {e}. Correct and call "
                                                  f"{self._emit} again."))
                else:
                    reply = toolkit.execute(self.ctx, tu.name, dict(tu.input or {}))
                    results.append(_tr(tu.id, reply.content))
                    turn_rec["checks"].append({
                        "tool": tu.name, "input": dict(tu.input or {}),
                        "result": (reply.content or "")[:2000]})
            self.messages.append({"role": "user", "content": results})
            round_trace.append(turn_rec)
            if verdict is not None:
                self.last_trace = round_trace
                return verdict
        self.last_trace = round_trace
        log.warning("[%s] reviewer %s did not emit; using default", self.ticker, self.phase)
        if self._default_factory is not None:
            return self._default_factory()
        return self.schema()  # type: ignore[call-arg]
