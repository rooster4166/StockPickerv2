# Micro-Cap Value Engine

A run-once, buy-and-hold **LLM research desk** for under-covered **$50–300M** US
stocks. The thesis (see the design spec): an LLM can read and integrate the full
public record on a neglected company better than the handful of humans covering
it, and no research firm does this work because the names are too small to move a
fund. This repo deploys an investment-firm-grade research desk against the
companies that have none.

It implements **both** halves of the plan, sharing one ranking/sizing/execution
layer:

- **Phase 0 — the proven baseline.** One "would Buffett buy this, ignoring that
  it's too small to bother with?" prompt per name. Cheap, forward-validated, and
  the bar the heavy engine must beat.
- **Phase 1 — the heavy engine.** A persistent orchestrator (PM) delegates
  price-blinded deep dives to context-isolated specialist subagents, fuses their
  cited briefs at a code-enforced consolidation gate, runs an adaptive,
  code-executed valuation, and hands the thesis to a decorrelated red-team — then
  ensembles for a confidence signal that feeds sizing.

> **This is a real strategy, not advice.** It carries real loss potential plus
> data-licensing, brokerage, tax, and securities-compliance obligations.
> Validate (A/B, paper, small real-money bridge) and seek professional/legal
> review before committing material capital. See *Risks* in the design spec.

---

## How the code maps to the design spec

| Spec section | Module |
| --- | --- |
| B.2 Conservative cheap reject-gate | `engine/gate.py` (`cheap_gate`, `should_drop`) |
| B.3 Specialist phases (financials → business → industry → news) | `engine/phases.py` |
| B.3 Persistent / fresh agents, context isolation | `llm/agent.py` (`Agent`) |
| B.3 Orchestrator + **code-enforced** consolidation gate | `engine/orchestrator.py` |
| B.3 Adaptive, **code-executed** valuation (DCF/rNPV/NAV/comps) | `engine/valuation.py` |
| B.3 Decorrelated red-team | `engine/redteam.py` |
| B.4 Ensemble for confidence (sizes, never filters) | `engine/ensemble.py` |
| B.5 Cross-sectional ranking & liquidity-capped sizing | `portfolio/ranking.py`, `portfolio/sizing.py` |
| B.6 One-time patient accumulation + C.3 slippage log | `portfolio/execution.py` |
| B.8 Per-name cascade `analyze_name` / `build_portfolio` | `pipeline.py`, `portfolio/build.py` |
| Phase 0 baseline sweep | `baseline/sweep.py` |
| Universe ($50–300M), data, filings | `data/` (yfinance + SEC EDGAR) |

**Price-blinding** (B.3) is enforced structurally: every deep-dive prompt is
built from `CompanyData.blinded_payload()`, which strips the market quote and
market cap. The price is only re-introduced in `portfolio/ranking.py` to compute
the margin of safety, *after* fair value is final.

**Judgment-in-LLM / math-in-code**: the model reasons to the valuation method and
assumptions; `engine/valuation.py` does the arithmetic deterministically, so
every fair value is reproducible and auditable.

---

## Install

```bash
pip install -r requirements.txt        # or: pip install -e .
cp .env.example .env                    # then fill in ANTHROPIC_API_KEY + SEC_USER_AGENT
```

The Anthropic SDK reads `ANTHROPIC_API_KEY` (and optional `ANTHROPIC_BASE_URL`)
from the environment. SEC EDGAR requires a descriptive `SEC_USER_AGENT` with a
contact address on every request.

## Run

```bash
# Screen a candidate list down to the $50-300M band (free data is slow; pass a list)
microcap universe --tickers ATXI,ZUMZ,BBW,ICCC,ATEX -v

# Phase-0 proven baseline sweep, $100k book
microcap baseline --tickers ATXI,ZUMZ,BBW,ICCC --capital 100000 -v

# Phase-1 heavy deep-dive engine
microcap analyze --tickers ATXI,ZUMZ,BBW,ICCC --capital 100000 -v

# Diagnostic: just the cheap reject-gate
microcap gate --tickers ATXI,ZUMZ -v
```

Outputs are written as timestamped JSON under `output/` (the book, per-name
results with cited briefs, gate verdicts, and valuation detail). Realized fills
logged via `portfolio.execution.log_fill` accumulate in `output/slippage_log.csv`
— the C.3 real-money bridge.

> Screening the *entire* SEC universe (`microcap universe --full`) is thousands of
> slow network calls; prefer a candidate list or `--full --limit N`.

## Configuration

All knobs live in `microcap_engine/config.py` and can be overridden with `MCE_*`
environment variables — universe bounds (`MCE_MCAP_MIN/MAX`), margin of safety
(`MCE_MARGIN_OF_SAFETY`, default 0.30), ensemble width (`MCE_ENSEMBLE_N`),
liquidity cap (`MCE_ADV_FRACTION`), and model choices (`MCE_DEEP_MODEL` default
`claude-opus-4-8`, `MCE_REDTEAM_MODEL` default `claude-sonnet-4-6` for
decorrelation).

---

## Validation hooks (Part C)

The central question is not "does the edge exist" (forward-validated) but "does
the heavy pipeline beat the cheap baseline, and can we capture it with real
money?" The code is built to run that comparison:

- **C.1 A/B** — `run_pipeline(..., mode="baseline")` vs `mode="heavy")` on the
  same fresh cohort; compare the resulting books.
- **C.2 Self-backtest** — point either mode at last year's universe and check it
  still surfaces the winners and now avoids the losers.
- **C.3 Real-money bridge** — `portfolio.execution.accumulation_plan` +
  `log_fill` measure realized slippage vs paper marks.

## Architecture (per name)

```
ticker
  └─ data provider: price-blindable CompanyData (yfinance + SEC EDGAR)
       └─ cheap reject-gate ── obvious_no @ high conf ──▶ drop (no deep work)
            └─ ensemble (N decorrelated runs):
                 Orchestrator:
                   financials → business → industry → news   (cited briefs)
                   → CONSOLIDATION GATE (code-enforced) → assumption set + method
                   → valuation (LLM assumptions, CODE arithmetic, price-blinded)
                   → red-team (decorrelated model)
                 → blend fair value + dispersion-based confidence
  → cross-sectional rank by margin of safety × confidence
  → size by rank × confidence, liquidity-capped, long-only, many names
  → one-time patient accumulation, hold one year
```

## Development

```bash
python -m pytest        # offline suite: fakes for LLM + data, no network/keys
```

The whole pipeline runs deterministically offline via the fakes in
`tests/conftest.py`, which is also the pattern for wiring a different data feed or
model: anything implementing the `complete`/`complete_json` interface (LLM) or
the `DataProvider` protocol drops straight in.
