"""FreeDataProvider — assembles a full CompanyData from yfinance + SEC EDGAR.

This is the concrete ``DataProvider`` used for live runs. yfinance supplies the
business profile, multi-period statements, and news; SEC EDGAR supplies the raw
10-K/10-Q text. The market quote is fetched too but kept on ``CompanyData.price``
so the deep dive can stay price-blinded.
"""

from __future__ import annotations

import logging
from typing import Optional

from ..config import SETTINGS, Settings
from .filings import SECFilings
from .market import YFinanceMarketData
from .types import CompanyData, NewsItem, PriceData

log = logging.getLogger(__name__)


class FreeDataProvider:
    def __init__(self, settings: Settings = SETTINGS):
        self.settings = settings
        self.market = YFinanceMarketData(settings)
        self.sec = SECFilings(settings)

    def get_price(self, ticker: str) -> PriceData:
        return self.market.get_price(ticker)

    def screen_universe(
        self, tickers: Optional[list[str]] = None, limit: Optional[int] = None
    ) -> list[str]:
        return self.market.screen_universe(tickers, limit)

    def get_company_data(self, ticker: str) -> CompanyData:
        import yfinance as yf

        data = CompanyData(ticker=ticker)
        try:
            t = yf.Ticker(ticker)
            info = _safe_info(t)
            data.name = info.get("longName") or info.get("shortName") or ticker
            data.sector = info.get("sector") or ""
            data.industry = info.get("industry") or ""
            data.description = info.get("longBusinessSummary") or ""
            data.financials = _statements(t)
            data.news = _news(t)
        except Exception as exc:
            data.notes.append(f"profile/financials fetch failed: {exc}")
            log.warning("company data fetch failed for %s: %s", ticker, exc)

        data.price = self.get_price(ticker)
        data.filings = self.sec.get_filings(ticker)
        if not data.filings:
            data.notes.append("no SEC periodic filings retrieved")
        return data


def _statements(t) -> dict:
    """Annual + quarterly statements as period->{line_item: value} dicts."""
    out: dict[str, dict] = {}
    for label, attr in (
        ("income_annual", "financials"),
        ("income_quarterly", "quarterly_financials"),
        ("balance_annual", "balance_sheet"),
        ("balance_quarterly", "quarterly_balance_sheet"),
        ("cashflow_annual", "cashflow"),
        ("cashflow_quarterly", "quarterly_cashflow"),
    ):
        try:
            df = getattr(t, attr)
            if df is not None and not df.empty:
                # columns are period timestamps; index is line items
                out[label] = {
                    str(col.date() if hasattr(col, "date") else col): {
                        str(idx): _clean(df.loc[idx, col]) for idx in df.index
                    }
                    for col in df.columns
                }
        except Exception:
            continue
    return out


def _news(t) -> list[NewsItem]:
    items: list[NewsItem] = []
    try:
        for n in (t.news or [])[:15]:
            # yfinance news shape varies; handle both flat and {'content': {...}}
            c = n.get("content", n)
            items.append(
                NewsItem(
                    title=c.get("title", "") or n.get("title", ""),
                    publisher=(c.get("provider", {}) or {}).get("displayName", "")
                    or n.get("publisher", ""),
                    published=str(c.get("pubDate", "") or n.get("providerPublishTime", "")),
                    link=(c.get("canonicalUrl", {}) or {}).get("url", "") or n.get("link", ""),
                    summary=c.get("summary", "") or "",
                )
            )
    except Exception:
        pass
    return items


def _clean(v):
    try:
        f = float(v)
        return None if f != f else f
    except (TypeError, ValueError):
        return None


def _safe_info(t) -> dict:
    try:
        return dict(t.info)
    except Exception:
        return {}
