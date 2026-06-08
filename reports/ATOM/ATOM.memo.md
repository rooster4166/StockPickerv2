## Atomera Incorporated (NASDAQ: ATOM) — Initiation / Intrinsic Value Memo (v3, final)

### Executive summary

Atomera is not an operating semiconductor company in any conventional sense. It is a **pre-revenue materials-IP optionality vehicle**: a 25-year-old, decade-public licensor of one core invention — Mears Silicon Technology (MST), an epitaxially deposited, oxygen-engineered thin film of "reengineered silicon" — that it hopes foundries, IDMs and fabless designers will insert into their fabrication flows for license fees and per-wafer/per-device royalties. As of FY2025 it generated **$65,000 of revenue** against **$20.9M of operating expense**, burned **about $15M of cash**, and carries an **accumulated deficit of roughly $242M**. It has never earned a production royalty.

Because there is essentially no current earnings stream, the only intellectually honest way to value ATOM is as a **probability-weighted, time-discounted bundle of future adoption outcomes (rNPV)** sitting on a **net-cash floor**. A DCF of today's (deeply negative) cash flows or a multiple of $65k revenue would be valuation theater. The whole question is: *what is the probability MST converts into a royalty-bearing, high-volume-manufacturing (HVM) license, when would that become visible, and what would the equity be worth if it does?*

**My answer:**
- **Intrinsic-value floor (no-growth / asset): about $1.00/share** — net liquid assets per share after the February 2026 raise (a built-up cash + weak-IP floor, Section 6).
- **Fair market value (probability-weighted): about $1.80/share** (model $1.77), confidence band **about $0.95–$3.70**.
- The FMV is **option value**: roughly 75–80% of it comes from the ≈15% combined probability of a "solid" or "blockbuster" adoption outcome; the modal (≈70% weight) outcome is failure, where the equity is worth little more than residual cash and a thin patent estate.

**Reconciliation to the market.** The shares trade around **$7.6**, with at least one sell-side target near **$10**. My independently-derived FMV of ≈$1.80 implies the market is pricing an **implied probability of commercial success roughly 2.5–3x** what a decade of evidence, the October-2025 STMicroelectronics qualification failure, and the historical record of *no-fab* materials-insertion plays support. This is the signature of a narrative-driven, AI-adjacent small cap: real science and real optionality, but a price that has run far ahead of the probability-weighted cash the business will actually return to owners. Rebuttal in Section 9.

---

### 1. Business deep-dive — how Atomera intends to make money

**The product.** MST is "a thin film of reengineered silicon, typically 100 to 300 angstroms (≈20 to 60 silicon atomic unit cells) thick" (10-K, Item 7) — an epitaxial silicon film with partial monolayers of oxygen inserted into the lattice. It does two physically validated things: (1) **blocks dopant diffusion** (pinning roving boron/phosphorus atoms, sharpening junctions), and (2) delivers a **secondary mobility/variability benefit**, much of which derives from the same diffusion-blocking effect. It is best understood as a **doping-profile-engineering tool**, not an exotic high-mobility material.

**The business model.** Atomera designs and manufactures nothing; it licenses. The revenue waterfall (10-K, Item 1): (1) **MSTcad software** + **paid integration engineering** (evaluations/JDAs) — small, used to *demonstrate* MST; (2) **R&D license** — fee when MST is installed on a fab tool for internal use; (3) **HVM license** — a *larger* fee at process qualification, **plus ongoing royalties "based on the number and/or sales price of MST-enabled products."** The prize is step 3: a per-wafer/per-device royalty at **near-100% incremental margin**, shielded for years by the ≈$242M NOL. The catch: **no customer has ever reached step 3.** Cumulative scorecard (Item 1A): one commercial license, four integration licenses, two JDAs — "neither of our JDAs commits the customers to take MST to production."

