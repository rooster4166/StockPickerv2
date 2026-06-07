"""Per-name cascade and full-universe runner.

``analyze_name`` is the conservative early-stop cascade: cheap gate -> (unless an
unambiguous reject) ensemble deep dive. ``run_universe`` screens, analyzes every
name, then joins prices ONCE at the end to build the ranked, sized book.
"""

from __future__ import annotations

from dataclasses import dataclass

from microcap_engine.config import settings
from microcap_engine.data.edgar import EdgarFilingsProvider
from microcap_engine.data.fmp import FMPProvider
from microcap_engine.data.universe import load_name_data, screen_universe
from microcap_engine.ensemble.ensemble import deepen, ensemble_deepdive
from microcap_engine.gate.cheap_gate import cheap_gate, should_drop
from microcap_engine.llm.audit import AuditLogger
from microcap_engine.llm.client import LLMClient
from microcap_engine.orchestrator.agentic import AgenticOrchestrator
from microcap_engine.portfolio.book import Book, build_portfolio
from microcap_engine.schemas.name_result import BlendedFairValue, NameData, NameResult
from microcap_engine.utils.ids import new_run_id
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)


@dataclass
class Engine:
    """Bundles the live providers + an audited LLM client for one run."""

    run_id: str
    client: LLMClient
    fmp: FMPProvider
    edgar: EdgarFilingsProvider

    @classmethod
    def create(cls, run_id: str | None = None) -> Engine:
        rid = run_id or new_run_id()
        audit = AuditLogger(rid)
        return cls(
            run_id=rid,
            client=LLMClient(audit),
            fmp=FMPProvider(),
            edgar=EdgarFilingsProvider(),
        )


def _attach_cost(result: NameResult, client: LLMClient) -> NameResult:
    s = client.audit.summary(result.ticker)
    result.cost_usd = s["cost_usd"]
    result.total_tokens = s["total_tokens"]
    result.n_calls = s["n_calls"]
    return result


def analyze_name(
    data: NameData, client: LLMClient, run_id: str, n_ensemble: int | None = None
) -> NameResult:
    gate = cheap_gate(data, client)
    if should_drop(gate, data):
        log.info("[%s] gate DROP (%.2f): %s", data.ticker, gate.confidence, gate.reason)
        result = NameResult(ticker=data.ticker, action="drop", gate=gate, reason=gate.reason)
        return _attach_cost(result, client)
    result = ensemble_deepdive(data, client, run_id, n=n_ensemble)
    result.gate = gate
    return _attach_cost(result, client)


def _outcome_to_result(outcome, client: LLMClient) -> NameResult:
    if outcome.action == "drop":
        r = NameResult(ticker=outcome.ticker, action="drop", reason=outcome.reject_reason)
    else:
        d = outcome.dossier
        r = NameResult(
            ticker=outcome.ticker, action="evaluated",
            fair_value=BlendedFairValue(
                median=d.fair_value_per_share, p10=d.fair_value_low,
                p90=d.fair_value_high, n_runs=1),
            confidence=d.confidence, memo_markdown=outcome.memo_markdown, dossier=d,
            red_team_rounds=outcome.red_team_rounds,
            unresolved_concerns=outcome.unresolved_concerns,
            thesis_breakers=outcome.unresolved_concerns,
            judge_approved=outcome.judge_approved,
            judge_score=outcome.judge_score,
            judge_gaps=outcome.judge_gaps,
            transcript_path=outcome.transcript_path,
        )
    return _attach_cost(r, client)


def agentic_analyze(data: NameData, engine: Engine, pre_gate: bool = True) -> NameResult:
    # Cheap recall-safe pre-filter before the expensive agentic deep dive: drop only
    # an unambiguous, asset-negative reject (the code floor never drops a cash-rich or
    # book-positive name). For a universe run this culls dead shells for ~$0.02 each;
    # everything plausible gets the full agentic analysis.
    if pre_gate:
        gate = cheap_gate(data, engine.client)
        if should_drop(gate, data):
            log.info("[%s] pre-gate DROP (%.2f): %s", data.ticker, gate.confidence, gate.reason)
            r = NameResult(ticker=data.ticker, action="drop", gate=gate, reason=gate.reason)
            return _attach_cost(r, engine.client)
    orch = AgenticOrchestrator(
        data, engine.client, engine.run_id,
        max_steps=settings.agentic_max_steps,
        max_cost_usd=settings.agentic_max_cost_usd,
    ).bind_providers(engine.fmp, engine.edgar)
    return _outcome_to_result(orch.analyze(), engine.client)


