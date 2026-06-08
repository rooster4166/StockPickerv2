"""Stage 1 — deterministic, FMP-only edge prior over the universe (no LLM, cheap).

edge_prior = complexity_prior x coverage_gap x (1 + dislocation)
  • complexity_prior — the dominant term (science/deep-tech barrier; see complexity.py)
  • coverage_gap     — thin/low-quality coverage (few analysts, few 13F holders)
  • dislocation      — a mild multiplier for pre-revenue / extreme-valuation tells

Multiplicative on the first two so BOTH must be present: a complex-but-well-covered
name (efficient) and a thin-but-simple name (no barrier) both score low — only complex
AND under-covered names rank high. Calibrated to the validation set (high: ARQQ/ANIX/
KINS ≈ 0.45-0.57; low: FLWS/ACRE/ROOT ≈ 0.04-0.07).
"""

from __future__ import annotations

from microcap_engine.data.fmp import FMPProvider
from microcap_engine.schemas.edge import EdgePrior, EdgeSignals
from microcap_engine.screen.complexity import complexity_prior
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)


def _first(rows) -> dict:
    if isinstance(rows, list) and rows:
        return rows[0]
    return rows if isinstance(rows, dict) else {}


def fetch_signals(fmp: FMPProvider, ticker: str, profile: dict | None = None) -> EdgeSignals:
    """Pull the cheap FMP signals for one name. Resilient: missing fields -> defaults."""
    if profile is None:
        profile = _first(_safe(fmp, "profile", symbol=ticker))
    grades = _first(_safe(fmp, "grades-consensus", symbol=ticker))
    n_analysts = sum(int(grades.get(k, 0) or 0)
                     for k in ("strongBuy", "buy", "hold", "sell", "strongSell"))
    inst = {}
    for y, q in ((2025, 3), (2025, 2), (2024, 4)):
        inst = _first(_safe(fmp, "institutional-ownership/symbol-positions-summary",
                            symbol=ticker, year=y, quarter=q))
        if inst:
            break
    ratios = _first(_safe(fmp, "ratios-ttm", symbol=ticker))
    km = _first(_safe(fmp, "key-metrics-ttm", symbol=ticker))

    npm = ratios.get("netProfitMarginTTM")
    rev = km.get("revenuePerShareTTM")  # proxy; revenue itself not always present
    evs = km.get("evToSalesTTM")
    pre_rev = bool((npm is not None and npm < -1.0) or (evs is not None and evs > 25))

    return EdgeSignals(
        ticker=ticker,
        sector=profile.get("sector"), industry=profile.get("industry"),
        market_cap=profile.get("marketCap"),
        n_analysts=n_analysts,
        n_institutions=int(inst.get("investorsHolding", 0) or 0),
        net_margin_ttm=npm, ev_to_sales=evs, ev_to_ebitda=km.get("evToEBITDATTM"),
        revenue_ttm=rev, beta=profile.get("beta"),
        is_pre_revenue=pre_rev,
    )


def _safe(fmp: FMPProvider, endpoint: str, **params):
    try:
        return fmp._get(endpoint, **params)
    except Exception as e:  # pragma: no cover - screener must not die on one field
        log.debug("edge signal %s failed for %s: %s", endpoint, params.get("symbol"), e)
        return []


def coverage_gap(n_analysts: int, n_institutions: int) -> float:
    """0..1; high when coverage is thin. Analyst count dominates (cleanest signal)."""
    analyst_term = max(0.10, 1.0 - n_analysts / 14.0)
    inst_term = max(0.0, 1.0 - n_institutions / 200.0)
    return round(0.7 * analyst_term + 0.3 * inst_term, 4)


def _dislocation(s: EdgeSignals) -> float:
    d = 0.0
    if s.is_pre_revenue:
        d += 0.25  # pre-revenue => value is contingent/optionality, often mis-analyzed
    if s.ev_to_sales is not None and (s.ev_to_sales > 20 or s.ev_to_sales < 0):
        d += 0.15
    return round(min(d, 0.40), 4)


def prior_score(s: EdgeSignals) -> EdgePrior:
    cx = complexity_prior(s.sector, s.industry)
    cg = coverage_gap(s.n_analysts, s.n_institutions)
    dis = _dislocation(s)
    score = round(cx * cg * (1.0 + dis), 4)
    return EdgePrior(
        ticker=s.ticker, sector=s.sector, industry=s.industry,
        complexity_prior=cx, coverage_gap=cg, dislocation=dis, edge_prior=score,
        n_analysts=s.n_analysts,
        note=f"{s.n_analysts} analysts, {s.n_institutions} 13F holders"
             + (", pre-revenue" if s.is_pre_revenue else ""),
    )
