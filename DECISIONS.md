# Autonomous-Mode Decision Log

Decisions made while the user was away. Each is my best call for the product;
flag any you'd reverse.

### D1 — StockPickerv2 made its own git repo
**Found:** `C:\Users\karaw` (your home directory) is itself a git repo — there's a
stray `.git` there, so the whole home folder is tracked. StockPickerv2 was just an
untracked subfolder of it.
**Decided:** ran `git init -b main` *inside* `StockPickerv2` so it's a standalone
repo with the `rooster4166/StockPickerv2` remote. A nested repo takes precedence
when working inside it. I did **not** touch the home-dir `.git` (not mine to clean
up, and it tracks your whole home directory).
**You may want to:** investigate/remove the home-dir `.git` separately — it's
almost certainly an accident and could leak personal files if ever pushed.

### D2 — API key rotation recommended
Moved the Anthropic key from `Docs/API key.txt` to `.env` (gitignored) and deleted
the plaintext file. **The key sat in cleartext on disk and passed through my
context**, so rotate it at console.anthropic.com when convenient and update `.env`.

### D3 — LIVE FMP (key provided) + EDGAR; fixtures for tests
You provided an FMP **premium** account (key in `.env`) — all endpoints available,
**3000 calls/min** — and added the API docs to `Docs/`. The data layer is built
against the live FMP `/stable/` API (base `https://financialmodelingprep.com/stable/`)
and validated with real probes. A full universe run (~1,500 names × ~7 endpoints
≈ 10.5k calls) runs in well under 5 min at 3000/min; a light token-bucket limiter
guards against bursts but the cap is no longer a constraint. I still capture live
responses for ATXI into `tests/fixtures/atxi/` so the e2e/integration tests are
deterministic and don't burn calls or require the network in CI.

### D4 — Model picks
Main pipeline: `claude-opus-4-8`. Red-team + cheap-gate: `claude-sonnet-4-6` (a
different model family member = genuine decorrelation for the red-team). Configurable
in `config.py`. For the first slice, ensemble runs decorrelate by temperature +
prompt variant; full multi-model ensemble is a one-line config bump after.

### D5 — Structured output via Anthropic tool-use
Every brief / assumption-set / verdict is forced through a single tool whose input
schema is the Pydantic model's JSON Schema, with `tool_choice` pinned to it. This
guarantees parseable, validated output and is the mechanism behind the
code-enforced consolidation gate.

