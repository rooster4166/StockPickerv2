"""Provider contracts (typing.Protocol) so vendors are swappable.

The engine depends on these shapes, not on FMP specifically. Swapping FMP for
Polygon later is implementing these Protocols against a different backend.
``get_quote`` lives here but is called ONLY by the portfolio layer — never by the
orchestrator (price-blinding).
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from microcap_engine.data.models import (
    CompanyProfile,
    FilingDocument,
    FilingRef,
    FinancialPeriod,
    KeyMetrics,
    NewsItem,
    Quote,
    UniverseRow,
)


@runtime_checkable
class DataProvider(Protocol):
    def screen_universe(self, min_cap: int, max_cap: int) -> list[UniverseRow]: ...
    def get_profile(self, ticker: str) -> CompanyProfile: ...
    def get_financials(
        self, ticker: str, period: str, limit: int
    ) -> list[FinancialPeriod]: ...
    def get_key_metrics(self, ticker: str, period: str, limit: int) -> list[KeyMetrics]: ...
    def get_quote(self, ticker: str) -> Quote: ...
    def get_adv_dollar(self, ticker: str) -> float: ...
    def get_news(self, ticker: str, limit: int) -> list[NewsItem]: ...


@runtime_checkable
class FilingsProvider(Protocol):
    def list_filings(self, cik: str, forms: list[str], limit: int) -> list[FilingRef]: ...
    def fetch_filing(self, ref: FilingRef) -> FilingDocument: ...
