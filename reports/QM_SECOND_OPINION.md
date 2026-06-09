# Independent second-opinion QM pass — 6 full reports

Each report was handed to a separate senior-analyst reviewer **with no knowledge that a pipeline
produced it** — framed as "a human colleague wrote this; you're the second set of eyes before we
deploy capital." The instruction was to assume errors exist until checked, re-derive the fair
value from the author's own assumptions, and refuse to be impressed by polish. (JRVR/VRCA/CDXS
were budget-truncated stubs — not reviewable.)

## Verdict table

| Report | Reviewer verdict | Deploy as-is? | Headline FV | Honest re-derived FV | Call survives? |
|--------|------------------|---------------|-------------|----------------------|----------------|
| **BZAI** | **STRONG** | **YES** (act on the overvalued/avoid call) | $0.36 (−79%) | $0.40–0.57 (still ≤ −67%) | ✅ yes |
| **VSTM** | MIXED | NO | $7.16 (+93%) | $5.5–6.2 (+50–65%) | ⚠️ buy, but thinner |
| **MFIN** | MIXED | NO | $10.88 (+12%) | $9.25–10.0 (≈ fair) | ❌ margin gone |
| **CPSS** | MIXED | NO | $8.08 (−13%) | ~$5.6–7.5 (−25 to −40%) | ❌ more bearish |
| **STIM** | MIXED | NO | $1.33 (+6%) | $1.18–1.25 (≈ fair/rich) | ❌ margin gone |
| **NUS** | **WEAK** | **NO** | $10.30 (+95%) | $8.5–9.0 (near floor) | ❌ BUY collapses |

## The cross-cutting pattern (this is the real finding)

Every reviewer independently reached the same structural conclusion: **the qualitative research
is strong and accurate, but the headline fair value is flattered at the consolidation step by one
or two convenient assumptions.** Five of six had the *same* failure mode.

1. **The "math in code" invariant is being bypassed in practice.** Two reviewers (NUS, MFIN)
   found the composite engine was fed **hand-supplied per-scenario `value_per_share` numbers** and
   merely probability-weighted them — the PM built the valuation table by hand and labelled it
   "engine output." MFIN reviewer: *"'Math in code' is cosmetic here."* NUS reviewer: *"The author
   rebuilt a valuation table by hand and labeled it as the engine's output."* This is the #1
   architecture defect — invariant #3 is not actually enforced for composite/scenario valuations.

2. **Consistent optimistic tilt at the final step** (the opposite of the old conservative-tilt
   concern — likely an ANCHOR-HONESTLY over-correction + weight-tinkering):
   - NUS — net-debt switched $125.6M→$67M and rate 11%→ "13.5% but DCFs ran at 11%"; weights
     visibly retuned (30/45/20 → 35/40/25) until the number "felt right."
   - MFIN — a **$42.4M deferred-tax add-back** vs **$19.6M actually on the balance sheet**
     (flagged twice by the internal red-team, never fixed); it *is* the entire +12% margin.
   - CPSS — ~$2.5/sh of FV rests on an undisclosed **buyback-accretion** assumption; strip it and
     the naïve residual-income value is ~$5.6.
   - STIM — dominant 30%-weighted path uses **80M shares (zero dilution)** while other paths use
     88–115M; FV anchored just above the activist's accumulation price.
   - VSTM — per-share divides by **112M shares** though the thesis itself says 130–145M after the
     near-certain pre-catalyst raise.

3. **Share-count / dilution is the most common quantitative gap** — STIM, VSTM, NUS all mis-handle
   post-dilution per-share. For cash-burners that must raise *before* the value-resolving catalyst,
   the shares that will exist at resolution aren't the shares the FV is divided by.

4. **The discount rate is built up, then a different rate is used** — NUS (13.5% asserted, DCFs ran
   11–12%), STIM (17–20% CoE built, discounted at 11%). The build-up is theatre if the engine runs
   a different number.

5. **Red-team finds issues but they don't get fixed** — MFIN's DTL (twice), VSTM's RAMP-205 PoS
   and a wrong Astellas competitive-stage claim (all three rounds). The gate surfaces, it doesn't
   block.

