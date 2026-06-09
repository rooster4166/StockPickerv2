# CLAUDE.md — Micro-Cap Value Engine

LLM equity-research desk that values every US stock in the $50–300M cap band and buys a
ranked, sized basket. See `Docs/` for the strategy spec, `STATUS.md` for build state, and
`DECISIONS.md` for autonomous-mode decisions.

## Run it

```bash
.venv\Scripts\activate                       # venv has anthropic>=0.107 (needs messages.parse)
microcap one AXTI                            # full cascade for one name (AXTI = golden test name)
microcap one ROOT                            # an insurer (tests composite/NAV valuation)
microcap universe                            # screen the $50-300M US universe
microcap run --capital 100000 --tier         # full universe -> ranked book (tiered, recall-safe)
microcap audit <RUN_ID> AXTI                 # per-call cost/token/latency breakdown
python scripts/inspect_result.py data/audit/<RUN_ID>/AXTI.result.json   # per-phase output
pytest                                       # 28 unit+integration tests (live tests opt-in: -m live)
```

Secrets in `.env` (gitignored): `ANTHROPIC_API_KEY`, `FMP_API_KEY`, `SEC_USER_AGENT`.

## Architecture (agentic — default, `engine_mode="agentic"`)

`runner/pipeline.py:agentic_analyze` → (universe: cheap recall-safe pre-gate) →
`orchestrator/agentic.py:AgenticOrchestrator.analyze()` — a tool-using PM loop, NOT a fixed
pipeline. The PM investigates dynamically, in any order, as many steps as it needs, then calls a
terminal tool. Price is joined only later, in `portfolio/book.py`.

- **The PM** (Opus, charter in `orchestrator/charter.py`) drives its own investigation. The edge
  is the **tools + the prompt** (process discipline), not hard-coded valuation logic.
- **Tools** (`orchestrator/tools.py`): data (`get_financials/ratios/peers/segments/
  read_filing_section/news/transcripts`), `research` (web-search subagent — `orchestrator/
  research.py`), a **persistent analyst team** (`spawn_analyst` stands up a tool-capable,
  citation-grounded analyst — `orchestrator/analyst.py` — that pulls filings/transcripts itself
  and consolidates; `ask_analyst` follows up with the same analyst, retaining context — the
  PM↔desk back-and-forth), `compute_valuation` (the gate — callable repeatedly), and two terminal
  tools.
- **Diagnose-then-lens valuation**: the charter has the PM first DIAGNOSE the dominant value
  driver (proven compounder / financial-spread / science-contingent / asset-NAV / cyclical /
  special-situation), then acquire only the lens that company needs — so Nike never gets biotech
  rNPV machinery and a pre-revenue drug never gets a P/E. For science-contingent names it values
  the SCIENCE (base-rate-anchored milestone PoS → probability-weighted PV), the edge vs human
  finance. Engines: dcf, comps (any multiple), nav, rnpv (now DISCOUNTS in code: prob × value ×
  timing), `excess_returns` (financials), `worked` (any framework via `key_inputs`+formula →
  `valuation/safe_eval.py`, which now has exp/ln/sqrt/norm_cdf for real-option/SOTP payoffs),
  composite. Never forces a method. Discount rates must be built up (rf+ERP+beta+micro-cap size
  premium) and not double-count risk; both gates stress-test the rate and probabilities vs
  external base rates.
- **Code-assembled report**: `submit_final(executive_summary, valuation_writeup, conclusion,
  dossier)` — the comprehensive report is ASSEMBLED IN CODE (`agentic._assemble_report`) from the
  analyst-authored `as_section` sections (verbatim, full depth) + those PM-written fields. The PM
  never re-types section prose (that re-drafting was 37% of cost). This also structurally
  guarantees no compression. Submit triggers a code-run red-team GATE; unresolved valuation-
  changing concerns force the PM back to fix/rebut (or `max_red_rounds`). `reject_early` drops.
- **Decisive + bounded**: diagnose → one lens → commission sections → value → reconcile → submit,
  in ~12-18 steps (`agentic_max_steps=22`, `agentic_max_cost_usd=16`, per-step `max_tokens=10000`).

The older **phased** cascade (`Orchestrator`, fixed 0–7 phases + ensemble) remains under
`engine_mode="phased"` for A/B.

## Non-negotiable invariants (don't break these)

1. **Code-enforced consolidation gate** — `schemas/assumptions.py:AssumptionSet` is the only
   path to a valuation; `valuation/dispatch.py:run_valuation` accepts nothing else.
2. **Price-blinding** — nothing under `orchestrator/`, `gate/`, `ensemble/` may import `Quote`
   or see the market price. `NameData` has no price field. Enforced by
   `tests/unit/test_price_blinding.py`. The price is joined ONLY in `portfolio/book.py`.
3. **Judgment in LLM, math in code** — the LLM emits assumptions; `valuation/engines/*.py`
   compute fair value deterministically. Never let the model return a fair-value number.
4. **Every LLM call audited** — all calls go through `llm/client.py` (the only `import
   anthropic`), which writes a JSONL record with full thinking/tool traces, tokens, and cost.

## Conventions

- **Models**: Opus 4.8 = reasoning + red-team; Sonnet 4.6 = extraction/triage. Thinking OFF on
  extraction, ON (`display=summarized`, so traces are captured) on reasoning. Set in `config.py`.
- **Structured output**: `llm/client.py:parse` tries strict `output_format`; on a
  "grammar too large" 400 it falls back to non-strict tool-use (`tool_choice:auto` + thinking),
  validated with Pydantic + repair-on-error. Retries escalate `max_tokens` on truncation.
- **Valuation methods**: dcf, comps, rnpv, nav, **composite** (event-branched: each scenario
  picks its own sub-method, probability-weighted). All in `valuation/engines/`.
- **Recall-safe gate**: `gate/cheap_gate.py:should_drop` only drops a high-confidence
  `obvious_no` that ALSO has no balance-sheet floor (net cash / positive equity override the
  LLM). False positives are cheap; false negatives are unrecoverable.
- **Cost-tiered universe**: n=1 deep dive on every survivor; ensemble top-up only on the
  undervalued pool (after the price-join). Never tier by dropping names.
- Add a unit test with hand-verified golden numbers for any new valuation engine.
