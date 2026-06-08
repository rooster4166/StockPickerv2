"""Financial Modeling Prep (`/stable/`) provider.

Implements DataProvider against the live FMP premium API (3000 calls/min). Field
names below were confirmed against live responses for AXTI. A light token-bucket
limiter guards against bursts; a disk cache avoids re-fetching within/across runs.
"""

from __future__ import annotations

import threading
import time
from datetime import date, datetime

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from microcap_engine.config import settings
from microcap_engine.data.cache import DiskCache
from microcap_engine.data.models import (
    CompanyProfile,
    FinancialPeriod,
    KeyMetrics,
    NewsItem,
    Quote,
    TranscriptItem,
    UniverseRow,
)
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)

BASE_URL = "https://financialmodelingprep.com/stable"


class _RateLimiter:
    """Simple token bucket. FMP premium is 3000/min; we cap well under that."""

    def __init__(self, per_minute: int = 2400):
        self._min_interval = 60.0 / per_minute
        self._lock = threading.Lock()
        self._next = 0.0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            if now < self._next:
                time.sleep(self._next - now)
            self._next = max(now, self._next) + self._min_interval


def _f(d: dict, *keys: str) -> float | None:
    for k in keys:
        v = d.get(k)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                continue
    return None


def _common_equity(b: dict) -> float | None:
    """GAAP common equity attributable to the parent's common shareholders.

    Critical for financials valued on book value: vendors (incl. FMP) often fold
    redeemable/mezzanine preferred into 'totalStockholdersEquity', overstating the
    common book a book-value valuation must use — so we strip preferred.

    Minority/non-controlling interest: FMP's 'totalStockholdersEquity' is already
    PARENT-attributable equity (NCI excluded), so we must NOT subtract minority from
    it (that would double-count). Only the consolidated 'totalEquity' fallback can
    include NCI, so minority is netted out solely in that branch.
    """
    pref = _f(b, "preferredStock") or 0.0
    total = _f(b, "totalStockholdersEquity")
    if total is not None:
        common = total - pref
    else:
        te = _f(b, "totalEquity")
        if te is None:
            return None
        minority = _f(b, "minorityInterest") or 0.0
        common = te - minority - pref
    if common < 0:
        log.warning("common equity negative (%.0f) — suspect data; preferred=%.0f", common, pref)
    return common


def _parse_date(s: str | None) -> date | None:
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s[: len(fmt) + 2], fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(s).date()
    except ValueError:
        return None


