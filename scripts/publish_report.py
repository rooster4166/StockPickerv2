"""Manually (re)publish a completed run's report into reports/<TICKER>/.

Deep dives auto-publish on completion (microcap one). This is a thin wrapper for
re-publishing an older run from its audit artifacts:

    python scripts/publish_report.py <RUN_ID> <TICKER>
"""

from __future__ import annotations

import json
import sys
from types import SimpleNamespace

from microcap_engine.config import AUDIT_DIR
from microcap_engine.runner.report import publish_from_result


def main(run_id: str, ticker: str) -> int:
    f = AUDIT_DIR / run_id / f"{ticker}.result.json"
    if not f.exists():
        print(f"[publish] no result.json for {ticker} in {run_id}")
        return 1
    r = json.loads(f.read_text(encoding="utf-8"))
    dossier = r.get("dossier")
    # Rehydrate enough of a NameResult-like object for the publisher.
    result = SimpleNamespace(
        memo_markdown=r.get("memo_markdown"),
        dossier=SimpleNamespace(model_dump=lambda d=dossier: d) if dossier else None,
        transcript_path=r.get("transcript_path"),
        judge_approved=r.get("judge_approved"), judge_score=r.get("judge_score"),
        judge_gaps=r.get("judge_gaps"), action=r.get("action"))
    out = publish_from_result(run_id, ticker, result)
    print(f"[publish] {ticker} -> {out}" if out else f"[publish] nothing to publish for {ticker}")
    return 0 if out else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python scripts/publish_report.py <RUN_ID> <TICKER>")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