**Why insertion is so hard.** A new material must clear *full production qualification* — performance AND reliability AND yield AND cost — against an incumbent flow fabs are loath to disturb. Disclosed cycle times: "18 to 36 months or longer" to integrate, plus "more than an additional year" to qualify. MST also carries a real **thermal-budget constraint** (oxygen desorbs at high anneal temperatures), narrowing addressable flows, and Atomera holds **no leverage** — it owns no fab and depends on customers' tools and time.

---

### 2. Industry & competition — how this niche works and is valued

The semiconductor industry is a **$700+ billion** market (10-K). Disaggregation of design, fab and IP created room for licensors (Arm, CEVA, Rambus, Synopsys). The bull macro is real: AI infrastructure strains power efficiency, signal integrity and advanced-node manufacturability, and the industry is in a genuine materials-innovation cycle (GAA at 2nm, DRAM verticalization, RF-SOI, GaN). MST is pitched directly at those pain points.

**How specialists value pre-revenue IP licensors.** No current-multiple anchor exists; practitioners use (a) **probability-weighted royalty-ramp DCF/rNPV**, (b) a **staged real-options** lens (value rises as a customer advances integration → R&D → HVM), and (c) **comparable royalty economics**, which tie my success marks to reality:

- **Arm:** royalties ≈1–2% of chip ASP; Apple reportedly <$0.30/device.
- **CEVA:** ≈$46M royalties on ≈2.1B units in 2025 ≈ **≈2 cents/unit**; trades ≈8–12x revenue as a mature ≈$100M-revenue licensor.
- **Rambus:** royalties capped at 0.25–0.5% of ASP post-FTC; ≈$550M revenue commands a multi-billion cap (**≈8–10x sales**).

For a *materials/process* licensor pricing **per wafer**, Atomera's own illustrative ceiling is "$180/wafer ≈ 1% of an $18,000 wafer, and we would charge much less." Modeling band: **≈$50–$200/leading-edge wafer**, far less on mature/RF/power wafers.

