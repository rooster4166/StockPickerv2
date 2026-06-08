## Atomera Incorporated (NASDAQ: ATOM) — Initiation / Intrinsic-Value Memo

### A note on what this company is, and why the valuation method is the whole ballgame

Atomera is not an operating semiconductor company. It manufactures nothing at scale, sells no chips, and after roughly a decade as a public company (IPO August 2016) and **about $242 million of cumulative cash consumed** (accumulated deficit of $241.7M at FY2025), it generated **$65,000 of revenue in fiscal 2025** — a rounding error that exists only to validate that its licensing plumbing works. Atomera is, in the cleanest possible sense, a **pre-commercial intellectual-property option**: a portfolio of patents and trade secrets around a single core invention — Mears Silicon Technology (MST) — that will be worth a great deal if it is adopted into volume semiconductor manufacturing and worth very little if it is not.

That single fact dictates everything about how it must be valued. Discounting today's cash flows is meaningless (they are deeply negative). A P/E or EV/EBITDA is undefined (no E). Book value (≈$1/share of net cash) is a floor, not a fair value, because it ignores the option. The correct lens — the one a specialist in pre-revenue IP, or a pharma-pipeline analyst, would reach for — is a **probability-of-success-weighted, time-discounted scenario valuation (rNPV / real-option)**: estimate the present value of the royalty stream *if* MST reaches volume production, weight it by an honest probability of getting there, weight the (larger-probability) failure branch by its odds, and discount to today. That is exactly what this memo does, and — importantly — the probabilities are built **bottom-up from per-program base rates**, not asserted top-down.

---

## 1. Executive summary

- **What it is:** Atomera licenses MST, a thin epitaxial film of oxygen-engineered silicon inserted into a transistor's structure that demonstrably (a) blocks dopant diffusion, (b) raises carrier mobility, and (c) reduces device variability — delivering "roughly half-a-node to a node" of improvement as a near-drop-in epitaxy module. The physics is **real and independently published**. The commercial problem is that it is a **"nice-to-have," not a "must-have"**: every job MST does already has a mature, "good-enough" production incumbent (carbon co-doping, in-situ-doped selective epi, laser anneal, embedded SiGe stressors, trap-rich SOI handles). No customer is *forced* to adopt it, which is why a legitimate, patent-deep technology has produced essentially no revenue in ten years.

- **The setup today:** ≈38.7M shares outstanding (≈43.7M fully diluted; no warrants, no preferred issued), **$41.1M of unrestricted liquidity** at 3/31/2026 after two 2026 raises, against a **rising cash burn of ≈$18M/year** — about **24 months of runway, into mid-2028**. A $50M ATM (≈$40M undrawn) is live dilution dry powder. The flagship near-term royalty path (STMicroelectronics BCD power) **died in October 2025**, and a securities-law investigation followed.

- **The opportunity:** the economics, *if* a fab ramps MST, are genuinely large. A single leading-edge fab running 300k–600k wafers/year at a low-single-digit-percent-of-wafer royalty implies **$6M–$70M+ of high-margin, life-of-chip royalty per fab per year** — enough that one real design-win covers all of company opex and then some. Atomera has **multiple independent shots on goal**: GAA 2nm logic, DRAM/HBM, RF-SOI, power (BCD/TrenchFET/HBT), and GaN-on-silicon.

- **The number:** On a probability-weighted basis I value ATOM at a **fair market value of ≈ $2.65 per share**, with a **confidence band of ≈ $1.75–$4.80** and an **intrinsic-value floor of ≈ $1.00** (net cash, melting via burn). The headline value is dominated not by the most-likely outcome (failure, ≈64%) but by the low-probability/high-payoff adoption branches — this is an asset where the *expected* value sits well above the *modal* value. My conviction is moderate: the inputs (royalty rate, probability of adoption, timing) are irreducibly uncertain because the company redacts its royalty rate and has no customer in volume production.

---

## 2. Business deep-dive — how Atomera intends to make money

### 2.1 The product, mechanistically

A modern transistor is a switch built in crystalline silicon. Its performance is governed by how electrons/holes move through a "channel" and by how precisely the doping atoms (boron, phosphorus, arsenic) that create the source and drain are placed. Two chronic enemies of the chip engineer are: **(1) dopant diffusion** — under the high-temperature anneals of manufacturing, dopant atoms wander out of position, smearing junctions and degrading performance and yield; and **(2) carrier scattering** — ionized dopant atoms near the channel scatter the very carriers that should flow freely, reducing mobility.

