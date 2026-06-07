"""SEC EDGAR filings: pull the most recent 10-K / 10-Q documents as text.

The deep dive consolidates *every available* periodic filing into multi-period
trends (design spec B.3, phase 1) — never a single filing. We fetch the latest
``max_filings`` 10-K/10-Qs, strip HTML to plain text, and truncate each to a
character budget so a name's filing pack stays within a sane token envelope.
"""

from __future__ import annotations

import html
import logging
import re
import time
from typing import Optional

import requests

from ..config import SETTINGS, Settings
from .types import Filing
from .universe import ticker_to_cik

log = logging.getLogger(__name__)

_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
_ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{doc}"

_PERIODIC_FORMS = {"10-K", "10-Q", "10-K/A", "10-Q/A", "20-F", "40-F"}

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"[ \t\r\f\v]+")
_BLANKLINES_RE = re.compile(r"\n{3,}")


class SECFilings:
    def __init__(self, settings: Settings = SETTINGS):
        self.settings = settings
        self._headers = {"User-Agent": settings.sec_user_agent}

    def get_filings(self, ticker: str) -> list[Filing]:
        cik = ticker_to_cik(self.settings).get(ticker.upper())
        if not cik:
            log.info("no CIK for %s; skipping filings", ticker)
            return []
        try:
            recent = self._recent(cik)
        except Exception as exc:
            log.warning("submissions fetch failed for %s: %s", ticker, exc)
            return []

        out: list[Filing] = []
        for row in recent:
            if len(out) >= self.settings.max_filings:
                break
            if row["form"] not in _PERIODIC_FORMS:
                continue
            url = _ARCHIVE_URL.format(
                cik=str(int(cik)), acc=row["accession"].replace("-", ""), doc=row["doc"]
            )
            text = self._fetch_text(url)
            if not text:
                continue
            out.append(
                Filing(
                    form=row["form"],
                    filed_date=row["filed"],
                    fiscal_period=row.get("report", ""),
                    url=url,
                    text=text[: self.settings.max_filing_chars],
                )
            )
            time.sleep(0.15)  # be polite to EDGAR (~10 req/s limit)
        return out

    def _recent(self, cik: str) -> list[dict]:
        resp = requests.get(
            _SUBMISSIONS_URL.format(cik=cik), headers=self._headers, timeout=30
        )
        resp.raise_for_status()
        recent = resp.json().get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        rows = []
        for i in range(len(forms)):
            rows.append(
                {
                    "form": forms[i],
                    "filed": recent.get("filingDate", [""] * len(forms))[i],
                    "report": recent.get("reportDate", [""] * len(forms))[i],
                    "accession": recent.get("accessionNumber", [""] * len(forms))[i],
                    "doc": recent.get("primaryDocument", [""] * len(forms))[i],
                }
            )
        return rows  # already newest-first from EDGAR

    def _fetch_text(self, url: str) -> Optional[str]:
        try:
            resp = requests.get(url, headers=self._headers, timeout=45)
            resp.raise_for_status()
        except Exception as exc:
            log.warning("filing doc fetch failed (%s): %s", url, exc)
            return None
        return _html_to_text(resp.text)


def _html_to_text(raw: str) -> str:
    """Cheap HTML -> text. Avoids a bs4 dependency; good enough for LLM context."""
    raw = re.sub(r"(?is)<script.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style.*?</style>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?i)</p>", "\n", raw)
    raw = _TAG_RE.sub(" ", raw)
    text = html.unescape(raw)
    text = _WS_RE.sub(" ", text)
    text = _BLANKLINES_RE.sub("\n\n", text)
    return text.strip()
