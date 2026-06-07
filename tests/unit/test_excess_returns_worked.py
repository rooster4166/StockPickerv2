"""Excess-returns + worked (formula) valuation, and the safe evaluator."""

from __future__ import annotations

import math

import pytest

from microcap_engine.schemas.assumptions import (
    AssumptionSet,
    ExcessReturnsAssumptions,
    ValuationMethod,
    WorkedValuationAssumptions,
)
from microcap_engine.schemas.briefs import Citation
from microcap_engine.valuation.dispatch import run_valuation
from microcap_engine.valuation.safe_eval import FormulaError, safe_eval


def _cit():
    return [Citation(source_kind="filing", quote="10-K")]


def test_excess_returns_warranted_multiple():
    a = ExcessReturnsAssumptions(
        book_value=400.0, shares_outstanding=20.0,
        sustainable_return=0.15, cost_of_equity=0.10, growth=0.04,
    )
    # warranted P/B = (0.15-0.04)/(0.10-0.04) = 0.11/0.06 = 1.8333; equity = 400*1.8333=733.3; /20=36.67
    res = run_valuation(AssumptionSet(method=ValuationMethod.EXCESS_RETURNS,
                                      rationale="bank", citations=_cit(), excess_returns=a))
    assert math.isclose(res.intermediate["warranted_price_to_book"], 1.8333, abs_tol=1e-3)
    assert math.isclose(res.fair_value_per_share, 36.6667, abs_tol=1e-2)


def test_excess_returns_requires_coe_gt_growth():
    with pytest.raises(Exception):
        ExcessReturnsAssumptions(book_value=100, shares_outstanding=10,
                                 sustainable_return=0.12, cost_of_equity=0.05, growth=0.08)


def test_worked_formula_evaluated_in_code():
    a = WorkedValuationAssumptions(
        framework="P/TBV x ROTE",
        key_inputs={"tbv_per_share": 25.0, "warranted_pb": 1.4},
        formula="tbv_per_share * warranted_pb",
    )
    res = run_valuation(AssumptionSet(method=ValuationMethod.WORKED,
                                      rationale="insurer", citations=_cit(), worked=a))
    assert math.isclose(res.fair_value_per_share, 35.0)
    assert res.intermediate["framework"] == "P/TBV x ROTE"


def test_worked_rejects_invalid_formula_at_validation():
    # references an undefined input -> schema validation fails
    with pytest.raises(Exception):
        WorkedValuationAssumptions(framework="x", key_inputs={"a": 1.0}, formula="a * b")


def test_safe_eval_blocks_dangerous_input():
    assert safe_eval("a + b * 2", {"a": 3, "b": 4}) == 11
    assert safe_eval("max(a, b)", {"a": 3, "b": 4}) == 4
    for bad in ["__import__('os')", "a.__class__", "open('x')", "a if b else 0"]:
        with pytest.raises(FormulaError):
            safe_eval(bad, {"a": 1, "b": 2})