### D5b — No temperature; structured output via messages.parse() (per claude-api skill)
The claude-api reference confirms `temperature`/`top_p`/`top_k` are **removed on
Opus 4.8 and return a 400**. So ensemble decorrelation uses **model + prompt-variant
+ effort level**, never temperature (revises the plan's "temperature variation").
Structured output uses `client.messages.parse(output_format=PydanticModel)` — the
SDK strips unsupported JSON-Schema constraints (ge/le/min_length) and validates
client-side, then Pydantic re-validates on our side. Analytical phases use
`thinking={"type":"adaptive"}`. Large filing text goes in the system prompt with
`cache_control` ephemeral so re-queries of the same agent hit cache. The audit log
records input/output/cache-creation/cache-read tokens, `_request_id`, latency, and
an estimated USD cost from a per-model pricing table.

### D7 — Golden test name is AXTI (not ATXI), and FMP data-quality caveat
The POC's 28x winner is **AXTI** (AXT, Inc. — compound semiconductor substrates,
gallium-arsenide/indium-phosphide; the spec's "oil-feedstock adjacent-exposure"
example maps to its raw-material supply chain). "ATXI" in the early plan was a
typo. AXTI is the canonical end-to-end test/fixture name. It is the C.2
self-backtest name (must resurface last year's winner) — not necessarily an
in-universe name today.
**FMP data-quality caveat:** AXTI's `/profile` returned price $89 / mktcap $4.1B,
which looks wrong for this ticker (historically low-priced). FMP fields can be
unreliable for individual names, so: (a) the engine cross-checks marketCap from
`/profile` vs `/key-metrics` vs `/quote` where it matters, (b) the universe screen
uses `/company-screener` server-side filters but re-validates cap client-side, and
(c) valuation is price-blinded so a bad *quote* never reaches the analysis — it
only affects the portfolio MOS check, which is logged and auditable.

### D8 — Structured output: strict output_format with tool-use fallback
**Problem found in live testing:** the `AssumptionSet` schema (5 method blocks +
nested composite scenarios) is too complex for the API's strict structured-output
grammar compiler — `messages.parse(output_format=AssumptionSet)` returns 400 "The
compiled grammar is too large." The simple briefs (phases 1–4) are fine.
**Fix:** `LLMClient.parse` tries strict `output_format` first (fast, guaranteed);
on a grammar/strict 400 it falls back to **non-strict tool-use** (`tool_choice:auto`
+ a "call the emit tool" instruction), validated with Pydantic + repair-on-error.
Note: forced `tool_choice:{type:tool}` is rejected when thinking is on ("Thinking
may not be enabled when tool_choice forces tool use"), so the fallback uses
`auto` + instruction, which reliably elicits the tool call AND keeps thinking.

### D9 — Robustness hardening (timeouts, truncation, traces)
- Per-call timeout 300s (the earlier "7-min phase-0 stall" was a genuine stall;
  same data runs in ~80–130s with thinking off). Caught by an explicit timeout now.
- Structured-output retry escalates `max_tokens` on truncation (`stop=max_tokens`/
  length errors), repairs on schema/constraint violations by feeding the error back.
- Audit captures FULL per-phase traces: thinking (via `display:summarized`), text,
  and tool_use blocks, plus `stop_reason` + `truncated` flag. Verified: reasoning
  phases show real thinking; extraction phases (Sonnet) correctly have none; no
  truncation observed.
- Earlier bug: referenced `anthropic.LengthFinishReasonError` which doesn't exist
  in SDK 0.107 — its `except` clause raised AttributeError and masked the real
  phase-5 error. Removed; classify recoverable errors by message instead.

### D10 — End-to-end validation results (live)
- **AXTI** (semiconductors, $1.72): composite chosen; DCF-bull/NAV-floor branches; red-team
  found subsidiary-level dilution + "overvaluation dressed as a long thesis"; PASSED at $89.
  Price-blinding proven (FV $2.57 computed without the +657% YTD context).
- **ROOT** (insurance, $1.61): composite chosen — DCF $93.83 (p.40) / NAV book floor $19.58
  (p.45) / direct $12 (p.15) = $48.14; red-team caught revenue-multiple-on-insurer, ignored
  convertible prefs, one-quarter-ROE annualization. PASSED at $53.54. Validates the composite
  method handles insurers exactly as intended (book-value floor + turnaround DCF).
- **CIX** (stable industrial): run to confirm the method selector picks DCF/comps (not composite)
  for non-binary businesses — verifying the selector adapts and isn't composite-biased.
Per-name cost is consistent ~$1.6–1.7 at n=1; ~$5 at n=3 (only paid on the undervalued pool).

### D11 — MAJOR PIVOT: agentic, generalizable, cohesive orchestrator
Three QM audits + user direction converged: the fixed 0→7 pipeline was (a) prescriptive
(generic DCF forced on an insurer — wrong framework), (b) starved of sector data (no book
value/ROE/combined-ratio/peer multiples fetched), and (c) a one-directional relay (the
red-team's findings acted on nothing — the 14.1M-preferred miss was never reconciled).

Rebuilt the orchestrator as a **tool-using PM loop** (`orchestrator/agentic.py`):
- The PM investigates in ANY order, as many steps as it needs (no fixed phases), using TOOLS:
  data (`get_financials/ratios/peers/segments/read_filing_section/news/transcripts`),
  `research` (web-search subagent to learn how to value THIS business), `spawn_analyst`,
  `compute_valuation` (the gate — callable repeatedly), and two terminal tools.
- **Generalizable valuation, not prescriptive**: added `excess_returns` (book×ROE, for
  financials), widened comps multiples, and a **`worked`** engine where the PM supplies
  `key_inputs` + a formula and CODE evaluates it (`valuation/safe_eval.py`) — any framework,
  math still in code. The PM researches/chooses the method; we never force one.
- **Enforced reconciliation (user requirement)**: `submit_final(markdown_memo, dossier)`
  triggers a code-run red-team GATE; unresolved valuation-changing concerns FORCE the PM back
  into the loop to fix or rebut, repeating until the memo survives (or a round cap).
  `reject_early` drops. Locked by `tests/unit/test_agentic_loop.py`.
- **The balance** (per user): edge = TOOLS + PROMPT (process discipline), not hard-coded
  valuation logic (too prescriptive) nor freestyling (default Claude). Charter prompts for
  process; tools provide leverage; the conclusion/method is the PM's.
- Non-negotiables preserved: gate (only AssumptionSet computes value), price-blinding (no tool
  returns the quote), judgment-in-LLM/math-in-code, every call audited with full traces.
- Also fixed real bugs: EDGAR sections cited the table-of-contents not the body; quotes were
  cached stale; (ensemble confidence/liquidity issues noted for the phased path).
Config `engine_mode="agentic"` (default); the old phased cascade remains for A/B.

### D12 — Validation across 3 sectors + cost controls
Agentic engine validated live on 3 sectors, each correctly choosing a DIFFERENT method:
- ROOT (insurance) → warranted P/B × through-cycle ROE + separately-valued NOL + peer P/B comps;
  FV $35; 2 red-team rounds, 0 unresolved; reconciled diluted shares incl. anti-dilutive Carvana
  warrants; rebutted the "knife-edge" critique with a sensitivity table. $3.90.
- AXTI (semis) → composite DCF-on-InP-ramp + sourced net-cash bridge + Tongmei NCI ("65% cash /
  35% AI-optical option"); FV $11.2; handled the $632.5M parent raise + NCI; 3 rounds, 1 unresolved
  (transparently flagged optimistic margins).
- CIX (industrial) → plain DCF.
Memos in data/ROOT_memo.md, data/AXTI_memo.md — institutional-grade, better than typical sell-side.

Cost controls (per user's earlier concern, recall-safe): (a) cheap pre-gate before the agentic
deep dive on UNIVERSE runs only — drops only asset-negative insolvent shells (code floor never
drops cash/book-positive names); `microcap one` skips it (explicit request = full analysis).
(b) multi-turn prompt caching on the agentic loop (the stable transcript prefix is cached each
turn). Per-name agentic cost ~$4-9 (depth-dependent); the cached charter + prefix keep it down.

### D13 — Independent validation caught a MATERIAL data bug; added trace + judge
Deep-validation phase (user demanded: verify full traces; an independent agent must declare the
report best-in-existence; orchestrator verified correct).
- **Found via my own SEC research:** FMP's `totalStockholdersEquity` for ROOT = $437.9M but the
  actual Q1'26 10-Q common equity is **$325.9M** — FMP folds the $112M redeemable convertible
  preferred (mezzanine) into equity. The engine used the inflated figure → ~20% overvaluation
  ($33→$26 base). **Fixed** in the data layer: `_common_equity = total − preferred − minority`,
  surfaced prominently in the digest with a book-value note. Verified = $325.9M, matches filing.
- **Full investigation transcript**: the agentic orchestrator now writes `{ticker}.transcript.md`
  — every thinking step, every tool call AND its RESULT, valuations, and red-team/judge rounds —
  so a run reads like the team's entire research history + the final paper. (The audit only had
  the PM's questions, not the answers; now both.)
- **Independent best-in-existence JUDGE** (`orchestrator/judge.py`): a final gate after the
  red-team. It fact-checks the memo's headline numbers against ground-truth reconciled financials
  (would have caught the book-value error) AND judges completeness/rigor vs the ideal. The engine
  is not finalized until the judge rates it best_in_existence (or round cap). Distinct from the
  red-team (flaws) — the judge assesses whether it's the best report that could exist.
- **Memo depth**: charter now demands a feature-length (~2,500-5,000+ word), explanatory HBR-grade
  memo (teach the business + industry + methods), not a terse one. max_tokens 20k for long memos.
- Other validated-correct facts (my web research vs memo): revenue $1.52B/+29%, NI $40.3M,
  preferred $126.5M, NOLs ~$1.28B federal (§382-limited). Calibration note: FY25 net combined
  ratio was 98.2% — the engine's "mid-90s" base was mildly optimistic (defensible, improving).

### D14 — Valuation philosophy + reviewer upgrades (user-driven)
- **Fair Market Value, not bull/bear stories.** FMV = probability-weighted expected PV across the
  full outcome distribution (the max a rational buyer pays today). Dropped the bull/base/bear
  narrative framing — the PM weighs the key uncertain drivers directly into one expected value
  with a confidence band. Also computes a separate no-growth INTRINSIC-VALUE FLOOR
  (`intrinsic_value_floor`) as the margin-of-safety anchor. Must steelman genuine optionality
  (platform/growth/catalyst) at its true probability so FMV isn't understated. (charter + dossier)
- **Tool-using reviewers** (`orchestrator/reviewer.py:ToolReviewer`): the red-team AND the judge
  now have the same data + web-search tools the PM has, to INDEPENDENTLY verify the memo's numbers
  against the filings — a real backstop, not just reasoning over text. They emit verdicts via an
  emit_<schema> tool (same pattern as the PM's submit).
- **Red-team dialogue**: the red-team is PERSISTENT across rounds — the PM adds a "Response to
  Reviewer" section (fix or evidence-based rebuttal), and the SAME reviewer concedes points it
  finds adequately answered. Red-team flags ERRORS only, not priced uncertainty.
- **Separate red-team (3) and judge (3) round budgets** so the judge actually drives quality.
- **Judge = conviction + beat-the-consensus**: the judge researches the market/analyst consensus
  (web), and approves best_in_existence ONLY if the report is accurate, complete, AND more
  convincing than the consensus (`more_convincing_than_consensus`) such that a skeptical elite
  investor would act on it (`would_act_on_it`). Bigger claimed mispricing → higher evidentiary bar.
- **Found & fixed a material data bug** (D13): FMP folds redeemable preferred into equity; data
  layer now computes COMMON equity = total − preferred − minority (ROOT $325.9M, matches the 10-Q).

### D6 — All five valuation engines implemented (UPDATED)
Originally planned rNPV/NAV as stubs, but I implemented all five engines fully:
DCF, Comps, rNPV (probability-weighted scenarios), NAV (asset lines net of
haircuts/liabilities), and Composite (event-branched, see D-composite). All have
unit tests with hand-verified golden numbers. The consolidation prompt offers all
methods and states each one's hard constraints to minimize validation failures.

---

## D15 — Generalizable "diagnose the value driver, then pick the lens" framework + QM fixes (2026-06-07)

**Context:** Drive toward the GLOBAL-MAXIMUM stock agent — value ANY company on
earth (biotech, insurer, Nike-like brand, REIT, quantum deep-tech, miner) at a
caliber above a top firm, WITHOUT becoming prescriptive or flooding the wrong
domain knowledge into the wrong company. Three QM line-by-line review agents also
reported.

**Charter (orchestrator/charter.py) — the methodology upgrades:**
1. **Comprehension precondition** — no valuation conclusion until the PM feels it
   has COMPLETE first-principles understanding of (1) the industry + how it is
   valued, (2) the company, (3) how to value a business *like this*. Reviewers
   probe all three.
2. **Diagnose the dominant value driver FIRST**, then pick the lens just-in-time.
   Archetypes: proven cash-flow compounder (DCF/multiples), financial/spread
   (excess_returns), SCIENCE-/TECH-CONTINGENT (understand the science → milestone
   success probabilities → rnpv/composite; the edge vs human finance), asset/NAV,
   cyclical (mid-cycle), special-situation (catalyst-weighted). Explicit
   anti-flooding rule: don't DCF a pre-revenue drug, don't load Nike with trial
   probabilities — match analysis depth to where the uncertainty actually is.
3. **"You are never stuck"** — when under-informed, name the gap and close it
   (data/filings/news/research/spawn_analyst); finalize only when every knowable
   value-changing gap is closed; unknowable gaps are priced as uncertainty.
4. **Archetype-adaptive memo** — science-contingent names get a "Technology /
   scientific assessment" section justifying milestone probabilities; compounders
   omit it. Go deepest where the value lives; don't pad.

**QM functional fixes (3 review agents):**
- **fmp.py `_common_equity`** — no longer double-subtracts minority interest;
  `totalStockholdersEquity` is already parent-only, so NCI is netted ONLY in the
  consolidated `totalEquity` fallback. (ROOT 437.9−112=325.9 unchanged; correct
  now for any name with NCI.)
- **safe_eval.py** — bounds `**` (overflow guard) and rejects non-finite
  (inf/nan) results instead of crashing or emitting inf as a fair value.
- **assumptions.py CompsAssumptions** — `multiple_type` normalized via alias map
  (EV/EBITDA, ev_to_ebitda, P/E, P/TBV, P/FFO…) and constrained; unknown rejected.
- **comps.py** — refuses a multiple on a non-positive metric (no spurious
  negative fair value).
- **reviewer.py / agentic.py** — the red-team's and judge's OWN verification
  tool-calls (what they checked + results) are now captured and rendered in the
  transcript, so the full reasoning of every gate is auditable (was: only the
  final verdict). 8 new regression tests; 44 total pass.

**Validation set (5 maximally different archetypes, real micro-caps):**
- ANIX ($83M) — clinical/pre-revenue biotech (science: biology)
- KINS ($224M) — P&C insurer (financial/spread)
- FLWS ($277M) — consumer brand (proven compounder, Nike-like)
- ACRE ($277M) — mortgage REIT (asset/book/NAV)
- ARQQ ($190M) — quantum-encryption deep-tech (science: physics/crypto)
ANIX run first as a canary to validate the new framework before the other four.
An expert valuation-concepts reviewer agent audits the methodology in parallel.

---

## D16 — Persistent analyst team + expert-valuation-review integration (2026-06-07)

Two upgrades toward the global maximum: (1) a real research team the PM
interrogates, and (2) the conceptual fixes from an independent expert-valuation
audit of the framework.

**Persistent, citing analyst team (orchestrator/analyst.py):**
- `spawn_analyst` now creates a PERSISTENT, tool-capable analyst that pulls the
  primary record itself (10-K/10-Q sections, transcripts, peers, segments) + web
  `research`, and CONSOLIDATES it. Returns an analyst_id.
- New `ask_analyst` tool — the PM follows up with the SAME analyst (full context
  retained): the back-and-forth a real PM has with the desk ("was this risk
  acknowledged on the last call?", "explain this biological mechanism vs
  competitor X"). Sometimes one pass; the team is always there for follow-ups.
- Every analyst answer must be CITATION-GROUNDED — each material claim, figure,
  and even a scientific/biological concept explanation must be pulled with a tool
  and cite its source (filing+section, the specific call, or the research source);
  uncited = not established.

**Expert-valuation-review fixes (independent audit, G1–G5):**
- G1 COST OF CAPITAL — charter now requires an explicit discount-rate build-up
  (rf + beta×ERP + a MANDATORY micro-cap size/illiquidity premium + country),
  consistent across names, with a no-double-count rule (risk-adjusted flows are
  discounted at a SYSTEMATIC-only rate, not an extra venture premium).
- G2 REAL rNPV — rnpv.py now DISCOUNTS in code: each scenario carries
  probability + value-if-realized + years_to_realization, plus a systematic
  discount_rate; engine returns the probability-weighted PRESENT value. The
  hardest math is audited, not done in the model's head. (Backward compatible.)
- G3 BASE-RATE PROBABILITIES — science memos must build each PoS as cited base
  rate → adjustment for this asset → final, + financing/dilution, erosion,
  time-to-peak.
- G4 OPTIONALITY/SOTP — added exp/ln/log/sqrt/norm_cdf to safe_eval so the
  generic `worked` engine can express Black-Scholes/real-option payoffs (verified
  =10.45 on the canonical call) and sum-of-the-parts (sum segment equity values),
  without adding prescriptive engines. Charter guides honest confidence bands.
  (Full Monte-Carlo engine = future enhancement.)
- G5 GATE HARDENING — red-team AND judge now STRESS-TEST the discount rate and
  every probability against external base rates via research (not just filing
  reconciliation — a wrong WACC/PoS isn't contradicted by any filing). Red-team
  told a blocker needs BOTH severity=high AND would_change_valuation. Judge's
  consensus-anchoring softened: justified divergence from a thin/hype micro-cap
  consensus is the edge, not a demerit.

3 QM line-by-line agents had earlier confirmed the loop control flow is sound and
fixed real data/eval bugs (see D15). 47 tests pass, lint clean.

---

## D17 — Invariant breaches found by expert trace-audit, and fixed (2026-06-07)

Three independent financial-expert agents audited the completed validation traces
(ANIX/ARQQ/KINS/ACRE/FLWS). Verdict: arithmetic CLEAN (every composite re-derived,
no fabricated headlines, gates genuinely recompute) — but TWO core invariants were
being violated. All fixed before the next run; KINS+ARQQ re-run on fixed code for a
confirmatory audit.

**Price-blinding (#2) — was breached (grade D/F):**
- `get_ratios` handed the price-blind PM `marketCap` + every price multiple (P/B, P/E,
  P/S, EV/x, yields) → it could back out the price; `get_dividends` leaked yield.
- The judge/red-team INJECTED the price into PM-facing feedback and penalized memos
  for not anchoring to it (PM transcript: "caught between two directives… instructions
  require me to stay price-blinded… but the judge is pushing back for anchoring").
- Reverse-engineering signature: fair values drifted monotonically AWAY from the
  revealed price across rounds (ANIX .93→.74, FLWS 4.25→3.55, KINS 11.75→11.0); ACRE
  was the clean control (held $4.77).
- FIX: strip all price/market-cap-derived fields from `get_ratios`/`get_dividends`
  (screener unaffected; test locks it); judge + red-team now NEVER state price/cap/
  targets in author-facing feedback and NEVER penalize price omission (consensus
  research informs the judge's own verdict only).

**Consolidation gate (#1) — was bypassed at the memo stage (grade D):**
- ANIX's published $0.74 was never produced by the engine (last compute_valuation
  $0.7971); a hand-edited composite table passed both gates. KINS dossier $11.0 vs
  computed $11.23.
- FIX: `submit_final` now REJECTS unless the dossier headline matches an actual
  `compute_valuation` output (±3%) — judgment in LLM, MATH IN CODE enforced at the gate.

**Gates absorbed soft-input objections:** KINS's 16-17% "through-cycle ROE" contradicted
the PM's OWN math (~28%); the judge flagged it twice then approved at 92. FIX: an
asserted-not-derived or self-contradicted LOAD-BEARING input is now disqualifying until
reconciled in the numbers (not the prose).

Also: transcript header now surfaces the judge score (was hiding scrutiny behind
"Red-team rounds: 0"). 52 tests pass. Remaining robustness item: research-subagent can
hang ~15 min on long-request retries once context balloons (ROOT) — needs context
compaction + a research timeout/retry cap (next).

## D18 — Replaced fluke-revenue complex names (2026-06-08 12:30Z)
The first complex-5 (BZAI/KRRO/RANI/STRO/STIM) included tiny-base "growing revenue" flukes:
KRRO $6.4M (lumpy milestones), RANI $1.6M (pre-commercial), STRO $102M but DECLINING
($154M→$62M→$102M, lumpy partnership). Per user ("be sure growing revenue is not a fluke
from tiny revenue"), swapped those three for names with REAL, substantial revenue:
- VSTM (Verastem, RAF/MEK oncology) $0→$10M→$31M — clean grower, very complex
- VRCA (Verrica, derma drug-device) $5M→$8M→$36M — clean grower
- CDXS (Codexis, enzyme/synthetic-biology platform) ~$70M real revenue — max complexity edge test
Kept STIM ($71→$75→$149M, clean commercial) and BZAI ($38.6M real AI-chip ramp).

## D19 — Deterministic post-analysis price injection (2026-06-08 12:30Z)
User: inject the real stock price into the report header AFTER completion, for comparison.
Implemented in runner/report.py:_price_header — at PUBLISH time (not during analysis) it
fetches the quote and prepends one line: market price · engine FMV · implied upside/downside ·
floor. Preserves the price-blinding invariant: the price is read at the publish layer, never
by the LLM/engine (same pattern as portfolio/book.py). 55 tests still green.
