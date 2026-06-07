"""Append-only JSONL audit log — one record per LLM call.

Every call through ``LLMClient`` produces exactly one record here, keyed by
run_id and ticker. This is the spec's "catalogue every LLM call for
audit/debugging" requirement, and it's the single source of truth for cost.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

from microcap_engine.config import AUDIT_DIR

# USD per 1M tokens, (input, output). Cache reads ~0.1x input; cache writes ~1.25x.
_PRICING: dict[str, tuple[float, float]] = {
    "claude-opus-4-8": (5.0, 25.0),
    "claude-opus-4-7": (5.0, 25.0),
    "claude-opus-4-6": (5.0, 25.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
}


def estimate_cost_usd(model: str, usage: dict) -> float:
    """Estimate the USD cost of one call from its token usage."""
    in_price, out_price = _PRICING.get(model, (5.0, 25.0))
    fresh_in = usage.get("input_tokens", 0)
    out = usage.get("output_tokens", 0)
    cache_write = usage.get("cache_creation_input_tokens", 0)
    cache_read = usage.get("cache_read_input_tokens", 0)
    cost = (
        fresh_in * in_price
        + cache_write * in_price * 1.25
        + cache_read * in_price * 0.10
        + out * out_price
    ) / 1_000_000
    return round(cost, 6)


class AuditLogger:
    """Thread-safe JSONL writer, one file per (run_id, ticker)."""

    def __init__(self, run_id: str):
        self.run_id = run_id
        self._dir = AUDIT_DIR / run_id
        self._dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def path_for(self, ticker: str) -> Path:
        safe = "".join(c for c in ticker if c.isalnum() or c in "-_") or "UNKNOWN"
        return self._dir / f"{safe}.jsonl"

    def record(self, ticker: str, record: dict) -> None:
        line = json.dumps(record, default=str, ensure_ascii=False)
        path = self.path_for(ticker)
        with self._lock:
            with path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")

    def total_cost(self, ticker: str) -> float:
        """Sum estimated cost across all recorded calls for a ticker."""
        return self.summary(ticker)["cost_usd"]

    def summary(self, ticker: str) -> dict:
        """Aggregate cost + token usage across all calls for a ticker."""
        path = self.path_for(ticker)
        agg = {
            "ticker": ticker,
            "n_calls": 0,
            "cost_usd": 0.0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 0,
            "latency_s": 0.0,
            "by_label": {},
        }
        if not path.exists():
            return agg
        with path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                agg["n_calls"] += 1
                agg["cost_usd"] += rec.get("cost_usd", 0.0)
                agg["latency_s"] += rec.get("latency_s", 0.0) or 0.0
                u = rec.get("usage", {}) or {}
                for k in ("input_tokens", "output_tokens",
                          "cache_read_input_tokens", "cache_creation_input_tokens"):
                    agg[k] += u.get(k, 0) or 0
                label = rec.get("label", "?")
                agg["by_label"][label] = round(
                    agg["by_label"].get(label, 0.0) + rec.get("cost_usd", 0.0), 6
                )
        agg["cost_usd"] = round(agg["cost_usd"], 6)
        agg["total_tokens"] = (
            agg["input_tokens"] + agg["output_tokens"]
            + agg["cache_read_input_tokens"] + agg["cache_creation_input_tokens"]
        )
        return agg
