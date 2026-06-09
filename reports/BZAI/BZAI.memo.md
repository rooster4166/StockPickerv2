> **Market price (joined post-analysis): $1.73**  ·  Engine FMV: $0.36  ·  Implied: -79% (OVERVALUED)  ·  Floor: $0.25
>
> *The analysis below is PRICE-BLIND; this one-line header is a deterministic post-hoc comparison the engine never saw.*

---

# Blaize Holdings, Inc. (NASDAQ: BZAI) — Initiation of Coverage

### A fraud-flagged, going-concern, pre-scale edge-AI chip company; the value is an option, not an earnings stream

**Fair market value (probability-weighted): about $0.36 per share · Confidence band: about $0.23 – $0.57 · Intrinsic (asset/liquidation) floor: about $0.25 — and melting · Method: probability-weighted, time-discounted scenario analysis (rNPV) with base-rate-anchored weights, cross-checked against asset value and edge-AI M&A comps.**

---

## 1. Executive summary

Blaize designs the **Graph Streaming Processor (GSP)**, a genuinely novel edge-AI inference architecture, and sells it as system-on-modules, PCIe/EDSFF accelerator cards, and a no-code software stack (AI Studio / Picasso / NetDeploy). It went public in January 2025 via merger with BurTech Acquisition Corp. at a $1.2 billion enterprise value. On paper, FY2025 was a "breakout": revenue rose about 20x, from $1.55M in FY2024 to $38.6M. Strip the surface and a very different company appears, and it is the one a capital allocator must underwrite.

The investigation produces five load-bearing conclusions:

1. **The 2025 growth is low-quality and contested.** About **88% of FY2025 revenue came from two newly-formed China counterparties** — NeoTensr (61%) and Starshine (27%) — recognized as **third-party GPU-server resale at roughly 10-16% gross margin**, not proprietary chip sales. NeoTensr was incorporated on December 22, 2025 with about $2M of capital, yet was booked for over $20M of revenue in the final weeks of Q4. Starshine had paid only $1.6M of an $8.8M receivable. Short-sellers (Pelican Way, White Diamond, Ragnarok) allege both are shells; at least six plaintiff firms opened **securities-fraud investigations** in May-June 2026. The about 10% gross-margin signature alone proves the revenue was distributor-grade pass-through, independent of how the fraud claims resolve.

2. **The silicon is real but uncompetitive.** The GSP is an authentic third architectural path (depth-first, hardware-scheduled graph dataflow), but on the one metric the edge market buys on — energy efficiency — Blaize delivers **about 2.3 TOPS/W on Samsung 14nm versus Hailo's about 10 TOPS/W on TSMC 16nm**, roughly 4x behind the leading pure-play and level with a 2019-vintage Google Coral. At 16 TOPS absolute, it is an order of magnitude short of where transformer/LLM edge workloads have moved. The "hybrid GSP-plus-GPU rack-scale" pivot is a tacit admission the chip cannot carry modern GenAI workloads.

3. **The balance sheet is a melting ice cube.** Pro-forma cash is about $66M (the $33.2M at 3/31/2026 plus the about $32.8M May 2026 raise), against **$15-20M/quarter cash burn** and a formal **going-concern qualification**. There is **no ATM, no equity line, and no debt facility** — every future raise is a discrete, price-damaging event. Funding the next 24 months requires about $120-160M of new capital, implying **about 65% dilution** (to roughly 235M shares).

4. **This is therefore not an earnings story or a clean-multiple story — it is a binary option.** A DCF of reported revenue would be valuing fabricated-quality cash flows; a revenue multiple would be applied to suspect revenue. The correct frame is the **probability-weighted present value of discrete outcomes**: wipeout, marginal heavily-diluted survival, strategic acquihire of the IP/team, and a low-probability genuine commercial scale.

5. **The probability-weighted fair value is about $0.36/share**, with an asset/liquidation floor of about $0.25 that itself erodes with every quarter of burn. The distribution is downside-skewed: a roughly one-third chance of near-total loss is balanced by a fat, but not dominant, acquihire/survival tail anchored by a strategic cap table (Denso, Mercedes-Benz, Samsung) and edge-AI M&A comps (NXP-Kinara at $307M cash; Meta's rejected about $800M for FuriosaAI; AMD's team-only absorption of Untether).

The asymmetry is poor unless the revenue-quality questions resolve cleanly in Blaize's favor — and even then, the dilution math caps the upside for today's holder.

---

## 2. Business deep-dive

### 2.1 What Blaize is trying to be

Blaize, founded in 2010 in El Dorado Hills, California, builds **programmable, energy-efficient inference silicon for the edge** — the layer of AI compute that runs trained models locally on cameras, vehicles, drones, kiosks, and edge servers rather than in a distant cloud. Its products serve three stated markets: automotive, smart vision, and enterprise edge computing. It went public in January 2025 via a de-SPAC with BurTech Acquisition Corp.; the merger valued Blaize at $1.2 billion and provided access to a convertible note and additional funding.

### 2.2 The product line and unit economics

| Product | Configuration | Performance | Power | Form factor | Launch price |
|---|---|---|---|---|---|
| Pathfinder P1600 | 16 GSP + dual Arm Cortex-A53 | 16 TOPS | 7W | System-on-Module | $399 |
| Xplorer X1600E | 1x GSP SoC | up to 16 TOPS | 7W | EDSFF / M.2 | $299 |
| Xplorer X1600P | 1x GSP SoC | 16 TOPS | 7W | HHHL PCIe Gen3 | $999 |
| Xplorer X1600P-Q | 4x GSP SoC | 64-80 TOPS | about 28W | PCIe Gen3 x16 | — |

- **Pathfinder P1600 (SoM)** is the embedded standalone module — GSP plus a dual Cortex-A53 host, MIPI CSI/DSI camera interfaces, an H.264/H.265 codec, and PCIe Gen3. It targets cameras, kiosks, and industrial vision where the customer builds the whole device.
- **Xplorer X1600 family (accelerators)** is the same silicon delivered as M.2/EDSFF (X1600E), single PCIe card (X1600P), and a **quad card (X1600P-Q, 64-80 TOPS)** that is the building block for the "hybrid AI rack-scale" servers Blaize now sells.

### 2.3 The pivot — and what it reveals

Through 2025, Blaize repositioned from an embedded edge-chip vendor into a **"hybrid AI rack-scale" + sovereign-AI + AI-services** company: selling co-branded servers that pair GSP quad-cards *with* third-party GPUs, orchestrated by a "Blaize AI Services" software layer (face recognition, document processing) sold per-query, targeting government/sovereign deployments in APAC and the Gulf. Management frames three pillars — sovereign AI infrastructure, smaller task-specific LLMs, and programmable energy-efficient compute — and claims a hybrid rack delivers about 50% lower infrastructure cost and about 60% lower power than GPU-only. Economically, **a "hybrid GSP-plus-GPU rack" is a GPU reseller with an optional Blaize card** — and the resale economics (about 10% gross margin) confirm it. The detailed mechanics of the GSP and why this pivot is a tell are dissected in the Technology Assessment (Section 5b).

