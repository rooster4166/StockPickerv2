"""Command-line entry point for the Micro-Cap Value Engine.

Subcommands:
  universe   Screen the $50-300M US universe (or a candidate list) by market cap.
  baseline   Run the Phase-0 proven Buffett sweep and build a book.
  analyze    Run the Phase-1 heavy deep-dive engine and build a book.
  gate       Run only the cheap reject-gate over a ticker list (diagnostic).

Tickers come from --tickers, --tickers-file, or (for analyze/baseline) a prior
universe screen. Outputs are written as JSON under the configured output dir.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import logging
import os
import sys
from typing import Optional

from .config import SETTINGS


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _load_tickers(args) -> list[str]:
    tickers: list[str] = []
    if getattr(args, "tickers", None):
        tickers += [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    if getattr(args, "tickers_file", None):
        with open(args.tickers_file) as fh:
            tickers += [line.strip().upper() for line in fh if line.strip()]
    # de-dup, preserve order
    seen: set[str] = set()
    return [t for t in tickers if not (t in seen or seen.add(t))]


def _write_output(name: str, payload: dict) -> str:
    os.makedirs(SETTINGS.output_dir, exist_ok=True)
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(SETTINGS.output_dir, f"{name}-{stamp}.json")
    with open(path, "w") as fh:
        json.dump(payload, fh, indent=2, default=str)
    return path


def _make_provider():
    from .data.provider import FreeDataProvider

    return FreeDataProvider(SETTINGS)


def _make_llm():
    from .llm.client import AnthropicLLM

    return AnthropicLLM(SETTINGS)


# --------------------------------------------------------------------- commands
def cmd_universe(args) -> int:
    provider = _make_provider()
    tickers = _load_tickers(args) or None
    if tickers is None and not args.full:
        print("Refusing to screen the entire SEC universe without --full "
              "(thousands of slow network calls). Pass --tickers/--tickers-file "
              "or --full with --limit.", file=sys.stderr)
        return 2
    kept = provider.screen_universe(tickers, limit=args.limit)
    payload = {"count": len(kept), "tickers": kept, "band": [SETTINGS.mcap_min, SETTINGS.mcap_max]}
    path = _write_output("universe", payload)
    print(f"Kept {len(kept)} names in band ${SETTINGS.mcap_min:,.0f}-${SETTINGS.mcap_max:,.0f}")
    print(f"Wrote {path}")
    return 0


def cmd_run(args, mode: str) -> int:
    from .pipeline import run_pipeline

    tickers = _load_tickers(args)
    if not tickers:
        print("No tickers. Use --tickers or --tickers-file.", file=sys.stderr)
        return 2
    provider = _make_provider()
    llm = _make_llm()
    result = run_pipeline(tickers, provider, llm, capital=args.capital, mode=mode, settings=SETTINGS)
    path = _write_output(mode, result)
    book = result["book"]
    print(f"[{mode}] analyzed {result['n_analyzed']}, dropped {result['n_dropped']}, "
          f"{book['n_positions']} positions, deployed ${book['deployed']:,.0f} "
          f"of ${book['capital']:,.0f}")
    for p in book["positions"][:25]:
        print(f"  {p['ticker']:<6} ${p['dollars']:>12,.0f}  w={p['weight']:.3f}  "
              f"gap={p['gap']:.2f}  conf={p['confidence']:.2f}  ({p['capped_by']})")
    print(f"Wrote {path}")
    return 0


def cmd_gate(args) -> int:
    from .engine.gate import cheap_gate, should_drop

    tickers = _load_tickers(args)
    if not tickers:
        print("No tickers. Use --tickers or --tickers-file.", file=sys.stderr)
        return 2
    provider = _make_provider()
    llm = _make_llm()
    rows = []
    for tk in tickers:
        company = provider.get_company_data(tk)
        g = cheap_gate(company, llm, SETTINGS)
        g["drop"] = should_drop(g, SETTINGS)
        g["ticker"] = tk
        rows.append(g)
        print(f"  {tk:<6} {g['verdict']:<11} conf={g['confidence']:.2f} "
              f"{'DROP' if g['drop'] else 'keep'}  {g['reason']}")
    _write_output("gate", {"results": rows})
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="microcap", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-v", "--verbose", action="store_true", help="info-level logging")
    sub = p.add_subparsers(dest="command", required=True)

    def add_ticker_args(sp):
        sp.add_argument("--tickers", help="comma-separated tickers")
        sp.add_argument("--tickers-file", help="file with one ticker per line")

    u = sub.add_parser("universe", help="screen the universe by market cap")
    add_ticker_args(u)
    u.add_argument("--full", action="store_true", help="screen the full SEC list (slow)")
    u.add_argument("--limit", type=int, default=None, help="stop after N kept names")
    u.set_defaults(func=cmd_universe)

    b = sub.add_parser("baseline", help="Phase-0 proven Buffett sweep")
    add_ticker_args(b)
    b.add_argument("--capital", type=float, default=100_000.0)
    b.set_defaults(func=lambda a: cmd_run(a, "baseline"))

    a = sub.add_parser("analyze", help="Phase-1 heavy deep-dive engine")
    add_ticker_args(a)
    a.add_argument("--capital", type=float, default=100_000.0)
    a.set_defaults(func=lambda a: cmd_run(a, "heavy"))

    g = sub.add_parser("gate", help="run only the cheap reject-gate")
    add_ticker_args(g)
    g.set_defaults(func=cmd_gate)
    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _setup_logging(args.verbose)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
