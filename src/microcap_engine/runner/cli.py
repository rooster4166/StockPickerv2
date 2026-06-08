"""`microcap` CLI — drive the engine end to end."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from microcap_engine.config import AUDIT_DIR, settings
from microcap_engine.data.fmp import FMPProvider
from microcap_engine.data.universe import screen_universe
from microcap_engine.portfolio.book import build_portfolio
from microcap_engine.runner.pipeline import Engine, analyze_ticker, run_universe
from microcap_engine.utils.logging import get_logger

# Engine outputs contain Unicode (minus signs, etc.); avoid cp1252 console errors.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

app = typer.Typer(add_completion=False, help="Micro-Cap Value Engine")
console = Console()
log = get_logger("microcap.cli")


@app.command()
def one(
    ticker: str,
    n_ensemble: int = typer.Option(1, help="Ensemble members (1 is the fast slice)."),
    capital: float = typer.Option(100_000.0, help="Capital for the single-name sizing demo."),
):
    """Run the full cascade for ONE name and print the result + audit path."""
    ticker = ticker.upper()
    engine = Engine.create()
    console.print(f"[bold]Analyzing {ticker}[/bold]  (run {engine.run_id})")
    # Explicit single-name request -> always run the full deep dive (no pre-gate).
    result = analyze_ticker(ticker, engine, n_ensemble=n_ensemble, pre_gate=False)

    if result.action == "drop":
        gate_conf = f"{result.gate.confidence:.2f}" if result.gate else "—"
        console.print(f"[red]REJECTED[/red] ({gate_conf}): {result.reason}")
        _show_cost(result)
        _show_audit_path(engine.run_id, ticker)
        return

    fv = result.fair_value
    console.print(f"[green]Evaluated[/green] | fair value [bold]{fv.median}[/bold] "
                  f"(bear {fv.p10} / bull {fv.p90}) | confidence {result.confidence}")
    if result.dossier:  # agentic result
        d = result.dossier
        console.print(f"Method: [bold]{d.valuation_method}[/bold]")
        console.print(f"Thesis: {d.thesis_summary}")
        console.print(f"[dim]Red-team rounds: {result.red_team_rounds}; "
                      f"unresolved: {len(result.unresolved_concerns)}; "
                      f"diluted shares: {d.diluted_shares_used}[/dim]")
        ji = "[green]YES[/green]" if result.judge_approved else "[yellow]no[/yellow]"
        console.print(f"Independent judge: best-in-existence={ji} "
                      f"(score {result.judge_score}/100)")
        for g in (result.judge_gaps or [])[:5]:
            console.print(f"  [dim]gap: {g}[/dim]")
        if result.memo_markdown:
            memo_path = (AUDIT_DIR / engine.run_id / f"{ticker}.memo.md")
            memo_path.write_text(result.memo_markdown, encoding="utf-8", newline="\n")
            console.print(f"[dim]Full memo: {memo_path}[/dim]")
        if result.transcript_path:
            console.print(f"[dim]Full investigation transcript: {result.transcript_path}[/dim]")
    elif result.runs:  # phased result
        rt = result.runs[0].redteam
        console.print(f"Red-team: would_break_thesis={rt.would_break_thesis}, "
                      f"concerns={len(rt.concerns)}")
        console.print(f"Method: [bold]{result.runs[0].assumption_set.method.value}[/bold]")

    # Single-name price join (portfolio layer — the only place we see the quote).
    fmp = FMPProvider()
    price = fmp.get_quote(ticker).price
    adv = fmp.get_adv_dollar(ticker)
    book = build_portfolio([result], {ticker: price}, {ticker: adv}, capital)
    if book.positions:
        p = book.positions[0]
        console.print(f"[bold green]BUY[/bold green] price {p.price} vs FV {p.fair_value} "
                      f"(upside {p.upside:.0%}) -> size ${p.dollars:,.0f}")
    else:
        console.print(f"[yellow]PASS[/yellow] at price {price} "
                      f"(below {settings.margin_of_safety:.0%} margin of safety)")
    _show_cost(result)
    _show_audit_path(engine.run_id, ticker)


def _show_cost(result) -> None:
    if result.cost_usd is None:
        return
    console.print(
        f"[dim]Cost for {result.ticker}: [bold]${result.cost_usd:.4f}[/bold] "
        f"across {result.n_calls} LLM calls, {result.total_tokens:,} tokens.[/dim]"
    )


def _show_audit_path(run_id: str, ticker: str) -> None:
    from microcap_engine.config import AUDIT_DIR
    console.print(f"[dim]Audit log: {AUDIT_DIR / run_id / (ticker + '.jsonl')}[/dim]")


@app.command()
def universe(
    out: str = typer.Option("", help="Optional path to write the screened universe JSON."),
):
    """Screen the $50-300M US universe and print a summary."""
    fmp = FMPProvider()
    rows = screen_universe(fmp)
    console.print(f"[bold]{len(rows)}[/bold] names in the $50-300M US common-stock universe.")
    table = Table("Ticker", "Name", "Mkt Cap ($M)", "Sector")
    for r in rows[:25]:
        table.add_row(r.ticker, r.name[:30], f"{r.market_cap/1e6:,.0f}", r.sector or "-")
    console.print(table)
    if out:
        Path(out).write_text(json.dumps([r.model_dump() for r in rows], indent=2))
        console.print(f"Wrote {out}")


@app.command()
def screen(
    top: int = typer.Option(10, help="How many top edge picks to return."),
    prior_keep: int = typer.Option(40, help="How many top-of-prior names get Sonnet triage."),
    tickers: str = typer.Option("", help="Comma list to screen instead of the universe "
                                         "(for backtests, e.g. ANIX,KINS,ACRE)."),
    limit: int = typer.Option(0, help="Cap universe names scored in stage 1 (0 = all)."),
    out: str = typer.Option("", help="Optional path to write the ranked picks JSON."),
):
    """Edge pre-screener: rank names by the engine's differential edge, return top picks."""
    from microcap_engine.screen.hunt import hunt
    fmp = FMPProvider()
    engine = Engine.create()
    if tickers.strip():
        names = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    else:
        rows = screen_universe(fmp)
        names = [r.ticker for r in rows]
        if limit:
            names = names[:limit]
    console.print(f"[bold]Edge-screening {len(names)} names[/bold] "
                  f"(stage-2 triage on top {prior_keep})...")
    pool = hunt(fmp, engine.client, names, prior_keep=prior_keep)
    picks = pool[:top]
    table = Table("Rank", "Ticker", "Edge", "Prior", "#An", "Barrier", "CovGap", "Dive?", "Sector")
    for i, c in enumerate(picks, 1):
        tr = c.triage
        table.add_row(
            str(i), c.ticker, f"{c.final_edge:.3f}", f"{c.edge_prior:.3f}", str(c.n_analysts),
            f"{tr.complexity_barrier:.2f}" if tr else "-",
            f"{tr.coverage_understanding_gap:.2f}" if tr else "-",
            ("YES" if tr and tr.recommend_deep_dive else "no") if tr else "-",
            (c.sector or "-")[:18])
    console.print(table)
    for c in picks[:top]:
        if c.triage:
            console.print(f"  [dim]{c.ticker}: {c.triage.reasoning}[/dim]")
    cost = sum(engine.client.audit.summary(c.ticker).get("cost_usd", 0.0) for c in picks)
    console.print(f"[dim]triage cost ≈ ${cost:.2f} for {len(picks)} names[/dim]")
    if out:
        Path(out).write_text(json.dumps([c.model_dump() for c in pool], indent=2, default=str))
        console.print(f"Wrote {out} ({len(pool)} names)")