## What's genuinely strong (the edge is real)

- **Research quality + primary-source accuracy.** VSTM's science was verified against Lancet/JCO/FDA
  (RAMP-201 ORR 44%, GOG-281 HR 0.48 — exact); BZAI's facts (gross-margin pass-through, silicon
  efficiency, NeoTensr shell) verified; STIM's covenant-breach timing verified against the 10-Q;
  MFIN's NII/equity-gains bridge and NUS's MLM/commission/Prysm-science teardown are first-rate.
- **Correct method selection** — warranted P/B for the lenders, rNPV for the science names, SOTP +
  survival for STIM; reviewers agreed the *lens* was right in every case.
- **A verified contrarian win** — BZAI: the engine called a hyped AI-inference name **−79% overvalued**
  on a verifiable thesis (10% pass-through gross margin + bottom-quartile TOPS/W) that survives even
  generous bull adjustments. That is exactly the cross-domain edge working.

## Bottom line

The pipeline's **investigation** is deploy-grade; its **valuation consolidation** is not. The fix
is not more research — it's closing the consolidation seam:
(a) force the composite/scenario engine to compute each branch's per-share value from structured
assumptions instead of accepting hand-supplied numbers (restore math-in-code);
(b) single-source the discount rate and the (post-dilution, diluted) share count so the built-up
rate is the rate used and one share count flows everywhere;
(c) require an explicit dilution/runway pro-forma into per-share for pre-catalyst burners;
(d) make the red-team gate **block** on unreconciled flagged items;
(e) guard against probability-weights being reverse-engineered to a target FV.

On an honest re-read: **1 STRONG (BZAI), 1 thinner-but-intact buy (VSTM), 4 calls that don't
survive (NUS/MFIN/CPSS/STIM).**

---

## Full reviews

### NUS — VERDICT: WEAK (do not deploy)
**Stake capital as-is? NO** — the headline FV is not the output of the author's own worked DCFs; scenario values and net-debt were silently rewritten between model and memo, and the honest re-derivation lands ~10–20% lower while the upside is overstated.
- Strengths: variable-cost commission structure as the melt-but-solvent mechanism (§2.3–2.4, §4.1b); field-force KPI collapse honestly surfaced (Customers −45%, Leaders ≈−50%, attrition *accelerating*); the Prysm iO science teardown (§2.7, validated biomarker vs "nutritional score" overreach, FTC consent-decree history).
- `[critical] §6.3/6.4` Memo scenario values (bear 7.62/base 10.36/bull 14.06/FMV 10.33) ≠ the engine's actual DCFs (bear 7.53/base 11.24/bull 17.06/composite 11.40 at 11–12% WACC, net debt $125.6M). Hand-built table labelled as engine output.
- `[critical] §4.5/6.3` Net-debt used opportunistically: §4.5 says ≈$15M net *cash*, valuation uses $67M net debt, DCFs used $125.6M. Switching to the low figure inflates every per-share output ~$1.20.
- `[critical] §6.2` 13.5% rate asserted but every DCF ran at 11–12%; build-up double-counts secular risk (in the rate AND the cash-flow path AND the weights AND a +0.5% terminal floor).
- `[major] §6.4/§7` Probability weights retuned to the answer (30/45/20→35/40/25). `[major] §6.3` Forced +0.5% terminal growth on a −12%/yr business inflates a TV that's 55–65% of EV. `[major] §4.4` FCF normalized $46M→$80M via three same-direction adjustments.
- Independent FV: on the engine's own worked numbers the composite is actually $11.40 (higher!), but that runs at 11.5% WACC + forced positive terminal + $80M normalized FCF. Re-run at the author's own 13.5%, flat/negative terminal, guided capex → ~$8.0–9.0, near the $7.75 floor; BUY collapses.
- Missed: no honest reconciliation between a thesis that screams "structurally declining MLM, accelerating attrition" and a base case that assumes deceleration-to-flat with perpetual positive terminal growth.

