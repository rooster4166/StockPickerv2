"""Shared test fixtures: a captured AXTI NameData and an offline LLM stub."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from microcap_engine.schemas.name_result import NameData

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def axti_name_data() -> NameData:
    raw = json.loads((FIXTURES / "axti" / "name_data.json").read_text(encoding="utf-8"))
    return NameData.model_validate(raw)
