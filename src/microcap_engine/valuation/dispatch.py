"""Valuation dispatcher — the code-enforced gate's terminal point.

``run_valuation`` accepts ONLY a validated ``AssumptionSet`` and routes to the
matching engine. There is no path to a ``ValuationResult`` that does not pass
through an ``AssumptionSet`` first — that is the consolidation gate, enforced by
the type system. This function never sees a market price (price-blinding).
"""

from __future__ import annotations

from microcap_engine.schemas.assumptions import AssumptionSet, ValuationMethod
from microcap_engine.schemas.valuation import ValuationResult
from microcap_engine.valuation.engines import (
    composite,
    comps,
    dcf,
    excess_returns,
    nav,
    rnpv,
    worked,
)

_ENGINES = {
    ValuationMethod.DCF: dcf.compute,
    ValuationMethod.COMPS: comps.compute,
    ValuationMethod.RNPV: rnpv.compute,
    ValuationMethod.NAV: nav.compute,
    ValuationMethod.EXCESS_RETURNS: excess_returns.compute,
    ValuationMethod.WORKED: worked.compute,
    ValuationMethod.COMPOSITE: composite.compute,
}


def run_valuation(assumption_set: AssumptionSet) -> ValuationResult:
    if not isinstance(assumption_set, AssumptionSet):
        raise TypeError(
            "run_valuation requires a validated AssumptionSet (consolidation gate)."
        )
    engine = _ENGINES[assumption_set.method]
    return engine(assumption_set.active_block())
