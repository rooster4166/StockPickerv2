"""Specialist deep-dive phases (design spec B.3, phases 1-4).

Each phase is run by its own context-isolated Agent that sees the price-blinded
company data (as a cached system block) and returns a distilled, cited brief.
The phases run in strict dependency order: financials -> business model ->
industry/adjacent exposure -> news/catalysts.
"""

from __future__ import annotations

from dataclasses import dataclass

# Shared system framing handed to every specialist subagent.
SPECIALIST_SYSTEM = """You are a specialist analyst on an investment-firm-grade \
research desk pointed at a neglected $50-300M US micro-cap that no sell-side \
analyst covers. You reason from the full public record provided below. You are \
PRICE-BLINDED: you never see the market quote, and you must not guess it or \
anchor to a market cap. Ground every claim in the data; cite the filing, \
statement line, or news item it comes from. Return a tight, decision-useful \
brief — distilled, not a data dump.

=== PRICE-BLINDED COMPANY DATA ===
{data}
=== END DATA ==="""


@dataclass
class Phase:
    key: str
    name: str
    prompt: str


# Phase prompts, in dependency order. The orchestrator feeds upstream briefs
# forward by appending them to the prompt where useful.
FINANCIAL_TRENDS = Phase(
    key="financials",
    name="Financial trends",
    prompt="""Consolidate EVERY available periodic filing and statement into \
multi-period trends — never a single period. Cover: revenue trajectory and \
quality, gross/operating/net margins, free cash flow generation, the balance \
sheet (cash, debt, net debt, working capital), and share count / dilution \
history. Flag accounting red flags, non-recurring items, and any going-concern \
or liquidity language. End with the normalized earning power and the cash/debt \
figures a valuation would need (state them numerically, in $M where possible).""",
)

BUSINESS_MODEL = Phase(
    key="business",
    name="Business model",
    prompt="""Explain precisely how this company makes money: segments, unit \
economics, pricing power, customer concentration, the key operating drivers, \
and what would have to be true for earning power to grow or decay. Be concrete \
about the economics, not generic.""",
)

INDUSTRY = Phase(
    key="industry",
    name="Industry + adjacent exposure",
    prompt="""Assess the industry: size/growth, competitive position, and a \
clean set of public comparables (name them, with rough multiples if known). \
Then do what a human would skip — trace INDIRECT and ADJACENT dependencies \
(supplier feedstock costs, downstream demand, regulatory or commodity linkages) \
that materially affect this specific company. Be explicit about the transmission \
mechanism.""",
)

NEWS_CATALYSTS = Phase(
    key="news",
    name="News + catalysts",
    prompt="""Summarize recent developments and identify anything that could \
force price-to-value convergence WITHIN a one-year holding period: catalysts \
(asset sales, refinancing, contract wins, capital returns, strategic review), \
and their rough likelihood and timing. Separately, flag any catastrophe risks \
(going concern, financing distress, litigation, fraud, delisting, auditor \
change).""",
)

ORDERED_PHASES = [FINANCIAL_TRENDS, BUSINESS_MODEL, INDUSTRY, NEWS_CATALYSTS]
