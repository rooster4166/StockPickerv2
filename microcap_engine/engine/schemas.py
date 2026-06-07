"""JSON schemas for the structured LLM calls.

Kept minimal and structured-outputs-safe: every object sets
``additionalProperties: false`` and avoids numeric/length constraints (not
supported by structured outputs). Heterogeneous, method-specific valuation
assumptions are handled with ``schema=None`` + lenient parsing instead.
"""

from __future__ import annotations

# --- cheap reject-gate (B.2) -------------------------------------------------
GATE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "verdict": {"type": "string", "enum": ["plausible", "obvious_no"]},
        "confidence": {"type": "number"},
        "reason": {"type": "string"},
    },
    "required": ["verdict", "confidence", "reason"],
}

# --- consolidation gate (B.3 phase 5) ---------------------------------------
# The PM fuses the four specialist briefs into one grounded assumption set and
# picks the valuation method. Valuation arithmetic happens later, in code.
CONSOLIDATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "recommended_method": {"type": "string", "enum": ["dcf", "rnpv", "nav", "comps"]},
        "method_rationale": {"type": "string"},
        "assumption_summary": {"type": "string"},
        "key_drivers": {"type": "array", "items": {"type": "string"}},
        "financial_quality": {"type": "string"},
        "catalyst": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "present": {"type": "boolean"},
                "description": {"type": "string"},
                "probability": {"type": "number"},
                "within_holding_year": {"type": "boolean"},
            },
            "required": ["present", "description", "probability", "within_holding_year"],
        },
    },
    "required": [
        "recommended_method",
        "method_rationale",
        "assumption_summary",
        "key_drivers",
        "financial_quality",
        "catalyst",
    ],
}

# --- red-team (B.3 phase 7) --------------------------------------------------
REDTEAM_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "disconfirming_findings": {"type": "array", "items": {"type": "string"}},
        "thesis_breakers": {"type": "array", "items": {"type": "string"}},
        # Multiplicative haircut applied to fair value, in [0, 1]. 1.0 = no change.
        "fair_value_adjustment": {"type": "number"},
        "verdict": {
            "type": "string",
            "enum": ["thesis_intact", "weakened", "broken"],
        },
        "summary": {"type": "string"},
    },
    "required": [
        "disconfirming_findings",
        "thesis_breakers",
        "fair_value_adjustment",
        "verdict",
        "summary",
    ],
}

# --- Phase-0 baseline single prompt (Part D, Phase 0) -----------------------
BASELINE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "would_buy": {"type": "boolean"},
        "fair_value_per_share": {"type": "number"},
        "confidence": {"type": "number"},
        "thesis": {"type": "string"},
    },
    "required": ["would_buy", "fair_value_per_share", "confidence", "thesis"],
}