### MFIN — VERDICT: MIXED · Deploy as-is? NO
The entire +12% margin evaporates once the $42.4M deferred-tax add-back is reconciled to the $19.6M actually on the balance sheet; on defensible inputs this is roughly fair-valued.
- Strengths: correct method (warranted P/TBV = (ROTCE−g)/(CoE−g), §3/§7.1, explicitly rejects EV/EBITDA & DCF); forensic Q1-26 EPS bridge ($12.0M→$5.0M = $9.1M equity-gains swing, provision flat — not credit, §4.2–4.3); honest credit-normalization table (§4.6).
- `[critical] §4.6/7.3/8` $42.4M DTL add-back vs $19.6M real (flagged twice by internal red-team, never fixed) → real DTL gives FMV ~$10.01 (≈ market), strict TCE ~$9.25 (below market). `[critical] §8` scenario per-share values were hand-supplied inputs, not engine outputs.
- `[major] §8` bear case ($5.59) labelled "near strict tangible book" but TBV is ~$10.05 — wants it both ways. `[major] §4.5` recreation NCO maybe understated (~3.95% used; public Q1 ~4.7%, activist cites 16-yr high). `[major] §7.3` ROTCE≈CoE means warranted≈book, so FV is mechanically whatever TCE you plug — making the DTL defect dispositive.
- Independent FV: author's formula reproduces to $10.88 exactly, but inherits the inflated $282M base; real DTL → ~$10.01, strict TCE → ~$9.25. ≈ fair, not a +12% PASS.
- Missed: the call isn't robust to its own flagged adjustment.

