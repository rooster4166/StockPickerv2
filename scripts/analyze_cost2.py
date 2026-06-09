"""Second cut: where the back-and-forth is, and why cache-write is so high."""
from __future__ import annotations
import json, glob, os, collections
from datetime import datetime

RUNS = ["NUS","JRVR","ACR","MFIN","CPSS","STIM","VSTM","VRCA","BZAI","CDXS"]

def load(t):
    g = glob.glob(f"data/audit/*/{t}.jsonl")
    if not g: return []
    jf = max(g, key=os.path.getmtime)
    out=[]
    for l in open(jf, encoding="utf-8"):
        try:
            r=json.loads(l)
            if isinstance(r,dict) and "usage" in r: out.append(r)
        except Exception: pass
    return out

def ts(r):
    try: return datetime.fromisoformat(r["ts"][:19])
    except Exception: return None

print(f"{'RUN':5} {'pm_steps':>8} {'maxOut':>7} {'val_runs':>8} {'analysts':>8} {'an_turns':>8} {'research':>8} {'redteam':>7} {'gap>5m':>7}")
for t in RUNS:
    rows=load(t)
    if not rows: continue
    pm=[r for r in rows if "pm" in ((r.get('label') or r.get('phase') or '').lower())]
    maxout=sum(1 for r in rows if (r['usage'].get('output_tokens',0) or 0)>=27000)
    val=sum(1 for r in rows if 'valuation' in (r.get('label','') or '').lower() or 'compute_val' in (r.get('label','') or '').lower())
    analysts=set()
    anturns=0
    for r in rows:
        lab=r.get('label') or ''
        if lab.startswith('analyst:'):
            anturns+=1
            parts=lab.split(':')
            if len(parts)>=2: analysts.add(parts[1])
    research=sum(1 for r in rows if (r.get('label') or '').startswith('research'))
    redteam=sum(1 for r in rows if 'redteam' in (r.get('label','') or '').lower() or 'judge' in (r.get('label','') or '').lower())
    # cache expiry: consecutive same-context calls (pm) >5min apart
    gaps=0; prev=None
    for r in rows:
        tt=ts(r)
        if prev and tt and (tt-prev).total_seconds()>300: gaps+=1
        if tt: prev=tt
    print(f"{t:5} {len(pm):8} {maxout:7} {val:8} {len(analysts):8} {anturns:8} {research:8} {redteam:7} {gaps:7}")

# total wall-clock + output cap analysis
print("\n=== output cap (>=27k tok) — over-generation signal ===")
allrows=[]
for t in RUNS: allrows+=[(t,r) for r in load(t)]
capped=[(t,r) for t,r in allrows if (r['usage'].get('output_tokens',0) or 0)>=27000]
print(f"{len(capped)} of {len(allrows)} calls hit the 28k output cap ({100*len(capped)/len(allrows):.0f}%)")
capcost=sum((r.get('cost_usd') or 0) for _,r in capped)
print(f"those capped calls cost ${capcost:.2f}")
byphase=collections.Counter()
for t,r in capped:
    lab=(r.get('label') or r.get('phase') or '').lower()
    p=next((x for x in ('redteam','judge','analyst','research','pm') if x in lab),'other')
    byphase[p]+=1
print("capped calls by phase:", dict(byphase))

# wall clock per run
print("\n=== wall-clock per run ===")
for t in RUNS:
    rows=load(t)
    if not rows: continue
    tss=[ts(r) for r in rows if ts(r)]
    if len(tss)>=2:
        mins=(max(tss)-min(tss)).total_seconds()/60
        print(f"  {t:5} {mins:6.0f} min  ({len(rows)} calls, {mins*60/len(rows):.0f}s/call avg)")
