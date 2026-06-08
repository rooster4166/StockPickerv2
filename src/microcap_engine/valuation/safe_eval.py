"""Safe arithmetic evaluator for PM-supplied valuation formulas.

The agentic PM expresses *any* valuation framework as ``key_inputs`` (named
numbers) + a ``formula`` string over those names. Code — not the LLM — evaluates
it, preserving "judgment in LLM, math in code" for arbitrary, un-enumerated
methodologies (insurer excess-returns, REIT cap-rate NAV, miner reserve NPV, …).

Only a tiny arithmetic grammar is allowed: numbers, the named inputs, + - * / **,
parentheses, unary minus, and a set of whitelisted pure functions (min/max/abs plus
exp/ln/log/log10/sqrt/norm_cdf — enough to express present-value and Black-Scholes /
real-option payoffs). No attribute access, calls to arbitrary names, comprehensions,
or builtins.
"""

from __future__ import annotations

import ast
import math
import operator

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _norm_cdf(x: float) -> float:
    """Standard-normal CDF — enables Black-Scholes / real-option payoffs in `worked`."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _ln(x: float) -> float:
    if x <= 0:
        raise FormulaError("log of a non-positive number")
    return math.log(x)


def _sqrt(x: float) -> float:
    if x < 0:
        raise FormulaError("sqrt of a negative number")
    return math.sqrt(x)


def _exp(x: float) -> float:
    if x > 700:  # exp(709) overflows float; guard before it raises
        raise FormulaError("exp argument too large (overflow guard)")
    return math.exp(x)


# Whitelisted pure functions. min/max/abs plus the math needed for option/PV formulas.
_FUNCS = {
    "min": min, "max": max, "abs": abs,
    "exp": _exp, "ln": _ln, "log": _ln, "log10": math.log10, "sqrt": _sqrt,
    "norm_cdf": _norm_cdf, "normcdf": _norm_cdf,
}


class FormulaError(ValueError):
    pass


def safe_eval(formula: str, variables: dict[str, float]) -> float:
    """Evaluate ``formula`` over ``variables``; raise FormulaError on anything unsafe."""
    if not formula or not formula.strip():
        raise FormulaError("empty formula")
    try:
        tree = ast.parse(formula, mode="eval")
    except SyntaxError as e:
        raise FormulaError(f"syntax error: {e}") from e
    try:
        result = _eval(tree.body, variables)
    except (OverflowError, ZeroDivisionError, ValueError) as e:
        if isinstance(e, FormulaError):
            raise
        raise FormulaError(f"arithmetic error: {e}") from e
    if not math.isfinite(result):
        raise FormulaError("formula produced a non-finite (inf/nan) result")
    return result


def _eval(node: ast.AST, v: dict[str, float]) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise FormulaError(f"non-numeric constant: {node.value!r}")
        return float(node.value)
    if isinstance(node, ast.Name):
        if node.id not in v:
            raise FormulaError(f"unknown input '{node.id}'")
        return float(v[node.id])
    if isinstance(node, ast.BinOp):
        op = _BIN_OPS.get(type(node.op))
        if op is None:
            raise FormulaError(f"operator not allowed: {type(node.op).__name__}")
        right = _eval(node.right, v)
        left = _eval(node.left, v)
        if op in (operator.truediv, operator.mod) and right == 0:
            raise FormulaError("division by zero")
        # Block only genuine overflow, not legitimate long-horizon discounting: (1+r)**N with
        # N up to ~1000 periods (e.g. monthly over decades) is finite and valid. The isfinite
        # post-check below catches anything that actually overflows.
        if op is operator.pow and (abs(right) > 1000 or abs(left) > 1e9):
            raise FormulaError("exponent/base out of bounds (overflow guard)")
        result = op(left, right)
        if isinstance(result, float) and not math.isfinite(result):
            raise FormulaError("non-finite intermediate result")
        return result
    if isinstance(node, ast.UnaryOp):
        op = _UNARY_OPS.get(type(node.op))
        if op is None:
            raise FormulaError(f"unary operator not allowed: {type(node.op).__name__}")
        return op(_eval(node.operand, v))
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCS:
            raise FormulaError("only min/max/abs calls are allowed")
        if node.keywords:
            raise FormulaError("keyword args not allowed")
        result = float(_FUNCS[node.func.id](*[_eval(a, v) for a in node.args]))
        if not math.isfinite(result):
            raise FormulaError(f"{node.func.id}() produced a non-finite result")
        return result
    raise FormulaError(f"expression element not allowed: {type(node).__name__}")