---

## 3. Industry and competitive landscape

*(This section authored by the desk's semiconductor / edge-AI specialist. Price-blinded except where a valuation level is itself the subject — private rounds and M&A prices.)*

### 3.1 Where edge-AI inference sits in the AI compute stack (first principles)

To value any AI-silicon company you must first locate it on two axes: **training vs. inference**, and **cloud vs. edge**. They define entirely different demand profiles, margin structures, and competitive dynamics.

**Training vs. inference.** *Training* is the one-time, capital-intensive process of building a model by iterating over enormous datasets — it demands massive clusters of the highest-end GPUs (NVIDIA H100/Blackwell-class), high-bandwidth memory (HBM), and exotic interconnect. *Inference* is the ongoing, repeated act of *running* a trained model to produce an answer. Inference is where the money is spent over a product's life — and it is far more fragmented, cost- and power-sensitive, and amenable to specialized silicon than training. This matters because the edge is almost entirely an inference market: **in 2024 the inference segment accounted for 99.8% of edge-AI volume** (Grand View Research / Mordor Intelligence). An edge-AI silicon company is therefore *never* competing for training dollars — it is competing for the inference workload that is migrating out of the cloud.

**Cloud vs. edge.** *Cloud* inference runs in a data center; *edge* inference runs locally — on a camera, vehicle, robot, gateway, drone, or PC — where the data is generated. The structural migration toward edge is the thesis underpinning the entire sector: **IDC projects that by 2027, 80% of CIOs will turn to edge services to meet the demands of AI inference**. The economic logic is concrete — a January 2025 study modeled that hybrid edge-cloud processing of agentic AI workloads can yield **energy savings up to about 75% and cost reductions exceeding about 80%** versus pure-cloud, because the edge eliminates latency, cloud data-egress fees, and privacy exposure.

**The compute stack, top to bottom**, runs: (1) data-center training (NVIDIA-dominated, HBM-bound); (2) data-center / edge-cloud inference (GPUs plus emerging inference ASICs); (3) edge-server / "near-edge" inference (rack-scale, the tier Blaize is pivoting into); and (4) device/embedded inference (cameras, vehicles, robots — the classic "edge-AI accelerator" socket). Blaize originally positioned in tier (4) with the GSP, and has pivoted toward tier (3).

### 3.2 Market structure, TAM and CAGR

The "edge AI" label spans several overlapping markets, and the single biggest analytical trap is conflating them.

**(a) Edge-AI accelerator / chip market — the high-growth core.** The purpose-built inference silicon segment directly relevant to Blaize and its pure-play peers. Two of the most-cited houses agree on both endpoints: Grand View Research, **USD 7.71B (2024) to USD 38.44B (2030), 30.8% CAGR**; Mordor Intelligence, **USD 7.45B (2024) to USD 35.75B (2030), about 31% CAGR**. *Caveat — definitional dispersion:* houses that fold commodity CPUs into "edge AI chip" report far lower growth (Lucintel: $19.9B by 2030 at 7.3%; DataM: $7.5B to $27.1B by 2032 at 17.4%). The about 30% figure is specifically the *purpose-built accelerator/NPU* sub-market; the all-in chip category grows about 17%. **Always confirm the segment boundary before applying a multiple.**

**(b) Broader edge-AI hardware market** (accelerators plus devices/systems): MarketsandMarkets, **USD 26.14B (2025) to USD 58.90B (2030), 17.6% CAGR** — the lower CAGR reflects volume-weighting toward mature components (smartphones 80.5% of 2024 volume, CPUs 88.8%).

**(c) Edge-AI whole solution** (HW + SW + services): Grand View, **$24.91B (2025) to $118.69B (2033), 21.7% CAGR**.

**Structural mix:** ASICs/domain-specific logic lead — **47.2% share in 2024** — with NPUs fastest-growing, confirming the secular pivot toward domain-tuned silicon for its 4-7x TOPS/W advantage. End markets: smartphones largest by device count; **automotive highest by revenue**; healthcare fastest-growing (about 27.9% CAGR to 2030, aided by 950 FDA AI/ML device clearances in 2024). Geography: North America led with **39.8% in 2024**; **Asia-Pacific is the fastest-growing region** (about 29.9% CAGR, on track to overtake by 2030 as APAC targets 62% of global semiconductor output) — directly relevant to Blaize's APAC/sovereign base.

### 3.3 Demand drivers (why inference is moving to the edge)

Five forces, in order: (1) **latency / real-time determinism** — autonomous machines, ADAS, robotics, live video cannot tolerate a cloud round-trip; local inference is a functional requirement, not an optimization. (2) **Cost-per-inference** — as models proliferate the recurring run cost dominates lifetime economics; edge eliminates per-query compute and data-egress fees (the about 80% reduction above); falling **$/TOPS** is named by Mordor as an accelerant. (3) **Power / energy efficiency (TOPS/W)** — the single most decisive metric at the edge, where thermal/battery budgets are fixed; the axis on which pure-plays try to beat NVIDIA and on which Blaize's 14nm, about 2.3-TOPS/W silicon underperforms. (4) **Data sovereignty / privacy** — regulatory and national-security mandates require data to stay in-country or on-device; Mordor names sovereign-AI regulations alongside $/TOPS and 5G. (5) **The workload regime shift — CNN vision to transformers/LLMs/VLMs at the edge** — through about 2022 the edge ran convolutional vision models where 4-26 TOPS sufficed (Coral, Hailo-8); the market has since moved to transformers/LLMs/VLMs needing INT4, far larger memory, and an external DRAM interface. This is why Hailo added a DDR interface in the Hailo-10H (the SRAM-bound Hailo-8 couldn't run LLMs), why Ambarella's CV7 added VLM support, and why SiMa built the GenAI-focused Modalix. It **structurally disadvantages a 16-TOPS part** and explains Blaize's GPU-reselling pivot.

### 3.4 How the industry is valued — which metrics matter

