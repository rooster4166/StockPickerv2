"""Universe screening + per-name data assembly.

``screen_universe`` returns the $50-300M US common-stock candidates.
``load_name_data`` assembles the price-blinded ``NameData`` bundle the
orchestrator consumes (profile + multi-period financials + filings text + news),
deliberately excluding the market quote.
"""

from __future__ import annotations

import re

from microcap_engine.config import settings
from microcap_engine.data.edgar import EdgarFilingsProvider
from microcap_engine.data.fmp import FMPProvider
from microcap_engine.data.models import UniverseRow
from microcap_engine.schemas.name_result import NameData
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)

# Crude post-filters to drop non-common-stock the screener may include.
_ADR_HINT = re.compile(r"\b(ADR|ADS|sponsored)\b", re.I)
_SPAC_HINT = re.compile(r"\b(acquisition corp|merger corp|spac|blank check)\b", re.I)
_PREF_HINT = re.compile(r"\b(preferred|warrant|unit)\b", re.I)


def screen_universe(
    fmp: FMPProvider | None = None,
    min_cap: int | None = None,
    max_cap: int | None = None,
) -> list[UniverseRow]:
    fmp = fmp or FMPProvider()
    rows = fmp.screen_universe(
        min_cap or settings.min_market_cap, max_cap or settings.max_market_cap
    )
    kept = [r for r in rows if not _looks_non_common(r)]
    log.info("Universe: %d screened, %d after common-stock filter", len(rows), len(kept))
    return kept


def _looks_non_common(row: UniverseRow) -> bool:
    name = row.name or ""
    if _SPAC_HINT.search(name) or _PREF_HINT.search(name):
        return True
    # Suffix tickers (e.g. BRK.A, FOO-P) are usually share-class/preferred lines.
    if any(sep in row.ticker for sep in (".", "-")) and len(row.ticker) > 5:
        return True
    return False


def load_name_data(
    ticker: str,
    fmp: FMPProvider | None = None,
    edgar: EdgarFilingsProvider | None = None,
    *,
    annual_years: int = 5,
    quarters: int = 4,
    n_filings: int = 4,
    n_news: int = 15,
    n_transcripts: int = 3,
) -> NameData:
    fmp = fmp or FMPProvider()
    edgar = edgar or EdgarFilingsProvider()

    profile = fmp.get_profile(ticker)
    annual = fmp.get_financials(ticker, "annual", annual_years)
    quarterly = fmp.get_financials(ticker, "quarter", quarters)
    key_metrics = fmp.get_key_metrics(ticker, "annual", annual_years)
    news = fmp.get_news(ticker, n_news)
    try:
        transcripts = fmp.get_transcripts(ticker, n_transcripts)
    except Exception as e:  # pragma: no cover - network
        log.warning("Transcript fetch failed for %s: %s", ticker, e)
        transcripts = []

    filings = []
    if profile.cik:
        try:
            refs = edgar.list_filings(profile.cik, ["10-K", "10-Q"], n_filings)
            filings = [edgar.fetch_filing(r) for r in refs]
        except Exception as e:  # pragma: no cover - network
            log.warning("EDGAR fetch failed for %s: %s", ticker, e)

    return NameData(
        ticker=ticker,
        profile=profile,
        financials=annual + quarterly,
        key_metrics=key_metrics,
        filings=filings,
        news=news,
        transcripts=transcripts,
    )
