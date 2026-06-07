"""ID and timestamp helpers (run_id, call_id, agent_id)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime


def new_run_id() -> str:
    """A human-sortable run id: UTC date-time + short random suffix."""
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    return f"run-{stamp}-{uuid.uuid4().hex[:6]}"


def new_call_id() -> str:
    return f"call-{uuid.uuid4().hex[:12]}"


def new_agent_id(role: str) -> str:
    return f"{role}-{uuid.uuid4().hex[:8]}"


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()
