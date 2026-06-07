"""Pretty-print every phase's structured output from a NameResult dump.

Usage: python scripts/inspect_result.py <path-to-Ticker.result.json>
Used to verify, phase by phase, that the pipeline returns exactly what's expected.
"""

from __future__ import annotations

import json
import sys
import textwrap

# The engine's memos/methods contain Unicode (minus signs, etc.); make Windows
# console output safe.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _wrap(label: str, value, width: int = 100) -> None:
    if value is None or value == [] or value == "":
        return
    print(f"  {label}:")
    if isinstance(value, list):
        for v in value:
            print(textwrap.fill(f"- {v}", width=width, subsequent_indent="    "))
    else:
        print(textwrap.fill(str(value), width=width, initial_indent="    ",
                            subsequent_indent="    "))


def _agentic_view(d: dict) -> None:
    print("=" * 100)
    print(f"AGENTIC RESULT: {d['ticker']}  action={d['action']}  cost=${d.get('cost_usd')}  "
          f"calls={d.get('n_calls')}  red_team_rounds={d.get('red_team_rounds')}")
    if d["action"] == "drop":
        print("REJECTED:", d.get("reason"))
        return
    ds = d.get("dossier") or {}
    print(f"\nFAIR VALUE: {ds.get('fair_value_per_share')} "
          f"(bear {ds.get('fair_value_low')} / bull {ds.get('fair_value_high')}) | "
          f"confidence {ds.get('confidence')}")
    print(f"METHOD: {ds.get('valuation_method')}")
    print(f"DILUTED SHARES: {ds.get('diluted_shares_used')}")
    _wrap("THESIS", ds.get("thesis_summary"))
    _wrap("VALUE DRIVERS", ds.get("key_value_drivers"))
    _wrap("KEY RISKS", ds.get("key_risks"))
    _wrap("WHAT WOULD CHANGE MY MIND", ds.get("what_would_change_my_mind"))
    if d.get("unresolved_concerns"):
        _wrap("UNRESOLVED RED-TEAM CONCERNS", d["unresolved_concerns"])
    print("\n" + "=" * 100 + "\nMEMO:\n")
    print(d.get("memo_markdown", "")[:12000])


def main(path: str) -> None:
    d = json.loads(open(path, encoding="utf-8").read())
    if d.get("dossier") is not None or (d.get("action") == "drop" and not d.get("gate")):
        return _agentic_view(d)
    print("=" * 100)
    print(f"NAME RESULT: {d['ticker']}  action={d['action']}  "
          f"cost=${d.get('cost_usd')}  tokens={d.get('total_tokens')}  calls={d.get('n_calls')}")
    if d.get("gate"):
        g = d["gate"]
        print(f"\nGATE: verdict={g['verdict']} conf={g['confidence']} :: {g['reason'][:200]}")
    if d["action"] == "drop":
        return
    fv = d.get("fair_value") or {}
    print(f"\nBLENDED FAIR VALUE: median={fv.get('median')} "
          f"(p10 {fv.get('p10')} / p90 {fv.get('p90')}, n={fv.get('n_runs')})  "
          f"confidence={d.get('confidence')}")
    if d.get("thesis_breakers"):
        _wrap("THESIS BREAKERS", d["thesis_breakers"])

    for i, run in enumerate(d.get("runs", [])):
        print("\n" + "-" * 100)
        print(f"RUN {i} [{run['config_label']}]")
        if run.get("transcripts"):
            tr = run["transcripts"]
            print("\n[PHASE 0 — TRANSCRIPTS]")
            _wrap("guidance", tr.get("guidance_signals"))
            _wrap("capital_allocation", tr.get("capital_allocation"))
            _wrap("tone_and_changes", tr.get("tone_and_changes"))
            _wrap("red_flags", tr.get("red_flags"))
            _wrap("summary", tr.get("summary"))

        fin = run["financials"]
        print("\n[PHASE 1 — FINANCIALS]")
        _wrap("summary", fin.get("summary"))
        _wrap("anomalies", fin.get("anomalies"))
        print(f"    revenue_trend: {[(p['period'], p['value']) for p in fin.get('revenue_trend', [])]}")
        print(f"    citations: {len(fin.get('citations', []))}")

        biz = run["business"]
        print("\n[PHASE 2 — BUSINESS]")
        _wrap("summary", biz.get("summary"))
        _wrap("moat", biz.get("moat_assessment"))
        _wrap("revenue_drivers", biz.get("revenue_drivers"))

        ind = run["industry"]
        print("\n[PHASE 3 — INDUSTRY]")
        _wrap("summary", ind.get("summary"))
        _wrap("adjacent_exposures", ind.get("adjacent_exposures"))
        _wrap("direct_comps", ind.get("direct_comps"))

        nw = run["news"]
        print("\n[PHASE 4 — NEWS/CATALYSTS]")
        _wrap("summary", nw.get("summary"))
        _wrap("catalysts", [c.get("description") for c in nw.get("catalysts", [])])

        aset = run["assumption_set"]
        print(f"\n[PHASE 5 — CONSOLIDATION GATE]  method={aset['method']}")
        _wrap("rationale", aset.get("rationale"))
        _wrap("key_risks", aset.get("key_risks"))
        block = aset.get(aset["method"])
        print(f"    assumption block ({aset['method']}): "
              f"{json.dumps(block)[:600] if block else None}")

        val = run["valuation"]
        print(f"\n[PHASE 6 — VALUATION]  method={val['method']} "
              f"fair_value_per_share={val['fair_value_per_share']}")
        print(f"    EV={val.get('enterprise_value')} equity={val.get('equity_value')}")
        _wrap("notes", val.get("notes"))

        rt = run["redteam"]
        print(f"\n[PHASE 7 — RED-TEAM]  would_break_thesis={rt['would_break_thesis']} "
              f"most_severe={rt['most_severe']}")
        _wrap("summary", rt.get("summary"))
        for c in rt.get("concerns", []):
            print(f"    [{c['severity']}] {c['category']}: {c['description'][:160]}")


if __name__ == "__main__":
    main(sys.argv[1])
