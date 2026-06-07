"""Adaptive, code-executed valuation (design spec B.3 phase 6).

The LLM reasons to the *assumptions* and picks the *method*; the arithmetic is
done here, deterministically, so a fair value is reproducible and auditable. The
method is chosen to fit the business:

  * ``dcf``   — multi-stage DCF for stable cash generators
  * ``rnpv``  — risk-adjusted NPV for binary-catalyst names
  * ``nav``   — net asset value / sum-of-the-parts for asset-heavy names
  * ``comps`` — peer multiples where comparables are clean

Each method returns an **equity value in $M**. A run supplies three assumption
sets (bear / base / bull) for the same method; we compute all three and report
low / median / high per share. Per-share uses shares outstanding from data —
never the price, preserving price-blinding.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

VALID_METHODS = ("dcf", "rnpv", "nav", "comps")


class ValuationError(ValueError):
    pass


# --------------------------------------------------------------------- methods
def dcf(a: dict) -> float:
    """Two-stage DCF. Returns equity value in $M."""
    fcf = float(a["fcf_base_m"])
    g1 = float(a["stage1_growth"])
    n1 = int(a["stage1_years"])
    gt = float(a["terminal_growth"])
    r = float(a["discount_rate"])
    if r <= gt:
        raise ValuationError("discount_rate must exceed terminal_growth")
    if n1 < 0:
        raise ValuationError("stage1_years must be >= 0")
    pv = 0.0
    cf = fcf
    for t in range(1, n1 + 1):
        cf *= 1 + g1
        pv += cf / (1 + r) ** t
    terminal_cf = cf * (1 + gt)
    terminal_value = terminal_cf / (r - gt)
    pv += terminal_value / (1 + r) ** n1
    enterprise_value = pv
    return enterprise_value - float(a.get("net_debt_m", 0.0))


def rnpv(a: dict) -> float:
    """Probability-weighted, discounted scenario payoffs. Returns equity $M."""
    scenarios = a["scenarios"]
    if not scenarios:
        raise ValuationError("rnpv requires at least one scenario")
    r = float(a["discount_rate"])
    total = 0.0
    for s in scenarios:
        p = float(s["probability"])
        payoff = float(s["payoff_equity_m"])
        years = float(s.get("years", 0))
        total += p * (payoff / (1 + r) ** years)
    return total


def nav(a: dict) -> float:
    """Sum-of-the-parts: assets minus liabilities. Returns equity $M."""
    assets = a.get("assets", [])
    asset_total = sum(float(x["value_m"]) for x in assets)
    return asset_total - float(a.get("liabilities_m", 0.0))


def comps(a: dict) -> float:
    """Peer-multiple valuation. Returns equity $M."""
    metric = float(a["metric_value_m"])
    multiple = float(a["peer_multiple"])
    value = metric * multiple
    if a.get("is_enterprise_multiple", False):
        value -= float(a.get("net_debt_m", 0.0))
    return value


_DISPATCH = {"dcf": dcf, "rnpv": rnpv, "nav": nav, "comps": comps}


def equity_value(method: str, assumptions: dict) -> float:
    if method not in _DISPATCH:
        raise ValuationError(f"unknown method {method!r}; expected one of {VALID_METHODS}")
    return _DISPATCH[method](assumptions)


# --------------------------------------------------------------------- result
@dataclass
class ValuationResult:
    method: str
    low: float  # per share
    median: float  # per share
    high: float  # per share
    equity_low_m: float
    equity_median_m: float
    equity_high_m: float
    shares_outstanding_m: float

    def to_dict(self) -> dict:
        return {
            "method": self.method,
            "fair_value_per_share": {"low": self.low, "median": self.median, "high": self.high},
            "equity_value_m": {
                "low": self.equity_low_m,
                "median": self.equity_median_m,
                "high": self.equity_high_m,
            },
            "shares_outstanding_m": self.shares_outstanding_m,
        }


def run_valuation(
    method: str,
    scenario_sets: dict,
    shares_outstanding_m: float,
) -> ValuationResult:
    """Compute low/median/high per-share fair value from bear/base/bull sets.

    ``scenario_sets`` is ``{"bear": {...}, "base": {...}, "bull": {...}}`` — each
    value being a full assumption dict for ``method``.
    """
    if shares_outstanding_m is None or shares_outstanding_m <= 0:
        raise ValuationError("shares_outstanding_m must be positive to derive per-share value")
    required = ("bear", "base", "bull")
    missing = [k for k in required if k not in scenario_sets]
    if missing:
        raise ValuationError(f"scenario_sets missing keys: {missing}")

    eq = {k: equity_value(method, scenario_sets[k]) for k in required}
    per_share = {k: eq[k] / shares_outstanding_m for k in required}
    ordered = sorted(per_share.values())
    ordered_eq = sorted(eq.values())
    return ValuationResult(
        method=method,
        low=ordered[0],
        median=ordered[1],
        high=ordered[2],
        equity_low_m=ordered_eq[0],
        equity_median_m=ordered_eq[1],
        equity_high_m=ordered_eq[2],
        shares_outstanding_m=shares_outstanding_m,
    )
