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
         prior_keep: int = 40) -> list[EdgeCandidate]:
    """Full funnel over `tickers` -> the triaged pool ranked by edge (size prior_keep)."""
    log.info("edge hunt: stage-1 prior over %d names", len(tickers))
    ranked = rank_universe(fmp, tickers)
    log.info("edge hunt: stage-2 triage on top %d", prior_keep)
    return triage_top(fmp, client, ranked, prior_keep)


def select_for_deepdive(fmp: FMPProvider, client: LLMClient, ranked: list[EdgeCandidate],
                        target: int = 10, max_per_sector: int = 3, require_long: bool = True
                        ) -> tuple[list[dict], list[dict]]:
    """Walk the edge ranking; Opus-sift each for OBVIOUS overvaluation (and, if
    `require_long`, a plausible undervaluation case); keep the first `target` buy
    candidates, capped at `max_per_sector` per sector so the basket is diversified.
    Returns (kept, cut) dicts with the verdict + cut-reason attached."""
    from microcap_engine.screen.overvaluation import fetch_valuation, sift
    kept: list[dict] = []
    cut: list[dict] = []
    per_sector: dict[str, int] = {}
    for c in ranked:
        if len(kept) >= target:
            break
        sec = c.sector or "?"
        prof = _profile(fmp, c.ticker)
        valn = fetch_valuation(fmp, c.ticker)
        v = sift(client, c.ticker, valn, prof.get("description", ""),
                 prof.get("companyName", c.ticker), c.sector, c.industry)
        rec = {"ticker": c.ticker, "edge": c.final_edge, "sector": c.sector,
               "industry": c.industry, "price": valn.get("price"),
               "posture": v.posture, "plausible_long": v.plausible_long,
               "obviously_overvalued": v.obviously_overvalued, "reason": v.reason}
        if v.obviously_overvalued:
            rec["cut_reason"] = "obviously overvalued"
        elif require_long and not v.plausible_long:
            rec["cut_reason"] = "no plausible long"
        elif per_sector.get(sec, 0) >= max_per_sector:
            rec["cut_reason"] = f"sector cap ({sec})"
        else:
            kept.append(rec)
            per_sector[sec] = per_sector.get(sec, 0) + 1
            log.info("sift KEEP %s (%s): %s", c.ticker, v.posture, v.reason[:80])
            continue
        cut.append(rec)
        log.info("sift CUT %s [%s]: %s", c.ticker, rec["cut_reason"], v.reason[:70])
    return kept, cut
