"""US-listed common-stock universe from SEC EDGAR.

SEC publishes the full ticker->CIK map at company_tickers.json. That is the
candidate set; ``market.py`` then filters by market cap to the $50-300M band.
This is the closest thing to a free, complete US screener.
"""

from __future__ import annotations

import logging
from functools import lru_cache

import requests

from ..config import SETTINGS, Settings

log = logging.getLogger(__name__)

_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"


@lru_cache(maxsize=1)
def _fetch_company_tickers(user_agent: str) -> list[dict]:
    resp = requests.get(_TICKERS_URL, headers={"User-Agent": user_agent}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Shape: {"0": {"cik_str": int, "ticker": str, "title": str}, ...}
    return list(data.values())


def sec_common_stock_tickers(settings: Settings = SETTINGS) -> list[str]:
    """Every ticker SEC knows about (de-duplicated, upper-cased)."""
    rows = _fetch_company_tickers(settings.sec_user_agent)
    seen: set[str] = set()
    out: list[str] = []
    for r in rows:
        tk = str(r.get("ticker", "")).upper().strip()
        # EDGAR uses '-' for share classes; yfinance expects '-' too, leave as-is.
        if tk and tk not in seen:
            seen.add(tk)
            out.append(tk)
    return out


def ticker_to_cik(settings: Settings = SETTINGS) -> dict[str, str]:
    """Map ticker -> zero-padded 10-digit CIK (needed for the submissions API)."""
    rows = _fetch_company_tickers(settings.sec_user_agent)
    out: dict[str, str] = {}
    for r in rows:
        tk = str(r.get("ticker", "")).upper().strip()
        cik = str(r.get("cik_str", "")).strip()
        if tk and cik:
            out[tk] = cik.zfill(10)
    return out
