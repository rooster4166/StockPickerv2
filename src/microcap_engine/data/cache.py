"""Tiny disk cache for vendor responses.

Keyed by a stable hash of (endpoint, params). JSON on disk under data/cache/.
Lets a name be re-analyzed (or replayed in tests) without re-hitting the vendor.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from microcap_engine.config import CACHE_DIR


class DiskCache:
    def __init__(self, namespace: str, root: Path | None = None):
        self._dir = (root or CACHE_DIR) / namespace
        self._dir.mkdir(parents=True, exist_ok=True)

    def _key(self, endpoint: str, params: dict) -> str:
        blob = endpoint + "|" + json.dumps(params, sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()[:24]

    def get(self, endpoint: str, params: dict) -> Any | None:
        path = self._dir / f"{self._key(endpoint, params)}.json"
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def set(self, endpoint: str, params: dict, value: Any) -> None:
        path = self._dir / f"{self._key(endpoint, params)}.json"
        try:
            path.write_text(json.dumps(value, default=str), encoding="utf-8")
        except OSError:
            pass
