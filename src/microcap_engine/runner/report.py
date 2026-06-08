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


def publish_from_result(run_id: str, ticker: str, result) -> Path | None:
    """Write reports/<TICKER>/ from a NameResult. Returns the folder, or None if the
    result has nothing publishable (a drop with no memo, or a phased result)."""
    memo = getattr(result, "memo_markdown", None)
    dossier = getattr(result, "dossier", None)
    if not memo and dossier is None:
        return None

    out = REPORTS / ticker
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{ticker}.memo.md").write_text(
        sanitize_markdown(memo or "*(no memo — run did not finalize)*"),
        encoding="utf-8", newline="\n")

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
