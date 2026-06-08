# Root, Inc. (ROOT) — Full Investigation Transcript

*The complete research history: every step the PM took, what each tool returned, every valuation computed, and every red-team round — followed by the final memo.*


**Outcome:** evaluated | **Red-team reject-rounds:** 0 | **Judge:** 91/100 (best-in-existence=True) | **Tool calls:** 20


*(Each submission was scrutinized by a tool-verifying red-team AND an independent best-in-existence judge; 'reject-rounds' counts only rounds that sent the memo back — the gates ran on every submission.)*


---


## Step 0

**🧠 PM reasoning:**

> I'm starting with Root, Inc., a tech-enabled auto insurance company, and need to gather their financials, key ratios, peer comparisons, and business segment data to build out a comprehensive analysis.

**PM note:** I'll start by building a complete picture of Root's financials, ratios, peers, and business model in parallel.

### ⚙️ `get_financials`

_input:_ `{"period": "annual", "years": 5}`

_returned:_

```
MULTI-PERIOD FINANCIALS (most recent first; values in reporting currency):
period | revenue | gross_profit | operating_income | net_income | ebitda | op_cash_flow | capex | free_cash_flow | cash | total_debt | total_equity | preferred | COMMON_EQUITY | shares
FY2025 | 1517100000.0 | 386600000.0 | 40800000.0 | 40300000.0 | 73600000.0 | 206500000.0 | -14100000.0 | 192400000.0 | 689900000.0 | 201300000.0 | 396300000.0 | 112000000.0 | 284300000.0 | 17200000.0
FY2024 | 1176500000.0 | 337100000.0 | 30900000.0 | 30900000.0 | 88000000.0 | 195700000.0 | -11800000.0 | 183900000.0 | 600300000.0 | 202300000.0 | 315700000.0 | 112000000.0 | 203700000.0 | 16900000.0
FY2023 | 455000000.0 | 76100000.0 | -147400000.0 | -147400000.0 | -88700000.0 | -33600000.0 | -9400000.0 | -43000000.0 | 679700000.0 | 299300000.0 | 277700000.0 | 112000000.0 | 165700000.0 | 14400000.0
FY2022 | 310800000.0 | -32200000.0 | -297700000.0 | -297700000.0 | -249300000.0 | -210600000.0 | -10100000.0 | -220700000.0 | 763100000.0 | 298600000.0 | 389100000.0 | 112000000.0 | 277100000.0 | 14100000.0
FY2021 | 345400000.0 | -51900000.0 | -521100000.0 | -521100000.0 | -484500000.0 | -403400000.0 | -11200000.0 | -414600000.0 | 707000000.0 | 14100000.0 | 648400000.0 | 112000000.0 | 536400000.0 | 13844444.0
Q12026 | 393500000.0 | 167300000.0 | 36100000.0 | 35900000.0 | 44000000.0 | 9300000.0 | -3500000.0 | 5800000.0 | 608900000.0 | 200300000.0 | 437900000.0 | 112000000.0 | 325900000.0 | 17200000.0
Q42025 | 397000000.0 | 96400000.0 | 5400000.0 | 5300000.0 | 13600000.0 | 70100000.0 | -4200000.0 | 65900000.0 | 689900000.0 | 201300000.0 | 396300000.0 | 112000000.0 | 284300000.0 | 17200000.0
Q32025 | 387800000.0 | 81400000.0 | -5000000.0 | -5400000.0 | 5000000.0 | 57600000.0 | -3900000.0 | 53700000.0 | 654400000.0 | 196800000.0 | 377000000.0 | 112000000.0 | 265000000.0 | 15400000.0
Q22025 | 382900000.0 | 101700000.0 | 22000000.0 | 22000000.0 | 29300000.0 | 52000000.0 | 0.0 | 52000000.0 | 642500000.0 | 196600000.0 | 356500000.0 | 112000000.0 | 244500000.0 | 17100000.0

BOOK VALUE NOTE (FY2025): COMMON equity = 284,300,000 (= total_equity 396,300,000 − preferred 112,000,000 − minority 0). Use COMMON equity for book-value valuation; the preferred is a SENIOR claim ahead of common. Common book value/share ≈ 16.53 (on 17,200,000 shares).

KEY METRICS (annual): period | ev/ebitda | ev/sales | fcf_yield | roic
FY2025 | 8.572894021739131 | 0.41590204996374663 | 0.17185246055387585 | 0.035447437011294526
FY2024 | 7.768079545454546 | 0.5810378240543986 | 0.1700273023721536 | 0.031174334140435835
FY2023 | 2.5872378804960543 | -0.5043692307692308 | -0.2849342663273961 | -0.1570256738041973
FY2022 | 1.609269955876454 | -1.2908333333333333 | -3.486076229288095 | -0.2897041650447645
FY2021 | -0.16433431413828675 | 0.2305152727272725 | -0.5366851515945112 | -0.5294655557813452
```

### ⚙️ `get_ratios`

_returned:_

```
TTM OPERATIONAL RATIOS (price-blind — margins, returns, turnover, leverage, liquidity):
grossProfitMarginTTM: 0.2862
ebitMarginTTM: 0.0506
ebitdaMarginTTM: 0.0589
operatingProfitMarginTTM: 0.0375
pretaxProfitMarginTTM: 0.0375
continuousOperationsProfitMarginTTM: 0.0377
netProfitMarginTTM: 0.037
bottomLineProfitMarginTTM: 0.0351
receivablesTurnoverTTM: 4.4504
payablesTurnoverTTM: 0
inventoryTurnoverTTM: 0
fixedAssetTurnoverTTM: 0
assetTurnoverTTM: 0.999
currentRatioTTM: 0
quickRatioTTM: 0
solvencyRatioTTM: 0.0629
cashRatioTTM: 0
debtToAssetsRatioTTM: 0.1282
debtToEquityRatioTTM: 0.4574
debtToCapitalRatioTTM: 0.3139
longTermDebtToCapitalRatioTTM: 0.3139
financialLeverageRatioTTM: 3.5689
workingCapitalTurnoverRatioTTM: 1.9604
operatingCashFlowRatioTTM: 0
operatingCashFlowSalesRatioTTM: 0.1211
freeCashFlowOperatingCashFlowRatioTTM: 0.9386
debtServiceCoverageRatioTTM: 4.4976
interestCoverageRatioTTM: 2.8537
shortTermOperatingCashFlowCoverageRatioTTM: 0
operatingCashFlowCoverageRatioTTM: 0.9436
capitalExpenditureCoverageRatioTTM: 16.2931
dividendPaidAndCapexCoverageRatioTTM: 16.2931
dividendPayoutRatioTTM: 0
revenuePerShareTTM: 100.0769
netIncomePerShareTTM: 3.7051
interestDebtPerShareTTM: 14.1538
cashPerShareTTM: 39.0321
bookValuePerShareTTM: 28.0705
tangibleBookValuePerShareTTM: 28.0705
shareholdersEquityPerShareTTM: 28.0705
operatingCashFlowPerShareTTM: 12.1154
capexPerShareTTM: 0.7436
freeCashFlowPerShareTTM: 11.3718
netIncomePerEBTTTM: 0.988
ebtPerEbitTTM: 1
effectiveTaxRateTTM: -0.0051
dividendPerShareTTM: 0
netDebtToEBITDATTM: -4.4461
incomeQualityTTM: 3.369
grahamNumberTTM: 48.3747
grahamNetNetTTM: -16.2115
taxBurdenTTM: 0.988
interestBurdenTTM: 0.7405
workingCapitalTTM: 959700000
investedCapitalTTM: 959700000
returnOnAssetsTTM: 0.037
operatingReturnOnAssetsTTM: 0.0377
returnOnTangibleAssetsTTM: 0.037
returnOnEquityTTM: 0.1475
returnOnInvestedCapitalTTM: 0.0374
returnOnCapitalEmployedTTM: 0.0374
capexToOperatingCashFlowTTM: 0.0614
capexToDepreciationTTM: 0.8992
capexToRevenueTTM: 0.0074
salesGeneralAndAdministrativeToRevenueTTM: 0.1611
researchAndDevelopementToRevenueTTM: 0
stockBasedCompensationToRevenueTTM: 0.0396
intangiblesToTotalAssetsTTM: 0
averageReceivablesTTM: 341800000
averagePayablesTTM: 0
averageInventoryTTM: 0
daysOfSalesOutstandingTTM: 82.0151
daysOfPayablesOutstandingTTM: 0
daysOfInventoryOutstandingTTM: 0
operatingCycleTTM: 82.0151
cashConversionCycleTTM: 82.0151
freeCashFlowToEquityTTM: 173400000
freeCashFlowToFirmTTM: 194005128.2051
tangibleAssetValueTTM: 437900000
netCurrentAssetValueTTM: -165200000
```

### ⚙️ `get_peers`

_input:_ `{"max_peers": 10}`

_returned:_

```
PEERS (TTM multiples):
[
 {
  "ticker": "PLMR",
  "name": "Palomar Holdings, Inc.",
  "market_cap": 2875938189.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 3.0064946515730853,
  "pe": 14.629217505010274,
  "ev_ebitda": 11.678697660389236,
  "roe": 0.21736343376767606
 },
 {
  "ticker": "HCI",
  "name": "HCI Group, Inc.",
  "market_cap": 2003819560.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.6432851157140222,
  "pe": 5.91148489733358,
  "ev_ebitda": 2.278199646877891,
  "roe": 0.32635170225937493
 },
 {
  "ticker": "STC",
  "name": "Stewart Information Services Corporation",
  "market_cap": 2003015993.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.238193030878567,
  "pe": 15.668094325775424,
  "ev_ebitda": 9.501921327025016,
  "roe": 0.08364444085456968
 },
 {
  "ticker": "SLDE",
  "name": "Slide Insurance Holdings, Inc. Common Stock",
  "market_cap": 1917721678.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.8540973696404133,
  "pe": 4.205329064346423,
  "ev_ebitda": 1.1454869237195098,
  "roe": 0.6666680244896962
 },
 {
  "ticker": "HMN",
  "name": "Horace Mann Educators Corporation",
  "market_cap": 1896704964.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.3164380952380952,
  "pe": 11.721162931556632,
  "ev_ebitda": 9.231994635786327,
  "roe": 0.11476634864362303
 },
 {
  "ticker": "SKWD",
  "name": "Skyward Specialty Insurance Group, Inc.",
  "market_cap": 1863359267.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.5175899823574988,
  "pe": 10.46066240685196,
  "ev_ebitda": 8.644594938224705,
  "roe": 0.17354519987128234
 },
 {
  "ticker": "AFGB",
  "name": "American Financial Group, Inc.",
  "market_cap": 1733456358.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 2.3587110859341602,
  "pe": 12.552958430034131,
  "ev_ebitda": 9.08359842121932,
  "roe": 0.18758002560819462
 },
 {
  "ticker": "AFGD",
  "name": "American Financial Group, Inc.",
  "market_cap": 1624334930.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 2.3587110859341602,
  "pe": 12.552958430034131,
  "ev_ebitda": 9.08359842121932,
  "roe": 0.18758002560819462
 },
 {
  "ticker": "AFGC",
  "name": "American Financial Group, Inc.",
  "market_cap": 1474388760.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 2.3587110859341602,
  "pe": 12.552958430034131,
  "ev_ebitda": 9.08359842121932,
  "roe": 0.18758002560819462
 },
 {
  "ticker": "KMPR",
  "name": "Kemper Corporation",
  "market_cap": 1457136450.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 0.5492657948369565,
  "pe": 34.73352386634845,
  "ev_ebitda": 76.96788166666667,
  "roe": 0.015213543321381563
 }
]
```

### ⚙️ `get_segments`

_returned:_

```
No segment data available.
```

## Step 1

**🧠 PM reasoning:**

> Root's revenue trajectory is striking—jumping from $345M in FY2021 to over $1.5B by FY2025—but I'm noticing some inconsistency in the fiscal year timing that I need to clarify before drawing conclusions about the growth pattern.
> 
> Looking at the quarterly breakdown, it appears Root uses calendar quarters with fiscal year labeling, so FY2025 represents the sum of Q1-Q4 2025, which totals $1.517B with net income of $40.3M—marking their first profitable year. The most recent quarter, Q1 2026, shows $393.5M in revenue with $35.9M in net income, suggesting the profitability is holding up.
> 
> For an insurer, the real story lies in metrics like combined ratio, loss ratio, and policies in force, which will tell me whether this turnaround is sustainable or just a temporary margin expansion.
> 
> Root's the InsurTech that disrupted auto insurance with telematics-based pricing, went public in 2020 at a sky-high valuation, then burned through cash and nearly collapsed before restructuring and reaching profitability. Now I need to think about valuation—it's fundamentally a P&C insurer, so the base case is book value times a warranted price-to-book multiple, but there's significant growth optionality given the recent profitability inflection and rapid expansion.
> 
> The equity structure is a bit complex: total equity is $437.9M as of Q1 2026, but $112M of that is preferred stock senior to common. Common equity is $325.9M on roughly 17.2M shares outstanding, which puts common book value per share around $19 per share.
> 
> Now I'm digging into the core questions: what's the sustainable ROE once the turnaround stabilizes, what's the growth trajectory for policies in force and partnerships like the Carvana embedded insurance deal, and what cost of equity makes sense for a micro-cap turnaround insurer. The real value here hinges on future underwriting margins and growth, not just current book value.
> 
> I'm going to pull the full income statement and balance sheet to reconstruct the underwriting economics—combined ratio, loss ratio, premium volume—and I'll spawn parallel research to get an industry perspective on InsurTech auto valuation benchmarks.

**PM note:** Root is a tech-enabled (telematics) auto insurer that IPO'd in 2020, nearly collapsed, and has just turned profitable with explosive revenue growth ($455M FY23 → $1.18B FY24 → $1.52B FY25). This is a financial/spread business with a major growth-optionality overlay. Let me pull the underwriting detail and stand up specialist analysts in parallel.

### ⚙️ `get_statement`

_input:_ `{"statement": "income", "period": "annual", "limit": 5}`

_returned:_

```
ROOT INCOME (annual, recent first) — full line items:

[2025-FY] (2025-12-31)
  revenue=1517100000
  costOfRevenue=1130500000
  grossProfit=386600000
  researchAndDevelopmentExpenses=0
  generalAndAdministrativeExpenses=96900000
  sellingAndMarketingExpenses=174800000
  sellingGeneralAndAdministrativeExpenses=271700000
  otherExpenses=74100000
  operatingExpenses=345800000
  costAndExpenses=1476300000
  netInterestIncome=19100000
  interestIncome=40100000
  interestExpense=21000000
  depreciationAndAmortization=11800000
  ebitda=73600000
  ebit=61800000
  nonOperatingIncomeExcludingInterest=-21000000
  operatingIncome=40800000
  totalOtherIncomeExpensesNet=0
  incomeBeforeTax=40800000
  incomeTaxExpense=-500000
  netIncomeFromContinuingOperations=41300000
  netIncomeFromDiscontinuedOperations=0
  otherAdjustmentsToNetIncome=-1000000
  netIncome=40300000
  netIncomeDeductions=0
  bottomLineNetIncome=38300000
  eps=2.49
  epsDiluted=2.24
  weightedAverageShsOut=15500000
  weightedAverageShsOutDil=17200000

[2024-FY] (2024-12-31)
  revenue=1176500000
  costOfRevenue=839400000
  grossProfit=337100000
  researchAndDevelopmentExpenses=0
  generalAndAdministrativeExpenses=69500000
  sellingAndMarketingExpenses=135800000
  sellingGeneralAndAdministrativeExpenses=205300000
  otherExpenses=100900000
  operatingExpenses=306200000
  costAndExpenses=1145600000
  netInterestIncome=-700000
  interestIncome=41500000
  interestExpense=42200000
  depreciationAndAmortization=14900000
  ebitda=88000000
  ebit=73100000
  nonOperatingIncomeExcludingInterest=-42200000
  operatingIncome=30900000
  totalOtherIncomeExpensesNet=0
  incomeBeforeTax=30900000
  incomeTaxExpense=0
  netIncomeFromContinuingOperations=30900000
  netIncomeFromDiscontinuedOperations=0
  otherAdjustmentsToNetIncome=0
  netIncome=30900000
  netIncomeDeductions=0
  bottomLineNetIncome=29200000
  eps=1.96
  epsDiluted=1.83
  weightedAverageShsOut=14900000
  weightedAverageShsOutDil=16900000

[2023-FY] (2023-12-31)
  revenue=455000000
  costOfRevenue=378900000
  grossProfit=76100000
  researchAndDevelopmentExpenses=0
  generalAndAdministrativeExpenses=83300000
  sellingAndMarketingExpenses=49300000
  sellingGeneralAndAdministrativeExpenses=132600000
  otherExpenses=90900000
  operatingExpenses=223500000
  costAndExpenses=602400000
  netInterestIncome=-13300000
  interestIncome=32800000
  interestExpense=46100000
  depreciationAndAmortization=12600000
  ebitda=-88700000
  ebit=-101300000
  nonOperatingIncomeExcludingInterest=-46100000
  operatingIncome=-147400000
  totalOtherIncomeExpensesNet=0
  incomeBeforeTax=-147400000
  incomeTaxExpense=0
  netIncomeFromContinuingOperations=-147400000
  netIncomeFromDiscontinuedOperations=0
  otherAdjustmentsToNetIncome=0
  netIncome=-147400000
  netIncomeDeductions=0
  bottomLineNetIncome=-147400000
  eps=-10.24
  epsDiluted=-10.24
  weightedAverageShsOut=14400000
  weightedAverageShsOutDil=14400000

[2022-FY] (2022-12-31)
  revenue=310800000
  costOfRevenue=343000000
  grossProfit=-32200000
  researchAndDevelopmentExpenses=0
  generalAndAdministrativeExpenses=127400000
  sellingAndMarketingExpenses=48000000
  sellingGeneralAndAdministrativeExpenses=175400000
  otherExpenses=90100000
  operatingExpenses=265500000
  costAndExpenses=608500000
  netInterestIncome=-26500000
  interestIncome=8100000
  interestExpense=34600000
  depreciationAndAmortization=13800000
  ebitda=-249300000
  ebit=-263100000
  nonOperatingIncomeExcludingInterest=-34600000
  operatingIncome=-297700000
  totalOtherIncomeExpensesNet=0
  incomeBeforeTax=-297700000
  incomeTaxExpense=0
  netIncomeFromContinuingOperations=-297700000
  netIncomeFromDiscontinuedOperations=0
  otherAdjustmentsToNetIncome=0
  netIncome=-297700000
  netIncomeDeductions=0
  bottomLineNetIncome=-297700000
  eps=-21.11
  epsDiluted=-21.11
  weightedAverageShsOut=14100000
  weightedAverageShsOutDil=14100000

[2021-FY] (2021-12-31)
  revenue=345400000
  costOfRevenue=397300000
  grossProfit=-51900000
  researchAndDevelopmentExpenses=0
  generalAndAdministrativeExpenses=97600000
  sellingAndMarketingExpenses=270200000
  sellingGeneralAndAdministrativeExpenses=367800000
  otherExpenses=101400000
  operatingExpenses=469200000
  costAndExpenses=866500000
  netInterestIncome=-16500000
  interestIncome=3500000
  interestExpense=20000000
  depreciationAndAmortization=16600000
  ebitda=-484500000
  ebit=-501100000
  nonOperatingIncomeExcludingInterest=-20000000
  operatingIncome=-521100000
  totalOtherIncomeExpensesNet=0
  incomeBeforeTax=-521100000
  incomeTaxExpense=0
  netIncomeFromContinuingOperations=-521100000
  netIncomeFromDiscontinuedOperations=0
  otherAdjustmentsToNetIncome=0
  netIncome=-521100000
  netIncomeDeductions=0
  bottomLineNetIncome=-521100000
  eps=-37.62
  epsDiluted=-37.62
  weightedAverageShsOut=13844444
  weightedAverageShsOutDil=13844444
```

### ⚙️ `get_statement`

_input:_ `{"statement": "balance_sheet", "period": "quarter", "limit": 2}`

_returned:_

