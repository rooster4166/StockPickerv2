"""Market data via yfinance: quotes, market cap, and average dollar volume.

yfinance has no real screener, so ``screen_universe`` takes a candidate ticker
list (default: the SEC's full common-stock list, see ``universe.py``) and keeps
the names whose market cap lands in the configured band. It is intentionally
tolerant of the missing/None fields that plague free data.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

from ..config import SETTINGS, Settings
from .types import PriceData

log = logging.getLogger(__name__)


class YFinanceMarketData:
    def __init__(self, settings: Settings = SETTINGS):
        self.settings = settings

    # ------------------------------------------------------------------ price
    def get_price(self, ticker: str) -> PriceData:
        import yfinance as yf

        pd = PriceData(ticker=ticker, as_of=datetime.now(timezone.utc).isoformat())
        try:
            t = yf.Ticker(ticker)
            info = _safe_info(t)
            pd.price = _num(info.get("currentPrice") or info.get("regularMarketPrice")
                            or info.get("previousClose"))
            pd.market_cap = _num(info.get("marketCap"))
            pd.shares_outstanding = _num(info.get("sharesOutstanding"))
            pd.currency = info.get("currency") or "USD"
            pd.avg_dollar_volume = self._avg_dollar_volume(t, info, pd.price)
            # Backfill market cap if the feed omitted it but gave price+shares.
            if pd.market_cap is None and pd.price and pd.shares_outstanding:
                pd.market_cap = pd.price * pd.shares_outstanding
        except Exception as exc:  # free data is flaky; never let one name kill a run
            log.warning("price fetch failed for %s: %s", ticker, exc)
        return pd

    def _avg_dollar_volume(self, t, info: dict, price: Optional[float]) -> Optional[float]:
        # Prefer a real 1-month history; fall back to info fields.
        try:
            hist = t.history(period="1mo", auto_adjust=False)
            if hist is not None and not hist.empty and "Volume" in hist and "Close" in hist:
                dollar = (hist["Volume"] * hist["Close"]).dropna()
                if len(dollar) > 0:
                    return float(dollar.mean())
        except Exception:
            pass
        vol = _num(info.get("averageDailyVolume3Month") or info.get("averageVolume"))
        if vol is not None and price is not None:
            return vol * price
        return None

    # --------------------------------------------------------------- universe
    def screen_universe(
        self, tickers: Optional[list[str]] = None, limit: Optional[int] = None
    ) -> list[str]:
        if tickers is None:
            from .universe import sec_common_stock_tickers

            tickers = sec_common_stock_tickers(self.settings)
        lo, hi = self.settings.mcap_min, self.settings.mcap_max
        kept: list[str] = []
        for i, tk in enumerate(tickers):
            if limit is not None and len(kept) >= limit:
                break
            p = self.get_price(tk)
            if p.market_cap is not None and lo <= p.market_cap <= hi:
                kept.append(tk)
            if (i + 1) % 100 == 0:
                log.info("screened %d/%d, kept %d", i + 1, len(tickers), len(kept))
        return kept


def _num(x) -> Optional[float]:
    try:
        if x is None:
            return None
        v = float(x)
        # yfinance sometimes returns NaN
        return None if v != v else v
    except (TypeError, ValueError):
        return None


def _safe_info(t) -> dict:
    try:
        return dict(t.info)
    except Exception:
        # newer yfinance exposes get_info(); fall back to fast_info-derived dict
        try:
            fi = t.fast_info
            return {
                "currentPrice": getattr(fi, "last_price", None),
                "marketCap": getattr(fi, "market_cap", None),
                "sharesOutstanding": getattr(fi, "shares", None),
                "currency": getattr(fi, "currency", None),
            }
        except Exception:
            return {}
