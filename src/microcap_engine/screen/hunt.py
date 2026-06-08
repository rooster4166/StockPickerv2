"""The edge-hunt funnel: rank the universe, triage the top, return the best picks.

Stage 0  universe screen (existing)            -> ~1,100 names
Stage 1  deterministic FMP prior (no LLM)      -> rank all; keep top `prior_keep`
Stage 2  Sonnet triage on the survivors        -> refined differential-edge judgment
         final_edge = blend(prior, triage)     -> ranked top `top` picks

Recall-safe: Stage 1 RANKS (never hard-drops except true data gaps), and triage fails
open. The deep dive is then spent only on the returned top picks (budget loop is the
caller's job — see pipeline).
"""

from __future__ import annotations

from microcap_engine.data.fmp import FMPProvider
from microcap_engine.llm.client import LLMClient
from microcap_engine.schemas.edge import EdgeCandidate
from microcap_engine.screen.prescreen import fetch_signals, prior_score
from microcap_engine.screen.triage import triage as triage_one
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)


def _profile(fmp: FMPProvider, ticker: str) -> dict:
    try:
        rows = fmp._get("profile", symbol=ticker)
        return rows[0] if rows else {}
    except Exception:
        return {}


def rank_universe(fmp: FMPProvider, tickers: list[str]) -> list[EdgeCandidate]:
    """Stage 1 over a ticker list -> EdgeCandidates ranked by the deterministic prior."""
    cands: list[EdgeCandidate] = []
    for i, t in enumerate(tickers):
        prof = _profile(fmp, t)
        sig = fetch_signals(fmp, t, profile=prof)
        pr = prior_score(sig)
        cands.append(EdgeCandidate(
            ticker=t, sector=pr.sector, industry=pr.industry,
            edge_prior=pr.edge_prior, final_edge=pr.edge_prior,
            n_analysts=pr.n_analysts, note=pr.note))
        if (i + 1) % 50 == 0:
            log.info("edge prior: %d/%d scored", i + 1, len(tickers))
    cands.sort(key=lambda c: c.final_edge, reverse=True)
    return cands


def triage_top(fmp: FMPProvider, client: LLMClient, cands: list[EdgeCandidate],
               prior_keep: int) -> list[EdgeCandidate]:
    """Stage 2 — Sonnet triage the top `prior_keep` candidates; set final_edge."""
    survivors = cands[:prior_keep]
    for c in survivors:
        prof = _profile(fmp, c.ticker)
        sig = fetch_signals(fmp, c.ticker, profile=prof)
        pr = prior_score(sig)
        tr = triage_one(client, sig, pr, prof.get("description", ""),
                        prof.get("companyName", c.ticker))
        c.triage = tr
        # Blend: triage (the smarter judgment) weighted slightly higher than the prior.
        c.final_edge = round(0.45 * min(c.edge_prior, 1.0) + 0.55 * tr.differential_edge, 4)
    survivors.sort(key=lambda c: c.final_edge, reverse=True)
    return survivors


def hunt(fmp: FMPProvider, client: LLMClient, tickers: list[str], *,
         prior_keep: int = 40, top: int = 10) -> list[EdgeCandidate]:
    """Full funnel over `tickers` -> the top `top` edge picks (triaged)."""
    log.info("edge hunt: stage-1 prior over %d names", len(tickers))
    ranked = rank_universe(fmp, tickers)
    log.info("edge hunt: stage-2 triage on top %d", prior_keep)
    triaged = triage_top(fmp, client, ranked, prior_keep)
    return triaged[:top]
