"""SEC EDGAR filings provider — full filing text with section-level citations.

FMP summarizes financials; for grounded analysis we need the raw 10-K / 10-Q
text. This hits data.sec.gov directly (honoring SEC's 10 req/sec limit and the
required descriptive User-Agent), fetches the primary document, and splits it
into the canonical Items so phase agents can cite (accession, 'Item 7').
"""

from __future__ import annotations

import re
import threading
import time
from datetime import date, datetime

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from microcap_engine.config import settings
from microcap_engine.data.cache import DiskCache
from microcap_engine.data.models import FilingDocument, FilingRef
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)

SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik10}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc_nodash}/{doc}"

# Canonical 10-K / 10-Q items we try to isolate for citation.
_ITEM_PATTERNS = [
    ("Item 1", r"item\s*1\b(?!\s*[aA])"),
    ("Item 1A", r"item\s*1a\b"),
    ("Item 7", r"item\s*7\b(?!\s*[aA])"),
    ("Item 7A", r"item\s*7a\b"),
    ("Item 8", r"item\s*8\b"),
    ("Item 2", r"item\s*2\b"),  # 10-Q MD&A
]


class _SecLimiter:
    """SEC asks for <=10 req/sec; we use ~6/sec to be safe."""

    def __init__(self, per_second: float = 6.0):
        self._min_interval = 1.0 / per_second
        self._lock = threading.Lock()
        self._next = 0.0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            if now < self._next:
                time.sleep(self._next - now)
            self._next = max(now, self._next) + self._min_interval


def _cik10(cik: str) -> str:
    digits = "".join(c for c in str(cik) if c.isdigit())
    return digits.zfill(10)


class EdgarFilingsProvider:
    def __init__(self, use_cache: bool = True):
        self._ua = settings.sec_user_agent
        self._client = httpx.Client(timeout=30.0, headers={"User-Agent": self._ua})
        self._limiter = _SecLimiter()
        self._cache = DiskCache("edgar") if use_cache else None

    @retry(
        retry=retry_if_exception_type((httpx.HTTPError,)),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=1, max=20),
        reraise=True,
    )
    def _get_text(self, url: str) -> str:
        self._limiter.wait()
        resp = self._client.get(url)
        resp.raise_for_status()
        return resp.text

    def _get_json(self, url: str):
        if self._cache is not None:
            hit = self._cache.get(url, {})
            if hit is not None:
                return hit
        import json

        data = json.loads(self._get_text(url))
        if self._cache is not None:
            self._cache.set(url, {}, data)
        return data

    def list_filings(self, cik: str, forms: list[str], limit: int) -> list[FilingRef]:
        if not cik:
            return []
        cik10 = _cik10(cik)
        data = self._get_json(SUBMISSIONS_URL.format(cik10=cik10))
        recent = (data.get("filings", {}) or {}).get("recent", {}) or {}
        out: list[FilingRef] = []
        n = len(recent.get("accessionNumber", []))
        for i in range(n):
            form = recent["form"][i]
            if form not in forms:
                continue
            out.append(
                FilingRef(
                    accession=recent["accessionNumber"][i],
                    form=form,
                    filed_date=_parse(recent["filingDate"][i]) or date(1900, 1, 1),
                    period_of_report=_parse(recent.get("reportDate", [None] * n)[i]),
                    primary_doc_url=ARCHIVE_URL.format(
                        cik=int(cik10),
                        acc_nodash=recent["accessionNumber"][i].replace("-", ""),
                        doc=recent["primaryDocument"][i],
                    ),
                )
            )
            if len(out) >= limit:
                break
        return out

    def fetch_filing(self, ref: FilingRef) -> FilingDocument:
        if not ref.primary_doc_url:
            return FilingDocument(accession=ref.accession, form=ref.form, filed_date=ref.filed_date)
        cache_key = ref.primary_doc_url
        text: str | None = None
        if self._cache is not None:
            cached = self._cache.get(cache_key, {"kind": "filing"})
            if cached is not None:
                text = cached.get("text")
        if text is None:
            html = self._get_text(ref.primary_doc_url)
            text = _html_to_text(html)
            if self._cache is not None:
                self._cache.set(cache_key, {"kind": "filing"}, {"text": text})
        sections = _split_items(text)
        return FilingDocument(
            accession=ref.accession,
            form=ref.form,
            filed_date=ref.filed_date,
            source_url=ref.primary_doc_url,
            sections=sections,
            full_text=text[:400_000],
        )

    def close(self) -> None:
        self._client.close()


def _parse(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def _html_to_text(html: str) -> str:
    try:
        import warnings

        from bs4 import BeautifulSoup
        from bs4 import XMLParsedAsHTMLWarning

        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
    except Exception:
        text = re.sub(r"<[^>]+>", " ", html)
    # collapse whitespace
    return re.sub(r"\s+", " ", text).strip()


def _split_items(text: str) -> dict[str, str]:
    """Best-effort split into canonical Items.

    The FIRST occurrence of "Item 7" is almost always the table-of-contents entry,
    not the MD&A body — so we take the LAST match past the first 10% of the document
    (the TOC sits up front). Each section is capped for context budget.
    """
    sections: dict[str, str] = {}
    lowered = text.lower()
    floor = int(len(text) * 0.10)  # skip the front matter / table of contents
    marks: list[tuple[int, str]] = []
    for name, pat in _ITEM_PATTERNS:
        body_matches = [m.start() for m in re.finditer(pat, lowered) if m.start() >= floor]
        pos = body_matches[-1] if body_matches else None
        if pos is None:  # fall back to any match if nothing past the floor
            m = re.search(pat, lowered)
            pos = m.start() if m else None
        if pos is not None:
            marks.append((pos, name))
    marks.sort()
    for idx, (pos, name) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else min(len(text), pos + 60_000)
        sections[name] = text[pos:end][:60_000]
    return sections
