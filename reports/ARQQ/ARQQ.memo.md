…

# Arqit Quantum Inc. (NASDAQ: ARQQ) — Initiation: SELL / AVOID

## A probability-weighted appraisal: intrinsic value is "cash plus a lottery ticket," and the stock trades at ≈5x that

---

## 1. Executive Summary

Arqit Quantum is a London-based "quantum-safe" encryption company that came public via the Centricus SPAC in September 2021 on a vision of satellite-distributed cryptographic keys, abandoned that vision after a full impairment, and re-emerged as a terrestrial software vendor selling a cloud-brokered **Symmetric Key Agreement (SKA) Platform**. In substance it is a **pre-commercial venture wearing the costume of a public company**: TTM revenue of ≈**$1.1–1.25 million**, operating cash burn of ≈**$50 million/year**, and **$28.9 million of cash** at 31 March 2026 — roughly twelve months of gross runway, shortened further by a **$7.0 million litigation-settlement cash payment due around mid-2026**.

The correct lens is **not** a DCF of earnings that do not exist, and **not** a revenue multiple on rounding-error sales (the implied ≈150x EV/Sales is meaningless). Arqit is a **science-/technology-contingent optionality stock**, so the right framework is a **probability-weighted scenario valuation (rNPV) with time discounting**: value each realistic end-state, divide by the *future* diluted share count that will exist after the company finances itself there, and discount at a systematic-risk rate.

**The robust conclusion, stated up front as the primary number:** Arqit's defensible intrinsic value is essentially **its net cash (≈$1.3/share after the settlement claim, ≈$1.6 before) plus a thin speculative option** — a **robust anchor of ≈$1.3–$2.2 per share**. The full probability-weighted expected value, *including* a 5%-probability "broad platform" lottery tail, is **≈$2.15 per share** (confidence band **≈$1.15–$4.40**). I report $2.15 as the headline FMV because it is the honest expected value across the distribution, but the reader must grasp its fragility: **strip out the single 5% tail scenario and the probability-weighted value of the operating business collapses to ≈$0.94 — below the cash the company is sitting on and burning.** *Ex the lottery ticket, Arqit's going concern is worth less than its cash.* That is the entire investment case in one sentence.