@app.command()
def shortlist(
    target: int = typer.Option(10, help="How many plausible-BUY candidates to collect."),
    prior_keep: int = typer.Option(45, help="Top-of-prior names triaged (the sift pool)."),
    max_per_sector: int = typer.Option(3, help="Diversity cap per sector."),
    tickers: str = typer.Option("", help="Comma list instead of the universe."),
    limit: int = typer.Option(0, help="Cap universe names scored in stage 1 (0 = all)."),
    out: str = typer.Option("data/buy_shortlist.json", help="Where to write the shortlist."),
):
    """Edge-rank, then walk DOWN the list Opus-sifting out OBVIOUSLY-overvalued names,
    keeping the first `target` plausible BUY candidates for the deep dive."""
    from microcap_engine.screen.hunt import hunt, select_for_deepdive
    fmp = FMPProvider()
    engine = Engine.create()
    if tickers.strip():
        names = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    else:
        rows = screen_universe(fmp)
        names = [r.ticker for r in rows]
        if limit:
            names = names[:limit]
    console.print(f"[bold]Edge-screening {len(names)} names[/bold], then sifting for buys...")
    pool = hunt(fmp, engine.client, names, prior_keep=prior_keep)
    kept, cut = select_for_deepdive(fmp, engine.client, pool, target=target,
                                    max_per_sector=max_per_sector)
    table = Table("#", "Ticker", "Edge", "Price", "Posture", "Long?", "Sector", "Why kept")
    for i, k in enumerate(kept, 1):
        table.add_row(str(i), k["ticker"], f"{k['edge']:.3f}", str(k.get("price")),
                      k["posture"], "yes" if k["plausible_long"] else "?",
                      (k.get("sector") or "-")[:16], (k["reason"] or "")[:50])
    console.print(table)
    if cut:
        console.print(f"\n[dim]Cut as obviously overvalued ({len(cut)}):[/dim]")
        for c in cut:
            console.print(f"  [dim]{c['ticker']} ({c['edge']:.2f}): {c['reason'][:90]}[/dim]")
    Path(out).write_text(json.dumps({"kept": kept, "cut": cut}, indent=2, default=str))
    console.print(f"\nWrote {out}: {len(kept)} buy-candidates, {len(cut)} cut.")