### CPSS — VERDICT: MIXED · Deploy as-is? NO
Method and facts largely right, but FV is flattered by undisclosed buyback-accretion and the residual equity is materially under-stressed; true picture is more bearish than −13%.
- Strengths: correct warranted-P/B framing for a levered spread lender (§7.1, §3.4); the ROE collapse correctly diagnosed as a cost-of-funds event (2.54%→8.48%→~5.5%, NCOs flat ~7.6–7.8%, §4.2–4.3); honest use of the 2008–09 near-death to justify a high hurdle.
- `[critical] §7.6` ~$2.5/sh rests on assuming surplus returned via buybacks at 0.6x book; the naïve residual-income build is ~$5.6/sh → −40% vs market, not −13%. `[critical] §7.5/8/4.7` residual leverage under-stressed: a ~50bp combined NIM miss (both in the author's own risk list) takes ROE ~11%→~3% → ~$3/sh, far below the $5.69 "bear."
- `[major] §7.9` sensitivity table not reproducible from its own stated formula (per-row g appears to flex). `[major] §7.2` central CoE (15.5% vs CACC-implied 13%) is hand-picked; the whole call hinges on a 250bp judgment dressed as derivation. `[major] §1/7.3` invented 22.5M share blend swings FV ±$0.5.
- Independent FV: reproduces to $8.08 exactly, but honest central ~$6.5–7.5 with a fat left tail; more clearly fully-to-over-valued.
- Missed: the violence is in the EARNINGS (thin first-loss residual), never stress-tests the joint correlated downside (NCO 9–10% AND sticky funding AND APR caps) that a subprime cycle delivers together.

### STIM — VERDICT: MIXED · Deploy as-is? NO
Diagnosis/segment/survival work is strong, but the headline rests on an over-weighted Strategic path with an overstated value and a no-dilution share count.
- Strengths: correct SOTP-plus-survival lens + the key fact that ~$34M corporate overhead exceeds either segment's contribution (§2,§4); covenant analysis verified vs Q1'26 10-Q (projected breach ~Q1'27, $13.2M cash vs $65M loan); BrainsWay FY2025 figures exact; honest about falling shipments (205→185→159).
- `[critical] §6` Strategic path uses "$2.55" but its own basis computes $2.49, on **80M shares (zero dilution)** vs 88–115M elsewhere → on a consistent ~88M count it's $2.26. `[critical] §6` discount at 11% though a 17–20% CoE was built; at 13–15% headline falls to $1.25–1.29.
- `[major] §6` valuation migrated $1.75→$2.05→$1.33, reverse-engineered to sit just above the activist's ~$1.33 accumulation price (anchor contamination). `[major] §6/7` dilution asserted, never modeled (no pro-forma share bridge).
- Independent FV: $1.33 reproduces mechanically, but fixing the Strategic path ($2.26) + 13% rate → ~$1.18–1.22, *below* the $1.25 market. Fairly valued at best.
- Missed: the going-concern covenant clock (~Q1'27) likely precedes any sale close, handing the one logical buyer (BrainsWay) pricing power — so the 30% clean-SOTP weight is too high and its value too generous; the two errors compound.

### VSTM — VERDICT: MIXED · Deploy as-is? NO
Science is accurate and primary-source-verifiable and the rNPV is auditable, but the per-share figure ignores the author's own near-certain forward dilution.
- Strengths: RAMP-201 (KRAS-mut ORR 44%, DoR 31.1mo) and GOG-281 (HR 0.48) verified against Lancet/JCO/FDA; rNPV cash-flow schedules tie out (LGSOC PV $1,020M, composite reproduces $7.161) with the discount properly applied and risk in the probabilities not double-counted; honest about the 40% RAMP-301 withdrawal tail and serial dilution.
- `[critical] §8.5/4.4/7` every scenario divides by 112M shares though §4.4/§7/§10 call ~130–145M "near-certain" by the mid-2027 readout → 135M cuts $7.16→~$5.93 (145M→~$5.52). The below-NAV leakage haircut is a *different* effect and doesn't substitute.
- `[major] §3.6/8.5` 60% LGSOC PoS sits near the 63% conversion rate, not the 43% that *demonstrated* benefit — top-of-range. `[major] §8.5` RAMP-205 PoS 12% ≈ 4× the stated 3% pancreatic base off n=12 (red-team-flagged, never cut). `[minor]` §8.3 arithmetic ($1,020×60%+$120×40% stated ≈648, correct 660); Astellas competitive-stage claim wrong (flagged all 3 rounds).
- Independent FV: $7.16 falls out cleanly at 112M; swap to the author's own forward share count → ~$5.5–6.2 (+50–65%, still a buy, thinner). PoS defensible but not conservative.
- Missed: per-share is on *today's* shares while the thesis requires a raise *before* the catalyst that resolves the binary.

### BZAI — VERDICT: STRONG · Act on the overvalued/avoid call? YES
The two load-bearing pillars (fraud-flagged ~88% revenue concentration at ~10% GM, bottom-quartile silicon efficiency) are independently verified, mutually reinforcing, and survive generous bull adjustments; FV math reproduces and the gap is wide enough to absorb soft spots.
- Strengths: the gross-margin tell (§4.2 — 10–11.9% H2'25 GM snapping to 50.8% when China orders paused proves pass-through resale *independent of how the fraud resolves*) is the right killer argument; verified factual spine (NeoTensr shell incorporated 12/2025, Hailo-8 ~10.4 TOPS/W vs Blaize ~2.3, NXP-Kinara $307M comp); correct rNPV frame with base-rate-anchored weights and an explicit acquihire reconciliation.
- `[major] §7.6/4.4` $0.02 wipeout value inconsistent with the author's own ~$0.25 orderly-liquidation floor (at the floor, FV $0.36→~$0.42). `[minor]` survival branch arithmetic ($0.40 text vs $0.45 used); acquihire sensitivity larger than the stated "±$0.05" (true range $0.23–0.57).
- Independent FV: reproduces to $0.36 exactly; honest point estimate ~$0.40–0.45; even at the optimistic $0.57 the downside to $1.73 is ~−67%. The call is robust; only the point-estimate precision is overstated — frame as "<$0.60, deeply overvalued," not a point.
- Missed: no explicit stress-test of the bear thesis against a *clean* revenue surprise (the Q2'26 >$11M NeoTensr guide shipping and collecting at normal margin) — matters most if deploying as a short rather than an avoid.
