"""Vendor-neutral data models.

These are what providers return and what the engine consumes. ``Quote`` is kept
deliberately separate from everything the orchestrator touches — it is the market
price, and price-blinding means the orchestrator never receives it.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class UniverseRow(BaseModel):
    ticker: str
    name: str
    market_cap: float
    exchange: str
    sector: str | None = None
    industry: str | None = None


class CompanyProfile(BaseModel):
    ticker: str
    name: str
    description: str
    sector: str | None = None
    industry: str | None = None
    country: str | None = None
    exchange: str | None = None
    currency: str = "USD"
    cik: str | None = None


class PriceBar(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float

    @property
    def dollar_volume(self) -> float:
        return self.close * self.volume


class Quote(BaseModel):
    """The current market price. NEVER passed into the orchestrator (price-blinding).

    Only the portfolio layer joins this in, after fair value is final.
    """

    ticker: str
    price: float
    asof: date


class FinancialPeriod(BaseModel):
    """One period from one statement set. ``period`` like 'FY2024' or 'Q3-2024'."""

    ticker: str
    period: str
    period_end: date
    fiscal_period: str  # "FY" or "Q1".."Q4"
    reported_currency: str = "USD"
    source_accession: str | None = None

    revenue: float | None = None
    cost_of_revenue: float | None = None
    gross_profit: float | None = None
    operating_income: float | None = None
    net_income: float | None = None
    ebitda: float | None = None

    operating_cash_flow: float | None = None
    capital_expenditure: float | None = None
    free_cash_flow: float | None = None

    cash_and_equivalents: float | None = None
    total_debt: float | None = None
    total_assets: float | None = None
    total_equity: float | None = None  # as reported (may include preferred/mezzanine)
    preferred_equity: float | None = None
    minority_interest: float | None = None
    common_equity: float | None = None  # total - preferred - minority (true common book)
    shares_outstanding: float | None = None


class KeyMetrics(BaseModel):
    ticker: str
    period: str
    pe_ratio: float | None = None
    ev_to_ebitda: float | None = None
    ev_to_sales: float | None = None
    price_to_book: float | None = None
    fcf_yield: float | None = None
    roic: float | None = None
    debt_to_equity: float | None = None


class FilingRef(BaseModel):
    accession: str
    form: str  # "10-K", "10-Q"
    filed_date: date
    period_of_report: date | None = None
    primary_doc_url: str | None = None


class FilingDocument(BaseModel):
    """A fetched filing, split into named sections for citation."""

    accession: str
    form: str
    filed_date: date
    source_url: str | None = None
    sections: dict[str, str] = Field(default_factory=dict)
    full_text: str = ""


class NewsItem(BaseModel):
    published: date
    source: str
    headline: str
    body: str = ""
    url: str | None = None


class TranscriptItem(BaseModel):
    """One earnings-call transcript (full text)."""

    ticker: str
    fiscal_year: int
    quarter: int
    call_date: date | None = None
    content: str = ""

    @property
    def label(self) -> str:
        return f"Q{self.quarter} FY{self.fiscal_year}"