def analyze_ticker(
    ticker: str, engine: Engine, n_ensemble: int | None = None, dump: bool = True,
    pre_gate: bool = True,
) -> NameResult:
    data = load_name_data(ticker, fmp=engine.fmp, edgar=engine.edgar)
    if settings.engine_mode == "agentic":
        result = agentic_analyze(data, engine, pre_gate=pre_gate)
    else:
        result = analyze_name(data, engine.client, engine.run_id, n_ensemble)
    if dump:
        from microcap_engine.config import AUDIT_DIR

        out = AUDIT_DIR / engine.run_id / f"{ticker.upper()}.result.json"
        out.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    return result


def _fetch_prices(engine: Engine, tickers: list[str]) -> tuple[dict, dict]:
    """Price join — done OUTSIDE the orchestrator (price-blinding boundary)."""
    prices: dict[str, float] = {}
    advs: dict[str, float] = {}
    for t in tickers:
        try:
            prices[t] = engine.fmp.get_quote(t).price
            advs[t] = engine.fmp.get_adv_dollar(t)
        except Exception as e:  # pragma: no cover
            log.warning("[%s] quote fetch failed: %s", t, e)
    return prices, advs


def run_universe(
    engine: Engine,
    capital: float,
    mos: float | None = None,
    n_ensemble: int | None = None,
    limit: int | None = None,
    tier: bool = True,
) -> tuple[Book, list[NameResult]]:
    """Two-pass, cost-tiered, recall-safe universe run.

    Pass 1: gate + ONE full deep dive on every survivor (no name is dropped except
    by the floors-protected gate). Pass 2: after the price-join identifies the
    undervalued pool, spend the extra ensemble members ONLY on those names (the
    dispersion->confidence->size signal only matters for buy candidates). This cuts
    cost ~n-fold versus ensembling everything, with zero added false-negative risk.
    """
    target_n = n_ensemble or settings.ensemble_n
    # Ensemble-tiering only applies to the phased engine; the agentic engine does
    # one deep, self-iterating analysis per name (no ensemble members to add).
    tier = tier and settings.engine_mode == "phased"
    universe = screen_universe(engine.fmp)
    if limit:
        universe = universe[:limit]
    log.info("Analyzing %d names (run %s, mode=%s, tier=%s, target_n=%d)",
             len(universe), engine.run_id, settings.engine_mode, tier, target_n)

    pass1_n = 1 if tier else target_n
    results: list[NameResult] = []
    for row in universe:
        try:
            results.append(analyze_ticker(row.ticker, engine, n_ensemble=pass1_n))
        except Exception as e:  # pragma: no cover - one bad name shouldn't stop the run
            log.warning("[%s] analysis failed: %s", row.ticker, e)

    evaluated = [r for r in results if r.action == "evaluated"]
    prices, advs = _fetch_prices(engine, [r.ticker for r in evaluated])

    if tier and target_n > 1:
        mos_f = settings.margin_of_safety if mos is None else mos
        by_ticker = {r.ticker: r for r in results}
        for r in evaluated:
            p = prices.get(r.ticker)
            if not p or p <= 0 or r.fair_value is None:
                continue
            upside = (r.fair_value.median - p) / p
            if upside >= mos_f:  # undervalued -> deepen for a real confidence signal
                log.info("[%s] undervalued (%.0f%%); deepening to n=%d",
                         r.ticker, upside * 100, target_n)
                data = load_name_data(r.ticker, fmp=engine.fmp, edgar=engine.edgar)
                deepened = deepen(r, data, engine.client, engine.run_id, target_n)
                _attach_cost(deepened, engine.client)
                by_ticker[r.ticker] = deepened
        results = list(by_ticker.values())

    book = build_portfolio(results, prices, advs, capital, mos)
    return book, results
