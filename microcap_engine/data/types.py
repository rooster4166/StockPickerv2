"""Data structures that flow through the engine.

The single most important property here is **price-blinding** (design spec B.3):
the deep-dive must reason to an independent fair value before it ever sees the
market quote. ``CompanyData`` therefore separates the analyzable fundamentals
from ``PriceData``; ``CompanyData.blinded_payload()`` is what subagents see, and
it deliberately contains no price or market cap.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PriceData:
    """Market quote — kept OUT of the deep-dive until fair value is final."""

    ticker: str
    price: Optional[float] = None
    market_cap: Optional[float] = None
    shares_outstanding: Optional[float] = None  # absolute share count
    avg_dollar_volume: Optional[float] = None  # trailing average daily $ volume
    currency: str = "USD"
    as_of: Optional[str] = None

    @property
    def shares_outstanding_m(self) -> Optional[float]:
        """Shares in millions — the unit valuation math expects."""
        if self.shares_outstanding is None:
            return None
        return self.shares_outstanding / 1_000_000.0


@dataclass
class Filing:
    """A single SEC filing (10-K / 10-Q), text truncated to a budget."""

    form: str
    filed_date: str
    fiscal_period: str = ""
    url: str = ""
    text: str = ""

    def header(self) -> str:
        return f"{self.form} filed {self.filed_date} ({self.fiscal_period})".strip()


@dataclass
class NewsItem:
    title: str
    publisher: str = ""
    published: str = ""
    link: str = ""
    summary: str = ""


@dataclass
class CompanyData:
    """Everything the engine knows about a name, price-blindable on demand."""

    ticker: str
    name: str = ""
    sector: str = ""
    industry: str = ""
    description: str = ""
    # Structured statements keyed period -> {line_item: value}; sourced from
    # the data provider (yfinance financials). Never a single period.
    financials: dict[str, Any] = field(default_factory=dict)
    filings: list[Filing] = field(default_factory=list)
    news: list[NewsItem] = field(default_factory=list)
    # The quote — held separately and excluded from blinded payloads.
    price: PriceData = field(default_factory=lambda: PriceData(ticker=""))
    # Free-form provider notes / data-quality flags.
    notes: list[str] = field(default_factory=list)

    def blinded_payload(self) -> dict[str, Any]:
        """Serializable view with the market quote stripped out.

        Shares outstanding and net-debt-relevant balance-sheet items remain —
        those are needed to turn an equity value into a per-share figure — but
        the price and market cap (which would anchor the model) are removed.
        """
        return {
            "ticker": self.ticker,
            "name": self.name,
            "sector": self.sector,
            "industry": self.industry,
            "description": self.description,
            "shares_outstanding": self.price.shares_outstanding,
            "financials": self.financials,
            "filings": [
                {"header": f.header(), "url": f.url, "text": f.text} for f in self.filings
            ],
            "news": [
                {"title": n.title, "publisher": n.publisher, "published": n.published,
                 "summary": n.summary} for n in self.news
            ],
            "notes": self.notes,
        }

    def blinded_text(self) -> str:
        """A compact text rendering of the blinded payload for prompt context."""
        return json.dumps(self.blinded_payload(), indent=2, default=str)