**Realistic royalty TAM — bottoms-up, corroborated by third-party data (not the company's $450B headline):**

| Segment | Third-party annual wafer volume | Wafer ASP | Royalty $/wafer (0.3–1.0%) | One-socket royalty potential |
|---|---|---|---|---|
| TSMC N2 GAA logic | ≈1.4–1.6M/yr (≈120–130k WPM exit 2026, TrendForce) | ≈$30k | ≈$100–300 | ≈$90–425M (penetration-dependent) |
| DRAM (one maker) | industry ≈24–25M/yr (DRAM ≈2.1M WSPM, TechInsights) | ≈$5k | ≈$20–50 | ≈$45–180M |
| RF-SOI (whole segment) | ≈2–3M/yr (1.6M in 2018, AnySilicon) | ≈$2.5k | ≈$15–40 | ≈$25–105M |

So **one socket ≈ $50–80M/yr** royalties (mid-case), **multi-socket "blockbuster" ≈ $250–350M/yr** — roughly 6–9% capture of the company's ≈$4B historical TAM, internally consistent. The third-party volumes confirm the *magnitudes* I use without relying on Atomera's framing; if anything they trim my prior TSMC figure (I now use ≈1.5M, not 2M, N2 wafers).

**Competitive reality.** The "competition" is the customers' own materials teams and incumbents already in use (strained silicon, HKMG, alternative liners). MST must be demonstrably *better* on proprietary advanced structures — today largely company-asserted at 2nm. The listed peer set (Ambarella, Wolfspeed, CEVA, Rambus) is not directly comparable (those firms have real revenue); it only bounds the mature royalty multiples used above.

---

### 3. Financial analysis

| ($000s) | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---|---|---|---|---|
| Revenue | 400 | 382 | 550 | 135 | 65 |
| Operating income | (15,529) | (17,526) | (20,677) | (19,336) | (21,123) |
| Net cash from ops | (12,441) | (12,499) | (14,557) | (13,236) | (14,871) |
| Cash + investments | 28,699 | 21,184 | 12,591 | 25,778 | 19,210 |
| Shares (M) | 22.5 | 23.2 | 24.8 | 27.2 | 30.8 |

**Revenue is noise** (evaluation/MSTcad dribbles, not royalties; it *fell* to $65k in FY2025); **opex is structural** (≈$21M, ≈60% R&D); **cash burn is steady at ≈$13–15M/yr and rising** (Q1 2026 opex $6.2M, up $0.7M YoY on higher PSU stock-comp); the company **funds itself by serially issuing equity** — shares rose from 22.5M (FY2021) to ≈35.3M (Q1 2026), **+57% in five years.** A new tell: the 2026 proxy (Proposal 3) seeks to **increase authorized common stock to 95 million shares** — institutional headroom for years of further issuance.

**Liquidity / runway.** Cash was $19.2M at 12/31/2025; the company closed a **$25M registered direct offering (5.0M shares at $5.00; ≈$23.6M net) on Feb 24, 2026**, lifting net liquid assets to roughly **$36–38M** (cash $14.2M + mutual funds at Q1 2026; total common equity $40.6M). Management states this funds **"at least the next 24 months"** (into ≈early 2028); a **$50M 2025 ATM** remains open.

**Dilution, modeled from the burn.** Net liquid ≈ $37M; burn ≈ $17M/yr and climbing; runway ends ≈early 2028. To reach a year-4 realization (≈2030) the company must fund ≈2 additional years ≈ **$35–40M of fresh equity.** In *success-tilted* states that comes at higher prices (≈$5–6/share → ≈7M new shares), taking fully diluted shares from ≈38M today to **≈46–47M**. In *failure* states it raises more at lower prices (≈$2–3/share → 15M+ new shares), to **≈52–53M**. These modeled counts are the per-share denominators in Section 6.

**Balance sheet** otherwise clean: $1.3M lease debt, 19x current ratio, no goodwill. Risk is not near-term insolvency; it is **slow dilution of a non-converting story.** Fully diluted shares today ≈ **≈38M** (35.3M basic + estimated option/RSU/PSU overhang; the company's executive comp now skews to multi-year PSUs vesting on relative TSR).

---

### 4. What management said (Q3 2025 → Q1 2026 calls)

- **The STMicro failure (Q3 2025) is the pivotal disclosure.** Atomera's only commercial license (April 2023) and most mature engagement: MST delivered "significant performance improvements" but "with a corresponding reduction in device lifetime (reliability), which failed to meet all of ST's specifications." ST migrated to 300mm BCD110 and shipped it **without MST**, "no plan for a future variant that includes it" — "we no longer have a line of sight to royalty revenue at ST for this particular program." Textbook fab-insertion failure: win on performance, lose on reliability/qualification.
- **Pivot to lower-friction "MST starting wafer" structures** (RF-SOI, GaN, DRAM) because the customer "will not view the cost as a royalty" and it avoids mid-line integration — a tacit admission that mid-line royalty insertion has been the choke point.
- **The GAA / equipment-OEM channel (April 2025)** — a "strategic marketing agreement with a global leader in chip fabrication technology" (very likely Applied Materials) — is the genuinely new lever; "actively working on evaluations with 2 of 4" GAA makers.
- **Tone:** relentlessly optimistic ("business deal announcements later this year") — the same tone through a decade of non-conversion. A **securities-law investigation (Johnson Fistel, May 2026)** now circles post-ST.

---

### 5. Technology & scientific assessment, with an outside-view calibration

**Is the science real?** Yes. MST's mechanisms are independently peer-reviewed (Applied Physics Letters 2015 with SK Hynix co-authors; J. Appl. Phys. 2018 with UC Berkeley's Tsu-Jae King Liu): boron junction depth cut >50%; mobility/Gm gains confirmed to derive substantially from doping-profile control rather than strain. It is **not snake oil** — but the demonstrated benefit is the modest, doping-engineering version, not the exotic band-structure story. MST sits at **TRL ≈5–6**: validated on test chips in customer fabs, never qualified for volume.

**Outside view — the materials-insertion case histories (added).** The successful disruptive insertions of the modern era all eventually became *near-universal* — but the *how* is the crucial lesson:

| Insertion | Lab/ID → HVM | Outcome | Driver |
|---|---|---|---|
| Copper interconnect (IBM) | ≈10–15 yrs → 1997 (180nm) | Near-universal | IDM-owned fab, product pull |
| Strained-Si / e-SiGe (Intel) | several yrs → 2003 (90nm) | Near-universal at leading edge | IDM-owned fab |
| High-k metal gate (Intel) | ≈3–4 yrs from material ID → 2007 (45nm) | Near-universal ≤45nm | IDM-owned fab |

Two implications. First, **insertion timelines are multi-year** even when the physics is compelling — consistent with my 3.5–4.5-yr realization. Second, and decisively, **every winner was pulled into production by an IDM that owned the fab, bore the integration cost, and had its own product as the demand pull.** The *no-fab licensing* analogs fared far worse: **SuVolta** (deeply-depleted-channel transistors — absorbed by a licensee, never an independent royalty franchise) and **Amberwave** (strained-silicon *substrate* licensing — largely failed; embedded process-strain won instead). Atomera is structurally the SuVolta/Amberwave model, not the IBM/Intel model. This is the single most important reason to keep success probabilities moderate despite genuinely good science.

**Probabilities via a correlation-adjusted TRL-gate funnel.** Per a representative live program: silicon results → R&D license ≈60% (Atomera already holds 5 such licenses, so this gate is *easier* than generic); R&D → full qualification ≈30% (the gate ST just failed; lowered for the no-fab model); qualification → customer commercializes ≈45% → **per-program ≈ 8%.** Across ≈5 programs (RF-SOI, DRAM, GAA, power, GaN), naive independence gives 1−(0.92)^5 ≈ 34%, but the programs share the same technology, thermal-budget window and qualification physics — they are **not independent**, so the aggregate is capped at **P(any HVM production) ≈ 28–30%.** The **high-volume, model-validating** subset (a GAA/DRAM/broad-RF win that scales) ≈ **15%**; the **multi-socket blockbuster** ≈ **5%.** This externally-anchored, correlation-aware funnel is what I carry into the model.

---

### 6. Valuation — method, why it fits, and the worked numbers

**Why rNPV (and not the alternatives).** ATOM has no earnings to DCF and a $65k revenue base that voids any sales multiple. Its value is a **binary, time-distant, probability-driven payoff** plus a cash floor — exactly rNPV's domain. Each outcome is valued at the **equity value per share it would command when the outcome becomes visible** (3.5–4.5 yrs out, per disclosed cycle times and the ST precedent), then discounted to today.

**Discount-rate build-up.** Idiosyncratic technical/commercial risk lives in the **probabilities**, so the rate carries **systematic + illiquidity risk only** (no double-counting): risk-free 4.3% (10-yr UST) + β≈1.9 × ERP 5.0% (=9.5%) → 13.8% + micro-cap illiquidity/size premium ≈2.2% = **≈16% central.** Sensitivity: 14% → ≈$1.95; 16% → $1.77; 18% → ≈$1.63 — robust to the rate.

**Success-case equity values — derived from a transparent royalty-ramp DCF (circularity removed).** I show the *cash-flow-only* PV and the *market realization mark* separately, so the reader sees the judgment, not a back-solved multiple:

- *Solid* (one socket): mature royalties ≈ $70M, ≈100% incremental margin less ≈$25M opex ⇒ ≈$45M after-tax FCF (NOL-shielded early). Pure-cash-flow value: a 4-yr ramp (0 → $70M) plus a terminal Gordon (g=3%, CoE=13%) discounts to roughly **$300–340M of intrinsic cash value at the yr-4 realization date.** A just-proven, fast-ramping IP licensor does not trade at intrinsic cash value, however; CEVA/Rambus comps (≈7–10x mature royalties) imply ≈$490–700M. I take a **realization mark of ≈$450M** — *below* the comp midpoint and only modestly above the pure-DCF, an explicit, defensible judgment rather than a calibration. ÷ ≈47M shares = **$9.5/share.**
- *Blockbuster* (multi-socket / TSMC-GAA baseline): ≈$250–350M royalties ⇒ ≈$200M FCF; pure-DCF ≈$1.0–1.3B at realization, comps (≈5–6x) ≈$1.5–2.0B; **mark ≈$1.4B ÷ ≈47M = $30/share.**
- *Marginal* (a license converts but stays small, $5–20M royalties): ≈$120M ÷ ≈47M = **$2.5/share.**
- *Failure*: **built-up asset value, not assertion.** Net cash erodes to a few million by yr 4.5; the patent estate ("hundreds of issued and pending patents") consists of *method/structure* claims that are hard to detect in a finished chip and have **zero licensing/litigation proof** — the weak end of the IP market (cf. Kodak imaging ≈ $94M for ≈2,350 assets in distress vs. MIPS ≈ $700k/patent for detectable processor IP). A distress sale clears ≈$5–20M; with residual cash, **residual equity ≈ $30M ÷ ≈53M diluted = $0.55/share.**

**Probability-weighted result (central, 16%):**

| Scenario | Prob | Value if realized | Yr | PV/share | Contribution |
|---|---|---|---|---|---|
| Blockbuster | 5% | $30.0 | 4 | $16.57 | $0.83 |
| Solid | 10% | $9.5 | 4 | $5.25 | $0.52 |
| Marginal | 15% | $2.5 | 3.5 | $1.49 | $0.22 |
| Failure | 70% | $0.55 | 4.5 | $0.28 | $0.20 |
| **FMV** | | | | | **≈ $1.77/share** |

**Floor cross-check.** Built-up asset floor = net liquid assets (≈$37M) + a thin strategic-IP option ($15–40M) ⇒ ≈$40–70M, i.e., ≈$1.05–$1.85 in a *strategic* sale but only ≈$1.00 on net cash alone. I anchor the **conservative floor at ≈$1.00/share** (net cash; the IP is not a reliable cushion). FMV at ≈1.8x the floor is the option premium for a ≈30% chance of *some* conversion.

**Takeout optionality (added).** A strategic acquisition (most logically by the epi-tool OEM partner, Applied Materials/ASM) is a plausible terminal outcome — but it is **not a downside hedge.** An OEM can already license/co-market; it would only *buy* to lock exclusivity *after* MST proves commercially valuable. So a takeout is best modeled as an alternative *realization mechanism for the success branch* (capitalizing the $50–350M royalty run-rate at ≈$300M–$1B+, possibly compressing the timeline), while a *pre-adoption* takeout would clear near or below today's price (≈$30–80M distress). It is already embedded in my success/failure values; it does not add a separate, uncorrelated scenario.

**Sensitivity.**

| | Low band | Central | High band |
|---|---|---|---|
| P(any production) | 24% | 30% | 42% |
| P(high-volume) | 10% | 15% | 24% |
| Success equity values | lower | mid | higher |
| **FMV/share** | **$0.95** | **$1.77** | **$3.70** |

**Independent cross-check.** Probabilistic mature-multiple: 15% chance of ≈$110M after-tax licensing earnings (solid+blockbuster weighted) at ≈10x ≈ $1.1B, plus 15% chance of ≈$10M at ≈12x ≈ $120M, discounted ≈4 yrs at 16% over ≈47M shares ≈ $1.7–2.0 — corroborating the rNPV from a different angle.

---

### 7. Probability-weighted outcome distribution (not a bull/bear split)

One FMV = the expected PV across the full distribution, integrated above. In words: **≈70% of the probability mass is failure** (worth roughly cash, eroded by dilution); **≈15%** is a marginal conversion that barely justifies cash-plus; and the **≈15% "it works" tail** (solid + blockbuster) holds ≈75–80% of the expected value. This is a **convex, lottery-like payoff**: a small probability of a 10–30x outcome dominates the mean. Crediting that tail at its honest probability is what separates this from both perma-bear dismissal ("no revenue, worthless") and narrative over-payment ("AI + TSMC = moonshot"). The wide $0.95–$3.70 band is not a hedge; it is the true central spread of a genuinely binary outcome set.

---

### 8. Risks & what would change my mind

**Risks (downside):** (1) the modal (≈70%) outcome is non-conversion and slow, price-dilutive raises (authorized share count headed to 95M); (2) ST-style reliability/qualification failures recur at the decisive gate; (3) customers hold all leverage and Atomera no fab — the structurally disadvantaged no-fab insertion model (cf. SuVolta/Amberwave); (4) thermal-budget/integration constraints; (5) dilution at depressed prices in weak states; (6) the live securities investigation; (7) single-technology, key-person concentration.

**What would raise my FMV materially:** a *signed HVM license with a named Tier-1 customer* (not a JDA/evaluation); an independently-validated 2nm GAA diffusion-blocking result; conversion of an RF-SOI or GaN starting-wafer customer to production royalties; or the equipment-OEM partner committing reactor co-development with a volume customer (which would also raise takeout odds). Any one shifts mass from "failure" to "solid/blockbuster" and could double-plus the FMV.

**What would lower it:** another flagship engagement collapsing at qualification; an accelerated/again-discounted raise; or evidence MST's advantage does not hold at advanced nodes.

---

### 9. Reconciliation to market price & rebuttal of the bull narrative

Valued independently the FMV is ≈$1.80. The shares trade around **$7.6**, with a sell-side target near **$10**. What probability of success is *embedded* in those prices?

- My **high band** (P(any production) 42%, P(high-volume) 24%, richer marks) already produces only **$3.70.** To reach **$7.6** you must push P(high-volume) toward ≈40%+ and/or the blockbuster weight into the mid-teens — i.e., assume the company is *more likely than not* to land a scaling socket within a few years. To justify **$10** you need the "solid" outcome approaching a coin-flip *plus* a meaningful blockbuster weight — an **implied P(high-volume success) of roughly 40–50%, about 2.5–3x** the correlation-adjusted funnel, the 10-year zero-royalty record, the just-failed ST qualification, and the poor historical record of *no-fab* materials-insertion plays.
- The bull case rests on three true things — credible peer-reviewed science, many shots on goal, and a real AI/GAA materials tailwind plus the new equipment-OEM channel. I credit all three; they are *why* the FMV is ≈1.8x cash rather than at the floor. But "true and promising" is not "probable and imminent." The decisive datum is that the most mature, Tier-1, multi-year engagement **failed at exactly the gate that matters** and got orphaned by a node migration — the pattern that has kept royalties at zero for a decade.

Conclusion: at ≈$7.6 the market pays ≈4x my probability-weighted intrinsic value and prices an implied success probability the public record does not yet warrant. My fair value would converge toward the market only upon a concrete, named HVM conversion — the catalyst to watch, not assume.

---

### 10. Conclusion

Atomera is a scientifically credible, commercially unproven, perpetually cash-consuming option on the semiconductor materials cycle — and, structurally, a *no-fab licensing* play of the kind that has historically struggled to capture value even when its science was sound. Valued correctly — as a probability-weighted bundle of future royalty outcomes over a hard net-cash floor, with success values derived from a transparent royalty-ramp DCF, probabilities anchored by a correlation-adjusted TRL-gate funnel and an explicit outside view (Cu/SiGe/HKMG vs. SuVolta/Amberwave), and a built-up IP floor — its **fair market value is about $1.80/share** (model $1.77), within a **confidence band of roughly $0.95–$3.70**, on a **no-growth floor of about $1.00.** The headline is overwhelmingly option value: a ≈15% chance that "it works" carries the mean against a ≈70% chance that a decade of non-conversion continues. My conviction in the *framework* is high; in the *point estimate*, appropriately modest given the binary nature of the bet — which is why the answer is a distribution with a ≈$1.80 expected value, well below the ≈$7.6 market price and ≈$10 street target, both of which embed an implied probability of success the public record does not yet justify.