```
ROOT BALANCE SHEET (quarter, recent first) — full line items:

[2026-Q1] (2026-03-31)
  cashAndCashEquivalents=608900000
  shortTermInvestments=0
  cashAndShortTermInvestments=608900000
  netReceivables=350800000
  accountsReceivables=350800000
  otherReceivables=0
  inventory=0
  prepaids=0
  otherCurrentAssets=0
  totalCurrentAssets=959700000
  propertyPlantEquipmentNet=0
  goodwill=0
  intangibleAssets=0
  goodwillAndIntangibleAssets=0
  longTermInvestments=471500000
  taxAssets=0
  otherNonCurrentAssets=131600000
  totalNonCurrentAssets=603100000
  otherAssets=0
  totalAssets=1562800000
  totalPayables=0
  accountPayables=0
  otherPayables=0
  accruedExpenses=0
  shortTermDebt=0
  capitalLeaseObligationsCurrent=0
  taxPayables=0
  deferredRevenue=0
  otherCurrentLiabilities=0
  totalCurrentLiabilities=0
  longTermDebt=200300000
  capitalLeaseObligationsNonCurrent=0
  deferredRevenueNonCurrent=0
  deferredTaxLiabilitiesNonCurrent=0
  otherNonCurrentLiabilities=927800000
  totalNonCurrentLiabilities=1124900000
  otherLiabilities=0
  capitalLeaseObligations=0
  totalLiabilities=1124900000
  treasuryStock=0
  preferredStock=112000000
  commonStock=0
  retainedEarnings=-1605700000
  additionalPaidInCapital=1931200000
  accumulatedOtherComprehensiveIncomeLoss=400000
  otherTotalStockholdersEquity=0
  totalStockholdersEquity=437900000
  totalEquity=437900000
  minorityInterest=0
  totalLiabilitiesAndTotalEquity=1562800000
  totalInvestments=471500000
  totalDebt=200300000
  netDebt=-408600000

[2025-Q4] (2025-12-31)
  cashAndCashEquivalents=689900000
  shortTermInvestments=0
  cashAndShortTermInvestments=689900000
  netReceivables=332800000
  accountsReceivables=332800000
  otherReceivables=0
  inventory=0
  prepaids=0
  otherCurrentAssets=0
  totalCurrentAssets=1022700000
  propertyPlantEquipmentNet=3200000
  goodwill=0
  intangibleAssets=27600000
  goodwillAndIntangibleAssets=27600000
  longTermInvestments=391400000
  taxAssets=0
  otherNonCurrentAssets=93500000
  totalNonCurrentAssets=515700000
  otherAssets=0
  totalAssets=1538400000
  totalPayables=0
  accountPayables=0
  otherPayables=0
  accruedExpenses=0
  shortTermDebt=2300000
  capitalLeaseObligationsCurrent=0
  taxPayables=0
  deferredRevenue=387400000
  otherCurrentLiabilities=0
  totalCurrentLiabilities=389700000
  longTermDebt=197000000
  capitalLeaseObligationsNonCurrent=2000000
  deferredRevenueNonCurrent=0
  deferredTaxLiabilitiesNonCurrent=0
  otherNonCurrentLiabilities=553400000
  totalNonCurrentLiabilities=752400000
  otherLiabilities=0
  capitalLeaseObligations=2000000
  totalLiabilities=1142100000
  treasuryStock=0
  preferredStock=112000000
  commonStock=0
  retainedEarnings=-1641600000
  additionalPaidInCapital=1922000000
  accumulatedOtherComprehensiveIncomeLoss=3900000
  otherTotalStockholdersEquity=0
  totalStockholdersEquity=396300000
  totalEquity=396300000
  minorityInterest=0
  totalLiabilitiesAndTotalEquity=1538400000
  totalInvestments=391400000
  totalDebt=201300000
  netDebt=-488600000
```

### ⚙️ `get_ownership`

_returned:_

```
INSTITUTIONAL (13F) OWNERSHIP for ROOT (as of 2025-09-30):
  holders=203 (prev 220, change -17)
  13F shares=9468809 (change 43737)
  total invested=$847642481; ownership%=61.4858
```

### ⚙️ `get_insider_activity`

_returned:_

```
RECENT INSIDER TRANSACTIONS (Form 4):
  2026-06-03 Hilsheimer Lawrence A. (director): A-Award 2864 @ 0 -> owns 43859
  2026-06-03 KRAMER NANCY J (director): A-Award 2864 @ 0 -> owns 20480
  2026-06-03 Ulman Doug (director): A-Award 2864 @ 0 -> owns 3983
  2026-06-03 DEVARD JERRI (director): A-Award 2864 @ 0 -> owns 21396
  2026-06-03 Birnbaum Beth A (director): A-Award 2864 @ 0 -> owns 17144
  2026-06-03 Szudarek Julie (director): A-Award 2864 @ 0 -> owns 14696
  2026-06-03 Dorsey Donna (director): A-Award 2864 @ 0 -> owns 12820
  2026-05-21 Forish Ryan (officer: Chief Accounting Officer): F-InKind 351 @ 57.85 -> owns 25100
  2026-05-15 Allison Jonathan (officer: Chief Administrative Officer): S-Sale 1606 @ 55.96 -> owns 68356
  2026-05-12 Allison Jonathan (officer: Chief Administrative Officer): S-Sale 1706 @ 55.74 -> owns 69962
  2026-05-01 Forish Ryan (officer: Chief Accounting Officer): F-InKind 82 @ 55.05 -> owns 25451
  2026-04-07 Allison Jonathan (officer: Chief Administrative Officer): S-Sale 1706 @ 44.35 -> owns 71668
  2026-04-01 Timm Alexander E. (director, 10 percent owner, officer: Chief Executive Officer): M-Exempt 62969 @ 0 -> owns 303861
  2026-04-01 Timm Alexander E. (director, 10 percent owner, officer: Chief Executive Officer): F-InKind 28557 @ 43.26 -> owns 275304
  2026-04-01 Timm Alexander E. (director, 10 percent owner, officer: Chief Executive Officer): F-InKind 14965 @ 43.26 -> owns 244372
  2026-04-01 Timm Alexander E. (director, 10 percent owner, officer: Chief Executive Officer): F-InKind 3480 @ 43.26 -> owns 240892
  2026-04-01 Timm Alexander E. (director, 10 percent owner, officer: Chief Executive Officer): M-Exempt 62969 @ 0 -> owns 83958
  2026-04-01 Bonakdarpour Mahtiyar (officer: President and CTO): M-Exempt 43043 @ 0 -> owns 391717
  2026-04-01 Bonakdarpour Mahtiyar (officer: President and CTO): F-InKind 19198 @ 43.26 -> owns 372519
  2026-04-01 Bonakdarpour Mahtiyar (officer: President and CTO): F-InKind 1642 @ 43.26 -> owns 359556
  2026-04-01 Bonakdarpour Mahtiyar (officer: President and CTO): F-InKind 10882 @ 43.26 -> owns 348674
  2026-04-01 Bonakdarpour Mahtiyar (officer: President and CTO): M-Exempt 43043 @ 0 -> owns 57390
  2026-04-01 Binkley Megan (officer: Chief Financial Officer): M-Exempt 4777 @ 0 -> owns 115971
  2026-04-01 Binkley Megan (officer: Chief Financial Officer): F-InKind 2131 @ 43.26 -> owns 113840
  2026-04-01 Binkley Megan (officer: Chief Financial Officer): F-InKind 8081 @ 43.26 -> owns 111194
```

## Step 2

**🧠 PM reasoning:**

> Root has turned profitable with strong recent earnings, and the common equity position looks solid at roughly $326M with about 17.2M diluted shares outstanding, giving a book value around $19 per share. The accumulated deficit is substantial at $1.6B from historical losses, though that's being offset by the $1.93B in additional paid-in capital. There's also a notable $928M in other non-current liabilities on the balance sheet worth tracking.
> 
> The real driver for valuation will be the combined ratio and policy growth trajectory. I'm seeing ROE metrics that look compelling—around 16-17% for FY2025, though the Q1 2026 annualized run rate appears inflated at roughly 45% due to a particularly strong quarter. I need to dig into the actual underwriting metrics and combined ratio from the 10-K filings to understand what's sustainable. I'm also noting insider transactions around the $44-58 range, but I'll set those aside and focus on independent valuation rather than using market price signals from insider trades.
> 
> I'm going to bring in specialists to analyze this properly—one focused on the insurance fundamentals like combined ratio, loss ratios, written premiums, policies in force, and the Carvana partnership dynamics, and another on the competitive landscape within InsurTech and traditional auto insurance. I should also research how to properly value a growth-stage insurer.

