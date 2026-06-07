"""Composite valuation — probability-weighted mix of methods across scenarios.

This is the "DCF depending on the events that occur" model: each event branch
picks the sub-method that fits *if that branch happens* (turnaround succeeds ->
DCF; stalls -> NAV floor; etc.), the code computes each branch with the matching
engine, and weights them by probability. All arithmetic stays in code; only the
judgment (which scenarios, which probabilities, which method per branch) is the
LLM's.
"""

from __future__ import annotations

from microcap_engine.schemas.assumptions import CompositeAssumptions, ValuationMethod
from microcap_engine.schemas.valuation import ValuationResult


def _branch_value(scenario) -> float:
    if scenario.sub_method == "direct":
        return float(scenario.value_per_share)
    # Lazy import to avoid any import cycle through the dispatcher.
    from microcap_engine.valuation.engines import comps, dcf, excess_returns, nav, worked

    engine = {
        "dcf": dcf.compute,
        "comps": comps.compute,
        "nav": nav.compute,
        "excess_returns": excess_returns.compute,
        "worked": worked.compute,
    }[scenario.sub_method]
    block = getattr(scenario, scenario.sub_method)
    return engine(block).fair_value_per_share


def compute(a: CompositeAssumptions) -> ValuationResult:
    branches = []
    expected = 0.0
    for s in a.scenarios:
        v = _branch_value(s)
        expected += s.probability * v
        branches.append(
            {
                "name": s.name,
                "probability": s.probability,
                "sub_method": s.sub_method,
                "value_per_share": round(v, 4),
                "rationale": s.rationale,
            }
        )
    values = sorted(b["value_per_share"] for b in branches)
    return ValuationResult(
        method=ValuationMethod.COMPOSITE,
        fair_value_per_share=round(expected, 4),
        fair_value_median=round(expected, 4),
        fair_value_p10=round(values[0], 4),
        fair_value_p90=round(values[-1], 4),
        intermediate={"branches": branches},
        notes=(
            f"Composite of {len(branches)} event branches "
            f"({', '.join(sorted({b['sub_method'] for b in branches}))}), "
            "probability-weighted."
        ),
    )