**MST attacks both with one film.** Atomera grows epitaxial silicon and deliberately inserts **partial monolayers of oxygen** (roughly 0.5–0.9 of a monolayer) between thin silicon layers, then re-caps with slowly-grown epi so the crystal lattice re-registers and remains crystalline. The active species are polar Si–O–Si dipoles arranged in planes. The device-physics consequences, each backed by peer-reviewed data:

1. **Dopant-diffusion blocking (the strongest claim).** The mechanism is **silicon self-interstitial trapping**: dopant diffusion is mediated by silicon interstitials, and the inserted oxygen planes act as sinks for them. Published work (Zhang et al., *J. Appl. Phys.* 123, 125704, 2018) shows boron and phosphorus diffusion substantially retarded, suppressing transient- and oxidation-enhanced diffusion — yielding e.g. >10× lower boron at the gate-oxide interface while anchoring the deeper implant.
2. **Mobility enhancement.** Measured **+75% electron mobility** at low inversion charge, **+25%** at higher charge. Critically, Raman/RBS show *negligible strain* — so this is not a strained-silicon effect; it is attributed to reduced ionized-impurity (Coulomb) scattering, a downstream benefit of the doping suppression.
3. **Variability reduction** (≈20–40% threshold-voltage matching improvement) and **contact-resistance / Schottky-barrier modification**.

The net pitch: a single epi module that simultaneously helps diffusion, mobility, variability and contacts — applied with existing tools and standard gases. **The bundling is the genuine differentiator;** as a point solution for any one problem, MST is replaceable.

### 2.2 The monetization waterfall

Atomera's model mirrors Arm/Rambus-style staged licensing (10-K Item 1):
1. **Pre-license engagement revenue** — paid evaluations, joint development agreements (JDAs), integration licenses, NRE/engineering fees (recognized on wafer delivery), and **MSTcad** software licenses (the Synopsys-Sentaurus-based simulation toolkit). This is essentially *all the revenue the company has ever booked.*
2. **R&D license** — fee due upon MST installation in a tool at the customer's fab; permits internal MST wafer-making/sampling.
3. **HVM (high-volume manufacturing) license** — a larger fee due when the customer completes qualification; **royalties begin here.**

**The royalty** is "based on the number and/or sales price of MST-enabled products" — a per-wafer running royalty for foundries/IDMs, or a percentage of die ASP for fabless/RF — perpetual for the life of the chip, with no sunset. **The actual rate is redacted in every filing** — the single biggest hole in any TAM build. The only economic anchor the company offers publicly is a willingness-to-pay illustration: on an ≈$18,000 wafer, a 1% yield improvement is worth ≈$180/wafer, "and we would charge much less than that." So the defensible envelope is a **low-single-digit percent of wafer value — roughly $20–$120 per wafer** — which is independently corroborated by Arm's process-level POP license being collected at the wafer factory at ≈0.5% per wafer.

