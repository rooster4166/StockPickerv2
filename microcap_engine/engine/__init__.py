"""The deep-dive engine: gate, phases, valuation, red-team, orchestrator, ensemble."""

from .ensemble import ensemble_deepdive
from .gate import cheap_gate, should_drop
from .orchestrator import Orchestrator, OrchestratorConfig
from .valuation import ValuationError, ValuationResult, equity_value, run_valuation

__all__ = [
    "cheap_gate",
    "should_drop",
    "ensemble_deepdive",
    "Orchestrator",
    "OrchestratorConfig",
    "run_valuation",
    "equity_value",
    "ValuationResult",
    "ValuationError",
]