@app.command()
def run(
    capital: float = typer.Option(100_000.0),
    mos: float = typer.Option(settings.margin_of_safety),
    n_ensemble: int = typer.Option(settings.ensemble_n),
    limit: int = typer.Option(0, help="Cap names analyzed (0 = full universe)."),
    tier: bool = typer.Option(True, help="Cost-tier: n=1 on all, ensemble only on the "
                                         "undervalued pool (recall-safe)."),
):
    """Run the full universe -> ranked, sized book."""
    engine = Engine.create()
    book, results = run_universe(engine, capital, mos, n_ensemble, limit or None, tier=tier)
    total_cost = sum(r.cost_usd or 0.0 for r in results)
    evaluated = [r for r in results if r.action == "evaluated"]
    avg_cost = total_cost / len(results) if results else 0.0
    console.print(f"[bold]Book[/bold] (run {engine.run_id}): {len(book.positions)} positions, "
                  f"{len(book.dropped)} dropped, {len(book.passed)} passed")
    console.print(f"[dim]Total cost ${total_cost:.2f} across {len(results)} names "
                  f"(avg ${avg_cost:.3f}/name; {len(evaluated)} full deep dives).[/dim]")
    table = Table("Ticker", "Price", "Fair Value", "Upside", "Conf", "Size $")
    for p in book.positions[:40]:
        table.add_row(p.ticker, f"{p.price:.2f}", f"{p.fair_value:.2f}",
                      f"{p.upside:.0%}", f"{p.confidence:.2f}", f"{p.dollars:,.0f}")
    console.print(table)
    out = AUDIT_DIR / engine.run_id / "book.json"
    out.write_text(book.model_dump_json(indent=2))
    console.print(f"Wrote {out}")


@app.command()
def audit(run_id: str, ticker: str):
    """Pretty-print the per-name audit log for a run."""
    path = AUDIT_DIR / run_id / f"{ticker.upper()}.jsonl"
    if not path.exists():
        console.print(f"[red]No audit log at {path}[/red]")
        raise typer.Exit(1)
    total = 0.0
    for line in path.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        total += rec.get("cost_usd", 0.0)
        console.print(f"[cyan]{rec.get('label')}[/cyan] {rec.get('model')} "
                      f"| {rec.get('usage', {})} | ${rec.get('cost_usd', 0):.4f} "
                      f"| {rec.get('latency_s')}s")
    console.print(f"[bold]Total estimated cost: ${total:.4f}[/bold]")


if __name__ == "__main__":
    app()
