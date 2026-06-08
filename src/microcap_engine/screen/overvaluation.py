"""Price-aware 'obviously overvalued?' sift for the deep-dive shortlist.

The edge screener finds high-edge names regardless of direction; many high-edge
names in hot sectors are richly-valued hype (great avoids, not buys). For a BUY
basket we walk DOWN the edge ranking and skip only the OBVIOUSLY-overvalued names —
keeping the deep-dive budget for plausible longs. This is a cheap, recall-safe,
Sonnet judgment over standard multiples; it lives in the screener tier and never
reaches the price-blinded engine.
"""

from __future__ import annotations

from microcap_engine.config import settings
from microcap_engine.llm.client import LLMClient
from microcap_engine.llm.fresh_agent import spawn_fresh
from microcap_engine.schemas.edge import OvervaluationVerdict
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)


def _first(rows) -> dict:
    if isinstance(rows, list) and rows:
        return rows[0]
    return rows if isinstance(rows, dict) else {}


def fetch_valuation(fmp, ticker: str) -> dict:
    """Cheap standard multiples + price context (no balance-sheet pull)."""
    def g(ep, **kw):
        try:
            return _first(fmp._get(ep, **kw))
        except Exception:
            return {}
    q = g("quote", symbol=ticker)
    rt = g("ratios-ttm", symbol=ticker)
    km = g("key-metrics-ttm", symbol=ticker)
    return {
        "price": q.get("price"), "price_avg200": q.get("priceAvg200"),
        "market_cap": km.get("marketCap"),
        "pe_ttm": rt.get("priceToEarningsRatioTTM"),
        "pb_ttm": rt.get("priceToBookRatioTTM"),
        "ps_ttm": rt.get("priceToSalesRatioTTM"),
        "ev_sales": km.get("evToSalesTTM"), "ev_ebitda": km.get("evToEBITDATTM"),
        "earnings_yield": km.get("earningsYieldTTM"), "fcf_yield": km.get("freeCashFlowYieldTTM"),
        "net_debt_to_ebitda": km.get("netDebtToEBITDATTM"),
        "ebitda_margin": rt.get("ebitdaMarginTTM"),
    }


_SIFT_SYSTEM = (
    "You are a seasoned value investor deciding whether a micro-cap is OBVIOUSLY overvalued — so "
    "obviously that an expensive deep fundamental analysis would clearly conclude 'avoid' without "
    "doing the work. We are building a BUY basket and must not waste deep dives confirming obvious "
    "avoids.\n"
    "Reason it through with real JUDGMENT — do NOT mechanically read the multiples. Standard "
    "ratios are inputs, not the verdict, and they MISLEAD by sector: an insurer/bank is judged on "
    "book value and through-cycle ROE (P/E is noisy); a REIT on FFO/NAV (GAAP P/E is meaningless); "
    "a pre-revenue biotech/deep-tech has no earnings and is an optionality/asset story (a huge "
    "EV/Sales is not automatically 'overvalued'); a cyclical/commodity name is judged on mid-cycle "
    "(trough earnings inflate P/E); a turnaround on normalized margins. Apply the RIGHT lens for "
    "THIS business, then ask whether the price is at an extreme premium to every plausible "
    "sector-appropriate floor with no credible long.\n"
    "BE CONSERVATIVE and RECALL-SAFE: only flag the blatant cases. Cheap, fair, beaten-down, "
    "discount-to-book/net-cash, or genuinely-uncertain names must PASS (obviously_overvalued="
    "FALSE) so the engine can value them. When in doubt, PASS — a wrongly-cut winner is "
    "unrecoverable; a wasted deep dive is cheap."
)


def sift(client: LLMClient, ticker: str, valn: dict, description: str, name: str,
         sector: str | None = None, industry: str | None = None) -> OvervaluationVerdict:
    # Opus: ratios alone don't tell the story by sector, and it's only ~30 names.
    agent = spawn_fresh(client=client, role="overval_sift", system=_SIFT_SYSTEM,
                        ticker=ticker, model=settings.main_model, thinking=True)
    msg = (
        f"{name} ({ticker}) — {sector or '?'} / {industry or '?'}\n"
        f"Multiples (TTM, as CONTEXT only): P/E={valn.get('pe_ttm')}, P/B={valn.get('pb_ttm')}, "
        f"P/S={valn.get('ps_ttm')}, EV/Sales={valn.get('ev_sales')}, "
        f"EV/EBITDA={valn.get('ev_ebitda')}, earnings_yield={valn.get('earnings_yield')}, "
        f"fcf_yield={valn.get('fcf_yield')}, net_debt/EBITDA={valn.get('net_debt_to_ebitda')}, "
        f"EBITDA_margin={valn.get('ebitda_margin')}.\n"
        f"Price {valn.get('price')} vs 200d avg {valn.get('price_avg200')}; "
        f"market cap {valn.get('market_cap')}.\n"
        f"Business: {(description or '(none)')[:1200]}\n\n"
        "Apply the right sector lens and decide: is this OBVIOUSLY overvalued (a clear 'avoid' "
        "without deep work)? When in doubt, pass."
    )
    try:
        return agent.ask_structured(msg, output_schema=OvervaluationVerdict,
                                    phase="overval_sift", max_tokens=3500)
    except Exception as e:  # pragma: no cover - fail OPEN (keep the name)
        log.warning("overvaluation sift failed for %s: %s", ticker, e)
        return OvervaluationVerdict(posture="uncertain", obviously_overvalued=False,
                                    plausible_long=True,
                                    reason="sift unavailable; kept (recall-safe).")