class FMPProvider:
    def __init__(self, api_key: str | None = None, use_cache: bool = True):
        self.api_key = api_key or settings.fmp_api_key
        if not self.api_key:
            raise RuntimeError("FMP_API_KEY is not set (see .env).")
        self._client = httpx.Client(timeout=30.0)
        self._limiter = _RateLimiter()
        self._cache = DiskCache("fmp") if use_cache else None

    # ── transport ──────────────────────────────────────────────────────────
    @retry(
        retry=retry_if_exception_type((httpx.HTTPError,)),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=1, max=20),
        reraise=True,
    )
    def _raw_get(self, endpoint: str, params: dict):
        self._limiter.wait()
        q = dict(params)
        q["apikey"] = self.api_key
        resp = self._client.get(f"{BASE_URL}/{endpoint}", params=q)
        if resp.status_code == 429:
            raise httpx.HTTPError("rate limited")
        resp.raise_for_status()
        return resp.json()

    # Volatile endpoints must never be served stale from disk (price/sizing).
    _VOLATILE = {"quote"}

    def _get(self, endpoint: str, **params):
        clean = {k: v for k, v in params.items() if v is not None}
        cacheable = self._cache is not None and endpoint not in self._VOLATILE
        if cacheable:
            hit = self._cache.get(endpoint, clean)
            if hit is not None:
                return hit
        data = self._raw_get(endpoint, clean)
        if cacheable:
            self._cache.set(endpoint, clean, data)
        return data

    # ── universe ───────────────────────────────────────────────────────────
    def screen_universe(self, min_cap: int, max_cap: int) -> list[UniverseRow]:
        rows: list[UniverseRow] = []
        data = self._get(
            "company-screener",
            marketCapMoreThan=min_cap,
            marketCapLowerThan=max_cap,
            country="US",
            isEtf="false",
            isFund="false",
            isActivelyTrading="true",
            limit=5000,
        )
        for d in data or []:
            cap = _f(d, "marketCap") or 0.0
            if not (min_cap <= cap <= max_cap):  # re-validate client-side
                continue
            rows.append(
                UniverseRow(
                    ticker=d.get("symbol", ""),
                    name=d.get("companyName", ""),
                    market_cap=cap,
                    exchange=d.get("exchangeShortName") or d.get("exchange") or "",
                    sector=d.get("sector"),
                    industry=d.get("industry"),
                )
            )
        return rows

    # ── per-name ───────────────────────────────────────────────────────────
    def get_profile(self, ticker: str) -> CompanyProfile:
        data = self._get("profile", symbol=ticker)
        d = data[0] if isinstance(data, list) and data else {}
        return CompanyProfile(
            ticker=ticker,
            name=d.get("companyName", ticker),
            description=d.get("description", ""),
            sector=d.get("sector"),
            industry=d.get("industry"),
            country=d.get("country"),
            exchange=d.get("exchange"),
            currency=d.get("currency", "USD"),
            cik=(d.get("cik") or None),
        )

    def get_financials(self, ticker: str, period: str, limit: int) -> list[FinancialPeriod]:
        inc = self._get("income-statement", symbol=ticker, period=period, limit=limit) or []
        bal = self._get("balance-sheet-statement", symbol=ticker, period=period, limit=limit) or []
        cfs = self._get("cash-flow-statement", symbol=ticker, period=period, limit=limit) or []
        # Index by fiscalYear+period (robust to one-day date drift across statements),
        # falling back to the raw date. Misaligned statements would otherwise blank
        # the balance/cash-flow fields silently.
        def _key(r):
            return (r.get("fiscalYear"), r.get("period")) if r.get("period") else r.get("date")

        bal_by = {_key(b): b for b in bal}
        cf_by = {_key(c): c for c in cfs}
        bal_by_date = {b.get("date"): b for b in bal}
        cf_by_date = {c.get("date"): c for c in cfs}
        out: list[FinancialPeriod] = []
        for i in inc:
            d = i.get("date")
            k = _key(i)
            b = bal_by.get(k) or bal_by_date.get(d, {})
            c = cf_by.get(k) or cf_by_date.get(d, {})
            if not b or not c:
                log.debug("[%s] statement-merge gap at %s (bal=%s cf=%s)",
                          ticker, d, bool(b), bool(c))
            out.append(
                FinancialPeriod(
                    ticker=ticker,
                    period=f"{i.get('period', '')}{i.get('fiscalYear', '')}".strip() or str(d),
                    period_end=_parse_date(d) or date(1900, 1, 1),
                    fiscal_period=str(i.get("period", "")),
                    reported_currency=i.get("reportedCurrency", "USD"),
                    source_accession=None,
                    revenue=_f(i, "revenue"),
                    cost_of_revenue=_f(i, "costOfRevenue"),
                    gross_profit=_f(i, "grossProfit"),
                    operating_income=_f(i, "operatingIncome", "ebit"),
                    net_income=_f(i, "netIncome", "bottomLineNetIncome"),
                    ebitda=_f(i, "ebitda"),
                    operating_cash_flow=_f(c, "operatingCashFlow", "netCashProvidedByOperatingActivities"),
                    capital_expenditure=_f(c, "capitalExpenditure"),
                    free_cash_flow=_f(c, "freeCashFlow"),
                    cash_and_equivalents=_f(b, "cashAndCashEquivalents", "cashAndShortTermInvestments"),
                    total_debt=_f(b, "totalDebt"),
                    total_assets=_f(b, "totalAssets"),
                    total_equity=_f(b, "totalStockholdersEquity", "totalEquity"),
                    preferred_equity=_f(b, "preferredStock"),
                    minority_interest=_f(b, "minorityInterest"),
                    common_equity=_common_equity(b),
                    shares_outstanding=_f(i, "weightedAverageShsOutDil", "weightedAverageShsOut"),
                )
            )
        return out

    def get_key_metrics(self, ticker: str, period: str, limit: int) -> list[KeyMetrics]:
        data = self._get("key-metrics", symbol=ticker, period=period, limit=limit) or []
        out = []
        for d in data:
            out.append(
                KeyMetrics(
                    ticker=ticker,
                    period=f"{d.get('period', '')}{d.get('fiscalYear', '')}".strip(),
                    ev_to_ebitda=_f(d, "evToEBITDA"),
                    ev_to_sales=_f(d, "evToSales"),
                    fcf_yield=_f(d, "freeCashFlowYield"),
                    roic=_f(d, "returnOnInvestedCapital"),
                )
            )
        return out

    def get_quote(self, ticker: str) -> Quote:
        """ONLY called by the portfolio layer (price-blinding)."""
        data = self._get("quote", symbol=ticker)
        d = data[0] if isinstance(data, list) and data else {}
        return Quote(
            ticker=ticker,
            price=_f(d, "price") or 0.0,
            asof=date.today(),
        )

    def get_adv_dollar(self, ticker: str) -> float:
        data = self._get("quote", symbol=ticker)
        d = data[0] if isinstance(data, list) and data else {}
        price = _f(d, "price") or 0.0
        avg_vol = _f(d, "averageVolume") or _f(d, "volume") or 0.0
        return price * avg_vol

    def get_news(self, ticker: str, limit: int) -> list[NewsItem]:
        data = self._get("news/stock", symbols=ticker, limit=limit) or []
        out = []
        for d in data:
            out.append(
                NewsItem(
                    published=_parse_date(d.get("publishedDate") or d.get("date"))
                    or date(1900, 1, 1),
                    source=d.get("publisher") or d.get("site") or "",
                    headline=d.get("title", ""),
                    body=(d.get("text") or "")[:2000],
                    url=d.get("url"),
                )
            )
        return out

    def get_ratios(self, ticker: str) -> dict:
        """TTM ratios + key metrics as a flat dict (P/B, ROE, margins, leverage, ...)."""
        out: dict = {}
        for ep in ("ratios-ttm", "key-metrics-ttm"):
            data = self._get(ep, symbol=ticker)
            rec = data[0] if isinstance(data, list) and data else (data or {})
            if isinstance(rec, dict):
                for k, v in rec.items():
                    if isinstance(v, (int, float)) and k != "symbol":
                        out[k] = v
        return out

    def get_peers(self, profile: CompanyProfile, max_peers: int = 12) -> list[dict]:
        """Sector/industry peers within a broad cap band, with TTM valuation multiples."""
        if not profile.sector:
            return []
        rows = self._get(
            "company-screener",
            sector=profile.sector,
            industry=profile.industry,
            country="US",
            isEtf="false",
            isFund="false",
            isActivelyTrading="true",
            marketCapMoreThan=20_000_000,
            marketCapLowerThan=3_000_000_000,
            limit=max_peers + 5,
        ) or []
        peers = []
        for r in rows:
            sym = r.get("symbol")
            if not sym or sym == profile.ticker:
                continue
            peers.append({
                "ticker": sym,
                "name": r.get("companyName"),
                "market_cap": _f(r, "marketCap"),
                "industry": r.get("industry"),
            })
            if len(peers) >= max_peers:
                break
        # Attach each peer's TTM multiples (P/B, P/E, EV/EBITDA) for grounded comps.
        for p in peers:
            try:
                rt = self.get_ratios(p["ticker"])
                p["price_to_book"] = rt.get("priceToBookRatioTTM")
                p["pe"] = rt.get("priceToEarningsRatioTTM")
                p["ev_ebitda"] = rt.get("enterpriseValueMultipleTTM")
                p["roe"] = rt.get("returnOnEquityTTM")
            except Exception:  # pragma: no cover
                pass
        return peers

    def get_segments(self, ticker: str) -> list[dict]:
        """Product-segment revenue breakdown (most recent period)."""
        for ep in ("revenue-product-segmentation", "revenue-geographic-segmentation"):
            try:
                data = self._get(ep, symbol=ticker)
            except Exception:  # pragma: no cover
                continue
            if isinstance(data, list) and data:
                return data[:8]
        return []

    def get_transcripts(self, ticker: str, n: int = 3) -> list[TranscriptItem]:
        """Most recent N earnings-call transcripts (full text)."""
        dates = self._get("earning-call-transcript-dates", symbol=ticker) or []
        out: list[TranscriptItem] = []
        for d in dates[:n]:
            year = d.get("fiscalYear")
            quarter = d.get("quarter")
            if year is None or quarter is None:
                continue
            try:
                data = self._get(
                    "earning-call-transcript", symbol=ticker, year=year, quarter=quarter
                )
            except Exception:  # pragma: no cover - some quarters 404
                continue
            rec = data[0] if isinstance(data, list) and data else {}
            content = rec.get("content", "")
            if not content:
                continue
            out.append(
                TranscriptItem(
                    ticker=ticker,
                    fiscal_year=int(year),
                    quarter=int(quarter),
                    call_date=_parse_date(d.get("date")),
                    content=content,
                )
            )
        return out

    _STATEMENT_EP = {
        "balance_sheet": "balance-sheet-statement",
        "income": "income-statement",
        "cash_flow": "cash-flow-statement",
    }

    def get_statement(self, ticker: str, which: str, period: str = "annual",
                      limit: int = 5) -> list[dict]:
        """Full as-reported statement (every line item) for balance_sheet/income/cash_flow."""
        ep = self._STATEMENT_EP.get(which)
        if ep is None:
            return []
        try:
            return self._get(ep, symbol=ticker, period=period, limit=limit) or []
        except Exception:  # pragma: no cover
            return []

    def get_insider_trades(self, ticker: str, limit: int = 25) -> list[dict]:
        """Recent insider (Form 4) transactions — buys/sells, who, when, how many shares."""
        try:
            return self._get("insider-trading/search", symbol=ticker, page=0, limit=limit) or []
        except Exception:  # pragma: no cover
            return []

    def get_institutional_summary(self, ticker: str) -> dict:
        """Most recent 13F institutional-ownership summary (holders, shares, net change)."""
        for y, q in ((2025, 3), (2025, 2), (2025, 1), (2024, 4)):
            try:
                rows = self._get("institutional-ownership/symbol-positions-summary",
                                 symbol=ticker, year=y, quarter=q)
            except Exception:  # pragma: no cover
                rows = None
            if isinstance(rows, list) and rows:
                return rows[0]
        return {}

    def close(self) -> None:
        self._client.close()
