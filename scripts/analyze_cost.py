"""Top-down cost autopsy of the overnight validation runs.

Reads the audit JSONL per run and answers: where did the money go, and how much of it
was unproductive context-churn vs. real new reasoning?
"""
from __future__ import annotations
import json, glob, os, collections

RUNS = ["NUS","JRVR","ACR","MFIN","CPSS","STIM","VSTM","VRCA","BZAI","CDXS"]
# Opus 4.8 pricing ($/Mtok): input 5, output 25, cache write 6.25 (1.25x), cache read 0.5 (0.1x)
P_IN, P_OUT, P_CW, P_CR = 5/1e6, 25/1e6, 6.25/1e6, 0.5/1e6

def phase_of(r):
    lab = (r.get("label") or r.get("phase") or "") or ""
    for p in ("redteam","judge","gate","analyst","research","pm","extract","triage","valuation"):
        if p in lab.lower():
            return p
    return r.get("phase") or "other"

def load(t):
    g = glob.glob(f"data/audit/*/{t}.jsonl")
    if not g: return None, []
    jf = max(g, key=os.path.getmtime)
    rows = []
    for l in open(jf, encoding="utf-8"):
        try: rows.append(json.loads(l))
        except Exception: pass
    return jf, [r for r in rows if isinstance(r, dict) and "usage" in r]

def tok(u, k): return u.get(k, 0) or 0

print(f"{'RUN':5} {'calls':>5} {'cost$':>8} {'fresh_in':>10} {'cacheWR':>11} {'cacheRD':>12} {'output':>9} | cacheRD%  redteam$  pm$")
grand = collections.Counter()
phase_cost = collections.Counter()
per_run = {}
for t in RUNS:
    jf, rows = load(t)
    if not rows:
        print(f"{t:5}  (no audit)")
        continue
    fin=cw=cr=out=cost=0.0
    pc = collections.Counter(); pcalls=collections.Counter()
    biggest=[]
    for r in rows:
        u=r["usage"]
        a,b,c,d = tok(u,"input_tokens"),tok(u,"cache_creation_input_tokens"),tok(u,"cache_read_input_tokens"),tok(u,"output_tokens")
        fin+=a; cw+=b; cr+=c; out+=d
        rc = r.get("cost_usd") or (a*P_IN+b*P_CW+c*P_CR+d*P_OUT)
        cost+=rc
        ph=phase_of(r); pc[ph]+=rc; pcalls[ph]+=1
        biggest.append((rc, ph, (r.get("label") or "")[:30], a+b+c, d))
    tottok=fin+cw+cr
    crpct = 100*cr/tottok if tottok else 0
    print(f"{t:5} {len(rows):5} {cost:8.2f} {fin:10,.0f} {cw:11,.0f} {cr:12,.0f} {out:9,.0f} | {crpct:5.1f}%  {pc['redteam']+pc['judge']:7.2f}  {pc['pm']:6.2f}")
    grand.update({"fresh":fin,"cw":cw,"cr":cr,"out":out,"cost":cost,"calls":len(rows)})
    for k,v in pc.items(): phase_cost[k]+=v
    per_run[t]={"rows":rows,"pc":pc,"pcalls":pcalls,"biggest":sorted(biggest,reverse=True)[:3],"cost":cost}

print("\n=== GRAND TOTALS ===")
tt=grand['fresh']+grand['cw']+grand['cr']
print(f"calls={grand['calls']:,}  cost=${grand['cost']:,.2f}  tokens: fresh={grand['fresh']:,.0f} cacheWR={grand['cw']:,.0f} cacheRD={grand['cr']:,.0f} out={grand['out']:,.0f}")
print(f"token mix: fresh {100*grand['fresh']/tt:.1f}% | cacheWRITE {100*grand['cw']/tt:.1f}% | cacheREAD {100*grand['cr']/tt:.1f}%")
print(f"COST attribution by token type: fresh_in ${grand['fresh']*P_IN:,.0f} | cacheWRITE ${grand['cw']*P_CW:,.0f} | cacheREAD ${grand['cr']*P_CR:,.0f} | output ${grand['out']*P_OUT:,.0f}")

print("\n=== COST BY PHASE (all runs) ===")
for ph,c in phase_cost.most_common():
    print(f"  {ph:10} ${c:8.2f}  ({100*c/grand['cost']:.0f}%)")

print("\n=== top-3 single most expensive calls per run ===")
for t,d in per_run.items():
    for rc,ph,lab,inT,outT in d["biggest"]:
        print(f"  {t:5} ${rc:5.2f} {ph:8} in={inT:>9,} out={outT:>6,}  {lab}")
