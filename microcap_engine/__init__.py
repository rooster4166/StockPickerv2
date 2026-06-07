"""Micro-Cap Value Engine.

A run-once, buy-and-hold LLM research desk for under-covered $50-300M US stocks.
See README.md and the design spec for the strategy; this package implements both
the Phase-0 proven baseline and the Phase-1 heavy deep-dive engine, sharing one
ranking/sizing/execution layer.
"""

from .config import SETTINGS, Settings
from .pipeline import analyze_name, run_pipeline

__version__ = "0.1.0"

__all__ = ["SETTINGS", "Settings", "analyze_name", "run_pipeline", "__version__"]
