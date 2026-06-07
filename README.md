# Micro-Cap Value Engine

A run-once, buy-and-hold LLM research desk for under-covered US stocks in the
**$50M–$300M** market-cap band. It reads and values every name in the universe,
buys a ranked basket of the ones it judges materially undervalued, and holds for
a year. See `Docs/Microcap value engine project plan and spec.txt` for the full
strategy and design spec.

## Status

**Phase 1 — the heavy engine.** A persistent orchestrator (PM) delegates a
strict, dependency-ordered deep dive to specialist subagents, fuses their cited
briefs through a **code-enforced consolidation gate** into a single assumption
set, runs a **price-blinded** code-executed valuation, and red-teams the result
with a decorrelated model. Ensembling produces a confidence signal that sizes
positions; cross-sectional ranking cancels uniform model bias.

The first slice runs a single name (ATXI) end-to-end. See `STATUS.md` for the
live build log and `DECISIONS.md` for autonomous-mode decisions.

## Architecture (non-negotiable properties)

| Property | Where it lives |
|---|---|
| Code-enforced consolidation gate | `schemas/assumptions.py` (`AssumptionSet`) — valuation can't run without it |
| Price-blinded valuation | `orchestrator/` never receives a `Quote`; only `portfolio/book.py` does |
| Judgment in LLM, math in code | LLM emits `AssumptionSet`; `valuation/engines/*.py` execute arithmetic |
| Context isolation | each phase has its own agent; only distilled cited briefs pass between them |
| Every LLM call audited | single chokepoint `llm/client.py` → JSONL in `data/audit/` |

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -e ".[data,dev]"
copy .env.example .env          # then fill in ANTHROPIC_API_KEY + FMP_API_KEY
```

## Usage

```bash
microcap one ATXI               # full cascade for one name; prints a NameResult
microcap universe               # screen the $50-300M US universe, cache it
microcap run --capital 100000   # full universe -> ranked, sized book
microcap audit RUN_ID ATXI      # pretty-print the per-name audit log
```

## Tests

```bash
pytest                          # unit + integration (live tests skipped)
pytest -m live                  # opt-in; hits real Anthropic / FMP / EDGAR
```
