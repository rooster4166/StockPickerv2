"""Provider interfaces.

The engine talks to data only through these protocols, so the free yfinance /
SEC EDGAR implementation can be swapped for a licensed feed (or a fixture for
tests) without touching the analysis code.
"""

from __future__ import annotations

from typing import Optional, Protocol, runtime_checkable

from .types import CompanyData, PriceData


@runtime_checkable
class MarketDataProvider(Protocol):
    def get_price(self, ticker: str) -> PriceData: ...

    def screen_universe(
        self, tickers: Optional[list[str]] = None, limit: Optional[int] = None
    ) -> list[str]:
        """Return tickers whose market cap falls inside the configured band."""
        ...


@runtime_checkable
class DataProvider(Protocol):
    """Assembles a full, price-blindable CompanyData for one ticker."""

    def get_company_data(self, ticker: str) -> CompanyData: ...

    def get_price(self, ticker: str) -> PriceData: ...

    def screen_universe(
        self, tickers: Optional[list[str]] = None, limit: Optional[int] = None
    ) -> list[str]: ...
