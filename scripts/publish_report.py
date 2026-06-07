"""Publish a completed run's report into the tracked `reports/<TICKER>/` folder.

Usage:
    python scripts/publish_report.py <RUN_ID> <TICKER>

Reads the run's audit artifacts (result.json + transcript.md) and writes a clean,
human-readable report set under reports/<TICKER>/ for committing to the repo:
  <TICKER>.memo.md        — the feature-length investment memo
  <TICKER>.transcript.md  — the full investigation transcript
  <TICKER>.dossier.json   — the structured dossier (fair value, band, judge verdict)
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "audit"
REPORTS = ROOT / "reports"


def _load_result(run_dir: Path, ticker: str) -> dict | None:
    f = run_dir / f"{ticker}.result.json"
    if not f.exists():
        return None
    return json.loads(f.read_text(encoding="utf-8"))


def publish(run_id: str, ticker: str) -> int:
    run_dir = AUDIT / run_id
    result = _load_result(run_dir, ticker)
    if result is None:
        print(f"[publish] no result.json for {ticker} in {run_id} — run not complete?")
        return 1

    out = REPORTS / ticker
    out.mkdir(parents=True, exist_ok=True)

    memo = result.get("memo_markdown") or "*(no memo — run did not finalize)*"
    (out / f"{ticker}.memo.md").write_text(memo, encoding="utf-8", newline="\n")

    dossier = result.get("dossier")
    if dossier is not None:
        # Attach the judge verdict alongside the dossier for the reader.
        judge = {k: result.get(k) for k in (
            "judge_approved", "judge_score", "judge_gaps", "action", "reject_reason")}
        payload = {"ticker": ticker, "run_id": run_id, "dossier": dossier, "judge": judge}
        (out / f"{ticker}.dossier.json").write_text(
            json.dumps(payload, indent=2, default=str), encoding="utf-8", newline="\n")

    tpath = result.get("transcript_path")
    src = Path(tpath) if tpath else (run_dir / f"{ticker}.transcript.md")
    if src.exists():
        shutil.copyfile(src, out / f"{ticker}.transcript.md")
    else:
        print(f"[publish] warning: transcript not found at {src}")

    fv = (dossier or {}).get("fair_value_per_share")
    print(f"[publish] {ticker}: memo + transcript + dossier -> {out}  (FMV/sh={fv})")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python scripts/publish_report.py <RUN_ID> <TICKER>")
        raise SystemExit(2)
    raise SystemExit(publish(sys.argv[1], sys.argv[2]))
