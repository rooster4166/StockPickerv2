"""Risk-adjusted NPV for catalyst / milestone names.

Real rNPV: the model supplies each scenario's probability, the value if it realizes,
and WHEN (years_to_realization); the code does the time value. Expected present value
= Σ p_i × value_i / (1+r)^years_i, with r the SYSTEMATIC-risk discount rate (the
idiosyncratic/technical risk is already in the probabilities — not double-counted).
The distribution endpoints are the present-valued min/max scenarios.
"""

from __future__ import annotations

from microcap_engine.schemas.assumptions import RNPVAssumptions, ValuationMethod
from microcap_engine.schemas.valuation import ValuationResult


def compute(a: RNPVAssumptions) -> ValuationResult:
    r = a.discount_rate
    rows = []
    for s in a.scenarios:
        pv = s.value_per_share / ((1.0 + r) ** s.years_to_realization) if r or \
            s.years_to_realization else s.value_per_share
        rows.append({"name": s.name, "probability": s.probability,
                     "value_if_realized": s.value_per_share,
                     "years": s.years_to_realization, "present_value_per_share": round(pv, 4)})
    expected = sum(row["probability"] * row["present_value_per_share"] for row in rows)
    pvs = sorted(row["present_value_per_share"] for row in rows)
    return ValuationResult(
        method=ValuationMethod.RNPV,
        fair_value_per_share=round(expected, 4),
        fair_value_median=round(expected, 4),
        fair_value_p10=round(pvs[0], 4),
        fair_value_p90=round(pvs[-1], 4),
        intermediate={"discount_rate": r, "scenarios": rows},
        notes=f"rNPV over {len(a.scenarios)} scenarios, discounted at {r:.1%} "
              f"to present value.",
    )