In order of weight: (1) **production design-win backlog** — the dominant value driver; a design win means your silicon is selected, soldered into, and shipping inside a customer's product, creating multi-year sticky revenue and high switching costs (the customer's models tuned to your compiler). The 2024-25 markup/markdown bifurcation turned almost entirely on this; **pilots and MOUs are heavily discounted, production sockets are everything.** (2) **TOPS/W and $/TOPS (proven, not claimed)** — independently benchmarked (MLPerf) numbers carry far more weight than vendor system-level claims. (3) **SDK / software ecosystem maturity** — often the real moat (CUDA); the market pays a premium for anti-CUDA ecosystem strategies (much of Tenstorrent's premium). (4) **Foundry access and process node** — a startup that can't fund its next tape-out is functionally dead; node also caps the efficiency ceiling. (5) **Next-gen roadmap and funding runway** — edge AI needs a new chip every about 18-24 months. (6) **Strategic backer quality** (Samsung, Arm, KT, TDK, NTT, Honda, government R&D). **Blaize scores poorly on 1-5 and well only on 6.**

### 3.5 Regulatory and structural forces

**US-China export controls.** A tightening BIS regime (Oct 2022 IFR; Oct 2023 and Apr 2024 updates) culminated in the **December 2, 2024** package — new/revised ECCN entries covering **HBM**, semiconductor equipment and software; two new Foreign Direct Product rules; **140 Entity List additions**; controls on 24 SME types and 3 software tools. HBM controls are especially consequential because HBM is the memory bottleneck for AI accelerators — and Blaize itself blamed an **HBM shortage** for its Q1 2026 miss. The regime then whipsawed: the **AI Diffusion Rule** (Jan 15, 2025) was **rescinded May 13, 2025** for a "trusted-partner" approach. The **NVIDIA H20 saga** (April 2025 license requirement, a $5.5B charge, curbed $2.5B of China revenue, then the unprecedented 15%-of-China-proceeds arrangement) is the case study in policy risk. Net effect: (a) inside China, forced efficiency/substitution (DeepSeek R1, Huawei Ascend) and an indigenization drive; (b) globally, a tailwind for locally-controlled edge/on-device inference. The whipsaw is itself a material risk to any addressable-market estimate.

**Sovereign AI.** Per CNAS's Sovereign AI Index, infrastructure projects accelerated sharply since mid-2024 (**23 new projects in Q4 2025 alone**), with **over 80% of tracked investment concentrated in the Middle East and East Asia** — Blaize's target geographies. The crucial paradox: **sovereignty in branding does not equal supply-chain independence** — US firms dominate nearly every layer, and **NVIDIA supplies GPUs for 52% of tracked sovereign-AI projects** (it is building 20 AI factories across Europe). The same data-residency/latency/foreign-dependence drivers do push some inference onto locally-controlled hardware — the explicit pillar of Blaize's pivot.

### 3.6 Competitive dissection — the players, with figures

**The incumbent: NVIDIA Jetson / Orin / Thor — the CUDA moat.** Jetson Orin scales to **275 TOPS across seven modules** (AGX Orin 64GB = 170 INT8 TOPS, 2048 CUDA + 64 Tensor cores; Orin Nano 67 TOPS at 7-25W; Orin NX 157 TOPS at 10-40W). **Jetson Thor** (Blackwell) delivers **2,070 FP4 TFLOPS — 7.5x Orin** — positioned for humanoid robotics (Project GR00T). The moat is **software, not silicon**: CUDA + TensorRT + a vast library/model ecosystem means a developer's existing models run on Jetson with zero porting. This is the gravitational center the memo must reckon with — every competitor's strategy is an answer to "how do you beat CUDA?"

**The pure-play challengers.**
- **Hailo (Israel):** Hailo-8 = **26 TOPS at 2.5W (about 10 TOPS/W, TSMC 16nm)**, on-die SRAM (caps model size); Hailo-10H adds a DDR interface and **40 INT4 TOPS** for edge LLMs/VLMs. **300+ customers, hundreds of shipping products** — the deepest real traction of any pure-play.
- **Ambarella (AMBA):** CVflow vision SoCs with best-in-class ISP + codec; CV5 (5nm, 8K@30fps <2W); **CV7 on Samsung 4nm** = 2.5x CV5 AI with transformer/VLM support. Owns the camera/security-vision niche.
- **Qualcomm Cloud AI 100 / Ultra:** edge-cloud/server tier — **400 INT8 TOPS (75W PCIe), 144MB SRAM, 7nm**; Ultra hits **870 INT8 TOPS / 1,044 FP8 TFLOPS**.
- **Google Coral / Edge TPU:** **4 TOPS, about 2 TOPS/W**, TF-Lite-locked — legacy/low-end.
- **Axelera AI (Netherlands):** RISC-V + Digital In-Memory Compute; **Metis 214 TOPS, Europa 629 INT8 TOPS**; **over $450M raised** (incl. Samsung; $250M+ Series C), a 61.6M euro EuroHPC grant, 500+ customers — Europe's best-funded pure-play.
- **SiMa.ai (US):** software-first MLSoC; **Modalix 25-200 TOPS, TSMC 6nm**; **$355M raised**; Micron/Synopsys/Cerence partners.
- **Kneron (US):** KL730 = **up to 8 TOPS, TSMC 12nm**, privacy/on-device-LLM.
- **Mythic (US):** analog compute-in-memory; M1076 = **25 TOPS at 3W (about 8 TOPS/W)**; re-funded **$125M (Dec 2025)**.
- **EdgeCortix (Japan):** SAKURA-II = **60 INT8 TOPS at 8W (about 7.5 TOPS/W)**; **over $110M cumulative** plus about $49M government R&D.

| Part | TOPS (INT8) | Power | TOPS/W | Node |
|---|---|---|---|---|
| Hailo-8 | 26 | 2.5W | about 10 | TSMC 16nm |
| Mythic M1076 | 25 | 3W | about 8 | 40nm flash CIM |
| EdgeCortix SAKURA-II | 60 | 8W | about 7.5 | TSMC (12nm-gen) |
| NVIDIA Orin NX | 157 | 10-40W | about 3-6 | Samsung 8nm |
| **Blaize X1600 / P1600** | **16** | **7W** | **about 2.3** | **Samsung 14nm** |
| Google Coral | 4 | 2W | about 2 | legacy |

**Blaize sits at the bottom of this table** — the single most important competitive fact in this memo.

### 3.7 The funding / markup-markdown bifurcation (2024-2025)

The sector split violently as capital became revenue-gated, on **traction over benchmarks**. **Marked up:** **Tenstorrent** (Series D post-money about $2.6B; over $693M raised; pedigree [Jim Keller] + an open-source anti-CUDA ecosystem); **Rebellions (Korea)** ($1.4B unicorn; Samsung/Arm/KT; formed by merging with SK Telecom's Sapeon; proven Samsung 4-5nm foundry); **FuriosaAI (Korea)** (rejected Meta's about $810M on strategy/autonomy, enabled by a real **LG design win** for its RNGD chip [TSMC 5nm, 48GB HBM3, 512 FP8 TFLOPS, 150W] and entry into mass production; later valued over $700M); **NXP-Kinara $307M all-cash** on about $54M raised (about 5-6x); EdgeCortix; Mythic. **Marked down / harvested:** **Hailo** (about 60%+ markdown from a **$1.2B Apr-2024 peak to sub-$500M** via a distressed SPAC; Delek's stake collapsed from about $412M to about $55M; about 10% staff cut) — *the most capable, best-traction pure-play still got marked down*; **Untether AI (Toronto)** (wound down; AMD took the engineering team only, chips/SDK discontinued, despite strong MLPerf efficiency). **The lesson:** the bifurcation criteria are exactly where Blaize is weakest. **If Hailo — with 300+ customers and 10 TOPS/W — was forced into a distressed sub-$500M SPAC, Blaize's standalone bar is daunting.**

### 3.8 Where Blaize's "hybrid GSP+GPU / rack-scale / sovereign-AI / AI-services" pivot fits

Directionally the tailwinds are real (sovereign AI in Blaize's geographies; the shift to smaller task-specific edge LLMs; export-control-driven localization). **But the structure does NOT support Blaize capturing it durably:** (1) the pivot tacitly admits the GSP can't carry GenAI (it resells GPUs into NVIDIA's strongest channel — NVIDIA already supplies 52% of sovereign projects); (2) no moat at the rack/services layer (crowded, low-barrier, contested by SIs, Dell/Supermicro, Qualcomm, hyperscalers); (3) the markup/markdown rubric runs against Blaize on every axis but strategic backing; (4) the "proof points" (Starshine, NeoTensr) are the very deals under securities-fraud investigation; (5) sovereign rack buildouts are working-capital-intensive (GPUs/HBM upfront) yet Blaize is HBM-constrained under going-concern doubt. **The macro tailwind is genuine; Blaize's claim on it is not.**

---

## 4. Financial analysis

*(This section authored by the desk's forensic accountant. Figures from get_financials, the FY2025 10-K and Amendment No. 1, the Q1-2026 10-Q, and the Q3/Q4-FY2025 and Q1-FY2026 calls.)*

### 4.1 Executive read

Blaize's profile is defined by three things: **(i) a revenue base that exploded about 20x in 2025 but is almost entirely two questionable, low-margin China hardware deals; (ii) a cost structure (about $97M/yr of operating expense) that dwarfs revenue and burns $15-20M/quarter; and (iii) a thin, serially-diluted balance sheet under a formal going-concern warning.** The headline -$206.9M GAAP loss is more than half non-cash de-SPAC noise; the economic loss is better captured by the **$91.8M operating loss** and the **about $81.4M of operating cash burned**. The investable question is not whether Blaize is growing but whether the growth is *collectible and repeatable*, and how much dilution is required to survive long enough to find out.

### 4.2 Revenue trajectory and the H2-2025 spike — what the numbers prove

| Fiscal year | Revenue | YoY |
|---|---:|---:|
| FY2021 | $0 | — |
| FY2022 | $3.84M | — |
| FY2023 | $3.86M | +0.4% |
| FY2024 | $1.55M | **-60%** |
| FY2025 | **$38.63M** | **+2,386%** |

A genuine inflection shows *progressive* sequential growth across many customers. Blaize shows four years of trivial, *declining* revenue — it actually fell 60% in FY2024 — followed by a single-year, near-vertical spike. **A near-vertical jump after years of stagnation demands you ask "from whom?" before celebrating the slope.** The decomposition (gross margins from the as-reported income statement):

| Quarter | Revenue | Gross profit | Gross margin | Primary driver |
|---|---:|---:|---:|---|
| Q1-2025 | $1.01M | $0.49M | 48.5% | — |
| Q2-2025 | $1.98M | $0.72M | 36.4% | about 82% from a related party |
| Q3-2025 | $11.87M | $1.41M | **11.9%** | **Starshine about $10.4M** |
| Q4-2025 | $23.78M | $2.38M | **10.0%** | **NeoTensr over $20M** |
| Q1-2026 | $2.74M | $1.39M | **50.8%** | mostly related-party HW / software |

*(Sources: get_financials quarterly; Q3-FY2025 call — "Approximately $10.4 million... under the Starshine contract"; Q1-FY2026 call — "more than $20 million... in Q4 of 2025" from NeoTensr. Full-year FY2025 gross margin was 12.9% — $4.999M on $38.632M; management referenced an approximate 16% figure.)*

Three structural facts: **concentration** (two China customers at **61% and 27%**, about 88% — single-thread-of-failure revenue); **opacity** (months-old entities — NeoTensr incorporated 12/22/2025 with about $2M of reported capital, booked about $20M weeks later — subject of short-seller reports and at least six plaintiff-firm investigations); **collection** (Starshine paid only **$1.6M of an $8.8M** receivable per the 10-K; offset by management's claim that **over 70% of NeoTensr Q4 billings have been collected**, consistent with the receivables roll-down).

**The gross-margin signature — the single most important tell.** Gross margin is the cleanest proxy for *what a company is actually selling*; a proprietary chip/software company earns 50-70%+ gross margins. Blaize's H2-2025 margin was **10.0-11.9%**; then in Q1-2026, when the China orders paused, it **jumped to 50.8%**. **A roughly 10% gross margin is the signature of pass-through, third-party hardware resale, not chip sales.** Management confirms it: "the higher portion of third-party hardware in our revenue mix," and the Q1 spike from "a mix shift towards our higher-margin software and Blaize-powered hardware." The H2-2025 revenue was largely Blaize buying GPUs/servers and reselling them at about a 10% markup — a distributor, not a chip designer. **The signature proves the spike was low-quality regardless of how the fraud claims resolve.** (DSO of about **151 days** vs 45-75 for healthy hardware reinforces the concern.)

### 4.3 Cost structure and the FY2025 net-loss bridge

Operating cost is about **$97M/yr against about $39M revenue and about $5M gross profit**: **R&D about $9.7M/quarter (about $39M/yr)**; **SG&A about $14-15M/quarter (about $58M/yr)** — larger than R&D, over 100% of revenue. Gross profit $5.0M minus about $96.8M opex = **operating loss $91.8M**.

| Component | FY2025 ($M) | Cash or non-cash |
|---|---:|---|
| **Operating loss** | **(91.8)** | mostly cash |
| **Total other expense, net** | **(114.9)** | almost entirely non-cash |
| — FV change, legacy converts & warrants | (226.0) | non-cash |
| — FV change, earnout shares | +117.1 | non-cash gain |
| — net financing/interest & other | about (6.0) | mixed |
| Income tax | (0.2) | |
| **GAAP net loss** | **(206.9)** | |

The arithmetic ties exactly: -91.8 - 114.9 - 0.2 = -206.9; within "other," -226.0 + 117.1 - 6.0 = -114.9. **The crucial reconciliation:** the entire de-SPAC remeasurement — the -$226.0M non-cash charge on the *legacy convertible notes/warrants* that converted to common at the Jan-2025 listing, partially offset by the +$117.1M non-cash earnout gain — is recorded in the "other" line, **not** in operating expense. So the operating loss is a clean $91.8M (not the $103.8M one would wrongly get by pushing the convert charge up the statement), and the -$226.0M is non-cash and non-recurring (zero converts remain). **Adjusted EBITDA loss about $50.5M** (the most flattering measure — it strips the non-cash items, SBC and D&A); treat the about $81.4M cash burn as the honest economic figure.

### 4.4 Cash flow and burn — the metric that matters most for a going concern

| Metric | FY2025 | Q1-2026 |
|---|---:|---:|
| Operating cash flow | **-$81.4M** | **-$12.6M** |
| Capex | -$0.8M | -$0.1M |
| Free cash flow | -$82.2M | -$12.7M |

**FY2025 OCF -$81.4M is the truest economic loss** — reconciling from -$206.9M by adding back the +$226M non-cash convert charge, subtracting the non-cash gains, adding back about $15M of SBC, and subtracting the cash tied up in the receivable build (receivables ballooned to $36.7M at year-end). **Normalized quarterly burn about $15-20M.** **Q1-2026 OCF -$12.6M is deceptive:** net loss was -$22.7M, but receivables fell about $20M (from $36.7M to about $16.7M) and that one-time collection flowed in as cash. You cannot collect the same receivable twice — annualizing the Q1 print would dangerously understate the cash need.

### 4.5 Balance sheet, liability bridge, dilution

Cash **$33.2M at 3/31/26** + about **$32.8M net** from the May 6, 2026 offering (18,918,918 shares at $1.85; Northland) = **about $66M pro-forma**; total debt about $2.7M (a $1.5M related-party working-capital loan and $2.9M of related-party advances). Total assets $70.8M (cash $33.2M; net receivables about $16.7M, concentrated in the disputed names — haircut heavily; inventory about $9.0M, turns about 3.8x; modest PP&E and a $1.3M lease ROU; the deferred tax asset is worthless in a wind-down).

**The liability bridge — separating real claims from accounting artifacts.** Total liabilities are **$45.3M, but only about $28.6M are genuine cash claims; about $16.7M are non-cash, share-settled derivatives that consume zero cash in a wind-down** (Q1-2026 10-Q): AP incl. related party $12.8M; accrued trade $1.6M; accrued/other current $7.3M (incl. a short-term D&O insurance loan); leases $1.2M; related-party loan/advances $4.4M; other $1.4M = $28.6M cash claims; **plus** Polar PIPE warrants $8.3M and earnout shares (incl. Burkhan) $8.4M = $16.7M non-cash. Under ASC 480/815 these equity-linked instruments are carried at fair value and marked to market each quarter, *settled in stock not cash*; in a wind-down they expire worthless and **claim nothing against assets** (while injecting swings into "other income/expense": +$1.0M in Q1-2026; the +$117M earnout gain in FY2025). **For a floor analysis the relevant stack is about $28.6M, not $45.3M.** Stockholders' equity +$25.4M is an accounting residual ($684M paid-in vs a $659M accumulated deficit), not durable value; it erodes quickly with burn.

### 4.6 Going concern, the 10-K/Amendment No. 1, guidance

Both the FY2025 10-K and Q1-2026 10-Q carry a formal **going-concern qualification** — management and auditors agree the company cannot fund itself from operations. An **Amendment No. 1** to the FY2025 10-K was filed within weeks of the original; the company does not state plainly whether it was routine (Part III) or substantive (revenue recognition / ICFR), and the distinction is material. Management reaffirmed **FY2026 revenue of $130M** and Q4-2026 GM 30-35%, back-half weighted — a further about 3.4x jump off a year about 88% concentrated in disputed customers, with Q1-2026 actual revenue only $2.74M, and leaning on the *same* names (NeoTensr expanded to a "$70M potential," Starshine, Yotta, Nokia). **It is only as credible as the unresolved revenue-quality questions.**

### 4.7 Fully-diluted share reconciliation

| Tranche | Shares | Strike / trigger | Treatment |
|---|---:|---|---|
| Common (5/7/26, post-raise) | 142.2M | — | always counted |
| Options | about 28M | about $1.18 | in-the-money, dilutive |
| RSUs | about 4M | none | always dilutive |
| Polar warrants | 9.4M | $3.00 | OTM today |
| BZAIW (public/private) | 29.6M | $11.50 | deep OTM |
| Earnout (legacy + Burkhan) | 17.6M | $12.50-$20.00 | conditional / deep OTM |
| Convertible notes | 0 | — | all converted at de-SPAC |

Three denominators: **liquidation about 142-145M** (options/warrants/earnout worthless in a wind-down); **realistic going-concern FD about 158M** (142.2M + about 4M RSUs + about 12M net from in-the-money options via treasury-stock method); **post-funding (24-month) about 235-270M** — funding the next 24 months needs about $120-160M (about 8 quarters x $15-20M), and with **no ATM/equity-line/debt backstop** each raise is a discrete, price-damaging sale, implying about 80-100M new shares (about +65% to about 235M), toward about 270M FD if a recovery pulls in the Polar warrants/earnout. **The dominant value sink is unproven/possibly-uncollectible revenue plus structurally guaranteed about 65% dilution.**

---

## 5. Management, governance, ownership, and what they said

CEO **Dinakar Munagala** (co-founder) and CFO **Harminder Sehmi** run a relentlessly promotional narrative ("breakout growth year," "20x growth," "practical/sovereign AI") and responded to the short-seller allegations by *expanding* the disputed NeoTensr contract to a "$70M potential" rather than de-risking — itself something plaintiffs intend to probe, weighing on governance credibility. **Insiders are net sellers/distributors, not buyers:** CFO Sehmi sold repeatedly (40,609 sh on 5/1 and 6/1; 123,460 on 4/20); the CEO, General Counsel, CRO and director Cannestra exercised options and sold; on 5/8/2026 10% owner **Bess Ventures** and Chairman **Lane Bess** executed "J-Other" transfers of **2,000,000 shares each (about 4.0M combined)** tied to the settlement/foreclosure of about $25M of sponsor loans; 10% owner **Ava Investors** distributed about 5.1M shares to its LPs "for no consideration." There is **no open-market insider buying.** The Ava distribution and expiring lock-ups convert locked stock into free float. Institutions hold about **25.5% (115 holders, 29.8M shares)** — thin, transient backing. The most telling call admission: the Q1-2026 miss blamed on an **HBM shortage**, confirming the "hybrid AI" business is GPU/HBM-dependent resale, not GSP silicon. Management's "over 70% of NeoTensr collected" claim is the key mitigant and is consistent with the about $20M receivable roll-down — but cash receipts do not prove legitimate end-demand (no direct round-tripping evidence found, though it cannot be excluded from public data).

---

## 5b. Technology / scientific assessment

*(This section authored by the desk's semiconductor / edge-AI technology analyst.)*

### 5b.1 Verdict up front

**The GSP is a real, genuinely differentiated architecture — but it is differentiated in the wrong direction for the market it now chases, and the company has effectively stopped selling it.** Blaize's Graph Streaming Processor is an authentic third architectural path (depth-first, hardware-scheduled graph dataflow) distinct from GPU SIMT and TPU-style systolic arrays, with non-trivial patents and a no-code software stack. But three facts collapse the bull case: (1) the silicon is uncompetitive on the one axis that matters — efficiency: about **2.3 TOPS/W on Samsung 14nm** vs Hailo-8's about **10 TOPS/W on TSMC 16nm**, about 4x behind and level with a 2019 Coral; 16 TOPS is an order of magnitude below where the market has moved (Orin Nano 67 TOPS, Axelera Metis 214 TOPS) and far too small for transformer/LLM workloads; (2) it is stuck in the middle — less efficient than Hailo/Ambarella, less programmable-with-ecosystem than NVIDIA, whose one edge (programmability + multi-network concurrency) is what CUDA already delivers at vastly greater scale; (3) the company has pivoted away from its own chip — essentially all of 2025's $38.6M was low-margin GPU-server resale (11-16% GM) to two China counterparties now alleged to be shells. **Probability of reaching meaningful, durable commercial scale as an independent edge-AI silicon franchise: low — about 10-20%**, and the path is acquihire, not "GSP wins design sockets."

### 5b.2 How the GSP works — from first principles

Every neural network is a **directed graph** (nodes = ops, edges = tensors). **GPUs (SIMT)** process it breadth-first, one layer at a time across thousands of threads (warps), writing each layer's full output to external DRAM (HBM/LPDDR) and reading it back — throughput-optimal at large batch but DRAM-bandwidth- and power-hungry, with the SIMT width exposed to software. **Systolic arrays (TPU)** march data through a fixed MAC grid — efficient for dense matmul but rigid, poor for irregular graphs/control flow/multi-network. **Blaize processes the graph depth-first and on-chip**: intermediate tensors stream core-to-core through on-chip memory, so **only the first input and final output touch external DRAM** — the source of the "50x less memory bandwidth / 10x lower latency / 60x system efficiency" claims (vendor system-level, not independently benchmarked — flag). Four ingredients: (1) **16 small instruction-programmable cores** at only hundreds of MHz (efficiency from data locality and low clock, not high frequency); (2) **composable 4-bit execution units** assembled at runtime into INT8-FP16, fed by a 2-D register file with a single unified address space (the SoC supports INT8/INT16/BF16/FP16/FP32/FP64; the SIMD width is hidden from software — the opposite of GPU SIMT); (3) a **proprietary single-cycle hardware scheduler** (compile-time "metamap," runtime scheduler instances allocating thread slots and reprogramming cores in a single clock cycle — data-driven dataflow, no program counter); (4) about 4 Mbit hierarchical on-chip memory as the streaming buffer. The novel capability is **concurrent multi-network execution** — running several different networks simultaneously on the same clock, useful for sensor fusion. Real engineering — but the dataflow *category* (Graphcore, Wave [bankrupt], Groq, Tenstorrent, SambaNova) is crowded and littered with failures; elegance does not equal commercial success.

### 5b.3 The software stack — the intended moat

**Picasso SDK** (graph-native; TensorFlow/PyTorch/Caffe2/ONNX; C/C++ and OpenVX); **AI Studio** (a no-code/GUI environment for domain experts, not coders — the genuine differentiator vs CUDA's code-heavy workflow); **NetDeploy** (automated quantization/optimization/compression, "months to weeks/days," many models concurrently each with a different context). The BLZP1600 SoC gained upstream support in mainline **Linux 6.14** — a real productization signal. But software is exactly where NVIDIA's moat is deepest; Hailo and SiMa also tout push-button toolchains. Blaize's stack is a feature, not a moat.

### 5b.4 Process node and the efficiency reality check (the most important slide)

The BLZP1600 SoC is built on **Samsung Foundry 14nm FinFET** (VeriSilicon design partner) — several generations behind rivals' 4-7nm (Ambarella CV7 4nm, SiMa Modalix 6nm, Qualcomm AI 100 7nm).

| Part | TOPS | Power | TOPS/W | Node |
|---|---|---|---|---|
| **Blaize X1600 / P1600** | 16 (INT8) | 7W | **about 2.3** | Samsung 14nm |
| Hailo-8 | 26 (INT8) | 2.5W | **about 10** | TSMC 16nm |
| Google Coral Edge TPU | 4 | 2W | **about 2** | legacy |
| Mythic M1076 (analog CIM) | 25 | 3W | **about 8** | 40nm flash |
| NVIDIA Jetson Orin NX | up to 157 | 10-40W | about 3-6 | Samsung 8nm |

**The "energy-efficient edge AI" positioning does not survive the spec sheet** — about 4x behind Hailo on a comparable node, behind Mythic, level with a six-year-old Coral. The efficiency story rests entirely on system-level comparisons against power-hungry GPUs ("60x"), not the relevant pure-play set; and 16 TOPS absolute is an order of magnitude short of where the workload has moved. A next-gen chip is "in development" but unfunded-to-completion and unshipped.

### 5b.5 Moat analysis — does it hold?

IP real but narrow (the scheduler and composable units are patented and non-trivial, but patents didn't protect Graphcore/Wave); the software stack is a genuine differentiator for non-coders but a feature, not a CUDA-beater; **design wins/switching costs are where the moat thesis fails** — switching cost comes from production sockets (soldered into a shipping device, the customer's models tuned to your compiler), and Blaize has very few, its largest "wins" being GPU-server resale to alleged shells. Real relationships (Yotta 250k cameras but only about $6M recognized; Winmate about $15M intent; Nokia/Datacom lab; VSBLTY conditional PO) are pilot-stage. Automotive (Denso/Mercedes/Magna investors/co-dev) is optionality not in production until 2028+. **The moat does not hold.**

### 5b.6 Where Blaize is on the commercialization curve (real vs pilot vs suspect)

**Blaize did not commercialize its chip in 2025 — it became a low-margin GPU-server reseller.** 61%/27% from two China customers at 11-16% GM. **Starshine (Hong Kong)** — a **$120M, 18-month** smart-city deal (July 2025); reality per the 10-K, only **$1.6M collected of an $8.8M** receivable; domain registered two weeks before the PR with stock-photo pages (Ragnarok). **NeoTensr** — the **about $20M+ Q4 spike** (plus an "up to $50M" follow-on); domain registered Dec 18, 2025, incorporated Dec 22, 2025 with about $2M capital, products allegedly photoshopped from AIC servers (Pelican Way, April 2026); the April-2026 PR nearly identical in structure to the year-earlier Starshine PR. At least four plaintiff firms have opened securities-fraud investigations. **Genuine (non-suspect) footing, discounted:** Yotta (India; about $6M recognized), Winmate (about $15M intent), Nokia/Datacom (lab), VSBLTY (conditional PO), CBIST (Korea), Turbo Federal (US defense), Technology Control Company (Saudi). Strip out Starshine/NeoTensr and the recurring, real, Blaize-silicon base is **low-single-digit millions** — roughly the FY2022-24 run-rate ($3.8M/$3.9M/$1.6M). **The "20x growth" is an artifact, not a franchise.**

### 5b.7 Failure modes vs. the CUDA ecosystem

(1) **The software/ecosystem moat (the primary killer)** — every non-NVIDIA accelerator forces a recompile/requantize through a proprietary compiler (NetDeploy/Picasso), introducing accuracy loss, unsupported-operator gaps and debugging pain; customers repeatedly choose "worse silicon that just works" over "better silicon I have to port to," and Blaize has neither a spec advantage nor an ecosystem. (2) **Performance-claim credibility gap** — vendor "60x" system numbers don't survive MLPerf-style scrutiny; analysts have criticized the lack of independent benchmarks since the first reveal. (3) **Node treadmill / capital starvation** — a fabless startup that can't fund its next mask set is dead (the Wave/Graphcore mode). (4) **Workload regime shift** — the CNN-to-transformer move strands a 16-TOPS part; reselling GPU servers is an admission its own silicon can't carry the workload. (5) **Go-to-market via shell/reseller counterparties** — a classic late-stage symptom that has metastasized into a fraud overhang.

### 5b.8 Sober technical viability verdict

A legitimate piece of computer architecture that has lost its race. Depth-first graph streaming with a single-cycle hardware scheduler is real engineering and genuinely differentiated; multi-network concurrency for sensor fusion is a real, if narrow, capability; the no-code toolchain is a credible deployment answer. But on the metrics that decide edge-AI sockets, Blaize loses on every axis that matters: efficiency (about 2.3 TOPS/W), absolute performance (16 TOPS), node (14nm), ecosystem (no CUDA answer), funding (going-concern doubt), and revenue quality (fraud-flagged resale). The architecture is differentiated but not defensible, and the commercial record is, on its real economics, still pre-revenue. Realistic upside is acquihire of the IP/team (the Denso/Mercedes/Samsung cap table makes this the most plausible non-zero outcome) or survival as a small sovereign-vision specialty supplier — a far smaller business than the narrative implies. **Probability of meaningful, durable commercial scale as an independent silicon company: about 10-20%.**

---

## 6. Catalysts and financing path

- **Q2-2026 results** — management guided to "over $11M to a single customer" (NeoTensr); whether it ships and *collects* is the near-term tell on revenue authenticity.
- **Securities-fraud investigations** maturing into filed complaints (or not) over 2026-27 — a binary overhang.
- **The next equity raise** — likely within about 12 months; about $100-140M of new money.
- **Q4-2026 gross-margin inflection** to 30-35% — the proof point that real product economics exist.
- **Next-gen GSP tape-out** — undisclosed timeline/funding; the single most important technical swing factor, currently unfunded-to-completion.

No ATM/equity line/debt facility; funding is 100% discrete dilutive equity (Polar PIPE; May offering at $1.85). Bridging 24 months (about $120-160M) implies about 80-100M new shares (about +65% to about 235M), toward about 270M FD if a recovery pulls in the Polar warrants ($3.00)/earnout. **This dilution drag, on a fraud-flagged, about $28.6M-net-cash-claim balance sheet, is the dominant value sink.**

---

## 7. Valuation

### 7.1 Why this method

Blaize is **technology-/commercialization-contingent with a binary, downside-skewed outcome**. A DCF of reported revenue would discount cash flows whose *quality* is the entire question (about 88% from fraud-flagged counterparties at about 10% margin). A clean revenue or EBITDA multiple is unusable on suspect revenue and negative EBITDA. Book value is an accounting residual that erodes with burn. The right frame is the **probability-weighted present value across discrete outcome scenarios (rNPV)**, anchored by an **asset/liquidation floor** and cross-checked against **edge-AI M&A comps**.

### 7.2 The asset/liquidation floor (the no-growth anchor)

| Item | Gross | Realizable (haircut) |
|---|---:|---:|
| Cash (incl. May raise) | $66.0M | $66.0M |
| Receivables | $16.7M | $8.4M (50% — disputed China names) |
| Inventory | $9.0M | $4.5M (50% — specialized AI HW) |
| PP&E + other | about $5M | about $2.0M |
| **Realizable assets** | | **about $80.9M** |
| Less: genuine cash claims | | ($28.6M) |
| Less: wind-down costs | | (about $10M) |
| **Residual to common** | | **about $42M** |
| Over about 145M shares | | **about $0.29/share** |

So the asset floor is **about $0.25-0.29/share** — but it is a **melting floor**: at about $15-20M/quarter burn, the cash that backs it is being spent. I anchor the intrinsic floor at **$0.25**.

### 7.3 Base-rate anchoring of the scenario probabilities

Each weight is built from a published base rate plus a reasoned company-specific adjustment, not narrative intuition:

- **Wipeout — 35%.** *Base rate:* a first-time going-concern opinion precedes bankruptcy/forced delisting in roughly **20-25% of cases over multi-year windows** (Altman 1982; Nogler 1995; GC precedes about 60% of bankruptcies, Carson et al. 2013) — survival is modal. *Adjustment up:* the activist-short literature (Brendel & Ryans 2021, JAR) shows catastrophic outcomes concentrate where reports contain *concrete new evidence* — here, counterparty incorporation dates, about $2M of capital, allegedly photoshopped product, about 88% revenue concentration, no financing backstop, and a death-spiral-dilution channel that wipes per-share value short of bankruptcy. Net **35%** (captures insolvency *and* dilution-to-near-zero).
- **Genuine scale — 8%.** *Base rate:* durable independent chip scale is a **single-digit-to-about-10% venture tail** (Correlation Ventures; about 75% of VC-backed firms fail to return capital, Ghosh/HBS); chips are harder than the cross-sector average. *Adjustment:* near the low end for bottom-quartile efficiency and an unfunded next-gen — **8%**.
- **Strategic acquihire — 19%.** *Base rate:* the chip "modest-success middle" is dominated by strategic absorption (Nuvia/Qualcomm, Habana/Intel, Annapurna/Amazon, Kinara/NXP $307M, Untether/AMD). *Adjustment up:* the Denso/Mercedes/Samsung/Nokia cap table makes an IP/team purchase materially more likely than for an unbacked peer — **19%**.
- **Marginal survival — 38%.** Residual; consistent with the going-concern literature (survival via recap/restructuring/partnership conversion is modal).

**Reconciliation with the technology specialist's "10-20% durable commercial scale":** that maps to the **Scale branch (8%) plus the genuine-franchise portion of Survival** — **not** Acquihire (an exit/IP sale, not commercial scale). Scale plus roughly the franchise-bearing half of Survival lands "reaches a real ongoing business" at about 15-20%, consistent with the range; the 19% Acquihire is separate and additive.

### 7.4 The acquihire branch — derived bottom-up (the single most swing-sensitive input)

The acquihire branch is the largest single contributor to FMV, so I derive its value bottom-up rather than merely comp-bound it. Blaize employs roughly **150 core silicon/software engineers** (consistent with about $39M/yr of R&D for a fabless team). Distressed chip-team acquihires clear at roughly **$1-2M per engineer** — the **AMD-Untether** template, where AMD took the engineering team only and the products/SDK were discontinued. At about $1.5M x 150 = about **$225M of gross talent value**, plus about **$50-100M** for the GSP dataflow patents and the automotive co-development IP (Denso/Mercedes/Magna). Two deductions then apply: (a) in a true team-only outcome much of that value accrues to **retention packages and to retiring obligations**, not to common; and (b) a **fraud-clouded target carries contingent securities-litigation liabilities** an acquirer will assume or price out. Net to common: about **$180M of equity over about 180M diluted shares = about $1.00/share** — *above* the pure team-only Untether outcome (where common received little) and *well below* Kinara's clean **$307M** product acquisition, reflecting the fraud discount. (I deliberately do not anchor to the Meta-FuriosaAI rejected about $800M offer, which reflected a *winning* product with a real design win — the opposite of Blaize's position.)

### 7.5 The survival branch — explicit revenue bridge

Today's genuine (non-suspect) revenue, stripping Starshine/NeoTensr, is **low-single-digit millions** (the FY2022-24 run-rate of $1.6-3.9M plus the non-China Q1-26 component). The branch assumes that, after a dilutive recapitalization, a *fraction* of the genuine pipeline converts by 2028: the **Yotta** 250k-camera VSaaS rollout (about $6M recognized, more contracted), partial **Winmate** (about $15M intent), genuine (non-shell) **Nokia/Datacomm** rack volume, and an early **AI-services** recurring layer — summed and heavily haircut to about **$20-35M of genuine revenue at about 25-30% GM**. At a distressed edge-AI **2-3x sales** plus residual recapitalized cash, equity is about **$80-120M** over about **250M post-dilution shares** = about **$0.40-0.45/share**. I use **$0.45**. (Deliberately a *fraction* of the pipeline; it does not assume the $130M guide or the disputed China deals.)

### 7.6 The probability-weighted FMV (rNPV)

Discount at a **systematic-risk cost of equity of 17%** — rf about 4.3% + beta about 2.0 x ERP about 5% + about 3% micro-cap size/illiquidity premium. The idiosyncratic/binary risk is in the probabilities, so it is not double-counted in the rate.

| Scenario | Prob. | Value/share if realized | Years | PV/share |
|---|---:|---:|---:|---:|
| **Wipeout** | 35% | $0.02 | 1.5 | $0.016 |
| **Marginal survival** (about $20-35M real revenue; equity about $100M over about 250M sh) | 38% | $0.45 | 3.0 | $0.281 |
| **Strategic acquihire** (bottom-up; about $180M equity over about 180M sh) | 19% | $1.00 | 2.0 | $0.731 |
| **Genuine scale** (about $200-300M franchise valued about $700M-1B over about 280M sh) | 8% | $3.00 | 5.0 | $1.368 |

**Probability-weighted fair value = about $0.36/share.**

### 7.7 Sensitivity / confidence band

The headline is dominated by the acquihire input, so the band varies it explicitly alongside the wipeout weight and survival value:

| Case | Wipeout | Survival | Acquihire | Scale | FMV/share |
|---|---:|---:|---:|---:|---:|
| **Pessimistic** | 45% | 35% ($0.38) | 15% ($0.80) | 5% ($2.50) | **$0.23** |
| **Base** | 35% | 38% ($0.45) | 19% ($1.00) | 8% ($3.00) | **$0.36** |
| **Optimistic** | 25% | 40% ($0.60) | 25% ($1.40) | 10% ($3.50) | **$0.57** |

**Explicit acquihire sensitivity (holding base weights):** an acquihire value of **$0.80/share** (closer to the team-only Untether outcome) pulls FMV to about **$0.33**; **$1.40/share** (a cleaner sale toward Kinara) lifts it to about **$0.42**. This single judgment moves the point estimate by roughly +/- $0.05, so the reader should treat it as the swing input. The band is **about $0.23-$0.57**, reflecting genuine uncertainty in the probabilities and realized values, not a bull/bear split. Note the pessimistic FMV ($0.23) sits just *below* the $0.25 liquidation floor because the pessimistic weighting embeds a 45% wipeout mass (an equity impaired *below* asset value in a fraud/default), whereas the floor assumes an orderly wind-down today — the two are answering different questions and the small gap is expected.

### 7.8 Cross-check

Stripping the suspect resale, the genuine revenue run-rate is low-single-digit millions; at a distressed 2-3x that is about $30-45M of enterprise value — *below* net cash — so the operating business has little standalone value beyond cash plus IP optionality, exactly what the rNPV captures. The acquihire branch is now derived bottom-up (Section 7.4) and sits between the Untether team-only floor and the clean Kinara $307M price. And the read-across discipline: Hailo — a far superior franchise (300+ customers, about 10 TOPS/W) — was marked to sub-$500M; Blaize's franchise must be worth a fraction of that, consistent with the about $100-180M equity in the survival/acquihire branches.

---

## 8. Probability-weighted outcome distribution

The FMV is the integral over the distribution, not a midpoint of stories. Key drivers and weights (Sections 7.3-7.5): **revenue authenticity** (the master variable — drives the 35% wipeout; the about 70% NeoTensr collection keeps it from being higher); **survival vs. dilution-to-death** (about $15-20M/quarter burn, no backstop, about 65% dilution → the 38% survival branch at about $20-35M real revenue); **strategic IP/team value** (the 19% acquihire, bottom-up at about $1.00/share — the swing input); **genuine scale** (8%, requiring a funded competitive next-gen chip vs the CUDA moat). Integrating yields about $0.36, with the about $0.25 floor as the margin-of-safety anchor.

---

## 9. Risks and what would change my mind

**Downside:** a securities-fraud finding or restatement; going-concern default / inability to raise; dilution beyond about 65%; the next-gen chip never funded; concentration in possibly-fictitious customers; the about 10% GM never inflecting; NVIDIA/Hailo/Qualcomm foreclosing the sockets; an acquihire that proves team-only with common impaired. **What would raise the value:** independent confirmation NeoTensr/Starshine revenue is real and fully collected; a clean 10-K/A with unqualified ICFR and no revenue-recognition material weakness; a substantiated, named *production* design win (not an MOU) at scale; a funded next-gen GSP tape-out on an advanced node; a committed financing facility; credible strategic-acquirer interest above the team-only level. A filed complaint, restatement, auditor change, or failed/again-discounted raise pushes value toward the wipeout branch.

---

## 10. Conclusion

Blaize owns a genuinely inventive architecture that has lost its race: a 14nm, 16-TOPS, about 2.3-TOPS/W part in a market that rewards 7.5-10 TOPS/W on 4-7nm and is gated by NVIDIA's CUDA ecosystem. Its 2025 "breakout" is, on real economics, still pre-revenue — low-margin GPU-server resale to two fraud-flagged China counterparties — and it burns about $15-20M/quarter under a going-concern warning with no financing backstop. This is not an earnings story; it is a **binary option** whose value is the probability-weighted present value of wipeout, dilution-heavy survival, a bottom-up strategic acquihire, and a thin scale tail = **about $0.36 per share** (band about $0.23-$0.57), just above a **melting asset floor of about $0.25**. The distribution is downside-skewed, the dilution is structurally guaranteed, and the upside for today's holder is capped by the share count required to reach it. I would not deploy capital unless the revenue-authenticity question resolves cleanly and a committed financing path emerges — and even then the entry must price the dilution.