**PM note:** I have the financial skeleton. Root reached profitability (FY24 NI $30.9M, FY25 $40.3M, Q1'26 $35.9M), common book value ≈ $19/share on 17.2M diluted shares, with a $112M senior preferred. Now I need the underwriting engine (combined ratio, loss ratio, gross written premium, policies-in-force, partnerships) and the right valuation lens. Let me delegate deep digs and research the InsurTech valuation framework in parallel.

### ⚙️ `spawn_analyst`

_input:_ `{"role": "P&C insurance / InsurTech specialist", "question": "Reconstruct Root Inc.'s (ROOT) underwriting and growth engine from its 10-K (FY2025) and recent 10-Qs. I need, by year (2021-2025) and latest quarter where available: (1) gross written premium and gross earned premium; (2) net earned premium; (3) GAAP loss ratio, LAE ratio, expense ratio, and COMBINED RATIO (gross and net basis as disclosed); (4) policies-in-force (PIF) and growth; (5) the reinsurance/quota-share structure and how much premium they cede; (6) the partnership channel (Carvana and other embedded partners) \u2014 how big is it, economics; (7) customer acquisition cost trends and marketing spend efficiency; (8) state/geographic expansion count. Also: what does management cite as the sustainable/target combined ratio and the long-term growth algorithm? Give me the actual numbers with citations.", "context": "Root is a telematics-based direct-to-consumer auto insurer, Columbus OH, IPO 2020, did a 1-for-18 reverse split in 2023. FY2025 revenue $1.517B, net income $40.3M (first full profitable year). Common equity ≈$326M Q1'26 + $112M preferred. 17.2M diluted shares."}`

_returned:_

```
ANALYST [a1-p&c] (P&C insurance / InsurTech specialist):
I now have what I need, with the GAAP statements as hard anchors and the KPI/ratio series cross-validated against them. Critically, Root's reported net combined ratios reconcile **exactly** to the GAAP income statement: net combined ratio = (total operating expenses − fee income) ÷ net earned premium → FY2025 (1,455.3 − 78.3)/1,401.7 = **98.2%**; FY2024 (1,098.0 − 66.0)/1,070.9 = **96.4%**; FY2023 (556.3 − 23.4)/399.9 = **133.2%** (10-K FY2025, Item 8 income statement). That gives me high confidence in the decomposition below.

---

# ROOT, INC. — Underwriting & Growth Engine Reconstruction

## Bottom line
Root is now a genuinely profitable, fast-de-risking underwriter. Two things drove the turnaround: (1) a gross loss ratio pulled down to ≈59% (from ≈82%), and (2) a near-total wind-down of quota-share reinsurance (from ceding ≈55%+ of premium in 2021 to mid-single-digits in 2025), which let Root keep the underwriting margin it created. FY2025 was the first *full* clean year of GAAP profit ($40.3M), and Q1 2026 was the most profitable quarter ever (91.4% net combined, 47% annualized ROE). The open question for the PM is durability of *growth*: direct new business is cyclically soft, and management is deliberately trading near-term margin for growth investment (R&D marketing + partnerships).

---

## (1)–(2)–(3) Premiums, loss/expense/combined ratios by year

**Hard GAAP figures** (10-K FY2025, Item 8, Consolidated Statements of Operations): Net premiums earned, Loss & LAE, and the expense lines are as-reported. **Gross written/earned premium, gross loss ratio, and gross combined ratio** are Root's KPI disclosures from its shareholder letters (via research). I reconciled every net combined ratio to the GAAP statement (shown above).

| ($M unless %) | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | Q1'26 |
|---|---|---|---|---|---|---|
| **Gross written premium (GWP)** | ≈$743* | ≈$600–650*† | ≈$770*† | **≈$1,300** | **≈$1,500** | **$389** |
| **Gross earned premium (GEP)** | ≈$720* | n/a† | n/a† | ≈$1,275‡ | ≈$1,475‡ | **$370** |
| **Net earned premium (NEP)** [GAAP] | $310.3 | n/a (≈$258)† | **$399.9** | **$1,070.9** | **$1,401.7** | ≈$345‡ |
| Loss & LAE [GAAP] | — | — | **$331.3** | **$733.0** | **$924.2** | — |
| **Gross loss ratio** (accident-period) | ≈82.0% | ≈82.1% | ≈70%† | **58.9%** | **≈59%** | improving |
| **Gross combined ratio** | **148.6%** | **137.8%** | **≈116.7%** | **94.7%** | **97.1%** | ≈88%‡ |
| **Net loss & LAE ratio** (Loss&LAE÷NEP) | ≈84%* | ≈88%* | **82.8%** | **68.4%** | **65.9%** | — |
| **Net expense ratio** ([opex−fee]÷NEP) | ≈107%* | ≈107%* | **50.4%** | **27.9%** | **32.3%** | — |
| **Net combined ratio** | **≈190.6%*** | **≈195.0%*** | **133.2%** | **96.4%** | **98.2%** | **91.4%** |

\* From Root shareholder letters (Q4'22 letter) via research; not independently re-derived from FY21/22 GAAP (those statements weren't in my pulled FY2025 10-K, which shows 2023–2025 only). †GWP/GEP for FY2022–FY2023 I could **not** pin to an exact published figure — treat as approximate. ‡My estimate from cession rate + GAAP NEP (GEP ≈ NEP ÷ (1−cession)); Q1'26 net combined 91.4% is from Root's Q1'26 disclosure (Seeking Alpha/IR, 2026-05-20). Q1'26 GWP $389M / GEP $370M are from the Q1'26 call (Binkley).

**Key reconciliations (my work, from 10-K Item 8):**
- FY2025 net combined = (1,455.3 total opex − 78.3 fee income) / 1,401.7 NEP = **98.2%** ✓
- FY2024 = (1,098.0 − 66.0) / 1,070.9 = **96.4%** ✓
- FY2023 = (556.3 − 23.4) / 399.9 = **133.2%** ✓ (matches Seeking Alpha 2026-06-01)

**The story in the ratios:** Gross loss ratio collapsed from ≈82% (2021–22) to ≈59% (2024–25) — that's the underwriting fix. Net combined fell from ≈190%+ to sub-100%. Note FY2025 net combined *rose* 1.8 pts YoY (96.4→98.2) **despite the loss ratio improving** (68.4→65.9%) — the entire deterioration is the expense ratio (27.9→32.3%), i.e., deliberate reinvestment in growth/marketing (confirmed by CFO Binkley, Q4'25 call: "deliberate investments in partnership acquisition and direct R&D marketing… modest increase in loss ratio due to elevated seasonality").

---

## (4) Policies-in-force (PIF) & growth

- **FY2024: 414,862 → FY2025: 481,869 PIF (+16.2%)** (Root shareholder letters via research).
- **Q1 2026: +9% YoY** (Timm & Binkley, Q1'26 call). Management noted the YoY comp is distorted because early-2025 PIF was temporarily inflated by tariff-driven shopping ("last year's growth temporarily increased on news of impending tariffs").
- FY2021–FY2023 year-end PIF: I could **not** extract exact figures from the FY2025 10-K (its KPI table only spans 2023–2025 and the tool wouldn't serve that sub-section). Flagging as a gap.
- Forward: management guided to **"accelerating annual PIF growth"** in 2026 (Timm, Q4'25 call), but Q1'26 direct was soft ("a difficult growth environment that intensified throughout the quarter").

---

## (5) Reinsurance / quota-share structure & cession

Root uses excess-of-loss (volatility/cat protection) **plus elective quota share** (surplus relief for a capital-constrained grower). As profitability and statutory surplus improved, it deliberately wound quota share down to retain margin:

| Period | Cession (% of premium) |
|---|---|
| FY2021 | **≈55–58%** (FY21 reinsurance table: direct written $725.9M, ceded $397.3M ≈ 54.7%; earned ceded $409.3M ≈ 57.5%) |
| Q1 2023 | **53.9%** of gross earned premium |
| Q1 2024 | **16.3%** |
| Q4 2024 | **≈6% of written / ≈9% of earned** |
| FY2025 | **mid-single digits**, falling further |

Cross-checks from the balance sheet/cash flow (10-K Item 8): **Prepaid reinsurance premiums fell from $25.1M (2024) to $6.3M (2025)**; **reinsurance premiums payable fell from $32.8M to $2.4M**; reinsurance recoverable & receivable $150.6M→$129.8M. All consistent with a program being run off. Management's own framing (Q3'25): the gross-to-net loss-ratio gap is now **≈1 point** (a 10-pt YoY reduct
```

### ⚙️ `spawn_analyst`

_input:_ `{"role": "insurance industry & competitive-landscape analyst", "question": "Write a deep competitive-landscape brief on the US personal auto insurance industry as it pertains to Root Inc. (ROOT), a telematics-based direct-to-consumer InsurTech. Cover: (1) industry structure, size, growth, and the current hard-market/pricing cycle in personal auto; (2) how telematics/usage-based insurance (UBI) actually works and whether it confers a durable pricing/loss-ratio advantage; (3) head-to-head vs the relevant competitors \u2014 Progressive, GEICO, State Farm, Allstate, and InsurTech peer Lemonade (LMND) \u2014 on scale, technology, loss ratios, distribution, and customer acquisition cost; (4) Root's embedded/partnership distribution strategy (Carvana stake/partnership) vs the incumbents' moats; (5) does Root have a defensible competitive advantage, or is it structurally disadvantaged on scale and cost of capital? Be specific and skeptical.", "context": "Root scaled revenue from $455M (2023) to $1.52B (2025) and turned profitable. It uses a mobile app + telematics to price auto risk and sells D2C plus through embedded partners. Carvana owns a stake / has a partnership."}`

_returned:_

```
ANALYST [a2-insurance] (insurance industry & competitive-landscape analyst):
# Root, Inc. (ROOT) — Competitive-Landscape Brief: US Personal Auto Insurance

**Prepared for the PM | Desk: Insurance & Competitive Landscape**

---

## BOTTOM LINE UP FRONT

Root is a genuinely better *auto underwriter* than its insurtech peer Lemonade and has, for the first time, demonstrated a sustainable full-stack model (FY2025 revenue $1.52B, net income $40.3M, Q1-FY2026 annualized ROE 47%). Its telematics-first pricing is real and additive, and its embedded/agent distribution gives it a credible, lower-CAC growth vector the incumbents are slower to copy. **But it is not structurally advantaged versus the incumbents on the two things that ultimately win in commoditized auto insurance: scale and cost of capital.** Root writes ≈$1.5B of premium into a ≈$359B market (≈0.4% share); Progressive *alone* spent ≈$3.5B on advertising in 2024 — more than 2x Root's entire premium base — and runs an 88.8 combined ratio vs. Root's ≈97; GEICO runs 81.5; Berkshire funds GEICO with ≈$171B of negative-cost float while Root funds growth with equity and a SOFR+600bps term loan. The telematics "moat" is real but **partially buyable and largely already replicated by the scaled incumbents who started earlier.** Root's defensible edge, to the extent one exists, is narrow: a modern, API-native technology stack that lets it win *embedded* distribution (Carvana, Toyota/Hyundai, independent-agent integrations) faster than 100-year-old incumbents can re-platform — not a durable pricing or loss-ratio advantage. The investable question is whether Root can compound that distribution edge into enough scale to matter before incumbents close the technology gap. **The skeptic's case — that Root is a well-run sub-scale price-taker in an oligopoly with a permanent cost-of-capital disadvantage — is strong and not yet refuted by the numbers.**

---

## 1. Industry Structure, Size, Growth & the Pricing Cycle

**Size and structure.** US private-passenger auto is the single largest P&C line — roughly **$359B in direct premiums written in 2024**, ≈35% of all US P&C premium, up **12.6–13.3% YoY** (S&P Global Market Intelligence; NAIC market-share report). It is a concentrated oligopoly: the **top five carriers held 63.6% share in 2024**, up from 62.5% in 2023 — concentration is *rising*, not fragmenting (NAIC). Approximate 2024 shares:

| Carrier | Personal-auto share | Note |
|---|---|---|
| State Farm | ≈16–19% | #1 on NAIC PPA basis |
| Progressive | ≈16–17% | **#1 on A.M. Best basis; fastest grower (+22–24% DPW)** |
| Berkshire (GEICO) | ≈10–12% | |
| Allstate | ≈8–10% | |
| USAA | ≈5–6% | |
| **Root** | **≈0.4%** | $1.5B GPW into a ≈$350B market (Q4-FY2025 call, Timm) |

The headline structural shift of the cycle: **Progressive overtook State Farm as the #1 auto writer on the A.M. Best basis in 2024** (16.4% vs. 16.2%), with Progressive's DPW +22.2% to $70.8B — the direct/telematics model taking share from the captive-agent model (A.M. Best).

**The pricing cycle.** Personal auto just completed a violent hard-market round trip driven by post-COVID claims inflation (parts, labor, used-car values, medical, litigation/"legal system abuse"):

- **Net combined ratio: 112.2 (2022) → ≈105 (2023) → 95.3 (2024)** — a ≈17-point swing back into solid underwriting profit, the best result since pre-pandemic (S&P GMI; A.M. Best).
- The lever was **≈54% cumulative rate increase 2020–2024** (auto insurance CPI rose 20.6% YoY in Jan-2024 alone) (BLS/CPI; S&P RateWatch ≈11% countrywide filed increase through Aug-2023).
- **2025 turned soft:** with profitability restored, average full-coverage premiums **fell ≈6% nationally in 2025** (Insurify).

**Why this matters for Root.** Root scaled revenue from $455M (FY2023) to $1.18B (FY2024) to $1.52B (FY2025) and flipped from a $147M net loss to $40M net income (get_financials) — i.e., **its turnaround coincided exactly with the industry's hard-market rate-earn-through.** A skeptic must ask how much of Root's profitability is idiosyncratic skill versus riding the same ≈50% rate wave every carrier rode. Management itself now flags a *softening* direct market: on the Q1-FY2026 call, Timm described "a difficult growth environment that intensified throughout the quarter" in direct, and GPW *declined* 5% YoY to $389M (partly a tariff-demand comp). The cycle is turning against new-business pricing just as Root needs to grow — a material near-term headwind.

---

## 2. How Telematics/UBI Actually Works — and Is the Edge Durable?

**Mechanics.** Telematics prices risk on *observed driving behavior* rather than only demographic proxies. Two archetypes:

- **Progressive Snapshot** (the incumbent model): an *add-on rating modifier* layered on top of a full traditional rating plan. Via OBD-II dongle or app, it scores **hard braking, rapid acceleration, time-of-day (night driving), and mileage**; the dominant signal is the **hard-brakes-per-mile ratio**. It is **two-sided** — ≈20% of users can be *surcharged*, not just discounted.
- **Root** (the insurtech model): telematics is the *primary underwriting and rating variable, not an add-on*. A 2–3 week "test drive" uses the phone's accelerometer/gyroscope to score braking, cornering, acceleration, time-of-day, mileage, consistency and distraction over ≈500 miles. Critically, **Root uses the score to *decline* bad risks**, not merely price them — driving score is "the No. 1 factor" in the rate.

**Does the signal work?** Yes, and the actuarial evidence is consistent:
- Telematics adds **≈79% additional lift above standard rating factors** and **8.7x claim-frequency separation** top-to-bottom decile (LexisNexis production model) — it roughly *doubles* segmentation power.
- Behavioral variables can render classic proxies **redundant** (the Verbelen/Antonio study found telematics makes *gender* redundant as a rating factor).
- **Mileage is the most powerful exposure variable** (Lemaire 
```

### ⚙️ `research`

_input:_ `{"question": "How do investors value a fast-growing, recently-profitable telematics auto InsurTech like Root Inc.? What valuation metrics and multiples matter (price/book, combined ratio, policies-in-force growth, gross written premium multiples), and how have Root and Lemonade been valued? What is a reasonable sustainable ROE and combined ratio for a scaled auto insurer?"}`

_returned:_

```
RESEARCH — How do investors value a fast-growing, recently-profitable telematics auto InsurTech like Root Inc.? What valuation metrics and multiples matter (price/book, combined ratio, policies-in-force growth, gross written premium multiples), and how have Root and Lemonade been valued? What is a reasonable sustainable ROE and combined ratio for a scaled auto insurer?
I'll research how investors value telematics auto InsurTech companies like Root, looking at the relevant metrics, multiples, and benchmarks.Let me run searches one at a time to avoid timeouts.Good, now it works. Let me run the searches sequentially with a helper function.Let me get a couple more specifics on valuation multiples and Lemonade's price/sales, plus how investors frame these names.I have enough detail. Let me grab a couple of fine data points on Root's combined ratio and Lemonade's loss ratio to round out the benchmarks.I now have a solid evidence base. Here's the synthesis.

# Valuing a telematics auto InsurTech (Root, Lemonade & peers)

## 1. The core valuation framework

These businesses sit at the intersection of **a P&C insurance carrier** (balance-sheet, regulated capital, underwriting risk) **and a high-growth tech/distribution story**. Investors therefore blend two lenses:

**(A) Insurance-carrier lens — book-value / ROE based.** A scaled, steady-state insurer is normally valued on **Price/Book (or Price/Tangible-Book) calibrated to its sustainable ROE.** The intuition: a carrier earning ROE = cost of equity should trade ≈1.0x book; excess ROE justifies a premium to book. The academic/actuarial approach (CAS) values a P&C insurer as the present value of future underwriting + investment profits discounted at cost of capital, with the value/premium (V/P) ratio falling directly out of expected profit margins. The combined ratio is calculated as incurred losses and operating expenses divided by premiums earned, and it is expressed as a percentage; you can assess how accurately an insurance company prices its premiums and ensures profits for shareholders.

**(B) Growth/tech lens — premium- or revenue-multiple based.** Because Root and Lemonade grow premiums 20–30%+/yr and only recently turned (or are nearing) profit, the market also looks at multiples of **In-Force Premium (IFP) / Gross Written Premium (GWP)** and of **revenue**, much like a SaaS multiple, with the multiple scaled by growth rate, loss-ratio trajectory and unit economics.

**Important caveat on GWP multiples:** practitioners increasingly distrust them. Gross Written Premium is no longer treated as a credible basis for valuation in most deals; it's widely viewed as a volume metric, not a value metric. Instead, the market has shifted toward Net Revenue, Net Commission for MGAs, or Earned Premium. GWP multiples are a quick screening shorthand, not a substitute for a profitability-based valuation.

## 2. The metrics/drivers that actually move the valuation

| Driver | Why it matters |
|---|---|
| **Combined ratio (loss ratio + expense ratio)** | The single most important profitability gauge. Below 100 = underwriting profit; above = underwriting loss. For telematics players the *loss ratio* is the proof their data/pricing edge is real. |
| **Policies-in-force (PIF) & IFP/GWP growth** | Validates the growth thesis and operating leverage. |
| **CAC / unit economics / LTV-to-CAC & payback** | Determines whether growth creates or destroys value; heavy marketing spend depresses near-term GAAP earnings. |
| **Gross profit / "direct contribution," adj. EBITDA, GAAP net income** | The bridge from a "premium multiple" to an "earnings multiple" as the company scales. |
| **Book value, capital adequacy, reserve adequacy** | Insurance is balance-sheet intensive; growth consumes statutory capital, so ROE and surplus matter. |
| **Reinsurance/quota-share structure** | Distinguishes *gross* vs *net* economics — critical, since Root cedes a large share, so net combined ratio ≠ gross. |

## 3. How Root and Lemonade have actually been valued

**Root (ROOT) — fundamentals:**
- Root achieved its first profitable year in 2024, with GAAP net income of $31 million, adjusted EBITDA of $112 million, gross premiums written of $1.3 billion, and policies in force growing 21% year over year to more than 414,000.
- Underwriting quality has improved markedly: gross loss ratio was 59% for the full year 2024 and gross combined ratio was 95% for the full year 2024. The net combined ratio is higher due to heavy reinsurance — net combined ratio improved 52 points to 91% in Q3 2024.
- Momentum continued: Root reported year-to-date net income of $35 million through Q3 2025, with unencumbered capital of $309 million and double-digit growth in policies in force and premiums.
- **Valuation marker:** Root trades on Price/Book, and the multiple has compressed sharply as book value grew and the stock cooled. Root's Price-to-Book (P/B) ratio decreased from 8.87x in Q1 2025 to 3.94x in Q4 2025. A ≈4–9x book multiple is *far* above a mature carrier (≈1–2x), reflecting embedded growth and the bet on a sustainably low loss ratio.

**Lemonade (LMND) — fundamentals (broader InsurTech, not pure auto):**
- Lemonade's In Force Premium reached $1,008 million in Q1 2025, growing 27% YoY — its sixth consecutive quarter of accelerating growth — while revenue also grew 27%; it crossed the $1 billion IFP mark in March.
- It is still pre-profit on an adjusted basis: full-year 2025 guidance was for IFP of $1,218–$1,223 million, gross earned premium of $1,044–$1,047 million, revenue of $727–$732 million, and an adjusted EBITDA loss of roughly $130 million.
- **Valuation marker:** Because it is not yet profitable, Lemonade is valued primarily on a **multiple of IFP / revenue** scaled by its growth rate and loss-ratio improvement — the classic "growth lens." Note the gap between IFP (≈$1.0–1.2bn) and revenue (≈$0.7bn) reflects heavy reinsurance ceding, so an IFP multiple overstates value vs. a revenue multiple.

```

## Step 3

**🧠 PM reasoning:**

> Now I'm thinking through the valuation framework for Root. Since it's a financial services business with strong growth momentum and recently turned profitable, I should model this as a multi-stage scenario where book value compounds at elevated returns for several years before normalizing to a mature P/B multiple. I'm starting with the Q1 2026 common equity of $325 million as my baseline.
> 
> But I need to nail down the fully diluted share count because the Carvana convertible preferred and warrant overhang are material to the per-share value. The diluted count of 17.2 million likely doesn't fully capture the convertible preferred conversion shares and the warrants that could represent up to 29.9% of the company, so I should get clarity on the precise dilution scenario before anchoring my valuation.
> 
> For the valuation itself, I'm weighing two approaches: using excess returns with a warranted P/B based on sustainable ROE and growth, which captures the Gordon-growth structure but assumes perpetual constants, versus a multi-stage model where book value compounds at the retained ROE for several years before applying a terminal P/B and discounting back. The key driver is nailing sustainable ROE, which depends on the mid-cycle combined ratio and investment income. I'm seeing the net combined ratio trending from 98.2% in FY2025 down to 91.4% in Q1'26, so a 95-97% mid-cycle target seems reasonable, giving 3-5% underwriting margin on net earned premiums. With roughly $1.08 billion in investments and cash earning 4-5%, I need to build out the ROE components from realized earnings—FY2025 net income was $40.3 million on common equity, so I'll work backward from there to establish what sustainable ROE is achievable. The real driver of Root's high ROE is the leverage—running premium-to-surplus at 4x is aggressive but sustainable with their reinsurance structure. The bull case hinges on maintaining 15-30% annual growth with a 95% combined ratio and 20%+ ROE for years, compounding book value; the bear case is a softening cycle, stalled growth, combined ratio creep, and warrant dilution bringing ROE back to 12-15%. I need to nail down the share count picture—specifically the fully-diluted shares, the conversion mechanics on that $112M preferred (likely the Carvana convertible), and the warrant dilution exposure up to 29.9%, then value this as a compounder using book-value growth and terminal P/B multiples.

**PM note:** I now have the underwriting engine, the competitive read, and the valuation framework. Two things are critical before I value: (1) the precise fully-diluted share count including the Carvana convertible preferred and warrant overhang, and (2) statutory capital/investment yield to normalize ROE. Let me close those gaps.

### ⚙️ `ask_analyst`

_input:_ `{"analyst_id": "a1-p&c", "question": "I need to nail the share count and capital structure for a per-share valuation. From the latest 10-Q (Q1'26) and FY2025 10-K, give me precisely: (1) Basic and diluted weighted-average shares, AND the actual shares outstanding at the cover date (Class A + Class B). (2) The Carvana convertible preferred ($112M carrying value): exact conversion terms \u2014 how many COMMON shares does it convert into, at what price, post-reverse-split? Is it the same $112M 'preferred' on the balance sheet? (3) The full Carvana warrant overhang: how many warrant shares are vested/outstanding vs unvested, and their strike prices (post-split). (4) Total options/RSUs outstanding. So: what is the TRUE fully-diluted share count if preferred converts and in-the-money warrants/options exercise? (5) Statutory surplus / capital at the insurance subsidiaries and any RBC commentary, plus the net investment yield on the ≈$1.08B investment+cash portfolio. I want to compute a normalized ROE and a fully-diluted per-share book value."}`

_returned:_

```
ANALYST [a1-p&c] (P&C insurance / InsurTech specialist) follow-up:
I now have the capital-structure detail. Before the numbers, one correction to flag for your model: the **reverse split was effective August 12, 2022** (not 2023) — that's what set the $162 conversion price. And a data-vendor warning: the FMP "book value/share = $28.07" figure is **wrong for common valuation** — it includes the $112M preferred and uses a low share count. The correct common BVPS is ≈$18–21 (derived below).

---

# ROOT, INC. — Share Count & Capital Structure for Per-Share Valuation

## (1) Shares outstanding & weighted-average shares

| | Class A | Class B | Total |
|---|---|---|---|
| **Outstanding 12/31/2025** (10-K balance sheet, Item 8) | 13.7M | 1.8M | **≈15.5M** |
| **10-K cover date (2/18/2026)** | 13,748,408 | ≈1.8M | ≈15.5M |
| **Q1'26 10-Q cover date (4/29/2026)** | not extracted* | not extracted* | ≈15.5–15.7M* |

Weighted-average shares (10-K Item 8 income statement; both classes combined):
- **FY2025: Basic 15.4M / Diluted 17.1M** (diluted EPS $2.36, basic $2.49)
- FY2024: Basic 14.9M / Diluted 16.9M
- FY2023: Basic 14.4M / Diluted 14.4M (anti-dilutive — net loss)
- **Q1'26: diluted ≈17.2M** (FMP); exact basic/diluted WAS not pulled.*

\*The Q1'26 10-Q cover share count and the exact Q1'26 basic/diluted WAS were not retrievable through my filing tool (it serves only fixed item chunks). The $75M buyback was authorized **May 4, 2026** — *after* quarter-end — so no Q1'26 repurchase affected the count. Class B (super-voting) steadily converts to Class A (4.0M→1.8M over 2024–25).

---

## (2) Carvana convertible preferred ($112M) — conversion terms

- **It is the same $112.0M "preferred" on the balance sheet** — Root's **Series A Redeemable Convertible Preferred Stock**, held by Carvana. Carried at **$112.0M**, with a **redemption/liquidation value of $126.5M** (10-K Item 8 balance sheet). It sits in the **mezzanine** (between liabilities and equity) and is a **senior claim ahead of common**.
- **14,053,096 preferred shares** outstanding (rounds to "14.1M" on the balance sheet).
- **Converts into just 780,727 shares of Class A common**, at a **$162.00 conversion price** (= original $9.00 × the 1-for-18 reverse split effected **Aug 12, 2022**).
- **Critical point:** with ROOT trading ≈$55–95, the $162 conversion is **deeply out-of-the-money** → Carvana will not convert; economically this is a **$126.5M senior preferred claim, not 0.78M common shares**. For book-value-to-common you should **deduct the preferred**, not add the shares.

This reconciles to GAAP diluted shares: 15.4M basic + 0.78M preferred (if-converted, dilutive for EPS) + ≈0.9M options/RSUs ≈ 17.1M — i.e., the preferred adds <0.8M shares, *not* 14M.

---

## (3) Carvana warrant overhang

Eight tranches issued to Carvana (2021), all **out-of-the-money with zero intrinsic value at 12/31/2025**:

| | Tranches | Strikes (post-split) | Expiry | Status |
|---|---|---|---|---|
| Short-term | 3 | $180.00–$216.00 | **Expired Sept 1, 2025** | Expired worthless (incl. original Tranche 1 of 2,365,841 sh) |
| Long-term | 5 | $180.00–$540.00 | Sept 1, 2027 | Partially vested |

Long-term vesting (from Carvana 13D/A tracking the milestones):
- **Vested/exercisable: 2,927,727 shares** = Tranche 1 (1,435,820 sh, exercisable 9/1/2025) + Tranche 2 (1,491,907 sh, exercisable 2/28/2026).
- **Remaining long-term tranches (3–5): unvested**, milestone-based, expiring 9/1/2027.
- Warrant comp expense FY2025 **$19.2M** (non-cash); ≈$7.8M unrecognized at 12/31/25 over ≈1.75 yrs.

**Valuation takeaway:** every warrant is struck at **$180–$540** vs. a ≈$55–95 stock → **zero dilution** in any realistic near-term scenario. They only matter if ROOT roughly triples-to-6x. Ignore in fully-diluted unless you're stress-testing a very high price.

---

## (4) Options & RSUs outstanding (12/31/2025)

- **Options: 100,000 outstanding**, weighted-avg exercise price **$34.80**, ≈2.3 yr remaining (in-the-money). Essentially de minimis.
- **Unvested equity awards (RSUs/PSUs): ≈1.3M**, of which up to ≈0.6M scheduled to vest in 2026 (10-K). FY2025 stock-comp expense $40.1M (Item 8 cash flow). *(Exact RSU rollforward ending balance not extractable from snippets — verify in the SBC note; 1.3M is the disclosed "unvested equity awards" aggregate.)*

---

## TRUE fully-diluted share count

| Component | Shares | In-the-money? |
|---|---|---|
| Common outstanding (12/31/25) | ≈15.5M | — |
| + Preferred as-converted | +0.78M | No ($162 strike) — but GAAP-dilutive |
| + Unvested RSUs/PSUs (no strike) | +≈1.3M | Yes (vest over time) |
| + Options (ITM) | +0.1M | Yes ($34.80) |
| + Warrants | **+0** | **No — all $180–$540, OTM** |
| **Realistic fully-diluted** | **≈17.5–17.7M** | |

So the **economically relevant fully-diluted count is ≈17.5–17.7M** (matches the ≈17.1M GAAP diluted WAS, point-in-time slightly higher). The "headline" 29.9% Carvana ownership (preferred + all warrants ≈ 0.78M + ≈7M warrant shares) is a **theoretical maximum that only materializes at a multiple of today's price** — do not use it for base-case per-share math.

---

## (5) Statutory capital / RBC and investment yield

**RBC / statutory (10-K):**
- Three insurance subs: Root Insurance Co. & Root P&C (Ohio-domiciled), Root Florida (new, 2025); plus Root Re (Cayman).
- **All subsidiaries above company-action RBC levels at 12/31/2025;** regulators require Root (given short operating history) to hold **RBC > 200% of authorized control level.**
- **Unencumbered capital ≈$312M** at YE2025 (mgmt; $309M at Q3'25). Management repeatedly states the subs carry **excess capital** ("position of excess capital across our insurance subsidiaries," Q3'25 call).
- **Exact per-subsidiary statutory surplus dollars at 12/31/2025 were not retrievable** (the statutory-information note wouldn't serve through my tool). For method/scale: FY2023 totals were $81.4M ($60.1M RIC + $21.3M R&PC). **Pull the exact FY2025 figures from the 10-K "
```

### ⚙️ `get_transcripts`

_returned:_

```
EARNINGS CALL TRANSCRIPTS (most recent first):

=== Q1 FY2026 (2026-05-07) ===
Operator: Ladies and gentlemen, greetings, and welcome to the Root, Inc. Q1 '26 Earnings Conference Call. [Operator Instructions] As a reminder, this conference is being recorded. It is now my pleasure to introduce your host for today, Matt LaMalva, Head of IR and Corporate Development. Please go ahead.
Matthew LaMalva: Good afternoon and thank you for joining us. Root is hosting this call to discuss its first quarter 2026 earnings results. Participating on today's call is Alex Timm, Co-Founder and Chief Executive Officer; and Megan Binkley, Chief Financial Officer. Earlier today, Root issued a shareholder letter announcing its financial results. We'll focus today on how we're executing against our model and the progress we're delivering across the business. While today's discussion will reflect the shareholder letter for more complete information about our financial performance, we also encourage you to read our first quarter 2026 Form 10-Q, which was filed with the Securities and Exchange Commission today. Before we begin, I want to remind you that matters discussed on today's call will include forward-looking statements related to our operating performance, financial goals and business outlook, which are based on management's current beliefs and assumptions. Please note that these forward-looking statements reflect our opinions as of the date of this call, and we are not obligated to revise this information as a result of new developments that may occur. Forward-looking statements are subject to various risks, uncertainties and other factors that could cause our actual results to differ materially from those expected and described today. For a more detailed description of our risk factors, please review our most recent 10-K, 10-Q and shareholder letter. A replay of this conference call will be available on our website under the Investor Relations section. I would also like to remind you that during the call, we will discuss some non-GAAP measures while talking about Root's performance. You can find reconciliations of these historical measures to the nearest comparable GAAP measures in our financial disclosures, all of which are posted on our website at ir.joinroot.com. I will now turn the call over to Alex.
Alexander Timm: Thanks, Matt. Good afternoon, and thank you, everyone, for joining us. We kicked off 2026 with the most profitable quarter in the company's history, generating an annualized ROE of 47%. The team has worked hard to deliver these fantastic results, and we're all grateful for their hard work. These results reflect a structurally stronger model driven by improvements in pricing, underwriting and capital allocation. On growth, we grew policies in force over 9% in the quarter year-over-year with gross premiums written of $389 million. Recall that last year's growth temporarily increased on news of impending tariffs, making year-over-year comparisons difficult. As a reminder, we continue to be focused on our 5-part growth strategy: one, create the lowest prices for customers; two, launch our product in every state; three, expand into the independent agency channel; four, scale our embedded insurance products; and five, leverage our AI expertise to grow our automated marketing machine. Some highlights from the quarter. On distribution, we're continuing to build a platform that is both diversified and scalable, which is very important to our long-term growth trajectory. Our overall partnerships grew new writings 30% year-over-year. On independent agents, we now partner with more than 15,000 agents across 5,000 agencies nationwide. In the first quarter, we launched our partnership with Freeway Insurance, the largest personal lines insurance distributor in the country. We're very excited by the prospects of continuing to scale in this channel, bringing products that are easier for agents and more affordable for customers to an over $100 billion market. As our models have continued to learn in this space, we were able to materially improve our pricing for this segment of our business in the first quarter as well. We also continue to scale our embedded insurance offering with Carvana now surpassing 200,000 policies sold. This channel allows us to present nearly frictionless insurance at the point of need, creating a great experience for customers. In addition, this allows for the potential to create new pricing models distinct to each partner, leveraging their unique data, including connected vehicle data, which is critical to our long-term AV strategy. In direct, we saw a difficult growth environment that intensified throughout the quarter. These cycles are common in our industry, and we are well positioned to manage them prudently, only deploying your capital when we see meaningful opportunities to exceed our hurdle rate. When conditions are attractive, we invest aggressively. When they are not, we remain disciplined and patient. This creates some fluctuations in our quarterly growth. But over the long term, we believe it creates much better outcomes for our shareholders. We believe a key source of value is our ability and willingness to act differently from the crowd and maintain our long-term orientation. Regardless of the cycle, we always invest in our technology and customer experiences that makes Root special. And right now, we are living in one of the most exciting times in technology that we've seen in our lifetimes. Since our inception, our founding principles lie at the heart of AI. We were born out of the forces of mathematical invention. And now the advancements of this technology have perfectly situated our strategy for acceleration. We are actively working to build a completely automated insurance company that will be the first of its kind. This allows us to create a closed loop tying customer acquisition, onboarding, pricing, underwriting and claims, together in one technical system. W
```

## Step 4

**🧠 PM reasoning:**

> I'm pulling together the capital structure details: common equity of about $326M with roughly 15.5M basic shares outstanding, translating to a book value per share around $18-21 depending on dilution assumptions. The preferred stock at $112M carrying value is senior and deeply out of the money as a convert, so I'm treating it as a senior claim. The warrants are all underwater at their strike prices, so they don't factor into the base case valuation.
> 
> Looking at the operating performance, last year generated $38.3M in net income to common shareholders with a 15.7% return on equity, though the most recent quarter showed an annualized 47% ROE which clearly isn't sustainable. The combined ratio has been improving—down to 91.4% in Q1'26 from 98.2% last year—and they're targeting a 60-65% loss ratio. The investment portfolio is yielding only 3.4% because they're holding 62% in cash, which represents meaningful upside if they can deploy that more productively. Premium growth is solid at 16% last year with partnerships driving about half of new business, and they're expanding geographically with plans to reach all contiguous states by 2027. There's no dividend currently, but they authorized a $75M buyback in May.
> 
> For valuation, I need to recognize this is a growth insurer with no dividend, so the book value compounds at the ROE as earnings are retained. The right framework is projecting book value per share forward through a multi-stage model, applying a terminal price-to-book multiple that reflects mature returns, then discounting back at the cost of equity. I'm starting to build out the cost of equity assumptions, beginning with the risk-free rate around 4.3%.
> 
> Now I'm working through the cost of equity calculation, factoring in Root's volatility as a small InsurTech company, the equity risk premium, and a size premium for the micro-cap nature of the business. The key question is what sustainable ROE to use going forward—the current 15.7% is depressed by excess capital and low investment yields, but normalizing for better combined ratios and operating leverage could push it toward 18-22%, though cyclical pressures might bring it down to 15-18% through the cycle.
> 
> For normalized earnings, I'm building up from the current premium base of roughly $1.45B, calculating underwriting margin at a 96% combined ratio, adding investment income on the portfolio, and subtracting interest and SBC expenses. The key insight is that GAAP net income already captures the SBC dilution, so I'm not double-counting. Q1'26 showed $36M in earnings, suggesting the run-rate is well above the $40M baseline from last year, though I need to account for seasonality and whether that pace is sustainable.
> 
> On the valuation side, I'm cross-checking two approaches: a P/E multiple on normalized earnings of around $75M (roughly $4.24 per share), which at a 10-12x multiple for a mature insurer gives $42-51, versus a price-to-book approach using the warranted P/B formula based on ROE, cost of equity, and growth. The P/B method yields about 1.55x book value, or roughly $28.50, which is lower. The divergence comes from the high leverage amplifying ROE relative to book value, so the earnings multiple approach is capturing that leverage benefit while the P/B approach is more conservative. I'm trying to reconcile whether a 22% ROE is actually sustainable given the capital structure.
> 
> The key insight is that Root isn't in steady state—it's growing premium in force at 10-20% annually with significant runway ahead (tiny market share, state expansion, agent channel growth). A simple Gordon growth model with 3% growth understates the value because it doesn't account for this high-growth phase. I need to build a multi-stage model that projects higher book value and earnings growth for the next 5-7 years before fading to maturity. I'm thinking through a book-value compounding approach where equity grows at the ROE, adjusted for share dilution from stock-based compensation running around 3-4% annually.
> 
> For the terminal value, I'd apply a mature P/B multiple—if ROE settles around 16-18% with a 13% cost of equity and 4% long-term growth, that gives a warranted P/B of roughly 1.33-1.56x. The cleanest approach is probably to use an excess returns model as a floor anchor, then layer in scenario analysis to capture the high-growth upside.
> 
> Let me work through a multi-stage model that projects book value per share forward over 7 years, assuming the company maintains strong ROE while managing share dilution through buybacks. If book value compounds at around 16% annually and I apply a 1.5x terminal P/B multiple, discounting back at the 14% cost of equity, I get a fair value around $31 per share. That assumes the equity base grows from $326M to roughly $920M over the period, with all earnings retained and reinvested.
> 
> Now I'm building out probability-weighted scenarios across the key drivers—sustainable ROE, premium growth trajectory, and terminal valuation multiple. In the upside case where Root sustains 18-20% ROE with 15%+ premium growth, book value compounds faster at 18% annually, reaching $58.60 per share by year 7, and with a 1.7x terminal multiple that values out to around $40 per share. The base case assumes a more moderate 16% ROE with 14% book growth and a 1.4x terminal multiple.
> 
> I'm also stress-testing downside scenarios—one where growth stalls and combined ratios drift higher, compressing ROE to 10% and the terminal multiple to 1.0x, and an adverse case with deteriorating underwriting that could trigger dilution. Weighting these scenarios by probability gives me a fair value around $26 per share, with a reasonable band from roughly $13 on the low end to $40 on the high end. For the floor, I'm using a conservative normalized earnings approach with 16% ROE and modest 3% growth to anchor a minimum intrinsic value.
> 
> Now I'm reconciling the floor estimate—the current normalized earnings power is running high because the loss ratio is benched below target, so there's some cyclical tailwind baked in. Through-cycle normalized earnings would be lower, maybe $55-65M. That gives me a P/B-based floor around $22, which feels more honest than a P/E multiple that might overstate sustainable earning power. I'm also refining the share count—using a fully diluted 17.7M to account for RSU vesting and the impact of buybacks, which is more realistic for per-share intrinsic value. And I need to revisit the cost of equity assumption—14% might be reasonable for a post-turnaround micro-cap with elevated volatility, but I should double-check the beta and size premium components.
> 
> Now I'm settling on 14% as my central discount rate and running a peer cross-check. Looking at comparable companies' P/B multiples and ROEs, Root's valuation of around $24-31 per share on a P/B basis aligns with my $26 fair value estimate, which is reassuring. Next I'm setting up the valuation engine to compute the worked book-compounding scenarios using a formula approach—letting the code handle the arithmetic for each scenario with a 7-year horizon, starting book value of $18.4, and the 14% cost of equity.
> 
> I'm now calculating the precise values for each scenario by working through the formula with the specific growth rates and P/B multiples, computing the compounded growth factors and discounting them back.
> 
> The weighted average across all four scenarios gives me a fair value of approximately $25.80 per share, with a reasonable valuation band ranging from $18 to $36, and an intrinsic floor around $20. I'm verifying the book value per share calculation from the Q1'26 equity data, which checks out at $18.41, and confirming that a 7-year high-growth horizon is appropriate given the company's growth drivers and ROE profile.
> 
> Now I'm setting up the composite valuation method and gathering the necessary citations from the financial statements before running the full calculation.

**PM note:** I now have everything needed: the underwriting engine, capital structure, dilution, and the valuation framework. Root is a financial/spread business (auto insurer) with a strong growth overlay — best valued on book value compounding at a sustainable ROE, with the growth runway captured in a multi-stage frame and cross-checked against warranted P/B and peers.

Let me reconcile the key inputs and compute. Common book (Q1'26): $325.9M ÷ ≈17.7M fully-diluted = $18.4/share; the $112M ($126.5M redemption) Carvana preferred is a senior deduction (deeply OTM convert), and warrants ($180–$540 strikes) are OTM and ignored. Let me run a probability-weighted composite (FMV) plus an excess-returns cross-check (floor).

### ⚙️ `compute_valuation`

_input:_ `{"method": "composite", "rationale": "Root is a recently-profitable, fast-growing telematics auto insurer with a long growth runway (0.4% share of a $350B market, state expansion to all contiguous states by 2027, embedded/agent channels ≈half of new writings). The dominant value driver is book value compounding at a high but cyclical ROE with no dividends (earnings fully retained). I therefore value it as multi-stage book-value-per-share compounding: BVPS today \u00d7 (1+g)^7 \u00d7 terminal P/B, discounted at a 14% cost of equity (rf 4.3% + beta 1.5\u00d75% ERP + 3% micro-cap/illiquidity premium). I integrate the key uncertain drivers \u2014 sustainable ROE/book-growth and the terminal multiple \u2014 across four probability-weighted scenarios to a single expected FMV. BVPS_0 = $18.4 (common equity $325.9M \u00f7 17.7M fully-diluted, preferred deducted as a senior claim).", "composite": {"scenarios": [{"name": "Compounder works \u2014 durable 18% ROE, share gains", "probability": 0.3, "sub_method": "worked", "rationale": "Telematics pricing + embedded/agent distribution sustain ≈15%+ premium growth and ≈18-20% ROE; book compounds ≈18%/yr for 7 yrs, terminal P/B 1.7x on a de-risked, scaled book.", "worked": {"framework": "BVPS compounding to terminal P/B, PV at CoE", "key_inputs": {"bvps0": 18.4, "g": 0.18, "n": 7, "pb": 1.7, "coe": 0.14}, "formula": "bvps0*(1+g)**n*pb/(1+coe)**n"}}, {"name": "Solid grower \u2014 base case, 16% ROE", "probability": 0.4, "sub_method": "worked"`

_returned:_

```
VALUATION (composite): fair value/share = 25.7663
equity_value=None EV=None
working={"branches": [{"name": "Compounder works \u2014 durable 18% ROE, share gains", "probability": 0.3, "sub_method": "worked", "value_per_share": 39.8205, "rationale": "Telematics pricing + embedded/agent distribution sustain ≈15%+ premium growth and ≈18-20% ROE; book compounds ≈18%/yr for 7 yrs, terminal P/B 1.7x on a de-risked, scaled book."}, {"name": "Solid grower \u2014 base case, 16% ROE", "probability": 0.4, "sub_method": "worked", "value_per_share": 25.76, "rationale": "Mid-teens ROE, ≈14% book growth, mid-90s combined ratio through cycle; terminal P/B 1.4x consistent with 16% ROE / 13-14% CoE."}, {"name": "Cycle softens / growth stalls \u2014 10% ROE", "probability": 0.2, "sub_method": "worked", "value_per_share": 13.4422, "rationale": "Soft auto market, competition compresses growth, combined ratio drifts to ≈99-100%, ROE ≈10%; book compounds ≈9%/yr, matures at 1.0x book."}, {"name": "Adverse \u2014 reserve/competitive shock, dilutive", "probability": 0.1, "sub_method": "worked", "value_per_share": 8.2775, "rationale": "Loss-ratio edge fails through a full cycle or adverse development; ROE ≈6%, book compounds ≈5%, trades below book at 0.8x; possible dilutive capital raise."}]}
notes: Composite of 4 event branches (worked), probability-weighted.
```

### ⚙️ `compute_valuation`

_input:_ `{"method": "excess_returns", "rationale": "Cross-check / no-heroic-growth FLOOR via warranted P/B = (ROE - g)/(CoE - g). Uses a conservative through-cycle ROE of 16%, modest 3% growth, 14% cost of equity, applied to common book equity. This deliberately strips out the multi-year hypergrowth runway to anchor the downside.", "excess_returns": {"book_value": 325900000, "shares_outstanding": 17700000, "sustainable_return": 0.16, "cost_of_equity": 0.14, "growth": 0.03}, "citations": [{"source_kind": "fundamentals", "quote": "Q1'26 common equity $325.9M; FY2025 ROE on common ≈15.7%; 17.7M fully-diluted shares", "section": "get_financials / analyst reconstruction"}]}`

_returned:_

```
VALUATION (excess_returns): fair value/share = 21.7601
equity_value=385154545.45 EV=None
working={"warranted_price_to_book": 1.1818, "book_value": 325900000.0, "sustainable_return": 0.16, "cost_of_equity": 0.14, "growth": 0.03, "shares_outstanding": 17700000.0}
notes: Excess returns: warranted P/B 1.18x (ROE 16.0%, g 3.0%, CoE 14.0%).
```

## Step 5

**🧠 PM reasoning:**

> Now I'm checking the valuation against comparable companies—at Root's 16% ROE and growth profile, a price-to-book multiple of 1.4x to 1.7x seems reasonable compared to peers like PLMR at 3.0x with 22% ROE, SKWD at 1.5x with 17% ROE, and HCI at 1.6x with 33% ROE. Using Root's current book value of $18.4, applying the 1.4x multiple gets me to $25.80, which aligns well with my composite FMV of $25.77.
> 
> But there's a tension when I cross-check against earnings: normalized earnings power of $80M translates to roughly $4.50 per share, and applying an 8-10x multiple (appropriate for a sub-scale, cyclical insurer) gives $36-45 per share—notably higher than my book-based valuation. This gap exists because the high ROE means current earnings are outsized relative to book value, but I need to be cautious here since current results are cyclically elevated with a loss ratio well below the 60-65% target, benign weather, and Q1 seasonality all working in Root's favor. The aggressive 4.4x premium-to-surplus leverage also constrains future ROE expansion, and regulators will likely require more capital retention as the company grows, which could pressure returns going forward.
> 
> The real crux is whether sustainable ROE is closer to 16% or actually 22%+, since that's the primary driver of valuation. FY2025 showed 15.7% ROE but was depressed by warrant expenses and heavy growth investment, while Q1'26 annualized to 47%—the truth likely sits somewhere between these extremes, and the excess capital on the balance sheet may allow for higher returns if deployed effectively.
> 
> My scenario weighting (30% at 18%, 40% at 16%, 20% at 10%, 10% at 6%) produces a probability-weighted ROE around 14.6%, which might be slightly conservative given current earnings momentum and available improvement levers like investment yield redeployment and operating leverage. The bear cases do warrant a meaningful haircut for cycle and reserve risk on a young, leveraged book, but I should consider whether I'm underweighting the upside given structural growth tailwinds and current performance. Rather than chase higher valuations, I want to stay disciplined—the competitive moat still needs to prove itself through a full cycle.
> 
> Let me triangulate with a normalized earnings floor to see if fair value should be closer to $27-28. Working through the math: a 96% through-cycle combined ratio on $1.5B NEP gives roughly $60M underwriting profit, plus normalized net investment income of $42M and interest expense of $13M, yielding pretax earnings around $89M. After accounting for warrant comp winding down and applying a normalized tax rate, normalized net income lands in the $70-80M range.
> 
> That translates to $4.0-4.5 EPS and a 22-24% ROE on the common equity base. But here's the tension: if the current 59% loss ratio normalizes upward to 63% (the midpoint of management's target), the combined ratio ticks to 98-99%, underwriting margin compresses to 1-2%, and net income falls to around $50M with ROE dropping to 15%. So the range of $50-80M normalized earnings maps to ROE between 15-24%, with my base case 16% sitting at the conservative end. This suggests my probability weighting might be slightly tight, and fair value could reasonably be $26 as a central estimate with upside to $32-36 if current returns prove durable. I'm also reconsidering the book-compounding model—growing book at ROE with a terminal P/B multiple isn't double-counting if I'm assuming a 2% leakage through dividends or dilution, which seems reasonable.
> 
> On the discount rate, 14% feels appropriate for a volatile micro-cap insurer whose competitive edge hasn't been tested through a full cycle, though I could justify 13% given the $690M cash, low leverage, and buyback activity. Lowering CoE by 1 point would lift valuations by roughly 6%, pushing fair value to $27.4, but I'll stick with 14% as my central case and note the sensitivity. I'm settling on fair value around $26, a floor of $21, and a band of $17-36, with 17.7M diluted shares outstanding.
> 
> Now I need to write the comprehensive memo, making sure to cover the preferred treatment, dilution dynamics, warrant overhang, statutory capital requirements, investment yield redeployment, management's capital allocation philosophy, the buyback program, and Carvana concentration risk. I have solid material from both analysts to integrate, so I'll aim for a dense 4,500-6,000 word piece that captures the complexity of this name.

**PM note:** The two methods triangulate tightly: probability-weighted composite FMV = **$25.77**, and the conservative no-growth warranted-P/B floor = **$21.76**. Let me cross-check the earnings-power angle and peer multiples to make sure the FMV isn't understating a sustainably high ROE.

The earnings cross-check: normalized through-cycle net income ≈ $60–80M (NEP ≈ $1.5B × 4% underwriting margin at a 96% combined + ≈ $40M net investment income − ≈ $13M interest) on 17.7M shares ≈ $3.5–4.5 EPS, ROE ≈ 16–22%. At a sub-scale-cyclical 8–10x that is $32–45 — above the book-compounding FMV, confirming my central case is, if anything, conservative on the upside (it assumes the cyclically-aided 59% gross loss ratio normalizes higher). Peer P/B (PLMR 3.0x at 22% ROE, SKWD 1.5x at 17%, HCI 1.6x) supports a 1.4–1.7x multiple on Root's ≈16% ROE. The composite captures this distribution. I'm confident in FMV ≈ $26, floor ≈ $21, band ≈ $17–36.

Let me commission the two specialist-authored deep sections for the memo before assembling.

### ⚙️ `ask_analyst`

_input:_ `{"analyst_id": "a2-insurance", "question": "Please write the publication-ready, fully-cited \"Industry & Competitive Landscape\" section for my investment memo on Root (700-1000 words). Teach a smart generalist from first principles: (1) how US personal auto insurance works economically (premium, loss ratio, expense ratio, combined ratio, float, premium-to-surplus leverage, the rate-filing/regulatory cycle); (2) the current cycle state (2022-24 hard market, 2025 softening); (3) how telematics/UBI actually works mechanically and whether it is a durable moat; (4) the head-to-head vs Progressive/GEICO/State Farm/Allstate/Lemonade with the specific loss-ratio/combined-ratio/scale numbers; (5) your verdict on whether Root has a defensible advantage. Keep all the specific figures and citations. Write it as clean prose/markdown ready to drop into the memo."}`

_returned:_

```
ANALYST [a2-insurance] (insurance industry & competitive-landscape analyst) follow-up:
# Industry & Competitive Landscape

**How the economics work.** A personal-auto insurer collects *premium*, pays *claims* (losses) plus the cost of settling them (loss-adjustment expense), and incurs *underwriting expenses* (acquisition/commissions, advertising, overhead). Two ratios define profitability: the **loss ratio** (losses ÷ earned premium) and the **expense ratio** (expenses ÷ premium); their sum is the **combined ratio**. Below 100 = an underwriting profit; above 100 = a loss. Crucially, insurers also earn on **float** — premiums collected and held in reserves before claims are paid, invested in the interim. Capital intensity is governed by **premium-to-surplus leverage**: regulators cap how much premium a carrier can write per dollar of statutory surplus (≈2:1 is conventional), so growth consumes capital. Pricing is regulated state-by-state: carriers must **file rates** for approval, creating a lag between when claims inflation hits and when rate increases earn through — the engine of the insurance cycle.

**The cycle (2022–2025).** Personal auto just completed a violent round trip. Post-COVID claims inflation (parts, labor, used-car values, medical, litigation) outran filed rates, pushing the industry **net combined ratio to 112.2 in 2022** — a deep underwriting loss (S&P Global Market Intelligence). Carriers then pushed through **≈54% cumulative rate increases from 2020–2024** (auto-insurance CPI rose 20.6% YoY in January 2024 alone; BLS), restoring profitability: the combined ratio fell to **≈105 in 2023 and 95.3 in 2024**, the best result since pre-pandemic (S&P GMI; A.M. Best). With margins restored, **2025 turned soft** — average full-coverage premiums fell **≈6% nationally** (Insurify). This matters for Root: its swing from a **$147M net loss (FY2023) to $40M net income (FY2025)** (company financials) coincided precisely with this rate-earn-through, so a portion of its turnaround reflects the cycle, not just idiosyncratic skill — and the cycle is now reversing.

**Market structure.** US private-passenger auto is ≈**$359B in direct premiums written (2024), +12.6–13.3% YoY**, ≈35% of all US P&C premium (NAIC; S&P GMI). It is a **consolidating oligopoly**: the top five carriers held **63.6% share in 2024**, up from 62.5% (NAIC). State Farm (≈16–19%) and Progressive (≈16–17%) lead — **Progressive overtook State Farm as #1 on the A.M. Best basis in 2024** (+22% DPW), the direct/telematics model taking share from captive agents. GEICO (≈10–12%), Allstate (≈8–10%) and USAA (≈5–6%) round out the top five. **Root holds ≈0.4% share** — ≈$1.5B of premium in a ≈$350B market (Q4-FY2025 call).

**How telematics/UBI works.** Usage-based insurance prices risk on *observed driving* rather than only demographic proxies. Progressive's **Snapshot** is an *add-on rating modifier* scoring hard braking, rapid acceleration, night driving and mileage (the dominant signal is hard-brakes-per-mile); it can *surcharge* ≈20% of users, not just discount. **Root** makes driving score the *primary* underwriting variable: a 2–3 week phone-based "test drive" scores braking, cornering, acceleration, time-of-day and mileage, and Root will *decline* bad risks outright. The signal is real — telematics adds **≈79% lift above standard rating factors** with **8.7x claim-frequency separation** (LexisNexis), and can render demographic proxies like gender redundant (Verbelen/Antonio). **But durability is questionable.** That lift is increasingly *buyable* from vendors (LexisNexis, CMT); the compounding early-mover advantage the academic literature describes accrues to **Progressive** (Snapshot since 2008, 3M+ users by 2015), not Root; and aggregate industry profitability didn't improve materially despite wide telematics adoption (112 combined in 2022). Telematics is **table stakes plus a few points of loss ratio** — not a unique structural moat against scaled incumbents who already have it.

**Head-to-head.** Root executes the model well but is sub-scale:

| | Combined ratio | Auto gross loss ratio | Ad spend (2024) | Auto share |
|---|---|---|---|---|
| **Root** | ≈97 gross / 98.2 net (FY25); 94.7 gross (FY24) | **≈58–59%** | modest | ≈0.4% |
| **Progressive** | **88.8** | embedded | **≈$3.5B** | ≈16–17% |
| **GEICO** | **81.5** | embedded | ≈$1.7–2.0B | ≈10–12% |
| **Allstate** | ≈mid-90s | — | ≈$1.87B | ≈8–10% |
| **State Farm** | underwriting profit | — | ≈$1.11B | ≈16–19% |
| **Lemonade (auto)** | net loss-making | **≈76%** | modest | <0.5% |

Two reads dominate. First, **Root is the superior insurtech auto underwriter** — its ≈58–59% gross loss ratio beats Lemonade's ≈76% car book by ≈17 points, and Root is net-income profitable (FY25 +$40M; Q1-FY26 47% annualized ROE) while Lemonade still loses money. Second, **Root loses to the incumbents on the metrics that win commoditized insurance.** A ≈97 combined leaves Root ≈3¢ of margin per premium dollar; Progressive keeps ≈11¢ and GEICO ≈18¢ — margin they redeploy to underprice Root *and* outspend it ≈50:1 on advertising (Progressive's single-year ad budget exceeds Root's total premium). And incumbents fund growth with **float** — Berkshire holds ≈$171B of negative-cost float — while Root funds it with equity and a secured term loan (recently refinanced to ≈SOFR+600bps).

**Verdict.** Root is a **well-run, sub-scale challenger with a real but narrow edge — not a structurally advantaged compounder.** Its defensible asset is a modern, API-native, full-stack platform that wins *embedded* distribution (Carvana exclusivity, 200,000+ policies; Toyota/Hyundai connected-car; Goosehead/Freeway agent integrations — partnerships were ≈half of Q4-FY2025 new writings) faster than legacy incumbents can re-platform. That lowers CAC and routes around the incumbents' advertising moat. But telematics confers no durable pricing edge, the embedded channel is replicable and partner-dependent (Carv
```

## Step 6

**🧠 PM reasoning:**

> Now I'm pulling together all the pieces—the industry analysis, the underwriting work, and my valuation—into one comprehensive memo that should run around five thousand words or more.

**PM note:** I have all the pieces. Let me assemble the final memo and dossier.

### ⚙️ `submit_final`

_gate verdict:_ The INDEPENDENT JUDGE has NOT yet rated this best-in-existence (score 86/100). Not accepted until it is the best, most accurate, most complete valuation of this company that could exist.

FACTUAL ERRORS — verify against the data tools and FIX:
- Cost of equity is stated as '≈14%' but the disclosed buildup (4.3% + 1.5×5.0% + 3.0%) sums to 14.8%; rounding down ≈0.8 points modestly inflates every scenario value.
- Current Carvana economic ownership is ≈19.3% as-converted (Feb 2026 13D/A), not the ≈14% cited in the risk section (the memo is internally inconsistent, elsewhere citing the 29.9% theoretical max).

GAPS vs best-in-class — close every one (deepen/explain/add):
- The base-case valuation sets book CAGR (14%) equal to the cost of equity (14%), so the seven-year compounding mathematically cancels and value reduces to BVPS × terminal P/B. The multi-stage framework is therefore largely cosmetic in the modal case; the memo should make transparent that the two true levers are current book and the terminal multiple.
- Terminal P/B assumptions (1.4x base, 1.7x bull) exceed the warranted (ROE−g)/(CoE−g) values they imply (≈1.2x and ≈1.5x). They are cross-checked against peers but not reconciled to the memo's own excess-return math.
- Scenario probability weights (30/40/20/10) are asserted with qualitative rationale rather than derived from base rates (e.g., how often a turnaround insurer sustains sub-target loss ratios through a soft cycle).
- The dominant named risk — reserve adequacy on a young, fast-growing, 4.4x-levered book — is discussed only narratively. A best-in-class memo would analyze prior-year reserve development / loss triangles quantitatively, since that is the variable most likely to break the thesis.
- Statutory surplus, RBC ratio, and the 4.4x premium-to-surplus figure are stated but not derived from the statutory filings; investment-portfolio composition and the 5%-yield redeployment lever are asserted, not modeled.
- Persistency/retention is correctly flagged as the key undisclosed variable but is left unestimated; a triangulation (e.g., from PIF vs new-writings growth) would strengthen the durability case.
- All three cross-checks (normalized earnings $32-45, peers $26-37) land at or above the $26 center; the memo does not fully reconcile why it anchors to the low end of its own evidence.

Correct the numbers, deepen the memo, then call submit_final again.

**🔬 Red-team's own verification (how it checked the numbers):**

> _reviewer reasoning:_ I'm verifying the core valuation drivers from the memo: the common book value per share of $18.40 on a fully diluted basis, the diluted share count of 17.7 million, the ROE around 16%, and checking the underlying equity figures—common equity of $325.9 million derived from total equity of $437.9 million minus the $112 million in preferred stock, with roughly 15.5 million shares outstanding on a basic basis.

  - 🔎 checked `get_financials` {"period": "annual", "years": 5}
    → `MULTI-PERIOD FINANCIALS (most recent first; values in reporting currency):
period | revenue | gross_profit | operating_income | net_income | ebitda | op_cash_flow | capex | free_cash_flow | cash | total_debt | total_equity | preferred | COMMON_EQUITY | shares
FY2025 | 1517100000.0 | 386600000.0 | 40800000.0 | 40300000.0 | 73600000.0 | 206500000.0 | -14100000.0 | 192400000.0 | 689900000.0 | 201300000.0 | 396300000.0 | 112000000.0 | 284300000.0 | 17200000.0
FY2024 | 1176500000.0 | 337100000.0 | 30900000.0 | 30900000.0 | 88000000.0 | 195700000.0 | -11800000.0 | 183900000.0 | 600300000.0 | 202300000.0 | 315700000.0 | 112000000.0 | 203700000.0 | 16900000.0
FY2023 | 455000000.0 | 76100000.0 | -147400000.0 | -147400000.0 | -88700000.0 | -33600000.0 | -9400000.0 | -43000000.0 | 679700000.0 | 299300000.0 | 277700000.0 | 112000000.0 | 165700000.0 | 14400000.0
FY2022 | 310800000.0 | -32200000.0 | -297700000.0 | -297700000.0 | -249300000.0 | -210600000.0 | -10100000.0 | -220700000.0 | 763100000.0 | 298600000.0 | 389100000.0 | 112000000.0 | 277100000.0 | 14100000.0
FY2021 | 345400000.0 | -51900000.0 | -521100000.0 | -521100000.0 | -484500000.0 | -403400000.0 | -11200000.0 | -414600000.0 | 70700`

  - 🔎 checked `get_ratios` {}
    → `TTM OPERATIONAL RATIOS (price-blind — margins, returns, turnover, leverage, liquidity):
grossProfitMarginTTM: 0.2862
ebitMarginTTM: 0.0506
ebitdaMarginTTM: 0.0589
operatingProfitMarginTTM: 0.0375
pretaxProfitMarginTTM: 0.0375
continuousOperationsProfitMarginTTM: 0.0377
netProfitMarginTTM: 0.037
bottomLineProfitMarginTTM: 0.0351
receivablesTurnoverTTM: 4.4504
payablesTurnoverTTM: 0
inventoryTurnoverTTM: 0
fixedAssetTurnoverTTM: 0
assetTurnoverTTM: 0.999
currentRatioTTM: 0
quickRatioTTM: 0
solvencyRatioTTM: 0.0629
cashRatioTTM: 0
debtToAssetsRatioTTM: 0.1282
debtToEquityRatioTTM: 0.4574
debtToCapitalRatioTTM: 0.3139
longTermDebtToCapitalRatioTTM: 0.3139
financialLeverageRatioTTM: 3.5689
workingCapitalTurnoverRatioTTM: 1.9604
operatingCashFlowRatioTTM: 0
operatingCashFlowSalesRatioTTM: 0.1211
freeCashFlowOperatingCashFlowRatioTTM: 0.9386
debtServiceCoverageRatioTTM: 4.4976
interestCoverageRatioTTM: 2.8537
shortTermOperatingCashFlowCoverageRatioTTM: 0
operatingCashFlowCoverageRatioTTM: 0.9436
capitalExpenditureCoverageRatioTTM: 16.2931
dividendPaidAndCapexCoverageRatioTTM: 16.2931
dividendPayoutRatioTTM: 0
revenuePerShareTTM: 100.0769
netIncomePerShareTTM: 3.7051
interestDebtPerShareTT`

  - 🔎 checked `get_statement` {"statement": "balance_sheet", "period": "quarter", "limit": 2}
    → `ROOT BALANCE SHEET (quarter, recent first) — full line items:

[2026-Q1] (2026-03-31)
  cashAndCashEquivalents=608900000
  shortTermInvestments=0
  cashAndShortTermInvestments=608900000
  netReceivables=350800000
  accountsReceivables=350800000
  otherReceivables=0
  inventory=0
  prepaids=0
  otherCurrentAssets=0
  totalCurrentAssets=959700000
  propertyPlantEquipmentNet=0
  goodwill=0
  intangibleAssets=0
  goodwillAndIntangibleAssets=0
  longTermInvestments=471500000
  taxAssets=0
  otherNonCurrentAssets=131600000
  totalNonCurrentAssets=603100000
  otherAssets=0
  totalAssets=1562800000
  totalPayables=0
  accountPayables=0
  otherPayables=0
  accruedExpenses=0
  shortTermDebt=0
  capitalLeaseObligationsCurrent=0
  taxPayables=0
  deferredRevenue=0
  otherCurrentLiabilities=0
  totalCurrentLiabilities=0
  longTermDebt=200300000
  capitalLeaseObligationsNonCurrent=0
  deferredRevenueNonCurrent=0
  deferredTaxLiabilitiesNonCurrent=0
  otherNonCurrentLiabilities=927800000
  totalNonCurrentLiabilities=1124900000
  otherLiabilities=0
  capitalLeaseObligations=0
  totalLiabilities=1124900000
  treasuryStock=0
  preferredStock=112000000
  commonStock=0
  retainedEarnings=-1605700000
 `

  - 🔎 checked `get_peers` {"max_peers": 10}
    → `PEERS (TTM multiples):
[
 {
  "ticker": "PLMR",
  "name": "Palomar Holdings, Inc.",
  "market_cap": 2875938189.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 3.0064946515730853,
  "pe": 14.629217505010274,
  "ev_ebitda": 11.678697660389236,
  "roe": 0.21736343376767606
 },
 {
  "ticker": "HCI",
  "name": "HCI Group, Inc.",
  "market_cap": 2003819560.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.6432851157140222,
  "pe": 5.91148489733358,
  "ev_ebitda": 2.278199646877891,
  "roe": 0.32635170225937493
 },
 {
  "ticker": "STC",
  "name": "Stewart Information Services Corporation",
  "market_cap": 2003015993.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.238193030878567,
  "pe": 15.668094325775424,
  "ev_ebitda": 9.501921327025016,
  "roe": 0.08364444085456968
 },
 {
  "ticker": "SLDE",
  "name": "Slide Insurance Holdings, Inc. Common Stock",
  "market_cap": 1917721678.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.8540973696404133,
  "pe": 4.205329064346423,
  "ev_ebitda": 1.1454869237195098,
  "roe": 0.6666680244896962
 },
 {
  "ticker": "HMN",
  "name": "Horace Mann Educators Corpo`

> _reviewer reasoning:_ I'm checking the equity figures against the memo—common equity of $325.9M looks right after subtracting preferred from the total. But there's a discrepancy with the share count: the memo claims around 15.5M outstanding and 17.7M fully diluted, while the data shows 17.2M shares for both FY2025 and Q1 2026, which doesn't quite align.
> 
> Let me work through the book value per share calculation. Using the memo's Q1'26 common equity of $325.9M divided by 17.7M diluted shares gives $18.41, which matches their stated BVPS of $18.4. If I use the data provider's 17.2M shares instead, I get $18.95—close enough. The memo's approach of stripping out preferred equity and using the diluted share count is the right way to calculate this, whereas the data provider's bookValuePerShareTTM of $28.07 incorrectly includes preferred and uses a lower share count of around 15.6M.
> 
> Now I'm checking the diluted share count methodology. The memo adds 1.3M RSUs, 0.1M options, and 0.78M if-converted preferred shares to the 15.5M basic shares to get 17.7M diluted. But it also subtracts the full $112M preferred from equity to calculate common equity. This creates a potential double-count issue—if the preferred con

  - 🔎 checked `get_statement` {"statement": "income", "period": "annual", "limit": 3}
    → `ROOT INCOME (annual, recent first) — full line items:

[2025-FY] (2025-12-31)
  revenue=1517100000
  costOfRevenue=1130500000
  grossProfit=386600000
  researchAndDevelopmentExpenses=0
  generalAndAdministrativeExpenses=96900000
  sellingAndMarketingExpenses=174800000
  sellingGeneralAndAdministrativeExpenses=271700000
  otherExpenses=74100000
  operatingExpenses=345800000
  costAndExpenses=1476300000
  netInterestIncome=19100000
  interestIncome=40100000
  interestExpense=21000000
  depreciationAndAmortization=11800000
  ebitda=73600000
  ebit=61800000
  nonOperatingIncomeExcludingInterest=-21000000
  operatingIncome=40800000
  totalOtherIncomeExpensesNet=0
  incomeBeforeTax=40800000
  incomeTaxExpense=-500000
  netIncomeFromContinuingOperations=41300000
  netIncomeFromDiscontinuedOperations=0
  otherAdjustmentsToNetIncome=-1000000
  netIncome=40300000
  netIncomeDeductions=0
  bottomLineNetIncome=38300000
  eps=2.49
  epsDiluted=2.24
  weightedAverageShsOut=15500000
  weightedAverageShsOutDil=17200000

[2024-FY] (2024-12-31)
  revenue=1176500000
  costOfRevenue=839400000
  grossProfit=337100000
  researchAndDevelopmentExpenses=0
  generalAndAdministrativeExpenses=69500000
  selli`

  - 🔎 checked `get_insider_activity` {}
    → `RECENT INSIDER TRANSACTIONS (Form 4):
  2026-06-03 Hilsheimer Lawrence A. (director): A-Award 2864 @ 0 -> owns 43859
  2026-06-03 KRAMER NANCY J (director): A-Award 2864 @ 0 -> owns 20480
  2026-06-03 Ulman Doug (director): A-Award 2864 @ 0 -> owns 3983
  2026-06-03 DEVARD JERRI (director): A-Award 2864 @ 0 -> owns 21396
  2026-06-03 Birnbaum Beth A (director): A-Award 2864 @ 0 -> owns 17144
  2026-06-03 Szudarek Julie (director): A-Award 2864 @ 0 -> owns 14696
  2026-06-03 Dorsey Donna (director): A-Award 2864 @ 0 -> owns 12820
  2026-05-21 Forish Ryan (officer: Chief Accounting Officer): F-InKind 351 @ 57.85 -> owns 25100
  2026-05-15 Allison Jonathan (officer: Chief Administrative Officer): S-Sale 1606 @ 55.96 -> owns 68356
  2026-05-12 Allison Jonathan (officer: Chief Administrative Officer): S-Sale 1706 @ 55.74 -> owns 69962
  2026-05-01 Forish Ryan (officer: Chief Accounting Officer): F-InKind 82 @ 55.05 -> owns 25451
  2026-04-07 Allison Jonathan (officer: Chief Administrative Officer): S-Sale 1706 @ 44.35 -> owns 71668
  2026-04-01 Timm Alexander E. (director, 10 percent owner, officer: Chief Executive Officer): M-Exempt 62969 @ 0 -> owns 303861
  2026-04-01 Timm Alexander `

  - 🔎 checked `research` {"question": "What is a reasonable cost of equity / required return for a small-cap (≈$1.5B premium, sub-scale) personal auto insurer like Root Inc, and what cost of equity do analysts typically apply to InsurTech / high-beta P&C insurers? Is 14% reasonable?"}
    → `RESEARCH — What is a reasonable cost of equity / required return for a small-cap (≈$1.5B premium, sub-scale) personal auto insurer like Root Inc, and what cost of equity do analysts typically apply to InsurTech / high-beta P&C insurers? Is 14% reasonable?
I'll research this question about cost of equity for small-cap InsurTech P&C insurers like Root Inc. Let me search for relevant data.Let me see the actual content of these results.The search results appear empty. Let me retry with the proper structure.Good, now I'm getting real data. The result needs json.loads. Let me gather the key data points - beta, risk-free rate, equity risk premium, and insurer cost of equity benchmarks.Let me get specific numbers: current ERP from Damodaran, current 10yr treasury, and the insurance sector cost of equity figures.I have strong data now. Let me get one more search on the actual insurance sector cost of equity figures from Damodaran's table and InsurTech-specific discount rates.I have enough data to build a rigorous answer. Let me compute the CAPM-based cost of equity for Root using the key inputs.I have everything I need. Here's the analysis.

## Bottom line: Yes, ≈14% is reasonable — arguabl`

  _reviewer note:_ Let me verify the underwriting figures and a couple of operational claims.

> _reviewer reasoning:_ The research supports the 14% cost of equity as reasonable within the 13-16% range, so the memo's assumption is defensible. I need to set aside the market price data mentioned in the research since that's not relevant to my concerns. Looking at the income statement, the weighted average shares outstanding for FY2025 are 15.5M basic and 17.2M diluted, while the memo uses 15.5M basic and 17.7M diluted—the diluted share count in the memo is slightly elevated compared to what the financials show.
> 
> The memo adds back the if-converted preferred shares (0.78M) on top of the reported diluted count, which technically double-counts since those preferred shares are already excluded from the reported diluted figure as out-of-the-money. This approach is conservative for book value per share since it inflates the denominator, resulting in $18.41 versus $18.95 if using the reported diluted count. The net income to common of $38.3M matches what the memo cites, and insider activity is indeed benign—just awards, tax withholding, and minor sales. The valuation methodology itself is sound for an insurer using book value compounding at ROE.
> 
> I'm narrowing down the concerns to note: the cost of equity r

  _reviewer note:_ I've verified the memo's key numbers against the filings. They tie out well. Let me summarize my findings.

**Verification results:**
- **Common equity $325.9M** (Q1'26 total equity $437.9M − $112M preferred) ✓ confirmed
- **BVPS ≈$18.4 fully diluted** — defensible; data screen's $28.07 is correctly identified as wrong (includes preferred, uses low share count). The author actually catches and corrects this screen error.
- **Share count** — filings show 15.5M basic / 17.2M diluted weighted-avg; memo uses 15.5M / 17.7M ✓ (conservative)
- **Net income** FY23 −$147.4M, FY24 +$30.9M, FY25 +$40.3M; NI to common $38.3M ✓ all match
- **Revenue** $455M→$1,177M→$1,517M ✓
- **ROE** TTM 14.75%, FY25 ≈15.7% ✓
- **Peer P/B vs ROE** — PLMR 3.0x/21.7%, SKWD 1.52x/17.4%, HCI 1.64x/32.6%, HMN 1.32x/11.5% ✓

_red-team concerns this round:_

- [low/valuation_assumption] Cost-of-equity build-up rounds down ≈14.8% to 14%.

- [low/data_error] Diluted share count adds if-converted preferred shares while preferred is also subtracted from equity as a senior claim.

- [low/valuation_method] Base-case book CAGR set equal to the discount rate, neutralizing the multi-stage compounding.

- [low/valuation_assumption] Through-cycle ROE of 16% used in the floor sits above current realized ROE.

**🔬 Judge's own verification (independent fact-check):**

> _reviewer reasoning:_ I'm checking the numbers in this memo against the ground truth data. The memo cites a fully diluted BVPS of $18.4 and Q1'26 common equity of $325.9M, but the ground truth shows FY2025 common equity at $284.3M with 17.2M shares and a BVPS of $16.53. I need to figure out whether the memo is referencing a different fiscal period or if there's a discrepancy in how these figures are calculated. The key issue is that BVPS₀ drives the entire valuation, and there's an 11% gap between the FY2025 figure of $16.53 and the memo's Q1'26 estimate of $18.4. The memo's more recent quarter is probably more relevant, but I need to verify those Q1'26 numbers to be sure. Let me pull the actual financial statements.

  - 🔎 checked `get_financials` {"period": "annual", "years": 5}
    → `MULTI-PERIOD FINANCIALS (most recent first; values in reporting currency):
period | revenue | gross_profit | operating_income | net_income | ebitda | op_cash_flow | capex | free_cash_flow | cash | total_debt | total_equity | preferred | COMMON_EQUITY | shares
FY2025 | 1517100000.0 | 386600000.0 | 40800000.0 | 40300000.0 | 73600000.0 | 206500000.0 | -14100000.0 | 192400000.0 | 689900000.0 | 201300000.0 | 396300000.0 | 112000000.0 | 284300000.0 | 17200000.0
FY2024 | 1176500000.0 | 337100000.0 | 30900000.0 | 30900000.0 | 88000000.0 | 195700000.0 | -11800000.0 | 183900000.0 | 600300000.0 | 202300000.0 | 315700000.0 | 112000000.0 | 203700000.0 | 16900000.0
FY2023 | 455000000.0 | 76100000.0 | -147400000.0 | -147400000.0 | -88700000.0 | -33600000.0 | -9400000.0 | -43000000.0 | 679700000.0 | 299300000.0 | 277700000.0 | 112000000.0 | 165700000.0 | 14400000.0
FY2022 | 310800000.0 | -32200000.0 | -297700000.0 | -297700000.0 | -249300000.0 | -210600000.0 | -10100000.0 | -220700000.0 | 763100000.0 | 298600000.0 | 389100000.0 | 112000000.0 | 277100000.0 | 14100000.0
FY2021 | 345400000.0 | -51900000.0 | -521100000.0 | -521100000.0 | -484500000.0 | -403400000.0 | -11200000.0 | -414600000.0 | 70700`

  - 🔎 checked `get_ratios` {}
    → `TTM OPERATIONAL RATIOS (price-blind — margins, returns, turnover, leverage, liquidity):
grossProfitMarginTTM: 0.2862
ebitMarginTTM: 0.0506
ebitdaMarginTTM: 0.0589
operatingProfitMarginTTM: 0.0375
pretaxProfitMarginTTM: 0.0375
continuousOperationsProfitMarginTTM: 0.0377
netProfitMarginTTM: 0.037
bottomLineProfitMarginTTM: 0.0351
receivablesTurnoverTTM: 4.4504
payablesTurnoverTTM: 0
inventoryTurnoverTTM: 0
fixedAssetTurnoverTTM: 0
assetTurnoverTTM: 0.999
currentRatioTTM: 0
quickRatioTTM: 0
solvencyRatioTTM: 0.0629
cashRatioTTM: 0
debtToAssetsRatioTTM: 0.1282
debtToEquityRatioTTM: 0.4574
debtToCapitalRatioTTM: 0.3139
longTermDebtToCapitalRatioTTM: 0.3139
financialLeverageRatioTTM: 3.5689
workingCapitalTurnoverRatioTTM: 1.9604
operatingCashFlowRatioTTM: 0
operatingCashFlowSalesRatioTTM: 0.1211
freeCashFlowOperatingCashFlowRatioTTM: 0.9386
debtServiceCoverageRatioTTM: 4.4976
interestCoverageRatioTTM: 2.8537
shortTermOperatingCashFlowCoverageRatioTTM: 0
operatingCashFlowCoverageRatioTTM: 0.9436
capitalExpenditureCoverageRatioTTM: 16.2931
dividendPaidAndCapexCoverageRatioTTM: 16.2931
dividendPayoutRatioTTM: 0
revenuePerShareTTM: 100.0769
netIncomePerShareTTM: 3.7051
interestDebtPerShareTT`

  - 🔎 checked `get_statement` {"statement": "balance_sheet", "period": "quarter", "limit": 3}
    → `ROOT BALANCE SHEET (quarter, recent first) — full line items:

[2026-Q1] (2026-03-31)
  cashAndCashEquivalents=608900000
  shortTermInvestments=0
  cashAndShortTermInvestments=608900000
  netReceivables=350800000
  accountsReceivables=350800000
  otherReceivables=0
  inventory=0
  prepaids=0
  otherCurrentAssets=0
  totalCurrentAssets=959700000
  propertyPlantEquipmentNet=0
  goodwill=0
  intangibleAssets=0
  goodwillAndIntangibleAssets=0
  longTermInvestments=471500000
  taxAssets=0
  otherNonCurrentAssets=131600000
  totalNonCurrentAssets=603100000
  otherAssets=0
  totalAssets=1562800000
  totalPayables=0
  accountPayables=0
  otherPayables=0
  accruedExpenses=0
  shortTermDebt=0
  capitalLeaseObligationsCurrent=0
  taxPayables=0
  deferredRevenue=0
  otherCurrentLiabilities=0
  totalCurrentLiabilities=0
  longTermDebt=200300000
  capitalLeaseObligationsNonCurrent=0
  deferredRevenueNonCurrent=0
  deferredTaxLiabilitiesNonCurrent=0
  otherNonCurrentLiabilities=927800000
  totalNonCurrentLiabilities=1124900000
  otherLiabilities=0
  capitalLeaseObligations=0
  totalLiabilities=1124900000
  treasuryStock=0
  preferredStock=112000000
  commonStock=0
  retainedEarnings=-1605700000
 `

  - 🔎 checked `get_peers` {"max_peers": 8}
    → `PEERS (TTM multiples):
[
 {
  "ticker": "PLMR",
  "name": "Palomar Holdings, Inc.",
  "market_cap": 2875938189.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 3.0064946515730853,
  "pe": 14.629217505010274,
  "ev_ebitda": 11.678697660389236,
  "roe": 0.21736343376767606
 },
 {
  "ticker": "HCI",
  "name": "HCI Group, Inc.",
  "market_cap": 2003819560.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.6432851157140222,
  "pe": 5.91148489733358,
  "ev_ebitda": 2.278199646877891,
  "roe": 0.32635170225937493
 },
 {
  "ticker": "STC",
  "name": "Stewart Information Services Corporation",
  "market_cap": 2003015993.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.238193030878567,
  "pe": 15.668094325775424,
  "ev_ebitda": 9.501921327025016,
  "roe": 0.08364444085456968
 },
 {
  "ticker": "SLDE",
  "name": "Slide Insurance Holdings, Inc. Common Stock",
  "market_cap": 1917721678.0,
  "industry": "Insurance - Property & Casualty",
  "price_to_book": 1.8540973696404133,
  "pe": 4.205329064346423,
  "ev_ebitda": 1.1454869237195098,
  "roe": 0.6666680244896962
 },
 {
  "ticker": "HMN",
  "name": "Horace Mann Educators Corpo`

  _reviewer note:_ I'll independently verify the memo's key numbers and the valuation inputs.

> _reviewer reasoning:_ I'm checking the memo's book value per share calculations against the actual Q1'26 data. The memo claims around $20.9 basic and $18.4 diluted, but when I work through the numbers with common equity of $325.9M and 17.2M shares, I'm getting $18.95 for basic BVPS, which doesn't quite match what's stated.
> 
> The memo does correctly identify that the $28 book value figure floating around includes preferred stock and uses an artificially low share count, so that's a solid catch. For the ROE calculation on common equity, the memo shows FY2025 at roughly 15.7% using $38.3M net income to common divided by $244M average common equity, but I need to verify whether preferred dividends were properly deducted from the $40.3M net income figure.
> 
> Looking at the loss ratios and combined ratios, the memo's claims check out: 65.9% net loss ratio and 98.2% combined for FY2025 track with the income statement data. The improvement in loss ratio from FY2024's 68.4% is offset by a higher expense ratio, which explains why the combined ratio actually worsened. The premium-to-surplus ratio of 4.4x seems reasonable given the equity base, and the investment income yield of around 3.1-3.4% on roughly $1.08B in in

  - 🔎 checked `research` {"question": "What is the current analyst/market consensus on Root Inc (ROOT auto insurance insurtech) in 2025-2026 \u2014 price targets, bull and bear thesis, and how analysts value it? Also what is Root's actual current shares outstanding (Class A + Class B) and Carvana's ownership stake and warrant terms?"}
    → `RESEARCH — What is the current analyst/market consensus on Root Inc (ROOT auto insurance insurtech) in 2025-2026 — price targets, bull and bear thesis, and how analysts value it? Also what is Root's actual current shares outstanding (Class A + Class B) and Carvana's ownership stake and warrant terms?
I'll research Root Inc (ROOT) thoroughly, covering analyst consensus, valuation approach, share counts, and the Carvana relationship details.The results came back empty in the printed view. Let me inspect the raw structure.The results are JSON strings. Let me parse them properly and extract content.Good progress. Let me get more recent and specific data — the latest analyst targets, exact share counts from the most recent 10-Q, and detailed Carvana warrant terms. Let me run targeted follow-up searches.I have strong, recent data. Let me get a couple final details: the exact total shares outstanding (Class A + Class B) from the most recent filing/cover page, and recent Q3/Q4 2025 financial specifics. Let me check the SEC 10-Q cover and a couple more recent points.I have comprehensive, recent data. Let me get the precise total shares outstanding figure by checking the StockTitan Q4 articl`

  - 🔎 checked `get_transcripts` {}
    → `EARNINGS CALL TRANSCRIPTS (most recent first):

=== Q1 FY2026 (2026-05-07) ===
Operator: Ladies and gentlemen, greetings, and welcome to the Root, Inc. Q1 '26 Earnings Conference Call. [Operator Instructions] As a reminder, this conference is being recorded. It is now my pleasure to introduce your host for today, Matt LaMalva, Head of IR and Corporate Development. Please go ahead.
Matthew LaMalva: Good afternoon and thank you for joining us. Root is hosting this call to discuss its first quarter 2026 earnings results. Participating on today's call is Alex Timm, Co-Founder and Chief Executive Officer; and Megan Binkley, Chief Financial Officer. Earlier today, Root issued a shareholder letter announcing its financial results. We'll focus today on how we're executing against our model and the progress we're delivering across the business. While today's discussion will reflect the shareholder letter for more complete information about our financial performance, we also encourage you to read our first quarter 2026 Form 10-Q, which was filed with the Securities and Exchange Commission today. Before we begin, I want to remind you that matters discussed on today's call will include forward`

  _reviewer note:_ Let me verify the consensus narrative, share count, and a couple of load-bearing industry claims.

> _reviewer reasoning:_ I'm seeing a significant disconnect between the memo's valuation and market consensus. The memo arrives at a fair value of $26 based on book value and a 1.4x multiple, while analysts are pricing Root at roughly 4x book value—substantially higher. This divergence is crucial because the memo deliberately avoids price-based reasoning, yet the consensus valuations are entirely price-driven.
> 
> On the share count front, the memo's figures are solid. The actual common shares outstanding are about 15.82 million, and the memo's 15.5 million basic shares is close enough. The fully diluted count of 17.7 million aligns well with the data. Book value per share checks out at $18.4 on a fully diluted basis, matching the memo's calculation of $20.6 on basic shares.
> 
> For Carvana's stake, there's a minor discrepancy—the research shows about 19.3% as-converted while the memo cites 14%, though the memo also mentions a theoretical maximum of 29.9%. The 14% figure might be capturing just the preferred and vested portions, so it's in the ballpark even if slightly conservative. The warrant tranches are consistent across sources at roughly 7 million shares with strikes ranging from $180 to $540.
> 
> The operat

  _reviewer note:_ I have enough to render a verdict. The memo's operational and financial facts check out remarkably well against the filings and my independent research. Let me finalize.

_independent judge:_ score 86/100, best_in_existence=False

  - FACTUAL ERROR: Cost of equity is stated as '≈14%' but the disclosed buildup (4.3% + 1.5×5.0% + 3.0%) sums to 14.8%; rounding down ≈0.8 points modestly inflates every scenario value.

  - FACTUAL ERROR: Current Carvana economic ownership is ≈19.3% as-converted (Feb 2026 13D/A), not the ≈14% cited in the risk section (the memo is internally inconsistent, elsewhere citing the 29.9% theoretical max).

  - GAP: The base-case valuation sets book CAGR (14%) equal to the cost of equity (14%), so the seven-year compounding mathematically cancels and value reduces to BVPS × terminal P/B. The multi-stage framework is therefore largely cosmetic in the modal case; the memo should make transparent that the two true levers are current book and the terminal multiple.

  - GAP: Terminal P/B assumptions (1.4x base, 1.7x bull) exceed the warranted (ROE−g)/(CoE−g) values they imply (≈1.2x and ≈1.5x). They are cross-checked against peers but not reconciled to the memo's own excess-return math.

  - GAP: Scenario probability weights (30/40/20/10) are asserted with qualitative rationale rather than derived from base rates (e.g., how often a turnaround insurer sustains sub-target loss ratios through a soft cycle).

  - GAP: The dominant named risk — reserve adequacy on a young, fast-growing, 4.4x-levered book — is discussed only narratively. A best-in-class memo would analyze prior-year reserve development / loss triangles quantitatively, since that is the variable most likely to break the thesis.

  - GAP: Statutory surplus, RBC ratio, and the 4.4x premium-to-surplus figure are stated but not derived from the statutory filings; investment-portfolio composition and the 5%-yield redeployment lever are asserted, not modeled.

  - GAP: Persistency/retention is correctly flagged as the key undisclosed variable but is left unestimated; a triangulation (e.g., from PIF vs new-writings growth) would strengthen the durability case.

  - GAP: All three cross-checks (normalized earnings $32-45, peers $26-37) land at or above the $26 center; the memo does not fully reconcile why it anchors to the low end of its own evidence.

## Step 7

**🧠 PM reasoning:**

> The judge marked it 86/100 and flagged the cost of equity discrepancy—I had 14% in some places but derived 14.8% using the buildup method (risk-free rate 4.3% plus beta 1.5 times equity risk premium 5.0%, plus size premium 3.0%). I need to pick one and stick with it; 14.8% is the more rigorous calculation, so I'll use that consistently and recompute the scenario valuations with the corrected rate.
> 
> Running through the math with the higher discount rate lowers the present values across all four scenarios—the weighted composite comes to around $24.5 instead of $26, which actually aligns better with the judge's concern that rounding down the cost of equity was inflating the valuation. The judge also flagged that my terminal price-to-book assumption of 1.4x exceeds what's warranted by fundamentals, and I need to check how the cross-checks are landing.
> 
> I'm realizing the core issue: when growth roughly equals the cost of equity, the compounding and discounting nearly cancel out, leaving the value as essentially today's book value times the terminal multiple. That's actually intuitive—if a company grows its book at its cost of equity, the present value of the terminal book equals today's book times the terminal P/B multiple, and value creation comes from the terminal P/B exceeding 1. But I need to make sure that terminal multiple is internally consistent with the ROE, cost of equity, and growth assumptions, rather than just asserting it. The warranted terminal P/B should flow from the relationship between terminal ROE, terminal growth, and cost of equity.
> 
> Let me recalculate the terminal multiples using the warranted formula to ensure consistency across my base, bull, bear, and adverse cases, then adjust my assumptions if the resulting multiples seem too extreme. Now I'm computing the valuations across all four scenarios using the reconciled terminal P/B multiples and the 7-year holding-period discount rate. The math shows the bear cases become more punitive—S3 drops to $10.89 and S4 to $4.93—which pulls the probability-weighted fair value down to around $24.50. But there's a tension here: the cross-checks all point to $26 or higher, so anchoring to the lower figure feels conservative relative to those other approaches.
> 
> I'm reconsidering the scenario weights and whether 30% on impairment is too harsh. The judge's feedback cuts both ways—the higher cost of equity does push value down, but the cross-checks suggest I shouldn't anchor to the low end. I think the honest middle ground is setting fair value around $25 with a band from $16 to $35, acknowledging that the central case sits between the DCF rigor and the upside signals from earnings and peer multiples. The 30/40/20/10 weighting feels defensible given Root's narrow competitive edge and only two years of sustained profitability, even if the current run-rate ROE and structural growth levers hint at potential upside.
> 
> Now I need to lock in the floor at roughly $20 based on excess returns at a 16% ROE, then address several gaps: clarifying the Carvana ownership to 19.3% as-converted per the February 2026 filing, making explicit that when growth approximates the cost of equity the value hinges on current book value and terminal multiple, and pulling the quantitative reserve adequacy data from the loss development triangles.
> 
> I'll reach out to the analyst for prior-year reserve development figures, statutory capital and surplus, RBC ratios, the current Carvana ownership percentage, and any retention or persistency metrics from the filings.

**PM note:** The judge raised fair, fixable points. Let me close the quantitative gaps (reserve development, statutory surplus/RBC, Carvana's actual ownership %), correct the cost-of-equity arithmetic, reconcile terminal multiples to warranted P/B, and re-run the valuation.

### ⚙️ `ask_analyst`

_input:_ `{"analyst_id": "a1-p&c", "question": "Five precise items from the FY2025 10-K and Carvana 13D/A, with figures and citations:\n(1) PRIOR-YEAR RESERVE DEVELOPMENT: from the loss & LAE reserve roll-forward (the \"incurred related to prior years\" line) in the 10-K, give me the dollar amount of favorable/(adverse) prior-year development for accident years recognized in 2023, 2024, and 2025. Was the young book developing favorably or adversely? Also net reserves for loss & LAE at YE2024 and YE2025.\n(2) STATUTORY SURPLUS & RBC: total statutory capital & surplus at 12/31/2025 (and per subsidiary if disclosed), and the actual RBC ratio / authorized-control-level multiple. Derive the consolidated premium-to-surplus ratio (gross and net written premium \u00f7 statutory surplus).\n(3) INVESTMENT PORTFOLIO: composition at 12/31/2025 (fixed maturities by type, cash, duration, average rating, book yield) \u2014 enough to model a redeployment of excess cash from ≈3.4% blended toward the bond-sleeve yield.\n(4) CARVANA OWNERSHIP: per the most recent 13D/A (\u2248Feb 2026), Carvana's CURRENT beneficial / as-converted economic ownership of Root (%), and the components (preferred + vested warrants). I've seen ≈19.3% \u2014 confirm.\n(5) RETENTION/PERSISTENCY: any disclosed retention rate, or triangulate it \u2014 given FY2025 ending PIF 481,869 vs FY2024 414,862 and the new-writings growth, what does implied retention look like?"}`

_returned:_

```
ANALYST [a1-p&c] (P&C insurance / InsurTech specialist) follow-up:
I now have the reserve development. Here's the complete, sourced answer on all five items.

---

# ROOT, INC. — Five Precise Items (FY2025 10-K / Carvana 13D/A)

## (1) Prior-year reserve development — the young book is developing FAVORABLY, and accelerating

"Incurred related to prior years" (net of reinsurance), from the loss & LAE reserve reconciliation in the FY2025 and FY2024 10-Ks:

| Calendar year | Prior-year development | Direction |
|---|---|---|
| 2022 | +$2.9M | Adverse (deficiency) |
| **2023** | **−$7.0M** | **Favorable** |
| **2024** | **−$19.4M** | **Favorable** |
| **2025** | **−$29.4M** | **Favorable** |

(Source: Root FY2025 10-K, accession 0001788882-26-000014; FY2024 10-K, accession 0001628280-25-008137 — loss & LAE reserve reconciliation footnote. Negative = reserve release = favorable.)

**Read-through:** This is one of the most important confirmations in the whole thesis. After a small deficiency in 2022 (legacy mispriced book), Root has booked **three consecutive years of growing favorable development — $7.0M → $19.4M → $29.4M.** The young, fast-growing book is developing **favorably and at an accelerating rate**, which (a) validates that pricing/reserving is conservative rather than aggressive, (b) is consistent with the auditor's CAM testing for reserve *bias* finding none, and (c) means the reported ≈59% gross / ≈66% net loss ratios are **not** being flattered by reserve weakening — if anything the opposite. For a telematics start-up that historically *under*-reserved, this is the single best evidence the underwriting turn is real. The 2025 release (−$29.4M) equals ≈2.1 pts of NEP of tailwind.

**Net loss & LAE reserves (10-K Item 8 balance sheet, which I pulled): YE2024 $413.2M → YE2025 $483.6M** (+$70.4M; ties to the cash-flow reserve build of $70.4M). Reserves grew slightly *faster* than NEP (+31% vs +31% NEP) — they are not running reserves down to manufacture earnings.

---

## (2) Statutory surplus, RBC, and premium-to-surplus

**What's confirmed (10-K + calls):**
- **All insurance subsidiaries' RBC is above company-action-level thresholds at 12/31/2025**; regulators require Root to hold RBC **>200% of authorized control level (ACL)** given its short operating history (10-K).
- Management cites **≈$312M unencumbered capital** at YE2025 and repeatedly states the subsidiaries carry **excess capital** ("position of excess capital across our insurance subsidiaries," Q3'25 call).
- Subsidiaries: Root Insurance Co. & Root P&C (Ohio), Root Florida (new 2025), plus Root Re (Cayman captive).

**What I could NOT verify:** the **exact per-subsidiary statutory capital & surplus dollars at 12/31/2025 and the specific ACL multiple.** These sit in the 10-K "Statutory Financial Information" note, which my filing tool cannot page to and which web snippets don't expose. I won't fabricate them. **Action: read the note directly** (FY2023 comparison for scale: combined ≈$81.4M — RIC $60.1M + R&PC $21.3M — but that was when ≈50%+ quota share provided surplus relief; the figure is materially higher now that quota share is largely gone).

**Premium-to-surplus (derived, with the surplus caveat):**
- Gross written premium FY2025 **≈$1.5B**; net written premium **≈$1.44B** (NEP $1,401.7M + $39.8M unearned build, per cash flow).
- Against an *estimated* combined group statutory/excess capital of ≈$300–450M:

| Surplus assumption | Gross P/S | Net P/S |
|---|---|---|
| $300M | ≈5.0x | ≈4.8x |
| $400M | ≈3.8x | ≈3.6x |
| $450M | ≈3.3x | ≈3.2x |

**This is the key structural point:** even on generous surplus assumptions, Root runs a **high premium-to-surplus ratio (≈3.3–5x net vs. the ≈3:1 P&C rule of thumb)**. And it has *risen* mechanically as Root wound down quota share — ceding less premium means retaining more risk per dollar of surplus. So the de-ceding that boosted the net combined ratio (prior memo) came at the cost of **higher underwriting leverage**. This is fine while the loss ratio holds at ≈59% and development is favorable, but it means the capital base has *less* cushion for a bad accident year than a typical mutual/standard carrier — a real risk for the red team. **Confirm the exact surplus before sizing this.**

---

## (3) Investment portfolio at 12/31/2025 — cash-heavy, high-quality, short; clear NII upside

Composition (10-K Item 8 / Q1'26 10-Q investments note):

| | $M | % of investable |
|---|---|---|
| Cash & cash equivalents | 669.3 | 62% |
| Restricted cash | 20.6 | 2% |
| **Fixed maturities** | **387.0** | **36%** |
| — US Treasury/agency | 49.2 | |
| — Municipal | 23.2 | |
| — Corporate | 159.0 | |
| — Asset-backed | 155.6 | |
| Other (private equity) | 4.4 | <1% |
| **Total investable** | **≈1,081** | 100% |

- **Credit quality (very high):** AAA 21.2% / AA 44.8% / A 28.1% / BBB 5.9% → **94.1% rated A- or better** (Q4'25 amortized-cost basis).
- **Duration (short):** maturity ladder (Q1'26): ≤1yr 11%, 1–5yr 63%, 5–10yr 12%, >10yr 15% → effective duration roughly **≈2.5–3 years** (Root doesn't publish a single duration number; Item 7A says a ±100bp SOFR move is "not significant" to interest expense given the small floating term loan).
- **Yields:** FY2025 NII **$33.7M → ≈3.1–3.4% blended.** Decomposed (Q1'26 run-rate): **bond sleeve ≈4.7–5.0%** ($4.7M/qtr on ≈$390–420M) vs. **cash ≈3.3%** ($5.3M/qtr on ≈$650M).

**Redeployment model (the upside you wanted to frame):** ≈64% of the portfolio sits in cash earning ≈3.3% while the bond sleeve earns ≈4.8%. Shifting **$400M of excess cash into the bond book at a ≈+1.5% spread ≈ +$6M/yr pre-tax NII** — roughly **+15% on FY2025 pre-tax income of $40.8M**, dropping almost entirely to the bottom line (Root carries a full DTA valuation allowance, so cash taxes are negligible). $500M shifted ≈ +$7.5M. This is low-risk, self-help earnings/ROE the company is currently leaving on the table; the only constraints are short-tail auto liquidity needs (well cover
```

## Step 8

**🧠 PM reasoning:**

> The favorable reserve development is accelerating significantly—jumping from a $7 million release in 2023 to nearly $30 million in 2025—which validates the underwriting improvement and substantially de-risks reserve adequacy concerns. That 2025 release translates to roughly 2.1 points of net earned premium tailwind, though it's worth noting that about 2 points of the loss ratio improvement comes from this favorable development, meaning the underlying accident-year loss ratio is still about 2 points worse than the calendar-year figure. Meanwhile, net reserves grew from $413.2 million at year-end 2024 to $483.6 million by year-end 2025.
> 
> The premium-to-surplus ratio has climbed to 3.3–5.0x as the quota share wound down, which is a meaningful risk. The investment portfolio sits heavily in cash at 62%, leaving a redeployment lever of $6–8 million in net investment income—roughly 15–20% of pretax earnings. The Carvana position needs correction: it's actually 19.3% on an as-converted basis, representing 3.7 million shares (0.78 million preferred plus 2.93 million vested warrants). Retention rates aren't disclosed, but the model runs at roughly 70–80% retention, so the book isn't compounding off a sticky base—growth requires heavy new business acquisition.
> 
> Now I'm reconciling everything to finalize the valuation. I'll use the corrected cost of equity at 14.8%, reconcile terminal price-to-book multiples to the warranted levels derived from ROE, growth, and cost of equity, recompute the composite with the three scenarios and their probability weights, and add sections on reserve development, statutory metrics, and retention dynamics. I'll also correct the Carvana position and explain why the anchor sits near $25 rather than higher multiples.
> 
> Running through the scenario analysis with the reconciled terminal multiples and a 7-year holding period at 14.8% cost of equity, the weighted fair value comes to approximately $24.50. The normalized earnings cross-check suggests $32–45, but that assumes favorable development and reserve releases persist indefinitely plus full capital productivity—none of which holds given the softening market and high churn risk. The peer multiple cross-check at 1.4–1.7x book lands at $26–31, so $25 sits at the low-center of the evidence.
> 
> I'm reconsidering whether I'm being too conservative. The favorable reserve development is genuine and supports the base and bull cases, but the high premium-to-surplus ratio, elevated churn, and softening cycle are real headwinds. I'll adjust the scenario weights slightly upward for the base case given the strong development evidence—moving to 30% bull, 42% base, 20% bear, 8% adverse gives a weighted value of about $25. For the floor, using an excess-return approach with 16% ROE, 3% growth, and 14.8% cost of equity yields roughly $20. I'll set the valuation band at $16 to $34, capturing the central distribution around the $25 midpoint.
> 
> Now I'm running the valuation model with these corrected inputs and weights to finalize the analysis.

**PM note:** The reserve work is decisive: Root has booked **three years of accelerating favorable prior-year development (−$7.0M → −$19.4M → −$29.4M)** — strong evidence the underwriting turn is real and reserves are conservative, not flattered. Offsetting that, premium-to-surplus is high (≈3.3–5x) and retention is undisclosed/high-churn. Let me re-run the valuation with the corrected 14.8% cost of equity and terminal multiples reconciled to warranted P/B.

### ⚙️ `compute_valuation`

_input:_ `{"method": "composite", "rationale": "Corrected build: cost of equity = 4.3% (10yr UST) + 1.5 beta x 5.0% ERP + 3.0% micro-cap/illiquidity = 14.8% (holding-period discount rate). Each scenario's terminal P/B is reconciled to warranted P/B = (terminal ROE - g)/(terminal CoE - g), where terminal CoE falls below 14.8% in good scenarios to reflect de-risking as Root scales. BVPS_0 = $18.4 (common equity $325.9M / 17.7M FD). Weights nudged to 30/42/20/8 to reflect three years of accelerating FAVORABLE reserve development (de-risks the young book) against high premium-to-surplus leverage, undisclosed/high churn, and a softening cycle. Note: because base-case book growth (14%) approximates the 14.8% discount rate, value in the modal case reduces to roughly BVPS_0 x terminal P/B - i.e., the two true levers are current book and the terminal multiple; growth mainly adds value in the high-ROE scenarios where it compounds above the discount rate.", "composite": {"scenarios": [{"name": "Compounder works \u2014 durable ≈18% ROE, share gains", "probability": 0.3, "sub_method": "worked", "rationale": "Telematics + embedded/agent flywheel sustains ≈15% premium growth, ≈18% ROE; terminal ROE 18% / g 5% / de-risked CoE 12% => warranted P/B 1.8x.", "worked": {"framework": "BVPS compounding to warranted terminal P/B, PV at 14.8% CoE", "key_inputs": {"bvps0": 18.4, "g": 0.18, "n": 7, "pb": 1.8, "coe": 0.148}, "formula": "bvps0*(1+g)**n*pb/(1+coe)**n"}}, {"name": "Solid grower \u2014 base, ≈16% ROE`

_returned:_

```
VALUATION (composite): fair value/share = 24.9171
equity_value=None EV=None
working={"branches": [{"name": "Compounder works \u2014 durable ≈18% ROE, share gains", "probability": 0.3, "sub_method": "worked", "value_per_share": 40.1487, "rationale": "Telematics + embedded/agent flywheel sustains ≈15% premium growth, ≈18% ROE; terminal ROE 18% / g 5% / de-risked CoE 12% => warranted P/B 1.8x."}, {"name": "Solid grower \u2014 base, ≈16% ROE", "probability": 0.42, "sub_method": "worked", "value_per_share": 24.5294, "rationale": "Mid-teens ROE, ≈14% book growth, mid-90s combined through cycle; terminal ROE 16% / g 4% / CoE 12.5% => warranted P/B 1.4x."}, {"name": "Cycle softens / growth stalls \u2014 ≈11% ROE", "probability": 0.2, "sub_method": "worked", "value_per_share": 10.88, "rationale": "Soft market + competition compress growth; loss ratio normalizes toward 63-65% target, combined ≈99-100%, ROE ≈11%; terminal ROE 11% / g 3% / CoE 13% => warranted P/B 0.85x."}, {"name": "Adverse \u2014 reserve/competitive shock, dilutive", "probability": 0.08, "sub_method": "worked", "value_per_share": 4.9263, "rationale": "Telematics edge fails through full cycle or adverse development on the 4x-levered book; ROE ≈7%, book +5%/yr; terminal ROE 7% / g 2% / CoE 14% => warranted P/B 0.5x; possible dilutive raise."}]}
notes: Composite of 4 event branches (worked), probability-weighted.
```

## Step 9

**🧠 PM reasoning:**

> I'm finalizing the valuation with FMV at $25, a floor of $20, and a trading band between $16-34. Now I need to update the memo with the complete analysis including the cost of equity at 14.8%, Carvana's comparable at 19.3%, and add sections covering reserve development, statutory metrics, premium-to-surplus ratios, retention rates, portfolio redeployment strategy, and terminal price-to-book reconciliation.

**PM note:** FMV = **$24.9 ≈ $25** with the corrected 14.8% cost of equity and warranted-P/B-reconciled terminal multiples. Now I'll resubmit with every judge point addressed: corrected arithmetic, Carvana at 19.3%, a quantitative reserve-development analysis, statutory/premium-to-surplus derivation, the portfolio-redeployment model, retention triangulation, terminal-multiple reconciliation, base-rate-justified weights, and an explicit reconciliation of the cross-checks.

### ⚙️ `submit_final`

_gate verdict:_ ACCEPTED.

**🔬 Red-team's own verification (how it checked the numbers):**

> _reviewer reasoning:_ The author has addressed my earlier concerns about the cost of equity rounding and acknowledged the base-case growth rate issue in their memo, though they've kept the if-converted preferred share count treatment as-is since it's conservative and doesn't materially affect the valuation.
> 
> Now I'm verifying the revised composite valuation of $24.92 by recalculating the weighted scenarios, and checking that the terminal P/B multiples align with the warranted formulas derived from ROE, growth, and cost of equity assumptions. The math checks out across all four scenarios—compounder, base, cycle, and adverse—and the individual scenario valuations are reconciling properly.
> 
> I'm also reviewing the supporting claims: the favorable reserve development figures are plausible and directionally supportive of the compounder thesis, the Carvana ownership correction to 19.3% as-converted is more accurate, and the premium-to-surplus range of 3.3–5x is appropriately flagged as a risk. The higher 14.8% cost of equity has been applied throughout, which actually brought the valuation down to $25 from the prior $26, so there's no value-changing error remaining. Everything I raised has been addressed, and 

  _reviewer note:_ The author has substantively addressed every concern I raised. Let me verify the revised numbers.

**Re-verification of the revised memo:**

1. **Cost of equity (my prior flag: 14.8% rounded to 14%)** — ✅ **CORRECTED.** The memo now uses 14.8% explicitly throughout, rebuilt as 4.3% + 1.5×5.0% + 3.0% = 14.8%, and re-runs the model. The composite correctly drops to $24.92. Verified: 0.30×40.1 + 0.42×24.5 + 0.20×10.9 + 0.08×4.9 = $24.89. Conceded.

2. **Base-case g = CoE cancels the compounding (my prior methodology note)** — ✅ **CONCEDED TRANSPARENTLY.** The memo now states this openly: "Because base-case book growth (14%) ≈ the 14.8% discount rate, the seven-year compounding nearly cancels… value there reduces to ≈ BVPS₀ × terminal P/B." The author discloses rather than hides it. Dropped.



_red-team concerns this round:_

- [low/dilution] Diluted share count includes if-converted OTM preferred shares while the preferred is also subtracted from equity as a senior claim.

**🔬 Judge's own verification (independent fact-check):**

> _reviewer reasoning:_ I'm reviewing the revised memo to see if my earlier concerns were addressed. The first issue about the base case—where 14% growth nearly equals the 14.8% discount rate, causing compounding to flatten—is now explicitly called out in the memo, which is good transparency. The second concern about terminal P/B ratios needs verification against the formula (ROE-g)/(CoE-g) for each scenario, and I'm starting to check the math on the Compounder case with 18% ROE, 5% growth, and 12% cost of equity.
> 
> Now I'm working through the terminal P/B calculations for each scenario to confirm they reconcile properly, then moving on to verify the per-share value computations using the book value growth rates and discount factors.
> 
> The weighted average across all four scenarios—30% compounder, 42% base, 20% cycle, 8% adverse—comes to roughly $25, which validates the internal consistency of the model.
> 
> The analysis has also been strengthened considerably: reserve development is now quantified with specific year-over-year figures showing the progression of adverse development, net reserve growth is documented at 17%, and the normalized release impact is calculated at roughly 2.1 points of net earned premi

  - 🔎 checked `read_filing_section` {"form": "10-K", "section": "prior year development reserves loss and loss adjustment expense reconciliation"}
    → `Section 'prior year development reserves loss and loss adjustment expense reconciliation' not found in 10-K. Available: Item 1A, Item 1, Item 2, Item 7, Item 7A, Item 8. Head:
root-20251231 false 2025 FY 0001788882 P2Y P2Y P1Y P2Y P1Y P3D http://fasb.org/us-gaap/2025#OtherLiabilities http://fasb.org/us-gaap/2025#OtherLiabilities http://fasb.org/us-gaap/2025#OtherAssets http://fasb.org/us-gaap/2025#OtherAssets http://fasb.org/us-gaap/2025#AccountsPayableAndAccruedLiabilitiesCurrentAndNoncurrent http://fasb.org/us-gaap/2025#AccountsPayableAndAccruedLiabilitiesCurrentAndNoncurrent 457 461 459 473 iso4217:USD xbrli:shares iso4217:USD xbrli:shares xbrli:pure root:day root:tranche root:claim root:vote 0001788882 2025-01-01 2025-12-31 0001788882 2025-06-30 0001788882 us-gaap:CommonClassAMember 2026-02-18 0001788882 us-gaap:CommonClassBMember 2026-02-18 0001788882 2025-12-31 0001788882 2024-12-31 0001788882 us-gaap:CommonClassAMember 2024-12-31 0001788882 us-gaap:CommonClassAMember 2025-12-31 0001788882 us-gaap:CommonClassBMember 2024-12-31 0001788882 us-gaap:CommonClassBMember 2025-12-31 0001788882 2024-01-01 2024-12-31 0001788882 2023-01-01 2023-12-31 0001788882 2022-12-31 0001788882 us-`

  - 🔎 checked `get_statement` {"statement": "income", "period": "annual", "limit": 2}
    → `ROOT INCOME (annual, recent first) — full line items:

[2025-FY] (2025-12-31)
  revenue=1517100000
  costOfRevenue=1130500000
  grossProfit=386600000
  researchAndDevelopmentExpenses=0
  generalAndAdministrativeExpenses=96900000
  sellingAndMarketingExpenses=174800000
  sellingGeneralAndAdministrativeExpenses=271700000
  otherExpenses=74100000
  operatingExpenses=345800000
  costAndExpenses=1476300000
  netInterestIncome=19100000
  interestIncome=40100000
  interestExpense=21000000
  depreciationAndAmortization=11800000
  ebitda=73600000
  ebit=61800000
  nonOperatingIncomeExcludingInterest=-21000000
  operatingIncome=40800000
  totalOtherIncomeExpensesNet=0
  incomeBeforeTax=40800000
  incomeTaxExpense=-500000
  netIncomeFromContinuingOperations=41300000
  netIncomeFromDiscontinuedOperations=0
  otherAdjustmentsToNetIncome=-1000000
  netIncome=40300000
  netIncomeDeductions=0
  bottomLineNetIncome=38300000
  eps=2.49
  epsDiluted=2.24
  weightedAverageShsOut=15500000
  weightedAverageShsOutDil=17200000

[2024-FY] (2024-12-31)
  revenue=1176500000
  costOfRevenue=839400000
  grossProfit=337100000
  researchAndDevelopmentExpenses=0
  generalAndAdministrativeExpenses=69500000
  selli`

  _reviewer note:_ This is a materially revised memo. Let me verify the new load-bearing additions — especially the quantitative reserve-development figures, which are now central to the thesis.

> _reviewer reasoning:_ Looking at the income statement, the revenue of $1,517.1M and net income to common of $38.3M align with the memo, along with the diluted EPS of $2.24 and share counts. But there's a discrepancy with stock-based compensation — calculating it from the ratio gives roughly $60M annually, which is notably higher than the $40M mentioned in the memo.
> 
> I couldn't retrieve the reserve development reconciliation table directly from the filing, but the specific figures (-$7.0M, -$19.4M, -$29.4M) are the type that would appear in the loss reserve notes and seem plausible given the direction of favorable development. The net loss reserves increasing from $413.2M to $483.6M is consistent with what I'd expect from the balance sheet. Investment income of $33.7M also checks out as reasonable for net investment income after expenses.
> 
> The core numbers are holding together — the reserve development is now quantified and integrated into the analysis, and the terminal P/B reconciles back to the warranted formula.
> 
> The memo is now quite thorough and well-reasoned, though a few minor uncertainties remain: I couldn't independently verify those exact reserve figures, there's a small discrepancy between the

  _reviewer note:_ This revision has addressed essentially every prior objection in the actual numbers. Let me verify the math and remaining figures before finalizing.

The income statement confirms: NI-to-common $38.3M, diluted EPS $2.24, 15.5M basic / 17.2M diluted weighted shares — all tie to the memo. Let me check the scenario math and reconciled terminal multiples:

- **Compounder:** 18.4 × 1.18⁷ × 1.8 ÷ 1.148⁷ = 18.4 × 3.186 × 1.8 ÷ 2.628 = **$40.1** ✓; warranted (0.18−0.05)/(0.12−0.05)=1.86→1.8x ✓
- **Base:** 18.4 × 1.14⁷ × 1.4 ÷ 1.148⁷ = **$24.5** ✓; warranted (0.16−0.04)/(0.125−0.04)=1.41→1.4x ✓
- **Cycle:** 18.4 × 1.09⁷ × 0.85 ÷ 1.148⁷ = **$10.9** ✓
- **Adverse:** 18.4 × 1.05⁷ × 0.5 ÷ 1.148⁷ = **$4.9** ✓
- **Weighted:** 0.30×40.1 + 0.42×24.5 + 0.20×10.9 + 0.08×4.9 = **$24.9** ✓
- **Floor:** (0.16−0

_independent judge:_ score 91/100, best_in_existence=True

  - FACTUAL ERROR: SBC is cited at ≈$40M/yr, but the TTM stock-based-comp-to-revenue ratio (≈3.96%) implies closer to ≈$55-60M on FY2025 revenue; if so, the ≈2-3% annual share-creep estimate is slightly understated. Not material to the valuation conclusion.

  - GAP: Statutory surplus is an estimated range (≈$300-450M), making the premium-to-surplus figure a wide 3.3-5x band; a precise pull from the statutory (yellow-book) filings would tighten the leverage analysis — though this is constrained by disclosure timing.

  - GAP: True policy-level retention/persistency remains undisclosed and is therefore estimated (≈70-80%) rather than observed; the thesis would be even stronger with cohort LTV/CAC data if Root ever discloses it.

  - GAP: The exact prior-year reserve-development figures, while specific and internally consistent, rest on the author's 10-K Item 8 citation that could not be re-pulled via the filing tool this review; a reproduced reconciliation table would be the final belt-and-suspenders.


---

# FINAL CONSOLIDATED MEMO

# Root, Inc. (NASDAQ: ROOT) — Initiation / Full Valuation Memo

**Sector:** Financial Services — P&C Insurance (telematics auto InsurTech) | **HQ:** Columbus, OH
**Valuation method:** Multi-stage book-value-per-share compounding at a probability-weighted sustainable ROE (financial/spread frame), discounted at 14.8% cost of equity; terminal multiples reconciled to warranted P/B; cross-checked vs normalized earnings power and peers.
**Headline fair value:** **$25 / share** | **Confidence band:** **$16 – $34** | **No-growth floor:** **$20** | **Fully-diluted shares:** 17.7M

---

## 1. Executive summary

Root is a telematics-first, direct-to-consumer and embedded auto insurer that has executed one of the more remarkable turnarounds in InsurTech. After IPO-ing in 2020 at ≈$6.7B and nearly self-immolating — cumulative losses drove the accumulated deficit to **−$1.64B** — it restructured, fixed its underwriting, wound down a capital-draining quota-share reinsurance program, and reached its first full year of GAAP profit in 2024. The trajectory since is genuinely strong: revenue grew **$455M (FY2023) → $1.18B (FY2024) → $1.52B (FY2025)**; net income **−$147M → +$31M → +$40M**; and Q1 2026 was the most profitable quarter in company history (**$36M net income, 47% annualized ROE**). Critically, the underwriting is **conservatively stated** — Root has booked three consecutive years of *accelerating favorable* prior-year reserve development (−$7.0M → −$19.4M → −$29.4M), the single best evidence that the loss-ratio turn is real rather than an artifact of under-reserving.

The investment question is **not** whether Root is viable — it now clearly is — but **how durable its high returns and high growth are**, because that is the entire valuation. Root is a financial/spread business, so the correct lens is **book value compounding at a sustainable ROE**, with its long growth runway (0.4% share of a $350B market) captured in a multi-stage frame and its cyclicality/competitive/leverage risk captured in the probability weighting and discount rate.

My probability-weighted fair market value is **$25 per share**, against a conservative no-growth floor of **$20** (≈1.1x current common book of $18.4). The central tension is real and I weight it honestly: Root is the best insurtech auto *underwriter* in existence (≈59% gross loss ratio, ≈17 points better than Lemonade's car book), with reserves developing favorably and a genuine, narrow distribution edge (embedded + independent-agent) — **but** it is sub-scale (0.4% share) against an oligopoly with a permanent cost-of-capital advantage, its telematics confers no durable pricing moat, it runs high underwriting leverage (≈3.3–5x premium-to-surplus), retention is undisclosed (a high-churn model), and a slice of the turnaround rode the 2022–24 hard-market rate wave now reversing. This is an execution/growth bet, not a moat bet — and the valuation reflects it with a 28% combined weight on impaired outcomes. Conviction: **moderate (0.55)**.

---

## 2. Business deep-dive — how Root actually makes money

**The product.** Root sells personal auto insurance (plus small renters/homeowners books) priced primarily on **telematics** — driving behavior captured through a smartphone app. A prospect takes a 2–3 week "test drive"; the app's accelerometer/gyroscope scores braking, cornering, acceleration, time-of-day, mileage and distraction over ≈500 miles. Driving score is the **No. 1 rating factor**, and Root will **decline** poor risks rather than merely surcharge. The bet, validated in the numbers, is that behavioral data segments risk better than the demographic proxies (credit, ZIP, age) that dominate legacy rating.

**The economics, with numbers.** Root earns two ways:

1. **Underwriting margin.** FY2025: **$1,401.7M net earned premium**, **$924.2M losses & LAE** (65.9% net loss ratio), **32.3% net expense ratio** → **98.2% net combined ratio** (≈1.8¢ underwriting profit per premium dollar). On a *gross* accident-period basis: loss ratio **≈59%**, combined **≈97%**. The net combined reconciles exactly to GAAP: (opex $1,455.3M − fee income $78.3M) ÷ NEP $1,401.7M = 98.2%.
2. **Investment income / float.** ≈**$1.08B** investable assets earning **$33.7M (FY2025) — ≈3.4% blended book yield** — with **62% sitting in cash/money-market**, a clear redeployment lever (Section 4).

The "tech company" framing is half-marketing, half-real: the actual edge is a modern **API-native full-stack platform** (quote/bind/underwrite/service/telematics in-house) that lets Root iterate pricing fast and embed insurance in partners' checkout flows.

**Distribution — the structural growth engine.**
- **Direct** (app/web, paid media): the legacy channel, now cyclically soft ("a difficult growth environment that intensified through the quarter," Q1'26).
- **Embedded / partnerships:** ≈**half of new writings in Q4'25**, +30% YoY. Flagship **Carvana** — exclusive embedded insurer across 36 states, quote-to-bind in "3 clicks, ≈30 seconds," **200,000+ cumulative policies**. OEM/connected-car (Toyota/Lexus consented telematics, Hyundai) and Experian extend it.
- **Independent agents:** fastest-growing — **15,000+ agents / 5,000 agencies**, ≈50% of partnership new writings, tripling YoY, yet **<10% of agents** in a ≈$100B channel. Goosehead (quote-to-bind time −50%) and Freeway integrations live.

**Capital structure.** Cash ≈$609–690M; debt only ≈$200M (term loan refinanced BlackRock SOFR+900 → Huntington May 2026, saving ≈$5M/yr). **$75M buyback** authorized May 2026. One wrinkle: a **$112M carrying / $126.5M redemption Carvana Series A convertible preferred**, in mezzanine as a **senior claim ahead of common**, economically debt-like (its $162 conversion is deeply out-of-the-money).

---

## 3. Industry & competitive landscape

*(authored by the desk's insurance industry specialist)*

**How the economics work.** A personal-auto insurer collects *premium*, pays *claims* (losses) plus loss-adjustment expense, and incurs *underwriting expenses* (acquisition/commissions, advertising, overhead). Two ratios define profitability: the **loss ratio** (losses ÷ earned premium) and the **expense ratio** (expenses ÷ premium); their sum is the **combined ratio** (below 100 = underwriting profit). Insurers also earn on **float** — premiums held in reserves before claims are paid. Capital intensity is governed by **premium-to-surplus leverage**: regulators cap premium written per dollar of statutory surplus (≈2:1 conventional), so growth consumes capital. Pricing is regulated state-by-state via **rate filings**, creating a lag between claims inflation and rate relief — the engine of the cycle.

**The cycle (2022–2025).** Post-COVID claims inflation pushed the industry **net combined ratio to 112.2 in 2022** (S&P GMI). Carriers pushed **≈54% cumulative rate increases 2020–2024** (auto-insurance CPI +20.6% YoY in Jan-2024; BLS), restoring profitability — combined fell to **≈105 (2023) and 95.3 (2024)** (A.M. Best). With margins restored, **2025 softened** — full-coverage premiums **−6% nationally** (Insurify). Root's swing from a **$147M net loss (FY2023) to $40M net income (FY2025)** coincided precisely with this rate-earn-through; a portion of its turnaround reflects the cycle, now reversing.

**Market structure.** US private auto is ≈**$359B DPW (2024), +12.6–13.3% YoY**, ≈35% of US P&C (NAIC; S&P GMI). A **consolidating oligopoly** — top-five share **63.6% (2024)**, up from 62.5%. State Farm (≈16–19%) and Progressive (≈16–17%) lead; **Progressive overtook State Farm as #1 on the A.M. Best basis in 2024** (+22% DPW). GEICO (≈10–12%), Allstate (≈8–10%), USAA (≈5–6%) follow. **Root holds ≈0.4%** (≈$1.5B premium).

**Telematics/UBI.** Progressive's **Snapshot** is an *add-on* modifier (hard-brakes-per-mile dominant), able to *surcharge* ≈20% of users. **Root** makes driving score the *primary* variable and *declines* bad risks. The signal is real — telematics adds **≈79% lift** above standard factors with **8.7x frequency separation** (LexisNexis). **But durability is questionable:** that lift is increasingly *buyable* (LexisNexis, CMT); the compounding early-mover advantage accrues to **Progressive** (Snapshot since 2008, 3M+ users by 2015), not Root; aggregate industry profitability didn't improve despite wide adoption (112 combined in 2022). Telematics is **table stakes plus a few points of loss ratio**, not a unique moat.

**Head-to-head.**

| | Combined ratio | Auto gross loss ratio | Ad spend (2024) | Auto share |
|---|---|---|---|---|
| **Root** | ≈97 gross / 98.2 net (FY25); 94.7 gross (FY24) | **≈58–59%** | modest | ≈0.4% |
| **Progressive** | **88.8** | embedded | **≈$3.5B** | ≈16–17% |
| **GEICO** | **81.5** | embedded | ≈$1.7–2.0B | ≈10–12% |
| **Allstate** | ≈mid-90s | — | ≈$1.87B | ≈8–10% |
| **State Farm** | underwriting profit | — | ≈$1.11B | ≈16–19% |
| **Lemonade (auto)** | net loss-making | **≈76%** | modest | <0.5% |

**Root is the superior insurtech underwriter** (≈59% vs Lemonade's ≈76% car book; net-income profitable vs Lemonade's losses). But **it loses to incumbents on the metrics that win commoditized insurance** — a ≈97 combined leaves ≈3¢ margin/premium dollar vs Progressive's ≈11¢ and GEICO's ≈18¢, margin they redeploy to underprice Root *and* outspend it ≈50:1 on advertising; and incumbents fund growth with **float** (Berkshire's ≈$171B negative-cost) while Root uses equity and a secured term loan.

**Verdict.** A **well-run, sub-scale challenger with a real but narrow edge — not a structurally advantaged compounder.** Its defensible asset is a modern, API-native platform that wins *embedded* distribution faster than legacy incumbents can re-platform (lowering CAC, routing around the ad moat). But telematics confers no durable pricing edge, the embedded channel is replicable and partner-dependent (Carvana owns ≈19% of Root), and the **scale and cost-of-capital disadvantages are near-permanent.** Underwrite Root as a high-beta, cycle-exposed share-gainer — an execution/growth bet.

---

## 4. Financial analysis

**The turnaround in the ratios:**

| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | Q1'26 |
|---|---|---|---|---|---|---|
| Revenue ($M) | 345 | 311 | 455 | 1,177 | 1,517 | 394 |
| Net premiums earned ($M) | 310 | ≈258 | 400 | 1,071 | 1,402 | ≈345 |
| Net income ($M) | −521 | −298 | −147 | +31 | +40 | +36 |
| **Gross loss ratio** | ≈82% | ≈82% | ≈70% | **58.9%** | **≈59%** | improving |
| **Net combined ratio** | ≈191% | ≈195% | 133.2% | **96.4%** | **98.2%** | **91.4%** |
| Reinsurance cession | ≈55% | ≈55% | ≈54% (Q1) | ≈6–9% | mid-single | — |
| Policies-in-force | — | — | — | 414,862 | 481,869 (+16%) | +9% YoY |

Three forces drove the swing: **(1)** gross loss ratio collapsed ≈82%→≈59% (the underwriting fix); **(2)** quota-share wound down from ≈55% cession to mid-single-digits, so Root keeps the margin it creates (prepaid reinsurance $25.1M→$6.3M; reinsurance payable $32.8M→$2.4M); **(3)** the industry rate wave earned through. Note FY2025 net combined *rose* 1.8pts YoY (96.4→98.2) **despite** the loss ratio improving (68.4→65.9%) — entirely a higher expense ratio (27.9→32.3%) from *deliberate* growth reinvestment. S&M grew $49M→$136M→$175M but held flat at ≈12.5% of NEP.

**Reserve adequacy (the variable most likely to break the thesis — analyzed quantitatively).** "Incurred related to prior years" (net) from the loss & LAE reconciliation: **+$2.9M adverse (2022) → −$7.0M favorable (2023) → −$19.4M (2024) → −$29.4M (2025).** After a small legacy deficiency, Root has released reserves in **three consecutive, accelerating years**, with the 2025 release ≈ **2.1 points of NEP**. Net loss & LAE reserves **grew** $413.2M (YE24) → $483.6M (YE25), i.e., +17%, broadly with the book — reserves are *not* being run down to manufacture earnings. This is the strongest evidence the underwriting turn is genuine and conservatively stated. The flip side: ≈2pts of the *calendar* loss ratio is favorable-development tailwind, so the *accident-year* loss ratio is ≈2pts worse than the 59% headline — a fact I bake into the normalization.

**Capital / leverage.** ≈$1.08B investable assets (62% cash, 36% fixed maturities — **94.1% rated A-/better**, ≈2.5–3yr duration); reserves ≈$0.9B; debt $200M; common equity **$325.9M** (Q1'26 total equity $437.9M less the $112M preferred). Against an estimated group statutory/excess capital of ≈$300–450M and net written premium ≈$1.44B, **premium-to-surplus is ≈3.3–5x** — above the ≈3:1 P&C rule of thumb, and it *rose* mechanically as quota-share wound down (retaining more risk per dollar of surplus). All subsidiaries are above company-action RBC and management cites ≈$312M unencumbered capital, but the cushion for a bad accident year is thinner than a standard carrier's. **Common book value per share ≈ $18.4 fully-diluted** (≈$20.9 basic) — materially below the $28 some screens show, which wrongly include the senior preferred and a low share count.

**Returns.** FY2025 ROE on common ≈ **15.7%** (NI to common $38.3M ÷ avg common equity $244M); TTM ≈14.7%. Q1'26's 47% annualized is a record, seasonally-flattered quarter, not a run-rate. Reported ROE is *depressed* by ≈$312M excess capital and the cash-heavy 3.4% yield, and *flattered* by a cyclically-low, development-aided loss ratio; normalized through-cycle ROE is most likely **16–20%** on ≈4.4x leverage.

**Investment-yield redeployment (a self-help lever, modeled).** Shifting ≈$400M of excess cash (at ≈3.3%) into the bond sleeve (≈4.8%) at a ≈+1.5% spread adds **≈+$6M/yr pre-tax** (≈+15% of FY2025 pre-tax income of $40.8M), nearly all to the bottom line (a full DTA valuation allowance means negligible cash tax). $500M ≈ +$7.5M. I add ≈$6–8M to normalized NII.

**Share count / dilution.** ≈15.5M outstanding; ≈**17.7M fully-diluted** (+1.3M unvested RSUs, +0.1M options @ $34.80, +0.78M if-converted preferred). The **Carvana warrants (up to ≈7M shares, strikes $180–$540) are deeply OTM and contribute zero base-case dilution** — they matter only if the stock roughly triples-to-6x. SBC ≈$40M/yr (real, in NI) drives ≈2–3% annual share creep, partly offset by the buyback.

**Carvana ownership.** Per the **13D/A (Feb 18, 2026)**, Carvana beneficially owns **3,708,454 as-converted shares = 19.3% of total common** (780,727 preferred-converted + 2,927,727 vested warrants). The earlier 36.9%/29.9% figures counted *all* warrant tranches; the three short-term tranches **expired worthless Sept 2025**, leaving ≈19.3% as the realistic overhang. The path to ≈30%+ only opens if remaining tranches vest *and* the stock clears $180–$540 — a high-price problem, not a base case.

---

## 5. What management said

CEO Alex Timm runs the company on an explicit **discounted-cash-flow / cost-of-capital discipline**, not calendar targets: *"optimize to continue to build the largest discounted future cash flow… when we have high returns we invest aggressively [which] might reduce short-term earnings; when there's not as many opportunities we're totally fine being patient… and you'll see us be very, very profitable"* (Q1'26). That is exactly right for a high-ROE compounder and explains lumpy GAAP earnings (CAC expensed up-front). Other takeaways: reaffirmed **60–65% long-run gross loss-ratio target** (FY24–25 ran below it); **"accelerating annual PIF growth" expected in 2026**; partnerships framed as a durable, technology-based edge; candid that **direct growth is cyclically soft** (GWP −5% YoY Q1'26, partly a tariff-demand comp). The CFO tied the buyback to "confidence in the intrinsic value of the business." Filter the **$17M non-cash Carvana warrant charge (Q3'25)** — it's a milestone-vesting *success* signal, not an operating cost. **Insider check:** benign — director awards and routine RSU tax-withholding, only small officer open-market sales; institutions hold ≈61%.

---

## 6. Valuation

**Why this method.** Root is a **financial/spread business**, so the anchor is **book value × warranted return**, not a DCF of "free cash flow" (distorted by reserves/float) and certainly not science-style rNPV (no binary technical risk). A single-stage warranted-P/B understates Root because the dominant driver is **multi-year compounding of retained book** at a high ROE (no dividend). I therefore value **BVPS compounding for 7 years, capitalized at a terminal P/B**, discounted at the cost of equity, integrating the two genuinely uncertain drivers — sustainable ROE (→ book-growth) and the terminal multiple — across a probability-weighted distribution.

**Cost of equity (built up).** 4.3% (10-yr UST) + 1.5 beta × 5.0% ERP (= 7.5%) + 3.0% micro-cap/illiquidity = **14.8%**. (I model terminal multiples on a *lower* mature CoE — see below — to reflect that Root de-risks as it scales; I test ±1pt in sensitivity.)

**Transparency on the mechanics.** Value/share = BVPS₀ × (1+g)⁷ × terminal P/B ÷ (1.148)⁷, with **BVPS₀ = $18.4**. Because base-case book growth (14%) ≈ the 14.8% discount rate, the seven-year compounding nearly cancels in the modal case, so value there reduces to **≈ BVPS₀ × terminal P/B** — i.e., the two true levers are **current book and the terminal multiple**; growth adds value chiefly in the high-ROE scenarios where it compounds *above* the discount rate. I make this explicit rather than hide behind the compounding.

**Terminal multiples reconciled to warranted P/B.** Each scenario's terminal P/B is set to (terminal ROE − g)/(terminal CoE − g), not assumed:

| Scenario | Prob | Book CAGR | Terminal ROE / g / CoE | ⇒ Warranted P/B | Value/share |
|---|---|---|---|---|---|
| Compounder works | 30% | 18% | 18% / 5% / 12% | **1.8x** | **$40.1** |
| Solid grower (base) | 42% | 14% | 16% / 4% / 12.5% | **1.4x** | **$24.5** |
| Cycle softens / stalls | 20% | 9% | 11% / 3% / 13% | **0.85x** | **$10.9** |
| Adverse / dilutive | 8% | 5% | 7% / 2% / 14% | **0.5x** | **$4.9** |

**Probability-weighted FMV = $24.9 ≈ $25/share.**

**Why these weights (base-rate reasoning, not vibes).** The 30% on the compounder reflects that Root *has* demonstrated, across two full years, the two things that matter — sub-target loss ratios *and* accelerating favorable reserve development — which empirically is uncommon for a young insurer and tilts the odds toward "the edge is real." But I cap it at 30% because the competitive analysis is decisive that the edge is *narrow* (no durable telematics moat; sub-scale; cost-of-capital disadvantage) and the soft cycle is already biting growth. The 28% combined on impaired outcomes (cycle/competition compresses returns; or adverse development on the 4x-levered book) reflects that personal-auto is mid-to-late cycle, Root's loss ratio is ≈2pts development-aided, and retention is undisclosed/high-churn — historically, sub-scale challengers that levered into a softening market have given back a chunk of cycle-peak margin. The 8% true-adverse tail prices the genuinely bad path (edge fails through-cycle / dilutive raise).

**No-growth floor.** Warranted P/B = (ROE − g)/(CoE − g) with a conservative 16% through-cycle ROE, 3% growth, 14.8% CoE = **1.10x book → $20/share**. The margin-of-safety anchor: current book plus a modest premium for above-cost-of-capital returns.

**Sensitivity** (FMV/share):

| | Terminal P/B 1.2x | 1.4x | 1.7x |
|---|---|---|---|
| Book CAGR 12% / CoE 14.8% | $18 | $21 | $26 |
| Book CAGR 14% / CoE 14.8% | $21 | $25 | $30 |
| Book CAGR 16% / CoE 13.8% | $26 | $30 | $36 |

**Cross-checks — and why I anchor where I do.**
1. **Normalized earnings power:** through-cycle NEP ≈$1.5B × 4% underwriting margin (96% combined, *accident-year* basis with no development tailwind) + ≈$42M investment income (post-redeployment) − ≈$13M interest ≈ $77M pretax; net ≈$60–75M (NOLs shield cash tax) → **$3.4–4.2 EPS**. At a sub-scale-cyclical 8–10x → **$30–42**.
2. **Peers:** PLMR 3.0x book @ 22% ROE; SKWD 1.5x @ 17%; HCI 1.6x @ 33%; HMN 1.3x @ 11%. Root at ≈16% ROE with superior growth supports **1.4–1.7x** → **$26–31** on current book.

Both cross-checks land at or above my $25 center. I deliberately anchor at the **lower edge of my own evidence** for three defensible reasons: (a) the earnings cross-check assumes the cyclically-low, ≈2pt-development-aided loss ratio and full deployment of excess capital all persist simultaneously — an optimistic confluence; (b) the peer multiples are struck in a benign-cycle moment that is now turning; and (c) the corrected 14.8% CoE (vs a generous 13–14%) and the high underwriting leverage warrant a haircut to mid-cycle. In other words, the gap between $25 and the $30+ cross-checks *is* the cycle/competitive/leverage risk, expressed as a discount rather than ignored. A reader who believes the edge is fully durable should read the upper half of the band ($30–34) as their number; the headline integrates the full distribution.

---

## 7. Probability-weighted outcome distribution

One FMV, not a bull/bear split. The distribution is driven by **(a) sustainable through-cycle ROE** (does the ≈59% gross loss ratio hold as the cycle softens and the book ages, can Root keep premium growing 12–18%, and what is true retention?) and **(b) the terminal multiple** a scaled Root earns. Integrating the four weighted points (30% × $40 + 42% × $25 + 20% × $11 + 8% × $5) gives **expected FMV ≈ $25, with a central confidence band of $16–$34.** The favorable-reserve-development evidence is what justifies a meaningful (30%) weight on the compounder; the narrow-moat, high-leverage, softening-cycle reality is what justifies the 28% on impairment.

---

## 8. Risks & what would change my mind

**Key risks.**
- **Loss-ratio durability through a full soft cycle** — the thesis rests on a structurally low loss ratio; the current ≈59% is partly hard-market- and ≈2pt development-aided. Severity already ticked to +9% (Q3'25).
- **High underwriting leverage** — ≈3.3–5x premium-to-surplus, risen as quota-share wound down; thinner cushion for a bad accident year on a young book.
- **Undisclosed retention / high churn** — to net +16% PIF, Root must write far more than 16% new business each year (implied 1-yr retention ≈70–80%); LTV/CAC, not loss ratio, is the real swing variable, and Root does not disclose a persistency rate.
- **Cyclical softening + competition** — premiums −6% nationally in 2025; Root's direct GWP −5% YoY in Q1'26.
- **Scale & cost of capital** — 0.4% share vs float-funded incumbents with ≈50x ad budgets; near-permanent.
- **Carvana concentration & dilution** — ≈19.3% as-converted owner and key partner; warrant dilution real only at much higher prices.

**Upgrade signals:** sustained PIF re-acceleration at the 60–65% loss-ratio target; partnership channel scaling past 50% of new writings with stable economics; portfolio yield lifting toward 5%; disclosure of healthy/ improving retention; continued favorable reserve development. **Downgrade signals:** loss ratio above 65%, net combined sustained above 100%, a *reversal* to adverse reserve development, or a dilutive equity raise.

---

## 9. Conclusion

Root has earned the right to be valued as a real, profitable, growing insurer — and its accelerating favorable reserve development is hard, auditable evidence the underwriting turn is genuine. It is the best auto underwriter among the InsurTechs and has a narrow but real distribution edge in embedded and independent-agent channels. But it is not a wide-moat compounder: it is sub-scale in a consolidating oligopoly, its telematics advantage is largely matched by far larger incumbents, it runs high underwriting leverage, and a slice of its turnaround rode a rate cycle now reversing. Weighing the full distribution — and building the cost of capital, leverage, and dilution honestly — my fair market value is **$25 per share**, within a **$16–$34** band, against a **$20 no-growth floor** (≈1.1x current book). The headline embeds real growth optionality (30% weight on a ≈$40 compounder outcome) balanced against a 28% weight on cycle/competitive/leverage impairment. Conviction is **moderate (0.55)** — appropriate for a high-beta name whose value hinges on a sustainable-ROE question only a full underwriting cycle can definitively answer.



---

## Structured Dossier
```json
{
  "fair_value_per_share": 25.0,
  "intrinsic_value_floor": 20.0,
  "fair_value_low": 16.0,
  "fair_value_high": 34.0,
  "valuation_method": "Multi-stage book-value-per-share compounding at a probability-weighted sustainable ROE (financial/spread frame), discounted at 14.8% cost of equity; terminal P/B reconciled to warranted (ROE-g)/(CoE-g); cross-checked with normalized earnings power and peer P/B-vs-ROE.",
  "confidence": 0.55,
  "thesis_summary": "Root is a recently-profitable telematics auto insurer that genuinely fixed its underwriting (gross loss ratio ≈82%->59%), wound down quota-share reinsurance, and grows fast (revenue $455M FY23->$1.52B FY25; first profit FY24-25). Three years of accelerating FAVORABLE reserve development (-$7.0M/-$19.4M/-$29.4M) confirm the turn is real and conservatively reserved. As a financial/spread business it is valued on book compounding at a sustainable ROE: common book ≈$18.4/share FD, ROE ≈16% through cycle (cyclically higher). It is the best insurtech underwriter but sub-scale (0.4% share) vs incumbents with permanent cost-of-capital advantages, runs high ≈3.3-5x premium-to-surplus leverage, and has undisclosed/high churn. Probability-weighted FMV ≈$25, floor ≈$20 (1.1x book), with 30% weight on a ≈$40 compounder outcome and 28% on cycle/competitive/leverage impairment.",
  "key_value_drivers": [
    "Sustainable through-cycle ROE / book-value compounding rate (the dominant driver)",
    "Durability of the ≈59% gross loss ratio (and accident-year vs development-aided calendar loss ratio) as the cycle softens",
    "PIF/premium growth from embedded (Carvana) + independent-agent channels, state expansion, and retention",
    "Terminal P/B (a function of terminal ROE vs cost of equity as Root de-risks)",
    "Investment-yield redeployment from cash-heavy 3.4% toward ≈5% (+$6-8M/yr) and operating leverage"
  ],
  "key_risks": [
    "Loss-ratio edge unproven through a full soft cycle; ≈2pts of 2025 calendar loss ratio aided by favorable prior-year development",
    "High premium-to-surplus (≈3.3-5x net), risen as quota share wound down - thin cushion for a bad accident year",
    "Undisclosed retention; high-churn model requires heavy new business to grow PIF (implied 1-yr retention ≈70-80%)",
    "Sub-scale (0.4% share) vs float-funded incumbents with ≈50x ad budgets and lower cost of capital",
    "Carvana concentration (≈19.3% as-converted owner/partner); warrant overhang dilutive only at much higher prices"
  ],
  "what_would_change_my_mind": [
    "Net combined ratio sustained above 100% or gross loss ratio drifting above the 65% target",
    "A reversal from favorable to adverse prior-year reserve development",
    "A dilutive equity raise",
    "Disclosure of weak/declining retention undermining LTV/CAC",
    "Conversely: sustained PIF re-acceleration at target loss ratio + portfolio-yield redeployment toward 5% would push FMV toward the low-$30s"
  ],
  "diluted_shares_used": 17700000.0,
  "citations": []
}
```