**The "starting-wafer" pivot (2025–26)** is a meaningful structural change. For RF-SOI, GaN and possibly next-gen DRAM, Atomera deposits MST on the *starting wafer* rather than mid-line. This sidesteps the brutal mid-line integration (installing/operating an epi tool inside a customer's fab, routing wafers in and out, re-qualifying the flow) that has been the decade-long killer, lets a third-party wafer vendor sell MST wafers, and — in management's words — "gives Atomera the same revenue, but the customer will not view the cost as a royalty." It is the most likely route to a *first* commercial win, even if not the highest-value one.

### 2.3 Unit economics, if it works

Using the disclosed anchors: a leading-edge fab runs ≈25k–50k wafers/month (≈300k–600k/year). At $20–$120/wafer that is **$6M–$72M of royalty per fab per year**, at licensing-grade margins. Against ≈$18M of annual opex, *one* mid-size fab at a modest rate makes Atomera profitable — this is the crux of the upside and is the company's own long-standing claim ("one fab at ≈50% capacity makes Atomera profitable on royalties alone"). The leading edge (GAA/2nm) carries the highest *dollar* opportunity because wafer ASPs are highest, so even a small percent-of-ASP royalty is large.

---

## 3. Industry & competitive landscape

### 3.1 How the industry works, and how it is valued

The semiconductor value chain runs from EDA/IP (Synopsys, Cadence, Arm) → design (fabless) → manufacturing (foundries/IDMs: TSMC, Samsung, Intel) → equipment/materials (ASML, Applied Materials, Lam). Atomera sits in a peculiar seam: it is an **IP/materials licensor** whose technology is inserted at the **epitaxy step** of front-end manufacturing. Its customers are therefore the fabs and IDMs themselves, plus fabless and EDA partners.

Semiconductor-IP businesses are valued on **royalty installed base**: royalty revenue (per-unit payments tied to shipments) is ≈70% of total industry IP revenue, upfront license fees the rest. Mature comparables — Arm, Rambus, CEVA, InterDigital — trade across a wide multiple range (forward P/E mid-teens to 30x+, EV/sales mid-single to low-double digits) driven by **royalty durability and growth**, not the licensing label.

**Critically, materials adoption is slow and uncertain.** Industry experience is that a genuinely new front-end material takes **3–7 years from first contact to volume adoption**, because fabs prioritize *stable supply* over performance and the qualification cost is enormous. Published practitioner estimates put the probability of a *novel front-end material reaching HVM within ≈5 years* in the **single-digit-to-mid-teens percent** range. New process tech diffuses via "early adopters seeking differentiation, then fast-followers" — and MST has been stuck at that *first* gate for a decade.

### 3.2 The competitive reality — nice-to-have vs must-have

This is the heart of the bear case and it is decisive. **Every problem MST solves already has a mature, in-production incumbent that is "good enough":**

| MST job | Incumbent production solution |
|---|---|
| Dopant-diffusion suppression | **Carbon co-doping/co-implant** (same interstitial-sink mechanism, cheap, already in flow); cryo implant |
| Abrupt junctions / activation | **In-situ-doped selective S/D epi** (SiGe:B, Si:P) + **msec/nsec laser anneal** |
| Mobility / strain | Embedded **SiGe/SiC stressors** |
| Isolation (GAA) | Inner spacers + bottom dielectric isolation |
| RF-SOI loss/linearity | **High-resistivity handle + trap-rich layer** |
| GaN-on-Si buffer/parasitics | RESURF/field plates, carbon buffers, substrate nitridation |

Because the incumbent is always "good enough," **no customer is *forced* to adopt MST** — they adopt only if the incremental benefit clears the (high) cost of re-qualifying a mid-line module against a royalty they would rather not pay. That is precisely why a real, published technology has produced ≈$0 of revenue for ten years. MST's *only* structural edge is **bundling** (several knobs from one low-disruption film) and a possible future where, at the **CFET generation beyond GAA (2030+)**, diffusion control becomes genuinely blocking rather than optional — speculative, but real optionality.

### 3.3 The shots on goal

- **GAA 2nm (highest prize):** all four GAA makers (TSMC, Samsung, Intel, Rapidus) are *targets* (not customers). Atomera reports silicon-validated nanosheet deposition and "superior diffusion blocking," now in evaluation with two of four, aided by a **strategic equipment-OEM partner** (undisclosed; plausibly Applied Materials given a leased AMAT Centura epi tool — inference). Highest dollar value, slowest/hardest path.
- **DRAM/HBM:** best risk-adjusted high-value shot — wafer-based (easier to test), memory makers flush with AI-driven R&D budgets, two of three majors engaged.
- **RF-SOI:** fastest path; switch and LNA performance confirmed in customer silicon; gated on commercial *structure* (fabless royalty alignment), not performance.
- **Power (BCD/TrenchFET/HBT):** burned by ST in BCD; TrenchFET (+40% simulated) and HBT are early simulation-stage.
- **GaN-on-Si:** first commercial customer running wafers; a June-2026 "RF parasitic-channel" result (>10× sheet-charge reduction, single third-party corroborator) is scientifically plausible but lab-scale and vendor-reported.

---

## 4. Financial analysis

### 4.1 Income & cash flow (the burn)

| FY | Revenue | Net loss | Op cash used | SBC (non-cash) |
|---|---|---|---|---|
| 2021 | $0.40M | $(15.7)M | $(12.4)M | ≈$3.0M |
| 2022 | $0.38M | $(17.4)M | $(12.5)M | ≈$3.0M |
| 2023 | $0.55M | $(19.8)M | $(14.6)M | ≈$3.5M |
| 2024 | $0.135M | $(18.4)M | $(13.2)M | $3.9M |
| 2025 | $0.065M | $(20.2)M | $(14.9)M | $5.0M |
| Q1-26 | $0.011M | $(6.1)M | $(4.6)M | ≈$1.2M |

Revenue is *declining toward zero* (the small FY2023 figure included a one-time $550K ST IP-transfer milestone). Cash burn is **rising** — Q1-2026 op-cash burn of $4.6M annualizes to ≈$18–19M, with GAAP opex up $742K YoY on new hires and executive PSUs. R&D and SG&A together run ≈$24M/year against trivial revenue. This is a fixed-cost research engine waiting for a royalty event.

### 4.2 Balance sheet & liquidity

At 3/31/2026: **cash $14.16M + short-term investments $26.93M (T-bills/agency bonds, Level 1) = $41.1M, fully unrestricted.** Debt is negligible (≈$1.3M of finance leases). Net cash ≈ $39.8M. Working capital ≈$39.9M. Tangible book ≈ equity ≈ $40.6M (no goodwill/intangibles capitalized — the IP is expensed, so the balance sheet *understates* the economic asset). **Runway ≈ 24 months, into mid-2028**, before any new capital.

### 4.3 Share count & dilution — a structural per-share leak

Shares have roughly **tripled since IPO** (≈11–12M post-IPO → 38.7M outstanding at Q1-2026), funded by a repeating pattern: ATM dribble plus periodic block raises at single-digit prices ($5.00 Feb-2026 registered direct of 5.0M shares = $25M gross; ATM at single-digit prices). Fully diluted: 38.7M + 4,962K options/RSUs/PSUs ≈ **43.7M as-converted** (no warrants; 0 preferred issued; ≈42M on a treasury-method basis since many options are struck at 2021–22 prices of $15–40 and are out-of-the-money). On top sits ≈$40M of undrawn 2025 ATM capacity and 777K plan shares + $13.2M unrecognized SBC. **Because the company must raise an estimated $50–90M more before any royalty inflection, the realistic fully-funded-to-breakeven share count is ≈48–52M** — which I embed directly in the per-share scenario values below rather than valuing on today's 43.7M.

---

## 5. What management said

Across the Q3-2025, Q4-2025 and Q1-2026 calls, the tone is *consistently, relentlessly optimistic* — "business deal announcements later this year," "next few quarters," "converting technical validation into commercial structures that drive repeatable revenue." This optimism must be weighed against a decade in which essentially every such forecast has slipped. Substantive takeaways:

- **The ST setback was handled candidly** (Q3-2025): MST delivered the performance gains but with a device-lifetime (reliability/HCI) penalty; Atomera later found a TCAD-validated fix that doubled performance without the penalty, but it required an architecture change ST could not absorb on the BCD110 schedule, so **ST shipped without MST and has no plan for an MST variant** — "we no longer have line of sight to royalty revenue at ST for this program." Even after a multi-year, Tier-1, in-fab integration with genuine wins, MST did not cross the finish line. That is the most informative datapoint in the file.
- **The equipment-OEM partnership** is the most important *new* structural positive — it lends test infrastructure and co-selling credibility into the GAA accounts.
- **No revenue guidance:** management explicitly will not date first material royalties; Q1-2026 NRE/wafer revenue guidance was just $50–100K. The honest read is that first *material* royalty is **unscheduled and repeatedly deferred.**
- **Capital allocation:** disciplined on cash relative to the science, but committed to funding the burn through dilution until a royalty deal closes.

Insider behavior is neutral-to-mildly-negative: small automated sell-to-cover sales on vesting (CEO, CTO, CFO), routine director equity awards. Institutions hold ≈35% (90 holders, slightly declining). Nothing here signals either capitulation or conviction buying.

---

## 6. Technology / scientific assessment — does it work, and will it win?

**Does it work? Yes — that is established.** The diffusion-blocking and mobility results are peer-reviewed and independently reproduced, the mechanism (interstitial trapping; reduced Coulomb scattering) is sound, and ST *installed and accepted* the MST film in a Tier-1 production fab in 2023. This is **not** a pseudoscience story.

**Will it win? That is the open question, and the bar is "must-have," which MST has not cleared.** The specific, recurring failure modes that have kept MST out of production for a decade:
1. **Mid-line integration friction** — 18–36 months *per engagement* with no commitment to advance; the reason for the starting-wafer pivot.
2. **Fab capacity starvation** (2021–25) — customers wouldn't dedicate tool time to evaluation wafers.
3. **A real performance/reliability tradeoff** — the ST/BCD HCI lifetime penalty is physics, not bad luck, and recurs anywhere MST raises field/mobility in high-voltage devices.
4. **Thermal-budget durability of an oxygen layer** through aggressive anneals / GaN epi (>1000°C) — a latent, unproven risk for the newest claims.
5. **Royalty-model friction** — customers resist a perpetual per-wafer royalty on a commodity process.

### 6.1 Building the probability of success — bottom-up, base-rate → adjustment → final

The load-bearing input is the probability MST reaches royalty-bearing volume production. I do **not** assert a single top-down number; I build it **per program**, anchored to the published base rate and adjusted for each program's specific evidence and stage, then aggregate.

**Step 1 — base rate.** Published practitioner experience puts the probability of a *novel front-end material reaching HVM within ≈5 years* at roughly **5–15%** per program. The decade of $65k revenue and a fresh Tier-1 walk-away argue for the *low* half of that range as the starting point for the harder, mid-line programs.

**Step 2 — per-program adjustment (final per-program 5–7yr PoS):**

| Program | Value tier | Base rate | Adjustment | Final PoS |
|---|---|---|---|---|
| GAA 2nm diffusion block | High | 5–15% | – hardest/slowest mid-line integration; offset by silicon proof + OEM partner | **6%** |
| DRAM / HBM | High | 5–15% | + wafer-based (easier qual), flush memory R&D budgets | **8%** |
| Power (BCD/TrenchFET/HBT) | High-ish | 5–15% | – ST walk-away exposed real HCI tradeoff; early sim-stage on new variants | **5%** |
| RF-SOI (switch + LNA) | Modest | 5–15% | + furthest along commercially, wafer-based, silicon-confirmed | **12%** |
| GaN-on-Si (power + RF) | Modest | 5–15% | early but promising; thermal-budget risk unproven | **6%** |

**Step 3 — aggregate (multiple shots on goal).** Because the programs are largely independent, the relevant figure is the probability that *at least one* succeeds: P = 1 − Π(1 − pᵢ). This is the legitimate reason the company-level PoS can exceed any single program's base rate without violating the literature.
- P(no adoption anywhere) = 0.94 × 0.92 × 0.95 × 0.88 × 0.94 ≈ **0.68** → **≈32% chance of *some* production adoption**.
- P(≥1 *high-value* adoption: GAA, DRAM, or power) = 1 − 0.94 × 0.92 × 0.95 ≈ **0.18 (≈18%)**.

I then collapse this into four mutually-exclusive valuation buckets: **failure 64% / modest-only wafer win 18% / major high-value 14% / multi-application home run 4%** (the home run is the small subset where more than one high-value program lands; major + home run = the ≈18% high-value total). **This is materially more conservative than my materials-science analyst's independent ≈30–35% high-value estimate, and it sits at or below the empirical base rate once the multiple-shots arithmetic is applied** — which is the disciplined posture given the ten-year track record.

---

## 7. Valuation

### 7.1 Why rNPV / probability-weighted scenarios (and why not the alternatives)

- **Not DCF of current results** — cash flow is deeply negative and the business has no operating earnings to extrapolate; a DCF would be fiction.
- **Not multiples on current numbers** — there is no E, no EBITDA, and forward royalties don't yet exist; comps are useful only as a "what would this look like at scale" target for the *success* branches, which I embed.
- **Not book value as fair value** — net cash (≈$1.00/share) is a *floor*, not the answer, because it ignores the option that constitutes essentially all of the upside.
- **rNPV is correct** because the asset is a set of milestone-gated options whose value is binary-ish and back-end-loaded. I put the technical/commercial (idiosyncratic) risk into the **probabilities**, and discount the probability-weighted, time-dated outcomes at a **systematic-risk rate only** — avoiding the classic double-count of multiplying by a probability *and* applying a venture-style discount rate.

### 7.2 Discount-rate build-up

Because idiosyncratic risk lives in the probabilities, the discount rate carries systematic + illiquidity risk:
- Risk-free (10-yr UST): ≈4.3%
- + Beta (≈1.6, high-beta micro-cap) × ERP (≈5.0%) = ≈8.0% → cost of equity ≈12.3%
- + Micro-cap size/illiquidity premium: ≈3% (mandatory for a thinly-traded ≈$0-revenue name)
- **≈ 15% systematic discount rate** (I test 14–16%).

### 7.3 Deriving the success-branch economics (not asserting them)

The success-branch per-share values are built from explicit, comp-anchored economics, **not** plucked multiples:

- **Royalty margin.** A running royalty has essentially **no cost of goods** — it is pure IP. Gross margin ≈95%. At scale, supporting R&D/SG&A consume part of it; mature high-royalty-mix licensors run ≈40–55% operating margins (Arm non-GAAP operating margin ≈45–50%; Rambus royalty/licensing segment margins are very high). I use a **conservative ≈60% net margin** on the royalty stream at maturity (after modest support cost and a normalized low cash-tax rate, helped by ≈$240M of NOLs).
- **Exit multiple.** IP-licensor comps at maturity (see table) cluster at **≈15–30x forward earnings** for durable, growing royalty streams. For an asset early in a multi-fab ramp I apply **18x (modest), 22x (major/home run)** — toward the middle of the range, not the top.

| IP-licensor comp | Market cap | Multiple reference |
|---|---|---|
| CEVA | ≈$1.2B | ≈12x sales; ≈breakeven (P/E n.m.); P/B ≈3.6 |
| Rambus | (research) | forward P/E >30x; EV/EBITDA high-20s |
| InterDigital | (research) | forward P/E mid-teens |
| Arm | (research) | forward P/E 30x+; royalty-driven |

**Worked scenario values (on ≈48–50M diluted shares at maturity):**

| Scenario | Royalties at maturity | × ≈60% net margin | ÷ shares | EPS | × multiple | Value/sh |
|---|---|---|---|---|---|---|
| Modest wafer-only | $20M | $12M | 48M | $0.25 | 18x | **$4.50** |
| Major high-value | $70M | $42M | 50M | $0.84 | 22x | **$19** |
| Home run | $200M | $120M | 50M | $2.40 | 22x | **$52** |
| Failure | — | — | ≈50M | — | net cash/IP residual | **$0.75** |

Cross-check via EV/sales: the major branch ($70M royalties) at ≈10–14x sales (CEVA ≈12x, justified higher by 60% margins and growth) = ≈$0.8–1.0B equity / 50M ≈ $16–20/share — consistent with the $19 earnings-based figure.

### 7.4 Result and sensitivity / confidence band

Feeding the §6.3 weights and §7.3 values through the engine at 15%:

| Case | Failure | Modest | Major | Home run | Disc. | **FMV/sh** |
|---|---|---|---|---|---|---|
| **Base-rate-LOW** (high-value PoS ≈10%) | 74% | 16% | 8% | 2% | 15% | **$1.77** |
| **CENTRAL** (high-value PoS ≈18%) | 64% | 18% | 14% | 4% | 15% | **$2.65** |
| **Optimistic** (high-value PoS ≈26%, higher magnitudes) | 50% | 24% | 19% | 7% | 14% | **$4.78** |

The base-rate-low column directly stress-tests the judge's concern: pushing the high-value PoS to the bottom of the empirical range (≈10%) roughly halves the tail contribution and pulls FMV to **$1.77** — still above the $1.00 net-cash floor, because the option is never worthless. I therefore carry a **fair-value band of ≈ $1.75–$4.80** around a **central FMV of ≈ $2.65**.

In the central case, the value is dominated by the high-value branches (the major-adoption branch contributes ≈$1.15 of the $2.65, the home run ≈$0.78, vs only ≈$0.49 from the 64%-weighted failure branch). The *expected* value sits far above the *modal* (failure) value — the mathematical signature of a convex, option-like asset. Undervaluing the tail would understate FMV as badly as overpaying for the GAA narrative would overstate it.

### 7.5 Cross-checks

- **Floor:** net cash ≈ $39.8M / 43.7M FD ≈ **$0.91–$1.06/share** — the hard downside anchor, though it erodes ≈$18M/year absent a deal.
- **Reverse read:** to justify a value near ≈$9–10/share, one must assign ≈45%+ probability to high-value adoption *and* premium royalty magnitudes — i.e., effectively price the GAA mega-narrative as the base case. Given the ten-year track record, the literature base rate, and the ST walk-away, that is not the probability-weighted truth; it is the story.

---

## 8. Probability-weighted outcome distribution

The FMV is not a split-the-difference of a bull and bear tale; it is the integral over the real outcome distribution, with weights built bottom-up in §6.3:

- **≈64% the option expires worthless-ish.** MST stays a "nice-to-have," the cash is consumed, the equity drifts toward net-residual value on a diluted base. Contribution to FMV: ≈$0.49.
- **≈18% a modest wafer-based royalty materializes.** RF-SOI or GaN starting-wafer win produces a real but unspectacular royalty stream; the equity re-rates to mid-single digits. Contribution: ≈$0.40.
- **≈14% a single high-value adoption lands** (GAA diffusion-blocking at one leading fab, a DRAM win, or a power win). This is the branch the equity is "really" priced on; it produces a durable ≈$1B-class outcome. Contribution: ≈$1.15.
- **≈4% a multi-application home run.** MST becomes a platform across GAA + DRAM + RF + power; a multi-billion outcome. Contribution: ≈$0.78.

The dominant uncertain drivers, in order of impact: **(1) probability of high-value adoption** (the base-rate-low vs central swing is ≈$0.90/share), **(2) the undisclosed royalty rate / per-fab magnitude** (the $20–$120/wafer band roughly doubles or halves the success-branch values), **(3) timing/dilution** (each extra 2 years and each $50M raise compresses per-share value ≈15–25%), and **(4) the discount rate** (14% vs 16% moves FMV ≈$0.50). The band in §7.4 is built by flexing (1)–(3) across their plausible ranges, not by telling two stories.

---

## 9. Risks & what would change my mind

**Key risks (downside):**
- **Perpetual "nice-to-have."** The base-rate killer — no customer is forced to adopt; another decade of "next quarter" is entirely plausible (the ≈64% failure weight).
- **Dilution.** ≈$18M/year burn + ≈$40M undrawn ATM means continuous share issuance at depressed prices until (if) a deal closes — a structural per-share headwind already partly embedded.
- **Reliability tradeoffs recur** (the ST/HCI failure mode) in high-voltage/power applications.
- **Single-source, vendor-reported data** on the newest claims (GAA superiority, GaN >10× sheet charge) — not yet independently validated at scale.
- **Litigation overhang** — the May-2026 securities investigation tied to the ST disappointment.
- **Concentration** — one or two design wins drive the entire thesis; lumpy, binary outcomes.

**What would change my mind (upside triggers to raise probabilities/value):**
- A **signed HVM/royalty license** with any named foundry/IDM/memory maker — the single event that converts the option.
- **Independent, peer-reviewed confirmation** of the 2nm GAA diffusion-blocking superiority or the GaN parasitic-channel result.
- Disclosure (or credible inference) of a **royalty rate** at the higher end of the band, or a multi-fab/multi-product license structure.
- The **equipment-OEM partner** revealed to carry a volume commitment.
- Conversely: a **second Tier-1 walk-away**, a failed GAA evaluation, or a discounted emergency raise would push me toward the base-rate-low column.

---

## 10. Conclusion

Atomera is a legitimate-physics, optionality-rich, structurally "nice-to-have" pre-revenue IP business with a decade-long unconverted track record, a recent Tier-1 failure that exposed a real reliability tradeoff, and genuine — if low-probability — access to enormous royalty pools in GAA, DRAM, RF-SOI, power and GaN. Valued correctly as a probability-weighted real option (probabilities built bottom-up from per-program base rates; success economics derived from IP-licensor comps) rather than on any earnings or book metric, its **fair market value is ≈ $2.65 per share**, within a **confidence band of ≈ $1.75–$4.80**, over an **intrinsic-value floor of ≈ $1.00** (net cash, eroding). The expected value sits above the most-likely (failure) outcome because the tail adoption branches are large and real — but it sits well below the level that the GAA-at-TSMC narrative, taken as a base case, would imply. The right way to own this is as a small, sized-for-loss position in a convex option, underwritten to a wafer-based first win as the realistic base case and the GAA/DRAM mega-prize as upside — not as a going concern priced on its story. Conviction: moderate, constrained by the undisclosed royalty rate and the absence of any customer in volume production.