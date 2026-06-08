# Night Report — 2026-06-07 → 06-08

## Headline
The expert trace-audit caught that the engine, while arithmetically sound, was **violating two of its four core invariants**. Both are now fixed, the memo architecture was rebuilt for genuine HBR depth, and a 6-name validation on the final code came back clean on every integrity dimension. All work is committed to `main`.

---

## What was done tonight

### 1. Critical invariant breaches — found by expert audit, fixed, validated
Three independent financial-expert agents audited the completed traces. Math was clean (A−), but:

- **Price-blinding (#2) was breached** — `get_ratios`/`get_dividends` leaked marketCap + price multiples to the price-blind PM; the judge/red-team *injected* the price into PM feedback and penalized memos for not anchoring to it; fair values then drifted monotonically away from the revealed price (reverse-engineering signature). **Fixed:** stripped all price/market/EV/yield fields (kept fundamentals like dividend/book-per-share — verified); judge + red-team forbidden from relaying price or penalizing its omission. **Validated: 0 price-leaks across all 6 new memos.**
- **Consolidation gate (#1) was bypassed at the memo stage** — ANIX's published $0.74 was never computed by the engine (hand-edited table). **Fixed:** `submit_final` rejects unless the headline matches a real `compute_valuation` output (±3%). **Validated: all 6 finalized, so every headline is engine-enforced.**
- **Gates absorbed soft-input objections** (KINS's 16-17% ROE contradicted its own ~28% math, approved anyway). **Fixed:** asserted-not-derived / self-contradicted load-bearing inputs are now disqualifying.

### 2. HBR-depth memo overhaul
- The memo must be a **self-contained dossier an IM deploys large capital from with nothing else**; teach the science **end-to-end** (ore→refining, chip design→fabrication), dissect the **competitive moat** vs named rivals, and contain **zero process artifacts**.
- **Specialist-authored sections**: analysts now author full, cited, first-principles sections (14k-token budget); the PM commissions and **integrates them (doesn't silo)**, reconciling science-vs-financial disagreements; **bespoke sections** allowed for unusual companies.
- Specialist prompt now conveys the **stakes + extreme-robustness bar** (be your own harshest critic; pre-empt the red-team).
- Plumbing: memo budget 20k→28k tokens; gate memo-truncation 40k→120k chars.

### 3. Full FMP data-tool surface
Added `get_statement` (full balance/income/cash-flow line items), `get_insider_activity`, `get_ownership`, `get_dividends`, peer-statement drill-down, and a **data-discipline** rule (pull numbers from tools, never web-search for them). Validated: heavily used in every run; no web-searching for statements.

### 4. Edge pre-screener (cost-targeting)
Ranks the universe by **differential edge = complexity × coverage-gap** (analyst-count-driven sweet spot), Opus "obviously-overvalued?" sift with a per-sector diversity cap. Backtest on the 6 labeled names was a clean separation. Lets the ~$15 deep dive target the few hundred high-edge names instead of a ~$13K full-universe sweep.

### 5. Infra / hygiene
- **Auto-publish**: `microcap one` writes `reports/<TICKER>/` automatically.
- **Repo fix**: the entire `data/` layer was gitignored (the `data/` pattern matched `src/microcap_engine/data/`) and missing from GitHub — the repo couldn't run; fixed.
- Dead code removed; 52 tests pass; lint clean.

---

## Validation — 6 runs on the final architecture

| Ticker | Sector | Cost | Judge | FMV | Words | Process-artifacts |
|--------|--------|------|-------|-----|-------|-------------------|
| EVMN | biotech | $15.54 | ✓ | $14.5 | 5,367 | 0 |
| ARMP | biotech | $18.93 | ✓ | $0.39 | 4,890 | 0 |
| GCTS | semis | $13.14 | ✓ | $0.22 | 5,215 | 0 |
| ATOM | semis | $11.24 | ✓ | $2.65 | 4,686 | 0 |
| SIDU | space | $10.11 | ✓ | $1.33 | 6,123 | 0 |
| ROOT | insurer | $19.34 | ✓ | $25.0 | 3,663 | 0 |
| **Total** | | **$88.30** | **6/6** | | ~5,000 avg | **0** |

**Clean on every integrity dimension:**
- **Price-blind**: 0 market-price references in any memo (old ROOT said "vs ≈$50 Market"; new memos don't).
- **Engine-enforced headlines**: all finalized → headlines = `compute_valuation` output.
- **Zero process artifacts**: the "could not retrieve this session" language is gone.
- **Deeper & longer**: ~4,700–6,100 words (vs old ~2,500–3,600), richly subsectioned.
- **Specialist-authoring fired** (commissioned in 4 of 6 traces); **bespoke sections** appeared (e.g. GCTS's "RF-CMOS Integration Edge — Mechanism and Head-to-Head").
- **ROOT** — never judge-approved in two prior attempts and the one memo with artifacts — is now **approved (91), artifact-free, and pulled the Note-5 reserve roll-forward** it previously "could not retrieve."

---

## Open items / next session
1. **Confirm quality independently.** All 6 cleared the (raised) judge bar — a strong signal, but run the same scrutinous expert audit on these new reports to confirm the all-approved result reflects true depth, not judge leniency. **(Top priority.)**
2. **ROOT depth** — still the leanest (3,663 words) for a complex insurer; push depth there.
3. **Parallelism decision** — concurrent batch execution of the PM's analyst calls would ~halve wall-clock (currently sequential; the main reason long runs take ~60–90 min). Implementation scoped; awaiting go-ahead.
4. **Phase-2 deterministic sectioning** — NOT needed yet; Phase-1 prompt-level authoring is working.
5. **Production run** — screener top-N → deep dives → sized buy basket.

**Cost reference:** ~$14.7 / deep dive on the final architecture (cheaper than feared despite the added depth).
