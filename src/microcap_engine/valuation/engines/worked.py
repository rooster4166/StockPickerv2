"""Worked valuation — any framework the PM judges correct, evaluated in code.

The PM supplies ``key_inputs`` (named numbers) and a ``formula`` over them; this
engine evaluates the formula with the safe arithmetic evaluator. This is the
generalization escape hatch: it values un-enumerated business types (REIT cap-rate
NAV, miner reserve NPV, AUM x fee, embedded value, ...) without forcing a method,
while keeping the arithmetic deterministic and out of the LLM.
"""

from __future__ import annotations

from microcap_engine.schemas.assumptions import ValuationMethod, WorkedValuationAssumptions
from microcap_engine.schemas.valuation import ValuationResult
from microcap_engine.valuation.safe_eval import safe_eval


def compute(a: WorkedValuationAssumptions) -> ValuationResult:
    per_share = safe_eval(a.formula, a.key_inputs)
    return ValuationResult(
        method=ValuationMethod.WORKED,
        fair_value_per_share=round(per_share, 4),
        fair_value_median=round(per_share, 4),
        intermediate={
            "framework": a.framework,
            "formula": a.formula,
            "key_inputs": a.key_inputs,
        },
        notes=f"Worked valuation — {a.framework}.",
    )