**This is decisively a SELL/AVOID.** Although I derive value independently of price, the fundamentals tool returns a precise **market capitalization of $190.0 million** on 16.58M shares — an implied **≈$11.46/share** (corroborated by the CEO's April-2026 insider sale at **$13.51** and a third-party GuruFocus GF Value of ≈$7.57). Against my ≈$2.15 intrinsic estimate, the implied **downside is ≈80–82%**. The market is paying ≈$190M (EV ≈$163M) for a sub-$1.25M-revenue, $50M/yr-burn venture with **zero contracted revenue minimums**, a technology being commoditized by free natively-shipped NIST PQC, ≈12 months of runway, and an unresolved SEC investigation plus a fully-accrued $7M securities-fraud settlement.

---

## 2. Business Deep-Dive: How Arqit Intends to Make Money

### 2.1 The product

The **SKA Platform** (formerly "QuantumCloud") is a cloud-mediated **symmetric key agreement** service. Endpoints are provisioned with a bootstrap/root key at registration, then derive fresh ephemeral pre-shared **symmetric** keys on demand via Arqit's cloud, instead of doing a public-key handshake over the wire. The pitch: never expose a breakable public-key exchange to a "harvest-now-decrypt-later" adversary; add a lightweight, crypto-agile symmetric layer that meets the NSA's CSfC symmetric-key-management requirements.

The nuance the bull narrative buries: **Arqit does not replace post-quantum cryptography — it consumes it.** The bootstrap key is delivered wrapped in **NIST's ML-KEM (FIPS 203)** plus other PQC KEMs. Management now frames the product as "crypto-agile… mix and match… post quantum algorithms and symmetric key [cryptography]" and "compliant with NIST and NSA standards" (Q2 FY26 call). The real differentiation is narrow: avoid a public-key handshake on the wire and add a pre-shared symmetric layer for defense-in-depth — valuable in specific classified/defense contexts, marginal in the mainstream.

### 2.2 The failed original vision — why it conditions everything

The IPO thesis was a satellite QKD constellation with the European Space Agency and Virgin Orbit. Abandoned December 2022; satellite assets fully impaired and contracts novated by 2024 (a $12.3M receivable from the now-bankrupt Virgin Orbit was written off in discontinued operations). This matters because the company's projections have catastrophically missed before — the August-2021 SPAC deck projected ≈$32M of 2022 revenue against $7.2M actual (itself flattered by a since-reclassified ESA contract) — which is the very subject of the SEC's fact-finding inquiry and the reason today's "imminent"/"expected" language must be discounted heavily.

### 2.3 Go-to-market and the decisive absence of contracted floors

Arqit sells **B2B2B** — licensing into partners' products and channels. The flagship references and what they actually are:

| Deal | What it actually is | Contracted minimum? |
|---|---|---|
| **Intel TDX** | Co-engineered integration; NetworkSecure inside Intel's TDX confidential-computing enclave on NetSec Accelerator cards | **No** royalty/minimum; monetizes only on downstream licenses |
| **Sparkle (Telecom Italia)** | 3-yr license-to-resell; Quantum-Safe Interconnect across 20 Equinix DCs as NaaS. Arqit's words: a *"volume defined license"* they "would welcome Sparkle's need to upsize." | **No floor** — pure consumption |
| **RSG / Fabric / 6WIND / RAD** | Telecom-edge integrations & resale licenses | Channel; **no minimum** |
| **AMK Travel Group** | Quantum-secure WAN deployment | Small; undisclosed |
| **Aerospace/defence partner (≈90% upsize, May 2026)** | Unnamed European defence solutions provider Arqit co-bids with | Real, upsized — **no $ value/floor disclosed** |
| **DoD program of record** | SKA embedded in a large IT vendor's solution | Real, undisclosed; **no minimum** |
| **Vodafone Tomorrow Street** | "Chosen to add to portfolio" | **Portfolio listing — not a revenue contract** |

**The decisive tell:** Arqit recognized FY2025 revenue from just **seven contracts** (two multi-year/recurring), and ran **eleven** in H1 FY26 — producing just **$623K**. The largest direct deal is described only as "*expected* to result in seven figures of ARR." Management claims "momentum in contracted backlog coming into fiscal year 2026," yet **discloses no backlog dollar value and no committed minimums anywhere.** Every forward revenue figure is therefore a *pipeline-conversion model*, not a backlog model — the structural reason any 20–25x ramp is speculative.

---

## 3. Industry & Competition: Right Demand Wave, Wrong Side of It

**The demand wave is real.** "Harvest-now-decrypt-later" is present-tense. **NIST finalized the first three PQC standards on 13 Aug 2024** (FIPS 203 ML-KEM, 204 ML-DSA, 205 SLH-DSA). The U.S. earmarked ≈$7.1bn for agency migrations (≈2026 deadlines); **NSA CNSA 2.0** mandates ML-KEM-1024 + ML-DSA-87 on a 2025–2035 timeline. On the Q2 FY26 call management cited Google (25 Mar 2026) and Cloudflare (7 Apr 2026) pulling migration advice forward to **2029**, and IonQ's claim it could threaten RSA-2048 in the 2028–29 window. The PQC software market is ≈$0.3–0.9bn (2024/25) growing ≈39–46% CAGR to ≈$2–4.6bn by 2030.

**But the structure disintermediates Arqit.** The NIST algorithms are **free, public, and shipping natively by default**: Cloudflare (>50% of human web traffic already PQ-protected), Google (ML-KEM default; Chrome hybrid), AWS (ML-KEM hybrid in KMS/ACM/Secrets Manager, no code changes), Microsoft (ML-KEM + ML-DSA in Windows 11 / Server 2025 / .NET 10), Cisco (firewalls/routers), Thales/Entrust/DigiCert/IBM (HSM/PKI). When ML-KEM is built into the OS, cloud, browser, firewall and HSM for free, there is little mainstream budget for a separate proprietary key-agreement subscription. The NSA's own objection to QKD — trusted relays, pre-placed keys, special infrastructure — is the same class of concern a cloud-brokered SKA broker raises. Arqit's defensible space is therefore narrow: CSfC dual-layer / classified VPNs / defense overlays where standard PQC isn't yet certified or sufficient.

**Exit anchors:** pure-play PQC software is private and small (PQShield ≈$65M raised total). Narrative quantum names (SandboxAQ ≈$5.6bn on ≈$18M revenue; Quantinuum ≈$14bn IPO chatter) prove a thematic tail premium exists but are not cash-flow comps. M&A multiples: at-scale data-security ≈6.1x (Thales/Imperva); high-growth sub-scale cyber median ≈16x; public cyber ≈7.8x; GovCon/defense-services ≈2–4x — so Arqit's blended exit multiple lands toward the lower end given its mix.

---

## 4. Financial Analysis

**Revenue & segmentation:** Arqit operates in a **single segment** — *"the provision of cybersecurity services"* (SKA Platform), with revenue recognized **at a point in time** (not ratably), which makes prints lumpy and back-end-weighted (FY2025: $67K in H1 vs $463K in H2). Geographically it discloses only a two-way GB vs "Other Countries" split (in FY2022 essentially all revenue was non-UK "Other Countries"); it provides **no customer-level or product-level disaggregation** — a genuine transparency limitation. The revenue series: FY2021 ≈$0.05M; FY2022 $7.2M (reclassified ESA); FY2023 $0.64M; FY2024 $0.29M; FY2025 $0.53M; H1 FY2026 $0.62M. The "829% YoY" is real arithmetic off a ≈$67K base. After 4+ years public, never a clean ≈$10M year.

**Profitability:** Operating losses persistent (FY2023 −$54.5M; FY2025 −$35.2M operating). The FY2022 +$65M net income was a non-cash warrant fair-value gain (operating income −$52M). FY2025's net loss (−$35.3M) includes a **$7.0M non-cash "exceptional" litigation provision** (see §5). Gross profit is frequently *negative* — no operating-leverage curve to model.

**Receivables — anomaly investigated and largely dismissed.** The screen shows a ≈1,110-day DSO and receivables ≈3x revenue, which looks alarming. On inspection it is **mostly a denominator artifact**: the metric divides a *combined* "trade **and other** receivables" caption (≈$3.04M at 30 Sep 2025, which bundles prepayments, VAT and other non-trade items) by a near-zero revenue base ($530K). Under IFRS 9, Arqit booked **nil** trade-receivable impairment in FY2025 and only $0.166M in FY2024 ("an unrecoverable customer balance"); the large $12.3M write-off relates to bankrupt Virgin Orbit and sits in **discontinued operations** (historical). So this is **not** a $3M bad-debt overhang. I flag only the residual transparency gap (no disclosed gross-trade-receivable sub-component or counterparty concentration) rather than treating it as a red flag.

**Cash & runway (gating):** Cash **$28.86M at 31 Mar 2026**; H1 FY26 operating burn **−$25.26M (≈$4.2M/mo, ≈$50M/yr)** → **≈7 months gross runway**, extended only by ≈$17–18M of ATM sales in the half, and reduced by the **$7M settlement cash outflow due ≈mid-2026**. Debt is just lease liabilities (≈$0.7–2.2M); **there is no live convertible loan** (the legacy £3.5M Series B notes converted to equity at the 2021 SPAC merger; the XBRL tag is a comparative artifact). Current ratio ≈4.9x. Capital *access* isn't the constraint ($250M shelf, ≈$100M+ ATM remaining) — *price/dilution* is.

**Dilution & share count:** One **25-for-1 reverse split (Sept 2024)**. Post-split, basic shares 2.7M (FY21) → **16.58M (31 Mar 2026)**. Fully-diluted (in-the-money basis): basic 16,580,855 + **5,393,562 Sept-2024 warrants at $2.50** (deeply ITM; +≈$13.5M cash on exercise) + ≈1.07M RSUs + ≈0.32M options → **≈22–23.5M today**; legacy warrants ($287.50/$50/$62.50/$19.50) are OTM/worthless. Crucially, **≈$80–150M of further raises to reach breakeven take the count to ≈30–45M.** This dilution overlay — not enterprise value — governs value to *today's* holder, and against a market cap of $190.0M the market is plainly not pricing it.

---

## 5. What Management Said (verbatim)

The tone across the Q2 FY25, Q4 FY25 and Q2 FY26 calls is one of accelerating engagement and credible repositioning toward NIST/NSA-compliant software ("detect, protect, and comply"). But the substance is consistently *forward-looking and unquantified*:

- On the marquee telco deal: *"take up of Sparkle's network as a service offering means consumption of its volume defined license with Arqit… we would welcome Sparkle's need to upsize its license"* — i.e., consumption-based, no floor (Q2 FY26).
- On defense: *"we believe a renewal and upsizing of our largest U.S. defense-related contract is imminent"* and *"It takes time to win contracts in the government and defense space"* (Q2 FY26). On Q4 FY25: *"sales cycles in defense can be slower than other markets, [but] we believe that this market will represent a large percentage of our revenue over time."*
- On pipeline as the proxy for traction: *"In the first two months of this fiscal year, we have already signed 12 demonstration and test engagements"* and *"we expect additional contract wins during the balance of the fiscal year"* (Q4 FY25 / Q2 FY26) — demonstrations, not bookings.

The pattern: emphasis on demonstrations, percentage growth, and "imminent"/"expected" milestones over hard, contracted dollars. The **CEO also sold 7,595 shares at $13.51 in April 2026** — a small but unhelpful signal while asking the market to fund the burn.

---

## 6. Technology / Scientific Assessment & Probability Justification

Each probability is built base-rate → adjustment → final.

**Base rate.** Deep-tech ventures with a working product but sub-$2M revenue and a credible TAM convert to "commercially meaningful" (>$50M sustainable revenue) at ≈10–15%; the modal outcome is failure or acqui-hire.

**Arqit-specific adjustments (net strongly negative):** (a) *Structural disintermediation* — the product consumes NIST PQC that hyperscalers give away natively; caps mainstream TAM. (b) *Credibility/legal overhang* — the April-2022 WSJ exposé; a securities class action whose motion to dismiss was **denied in full** (Mar 2025) and then **settled for $7.0M** (term sheet 20 Oct 2025; preliminary approval 3 Feb 2026; final hearing 1 June 2026), fully accrued at 30 Sep 2025; and an **SEC fact-finding investigation into the Centricus merger projections that has no public resolution** (no source confirms it closed; no enforcement action announced — treat as likely-still-open). (c) *Runway/dilution reflexivity* — ≈12 months of cash plus the $7M outflow + ATM supply pressures price, raising shares-per-dollar. (d) *No contracted floors* — eleven contracts → $623K. (e) *Positive offset* — a genuine CSfC/defense niche, statutory deadlines, a replicable Sparkle blueprint, standards-aligned product.

**Net probabilities adopted:** **5% broad / 22% niche / 28% muddle / 45% failure.** I deliberately stress the failure weight UP to 45% (from a "balanced" 40%) because zero contracted backlog + active disintermediation + a 12-month cash clock + a near-term $7M cash claim make a punitive-raise-or-wind-down outcome more likely than a generous base rate implies — and a higher failure weight both *strengthens the thesis* and pulls the point estimate toward the cash-plus-option anchor.

---

## 7. Valuation

### 7.1 Why rNPV, and why not the alternatives

A DCF needs a forecastable stream; Arqit has negative gross profit and a binary outcome — DCF would be fiction. A revenue multiple on ≈$1.2M sales gives absurd outputs (the market's implied ≈150x EV/Sales is not analysis). Excess-returns/book frames are for financials. The correct frame is **probability-weighted scenarios with time discounting**: value each end-state, divide by *future* diluted shares (so dilution is captured — every share, whenever issued, has the same per-share claim), discount at a **systematic-risk** rate. Binary/technical risk lives in the probabilities, so no venture rate on top (no double-count). **Discount-rate build-up:** rf ≈4.3% + beta ≈1.8 × ERP ≈5.0% + ≈2% micro-cap/illiquidity ≈ **≈15%**.

### 7.2 Bottoms-up niche bridge — with an explicit per-line conversion-probability layer

The niche-success *state* targets ≈$30M FY2030 revenue. But each line is itself a conversion bet; weighting each by a standalone probability shows why the *unconditional* expected revenue is far lower (≈$10M, i.e. the "muddle" zone) and why full niche success warrants only ≈22%:

| Stream | FY30 target (mid) | Standalone conversion prob. | Prob-wtd revenue |
|---|---|---|---|
| Defense/gov programs of record | $15M | 35% | $5.25M |
| Tier-1 telco NaaS (consumption) | $7.5M | 30% | $2.25M |
| Enterprise direct licenses | $4.5M | 25% | $1.13M |
| Encryption Intelligence + services | $3.0M | 40% | $1.20M |
| **Conditional niche total** | **≈$30M** | | **Unconditional E[rev] ≈ $9.8M** |

ARR anchors peg to the one hard datapoint (a gov license "expected to result in seven figures of ARR"). In the *niche-success* state (all lines convert), mix ≈ 60% GovCon/services-like (3–6x) + 40% software/NaaS (8–12x) → **blended ≈6x → EV ≈ $180M**. Divided by ≈30M future shares → ≈$6.0/share at exit. (I explicitly refuse the 16x cyber-M&A median — the GovCon weight and lumpiness don't earn it.)

### 7.3 The result

| Scenario | Prob. | Equity/share at exit | Yrs | PV/share @15% | Weighted |
|---|---|---|---|---|---|
| Broad platform (tail) | 5% | $57.0 | 6 | $24.64 | **$1.23** |
| Niche success | 22% | $6.0 | 5 | $2.98 | **$0.66** |
| Muddle / zombie | 28% | $1.9 | 5 | $0.94 | **$0.26** |
| Failure / wind-down | 45% | $0.05 | 2 | $0.04 | **$0.017** |
| **Probability-weighted FMV** | | | | | **$2.17 (≈$2.15)** |

### 7.4 The floor, and the tail-fragility — the crux

The conservative no-growth **floor is net cash, less the senior $7M settlement claim**: ($28.86M cash − ≈$2.2M debt − $7.0M settlement) ÷ 16.58M ≈ **$1.2/share** (≈$1.6 before the settlement). This is what an *immediate* liquidation returns; the going concern actively burns it, which is why the 45% failure case is ≈$0, not cash.

**Decompose the $2.17:** the 5% broad tail alone contributes **$1.23 (57%)**. The *operating business ex-tail* is worth only **$0.94** — *below* the ≈$1.2–1.6 cash floor. So the structure is: **≈$1.2–1.6 of cash, an operating business worth roughly nothing-to-slightly-negative after burn, and a ≈$1.2 speculative call option.** A disciplined investor who declines to pay for an unfalsifiable 5% jackpot should anchor to **≈$1.3–$2.2**. I keep $2.15 as the honest tail-inclusive expected value, but the *robust* number is the cash-plus-thin-option band.

### 7.5 Dilution / raise-price sensitivity (the variable that actually moves per-share value)

Holding the *niche-success* state fixed ($180M exit EV, 5 yrs, 15% discount, ≈22M shares pre-raise incl. warrants), varying the ATM clearing price at which ≈$100M is raised:

| ATM clearing price | New shares | Total future shares | Exit equity/share | PV/share @15% |
|---|---|---|---|---|
| $13 | 7.7M | ≈29.7M | $6.06 | $3.01 |
| $10 | 10.0M | ≈32.0M | $5.63 | $2.80 |
| $6 | 16.7M | ≈38.7M | $4.65 | $2.31 |
| $4 | 25.0M | ≈47.0M | $3.83 | $1.90 |

The reflexive trap: a falling share price *raises* shares issued per dollar, which *lowers* per-share value, which pressures the price — a doom loop for a thin-revenue ATM-funded name. Even the niche-success "win" returns only ≈$1.9–3.0/share to today's holders.

### 7.6 Sensitivity band & cross-checks

- **Low (≈$1.15):** failure 54%, niche 16% @ lower EV, broad 3%, 16% discount — converges on/below the cash floor.
- **Central (≈$2.17):** as tabled.
- **High (≈$4.42):** niche 32%, broad 8%, failure 30%, 14% discount.
- Even the *high* case (≈$4.4) sits ≈60% below the ≈$11.46 implied market price — the stock is overvalued across the entire plausible band.

**Cross-check #1 (aggregate-equity):** naive EV-weighted business value ≈ $130–150M; discounting ≈5 yrs and applying the dilution haircut (current holders own ≈40–55% of outcome equity, ≈0 in failure) → ≈$40–65M expected present equity over the ≈22M ITM diluted base → low-$2s/share. Agrees.

**Cross-check #2 (dismantling the lone bull anchor — HC Wainwright $60, Scott Buck, Buy):** (1) It is a *one-analyst* "consensus" — Street high and low are the same $60; GuruFocus GF Value ≈ $7.57. (2) No disclosed valuation bridge; the analyst's own model shows losses for years (FY26 EPS −$1.52, FY27 −$1.06) — an undisclosed multiple on an assumed ramp. (3) $1.2M FY26 revenue is less than one month of burn; even a $250M EV at 8–10x needs ≈$25–30M revenue (a 20–25x jump), none contracted. (4) It ignores disintermediation. (5) Pilots/integrations/listings are treated as backlog. *One line:* **the $60 target is a single analyst's undisclosed multiple on a hypothetical 20×+ ramp that is neither contracted nor defended against free, native PQC — against a company burning $4M/month with ≈$29M of cash and a $7M settlement due.**

---

## 8. Probability-Weighted Outcome Distribution

One distribution, not a bull/bear pair:
- **45% — equity impairment to ≈zero.** Cash exhausts (the $7M settlement accelerates this); a raise fails or prices punitively; assets ($10–40M of patents/CSfC certs/DoD reference/team) sell but steer to retention/creditors ahead of common.
- **28% — zombie/muddle.** Revenue $3–10M (≈ the unconditional expected revenue from §7.2), perpetual dilution, EV ≈$80M but per-share bleeds (+$0.26).
- **22% — niche success.** ≈$30M revenue, ≈6x, ≈$180M EV to a defense prime/PKI vendor (+$0.66 weighted).
- **5% — broad platform.** Beats disintermediation, ≈$200M revenue, ≈$2.4B EV (+$1.23 weighted) — the convex tail carrying the headline.

Left-skewed and tail-dependent: ≈73% of probability sees holders impaired or heavily diluted. The band ($1.15–$4.40) reflects honest uncertainty in those weights, not alternative narratives.

---

## 9. Risks & What Would Change My Mind

**Risks:** (1) near-certain $80–150M further dilution, possibly at depressed prices (reflexive doom-loop); (2) disintermediation by free native NIST PQC; (3) ≈12-month runway / going-concern, tightened by the $7M settlement cash-out ≈mid-2026; (4) unresolved SEC fact-finding investigation into the SPAC projections; (5) zero contracted revenue minimums anywhere; (6) disclosure opacity (single segment, no customer concentration, point-in-time lumpy revenue). (7) **For the short side:** thin float + 5.4M ITM warrants + a hot "quantum" theme = real squeeze/borrow risk despite correct fundamentals — express via puts to cap it; size small.

**Bearish catalyst path (how the gap closes):** the next dilutive raise (likely H2-CY26 as cash nears exhaustion and the settlement is paid) at a discount; flat revenue prints through FY2027 exposing the pipeline-vs-backlog gap; an SEC enforcement step; or the theme simply cooling.

**What would move me off SELL:** a disclosed multi-year defense program of record with hard, multi-million-dollar contract value; a telco converting a "volume-defined license" into disclosed eight-figure recurring revenue; a strategic investment removing the financing overhang; FIPS/CSfC certifications locking Arqit into classified architectures; formal closure of the SEC inquiry with no action.

---

## 10. Conclusion

Arqit is a legitimate-technology, wrong-side-of-commoditization, serially-diluting optionality stock with a live legal overhang. Its defensible intrinsic value is **net cash (≈$1.3 after the settlement claim) plus a thin speculative option** — a robust anchor of **≈$1.3–$2.2**, with a full tail-inclusive probability-weighted **FMV of ≈$2.15** (band **≈$1.15–$4.40**). The decisive fact: **ex the 5% lottery tail, the operating business is worth ≈$0.94 — less than its own cash.** Against a market capitalization of **$190.0M (≈$11.46/share)**, corroborated by the CEO's $13.51 sale and a ≈$7.57 GF Value, the shares are **≈80% overvalued**. **Rating: SELL / AVOID.** For holders, a source of funds; for new entrants, wait for intrinsic value to be re-anchored by a genuine, contracted, multi-million-dollar revenue event — which does not yet exist.
