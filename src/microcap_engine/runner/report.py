"""Publish a completed analysis to the tracked ``reports/<TICKER>/`` folder.

Called automatically when a deep dive finishes (CLI ``one``) so a clean, committable
report set (memo + transcript + dossier) appears without a manual step. Markdown is
sanitized so it renders correctly on GitHub (the models write '~' for 'approximately',
which GFM turns into strikethrough).
"""

from __future__ import annotations

import json
from pathlib import Path

import microcap_engine

REPORTS = Path(microcap_engine.__file__).resolve().parents[2] / "reports"


def sanitize_markdown(md: str) -> str:
    """'~' (approximately) -> '≈' so GitHub doesn't render tilde-spans as strikethrough."""
    if not md:
        return md
    return md.replace("~~", "≈").replace("~", "≈")


def _dval(dossier, key):
    """Read a dossier field whether it's a pydantic model or a dict."""
    if dossier is None:
        return None
    v = getattr(dossier, key, None)
    if v is not None:
        return v
    if hasattr(dossier, "model_dump"):
        try:
            return dossier.model_dump().get(key)
        except Exception:
            return None
    return dossier.get(key) if isinstance(dossier, dict) else None


def _price_header(ticker: str, dossier) -> str:
    """Deterministic post-analysis price-vs-FMV comparison header (price read HERE, never
    by the price-blind engine). Returns '' if the quote can't be fetched."""
    try:
        from microcap_engine.data.fmp import FMPProvider
        price = FMPProvider().get_quote(ticker).price
    except Exception:
        return ""
    if not price:
        return ""
    fmv = _dval(dossier, "fair_value_per_share")
    floor = _dval(dossier, "intrinsic_value_floor")
    head = f"> **Market price (joined post-analysis): ${price:,.2f}**"
    if fmv:
        gap = (fmv - price) / price
        verdict = ("UNDERVALUED" if gap > 0.15 else
                   "OVERVALUED" if gap < -0.15 else "≈ fairly valued")
        head += f"  ·  Engine FMV: ${fmv:,.2f}  ·  Implied: {gap:+.0%} ({verdict})"
    if floor:
        head += f"  ·  Floor: ${floor:,.2f}"
    return (head + "\n>\n> *The analysis below is PRICE-BLIND; this one-line header is a "
            "deterministic post-hoc comparison the engine never saw.*\n\n---\n\n")


def publish_from_result(run_id: str, ticker: str, result) -> Path | None:
    """Write reports/<TICKER>/ from a NameResult. Returns the folder, or None if the
    result has nothing publishable (a drop with no memo, or a phased result)."""
    memo = getattr(result, "memo_markdown", None)
    dossier = getattr(result, "dossier", None)
    if not memo and dossier is None:
        return None

    out = REPORTS / ticker
    out.mkdir(parents=True, exist_ok=True)
    body = sanitize_markdown(memo or "*(no report — run did not finalize)*")
    # Deterministic POST-analysis price join: the engine was price-BLIND throughout; only now,
    # at publish, do we fetch the quote and inject a price-vs-FMV comparison header for the
    # reader. The price never touched the analysis (it is read here, not by the LLM).
    (out / f"{ticker}.memo.md").write_text(
        _price_header(ticker, dossier) + body, encoding="utf-8", newline="\n")

    if dossier is not None:
        payload = {
            "ticker": ticker, "run_id": run_id,
            "dossier": dossier.model_dump() if hasattr(dossier, "model_dump") else dossier,
            "judge": {
                "approved": getattr(result, "judge_approved", None),
                "score": getattr(result, "judge_score", None),
                "gaps": getattr(result, "judge_gaps", None),
            },
            "action": getattr(result, "action", None),
        }
        (out / f"{ticker}.dossier.json").write_text(
            json.dumps(payload, indent=2, default=str), encoding="utf-8", newline="\n")

    tpath = getattr(result, "transcript_path", None)
    src = Path(tpath) if tpath else None
    if src and src.exists():
        (out / f"{ticker}.transcript.md").write_text(
            sanitize_markdown(src.read_text(encoding="utf-8")),
            encoding="utf-8", newline="\n")
    return out
