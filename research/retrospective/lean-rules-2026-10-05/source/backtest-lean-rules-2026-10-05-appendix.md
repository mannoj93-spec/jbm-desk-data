# Lean-rule backtest — appendix: specification, code, outputs, input hashes (Oct 6 2026)

Companion to `claude/backtest-lean-rules-2026-10-05.md`. Unversioned thread code (crypto-desk 12.4.11 `runbook.md` requirement 131). Container file times (UTC, Oct 6): SPEC.md 00:42:10 · run.py 00:42:32 · run2.py 00:42:58 · run3.py 01:07:08 · manifest.py 01:09:33 · data_manifest.json 01:11:41 · run4.py 01:30:16; inputs k4h.json 00:40:26 · metrics.json 00:41:36 · funding.json 00:41:43. run.py and run2.py (and the SPEC's declared secondary grid) are the pre-specified runs; run2's "What S-04 removed" block, run3 and run4 are post hoc.

## Input hashes (sha256, computed after the runs; files unmodified since their fetch times above)
- `k4h.json` (14,814 Binance BTCUSDT perp 4H bars) `1e7d2245aad47132fb6e086bdef344bcff4d99591ee74d86edfb59271391e615`
- `metrics.json` (Binance OI archive metrics, Oct 2024 – Oct 2026) `cefa919b51140609874ea025821f3dbd484675ed807d8747d517d9e485f66ebb`
- `funding.json` (7,411 Binance BTCUSDT funding settlements) `7382cc208ebd9ed9f9f566c57180545faee1adacd7d523e836581ec2efec738f`
- `data_manifest.json` (per-file archive manifest from a re-fetch at 01:09Z, after run.py–run3.py; provider checksums match; records the file set and states, not the bytes the runs read; funding not included) `23293deb1a6d355880900c2e53c79b0067e026573c79a4f10dac04f5b0ebd25f` — the 450 KB manifest itself is not stored in the project; it is in the bundle delivered to the operator's `Claude outputs` folder.

## SPEC.md (verbatim; its "~00:50Z" header is wrong — the file time is 00:42:10Z)

```markdown
# Backtest spec — written before results (Oct 5 2026, ~00:50Z Oct 6)

Class: retrospective exploration (E-01 "exploratory"). Not a registered prospective test.

Question: do the desk's lean rules (S-04 deferral + structure-break conversion + OI/funding
confirmation) produce directional calls that beat a no-skill baseline, and how often do they fire?

Data: Binance BTCUSDT perp 4H klines 2020-01-01 → 2026-10-04 (data.binance.vision via jbm_archive);
Binance BTCUSDT OI (archive metrics, 5-min, ok days only) 2024-10-01 → 2026-10-04; Binance funding
history 2020 →. Cross-venue OI has no history before Sep 2026, so Binance OI stands in (labelled).

Mechanical proxy for a lean (the live process is partly judgmental; this tests the rules, not me):
- Structure break: long if close_t > max(high, prior N bars); short if close_t < min(low, prior N).
- S-04 gate: bar move m_t = close_t − open_t. If m_t in the lean direction exceeds T, defer to the
  next close: convert if that close is still beyond the level and its bar move ≤ T in that
  direction; carry once more if it is again > T; withdraw after two carries; cancel if back inside.
- OI confirmation: Binance OI change over the decision bar > 0 (new positions, not covering).
- Funding not crowded: long needs last settled funding ≤ +1 bp; short needs ≥ −1 bp.

Variants: V0 raw break; V1 + S-04 (desk rule); V2 = V1 + OI; V3 = V2 + funding.

PRIMARY (declared now): N = 24 bars, T = 0.353% of price (300 pts at 85,000), horizon 24h
(6 bars), cost 10 bp round trip (taker both sides), metric = mean signed log return net of cost,
drift-adjusted (minus direction × the sample's mean 24h return), 95% CI by weekly block bootstrap.
Samples: full 2020-01→2026-10 (V0, V1), last 24 months (V0–V3).

Secondary (multiplicity noted, not used to pick a winner): N ∈ {24, 42}; T ∈ {0.353% of price,
0.5 × trailing 42-bar 4H σ}; horizons 4h and 24h; last 6 months.

Also measured: S-04 directly — after a bar moving more than T, the next-4h and next-24h return in
the move's direction (continuation) vs. all bars.

Baselines: zero (no skill, before drift), and the drift adjustment above. Hit rate vs 50%.
```

## fetch.py

```python
import sys, json, datetime as dt, time, urllib.request
sys.path.insert(0,'/mnt/skills/plugins/crypto-desk')
import jbm_archive as ja
from concurrent.futures import ThreadPoolExecutor
t0=time.time()
st,rows,man=ja.load_klines_span(dt.date(2020,1,1), dt.date(2026,10,4), '4h')
bad=[m for m in man if m.get('state')!='ok'] if isinstance(man,list) else []
print('klines',st,len(rows),'non-ok files',len(bad), round(time.time()-t0,1)); json.dump(rows,open('k4h.json','w'))
# metrics (Binance BTCUSDT OI etc.), last ~24 months
days=[dt.date(2024,10,1)+dt.timedelta(days=i) for i in range((dt.date(2026,10,4)-dt.date(2024,10,1)).days+1)]
def one(d):
    for a in range(3):
        try:
            s,r,_=ja.load_metrics(d); return d.isoformat(),s,r
        except Exception as e: err=str(e); time.sleep(1)
    return d.isoformat(),'retrieval_error',[]
t0=time.time()
with ThreadPoolExecutor(12) as ex: res=list(ex.map(one,days))
states={}
out=[]
for d,s,r in res:
    states[s]=states.get(s,0)+1
    out+= [{'t':x['available_at_utc'],'stamp':x['archive_stamp_utc'],'oi':x['oi_btc']} for x in r if x.get('oi_btc') is not None]
print('metrics days',len(days),states,'rows',len(out),round(time.time()-t0,1)); json.dump({'rows':out,'states':{d:s for d,s,_ in res}},open('metrics.json','w'))
# funding history
B='https://www.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=1000&startTime='
start=int(dt.datetime(2020,1,1,tzinfo=dt.timezone.utc).timestamp()*1000); fr=[]
while True:
    js=json.load(urllib.request.urlopen(B+str(start),timeout=30))
    if not js: break
    fr+=js; start=js[-1]['fundingTime']+1
    if len(js)<1000: break
    time.sleep(0.3)
print('funding',len(fr),fr[0]['fundingTime'],fr[-1]['fundingTime']); json.dump(fr,open('funding.json','w'))
```

## run.py

```python
import json, math, bisect, random, datetime as dt
from collections import defaultdict

P = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
K = json.load(open("k4h.json"))
K.sort(key=lambda r: r["open_utc"])
T_OPEN = [P(r["open_utc"]) for r in K]
T_CLOSE = [P(r["close_utc"]) for r in K]
O = [r["open"] for r in K]; H = [r["high"] for r in K]; L = [r["low"] for r in K]; C = [r["close"] for r in K]
n = len(K)
lr = [0.0] + [math.log(C[i] / C[i - 1]) for i in range(1, n)]

# trailing 42-bar sigma of 4H log returns, in points at the prior close
SIG = [None] * n
for i in range(43, n):
    w = lr[i - 42:i]; m = sum(w) / 42
    SIG[i] = math.sqrt(sum((x - m) ** 2 for x in w) / 41) * C[i - 1]

# OI (ok days only), as-of by availability
M = json.load(open("metrics.json"))
okdays = {d for d, s in M["states"].items() if s == "ok"}
oi_rows = sorted((P(r["t"]), r["oi"]) for r in M["rows"] if r["stamp"][:10] in okdays)
oi_t = [t for t, _ in oi_rows]
def oi_at(t, max_age=dt.timedelta(minutes=30)):
    j = bisect.bisect_right(oi_t, t) - 1
    if j < 0 or t - oi_t[j] > max_age: return None
    return oi_rows[j][1]
OI_START = P("2024-10-01T00:00:00Z")

F = json.load(open("funding.json"))
f_t = [dt.datetime.fromtimestamp(x["fundingTime"] / 1000, dt.timezone.utc) for x in F]
f_v = [float(x["fundingRate"]) * 1e4 for x in F]
def fund_at(t):
    j = bisect.bisect_right(f_t, t) - 1
    return f_v[j] if j >= 0 else None

def thr(i, mode):
    return 0.00353 * C[i - 1] if mode == "pct" else (0.5 * SIG[i] if SIG[i] else None)

def signals(N, mode, variant, start, end):
    """Return list of (decision_index, dir). Deferral per S-04 for variants >= 1."""
    out, pending = [], None   # pending: (dir, level, carries)
    oi_missing = 0
    for i in range(max(N, 43), n - 1):
        if not (start <= T_CLOSE[i] < end): continue
        T = thr(i, mode)
        if T is None: continue
        m = C[i] - O[i]
        def confirm(i, d):
            nonlocal oi_missing
            if variant >= 2:
                a, b = oi_at(T_OPEN[i]), oi_at(T_CLOSE[i])
                if a is None or b is None: oi_missing += 1; return False
                if b - a <= 0: return False
            if variant >= 3:
                f = fund_at(T_CLOSE[i])
                if f is None: return False
                if d > 0 and f > 1: return False
                if d < 0 and f < -1: return False
            return True
        if pending:
            d, lvl, carries = pending
            still = (C[i] > lvl) if d > 0 else (C[i] < lvl)
            if not still: pending = None
            elif m * d > T:
                pending = (d, lvl, carries + 1) if carries + 1 < 2 else None
            else:
                pending = None
                if confirm(i, d): out.append((i, d))
            continue
        hi = max(H[i - N:i]); lo = min(L[i - N:i])
        d = 1 if C[i] > hi else (-1 if C[i] < lo else 0)
        if d == 0: continue
        lvl = hi if d > 0 else lo
        if variant >= 1 and m * d > T:
            pending = (d, lvl, 0); continue
        if confirm(i, d): out.append((i, d))
    return out, oi_missing

def evaluate(sig, h, cost_bp, start, end):
    idx = [i for i in range(n - h) if start <= T_CLOSE[i] < end]
    drift = sum(math.log(C[i + h] / C[i]) for i in idx) / len(idx)
    rows = []
    for i, d in sig:
        if i + h >= n: continue
        r = d * math.log(C[i + h] / C[i])
        rows.append((T_CLOSE[i], r * 1e4 - cost_bp, (r - d * drift) * 1e4 - cost_bp, r > 0))
    return rows, drift * 1e4

def boot(rows, k=2, B=2000, seed=7):
    if len(rows) < 5: return (None, None)
    wk = defaultdict(list)
    for t, *v in rows: wk[t.isocalendar()[:2]].append(v[k - 1])
    weeks = list(wk.values()); rnd = random.Random(seed); ms = []
    for _ in range(B):
        s = [x for _ in weeks for x in rnd.choice(weeks)]
        ms.append(sum(s) / len(s))
    ms.sort(); return ms[int(.025 * B)], ms[int(.975 * B)]

def summ(label, sig, h, start, end, cost=10, extra=""):
    rows, drift = evaluate(sig, h, cost, start, end)
    weeks = (end - start).days / 7
    if not rows:
        print(f"{label:46} n=0 {extra}"); return
    k = len(rows)
    net = sum(r[1] for r in rows) / k; adj = sum(r[2] for r in rows) / k; hit = sum(r[3] for r in rows) / k
    lo, hi = boot(rows, 2)
    # non-overlapping count (greedy)
    last = None; nov = 0
    for t, *_ in rows:
        if last is None or (t - last) >= dt.timedelta(hours=4 * h): nov += 1; last = t
    ci = f"[{lo:+.0f},{hi:+.0f}]" if lo is not None else "[n/a]"
    print(f"{label:46} n={k:4d} ({k/weeks:4.2f}/wk, {nov} non-ovl) hit {hit*100:4.1f}%  net {net:+6.1f}bp  drift-adj {adj:+6.1f}bp 95%CI {ci} {extra}")

UTC = dt.timezone.utc
FULL = (dt.datetime(2020, 3, 1, tzinfo=UTC), dt.datetime(2026, 10, 4, tzinfo=UTC))
R24 = (dt.datetime(2024, 10, 2, tzinfo=UTC), dt.datetime(2026, 10, 4, tzinfo=UTC))
R6 = (dt.datetime(2026, 4, 4, tzinfo=UTC), dt.datetime(2026, 10, 4, tzinfo=UTC))

if __name__ == "__main__":
    import sys
    print(f"bars {n}: {K[0]['open_utc']} -> {K[-1]['close_utc']}; OI rows {len(oi_rows)} (ok days {len(okdays)}); funding {len(F)}")
    print("\n=== PRIMARY: N=24, T=0.353% price, 24h horizon, 10bp cost ===")
    for lab, (s, e) in (("FULL 2020-03..2026-10", FULL), ("LAST 24M", R24)):
        for v in ((0, 1) if lab.startswith("FULL") else (0, 1, 2, 3)):
            sig, miss = signals(24, "pct", v, s, e)
            summ(f"{lab} V{v}", sig, 6, s, e, extra=f"(OI-missing bars {miss})" if v >= 2 else "")
```

## run2.py

```python
from run import *
print("=== Q1: S-04 directly. After a bar moving > T, return in the move's direction (no cost) ===")
for lab,(s,e) in (("FULL",FULL),("LAST 24M",R24),("LAST 6M",R6)):
  for mode in ("pct","sig"):
    for h in (1,6):
        big=[];allb=[]
        for i in range(44,n-h):
            if not (s<=T_CLOSE[i]<e): continue
            T=thr(i,mode); m=C[i]-O[i]
            if T is None or m==0: continue
            d=1 if m>0 else -1
            r=d*math.log(C[i+h]/C[i])*1e4
            allb.append((T_CLOSE[i],r,r,r>0))
            if abs(m)>T: big.append((T_CLOSE[i],r,r,r>0))
        def st(rows):
            k=len(rows); lo,hi=boot(rows,1); return f"n={k:5d} cont {sum(x[3] for x in rows)/k*100:4.1f}% mean {sum(x[1] for x in rows)/k:+6.1f}bp CI[{lo:+.0f},{hi:+.0f}]"
        print(f"{lab:8} T={mode:3} h={h*4:2}h  big moves: {st(big)} | all bars: {st(allb)}")
print("\n=== What S-04 removed: breakouts on a >T bar, entered immediately vs deferred outcome (N=24, pct, 24h, 10bp) ===")
for lab,(s,e) in (("FULL",FULL),("LAST 24M",R24)):
    v0,_=signals(24,"pct",0,s,e)
    gated=[(i,d) for i,d in v0 if (C[i]-O[i])*d>thr(i,"pct")]
    kept=[(i,d) for i,d in v0 if (C[i]-O[i])*d<=thr(i,"pct")]
    summ(f"{lab} breakouts on big bars (immediate)",gated,6,s,e)
    summ(f"{lab} breakouts on normal bars",kept,6,s,e)
    v1,_=signals(24,"pct",1,s,e); ks=set(kept); conv=[x for x in v1 if x not in ks]
    summ(f"{lab} deferred-then-converted",conv,6,s,e)
print("\n=== Sensitivity grid (secondary; 4 x 2 x 2 cells per sample, multiplicity applies) ===")
for lab,(s,e) in (("FULL",FULL),("LAST 24M",R24),("LAST 6M",R6)):
  for N in (24,42):
    for mode in ("pct","sig"):
      for h in (1,6):
        for v in (0,1):
            sig,_=signals(N,mode,v,s,e); summ(f"{lab} N={N} T={mode} h={h*4}h V{v}",sig,h,s,e)
```

## run3.py

```python
import sys; sys.path.insert(0,'/home/claude/pkg/crypto-desk')
import jbm_measure as jm
import run as R
from run import *
# 1) re-derive sigma with the versioned module and confirm the backtest's hand-rolled sigma matches
mx=0.0
for i in range(44,n,97):
    s=jm.sd_c2c(C[i-43:i]).value*C[i-1]
    mx=max(mx,abs(s-SIG[i])/s)
print('max rel diff hand sigma vs jm.sd_c2c (sampled):',mx)
# 2) operative-sigma variant (Parkinson 6-bar via jm, the O21 default) for S-04's 0.5x rule
P6=[None]*n
for i in range(6,n): P6[i]=jm.sd_parkinson(H[i-6:i],L[i-6:i],min_bars=6).value*C[i-1]
_thr=R.thr
def thr2(i,mode):
    if mode=='park6': return 0.5*P6[i] if P6[i] else None
    return _thr(i,mode)
R.thr=thr2
for lab,(s,e) in (("FULL",FULL),("LAST 24M",R24)):
    tot=sum(1 for i in range(44,n) if s<=T_CLOSE[i]<e); big=sum(1 for i in range(44,n) if s<=T_CLOSE[i]<e and abs(C[i]-O[i])>thr2(i,'park6'))
    print(lab,'share of bars > 0.5*park6:',round(big/tot,3))
    for v in (0,1):
        sig,_=R.signals(24,'park6',v,s,e); R.summ(f"{lab} N=24 T=0.5*park6 h=24h V{v}",sig,6,s,e)
# 3) containment base rates: next 4H close inside a symmetric band around the current close
print('\n=== naive containment: next 4H close within +/-h of the current close ===')
for lab,(s,e) in (("FULL",FULL),("LAST 24M",R24),("LAST 6M",R6)):
    idx=[i for i in range(44,n-1) if s<=T_CLOSE[i]<e]
    row=[]
    for h in (0.005,0.006,0.0075,0.009,0.01,0.0125):
        k=sum(1 for i in idx if C[i]*(1-h)<C[i+1]<C[i]*(1+h)); lo,hi=jm.wilson(k,len(idx)); row.append(f"±{h*100:.2f}% {k/len(idx)*100:4.1f}% [{lo*100:.1f},{hi*100:.1f}]")
    print(f"{lab:8} n={len(idx)}: "+" | ".join(row))
    row=[]
    for kk in (1.0,1.5,2.0):
        k=sum(1 for i in idx if abs(C[i+1]-C[i])<kk*P6[i+1-0] if P6[i]) ; m=sum(1 for i in idx if P6[i])
        k=sum(1 for i in idx if P6[i] and abs(C[i+1]-C[i])<kk*P6[i]); row.append(f"±{kk}σp6 {k/m*100:4.1f}%")
    print(f"{'':8} operative-σ bands (Parkinson 6-bar at issue): "+" | ".join(row))
```

## run4.py

```python
"""POST-HOC additions (written Oct 6 ~01:30Z, after the primary results and the independent review).
Not part of SPEC.md. Labelled post-hoc wherever cited."""
import sys; sys.path.insert(0,'/home/claude/pkg/crypto-desk')
import os; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
import jbm_measure as jm
import run as R
from run import *
# sigma incl. the issue bar: c2c over the 42 returns ending at close i; Parkinson over bars i-5..i
SIGI=[None]*n; P6I=[None]*n
for i in range(43,n): SIGI[i]=jm.sd_c2c(C[i-42:i+1]).value*C[i]
for i in range(5,n): P6I[i]=jm.sd_parkinson(H[i-5:i+1],L[i-5:i+1],min_bars=6).value*C[i]
def T(i,mode):
    if mode=='pct': return 0.00353*C[i-1]
    if mode=='c2c0.5': return 0.5*SIGI[i]
    if mode=='p6_0.5': return 0.5*P6I[i]
    if mode=='c2c1': return 1.0*SIGI[i]
    if mode=='c2c2': return 2.0*SIGI[i]
def wkboot_diff(a,b,B=2000,seed=11):
    """weekly-block bootstrap of mean(a)-mean(b); a,b lists of (t,value)"""
    import random
    wa=defaultdict(list); wb=defaultdict(list)
    for t,v in a: wa[t.isocalendar()[:2]].append(v)
    for t,v in b: wb[t.isocalendar()[:2]].append(v)
    keys=sorted(set(wa)|set(wb)); rnd=random.Random(seed); ds=[]
    for _ in range(B):
        ks=[rnd.choice(keys) for _ in keys]
        xa=[v for k in ks for v in wa.get(k,[])]; xb=[v for k in ks for v in wb.get(k,[])]
        if xa and xb: ds.append(sum(xa)/len(xa)-sum(xb)/len(xb))
    ds.sort(); return ds[int(.025*len(ds))], ds[int(.975*len(ds))]
print("=== P1 (post-hoc): continuation after bars > T vs bars <= T (complement), in the bar's direction, no cost ===")
for lab,(s,e) in (("FULL",FULL),("LAST 24M",R24)):
  for mode in ('pct','c2c0.5','p6_0.5','c2c1','c2c2'):
    for h in (1,6):
        big=[];small=[];bh=[];sh=[]
        for i in range(44,n-h):
            if not (s<=T_CLOSE[i]<e): continue
            m=C[i]-O[i]
            if m==0: continue
            d=1 if m>0 else -1; r=d*math.log(C[i+h]/C[i])*1e4
            (big if abs(m)>T(i,mode) else small).append((T_CLOSE[i],r))
            (bh if abs(m)>T(i,mode) else sh).append((T_CLOSE[i],1.0 if r>0 else 0.0))
        lo,hi=wkboot_diff(big,small); hlo,hhi=wkboot_diff(bh,sh)
        mb=sum(v for _,v in big)/len(big); ms=sum(v for _,v in small)/len(small)
        cb=sum(v for _,v in bh)/len(bh); cs=sum(v for _,v in sh)/len(sh)
        print(f"{lab:8} T={mode:6} h={h*4:2}h big n={len(big):5d} cont {cb*100:4.1f}% mean {mb:+6.1f} | small n={len(small):5d} cont {cs*100:4.1f}% mean {ms:+6.1f} | diff cont {100*(cb-cs):+4.1f}pp [{hlo*100:+.1f},{hhi*100:+.1f}] mean {mb-ms:+5.1f}bp [{lo:+.1f},{hi:+.1f}]")
print("\n=== P2 (post-hoc): paired deferral test on the same breakout signals (N=24, 24h, 10 bp) ===")
print("each V0 signal on a bar > T: immediate = enter at that close; deferred = S-04 path (enter at conversion close, else no trade = 0)")
for lab,(s,e) in (("FULL",FULL),("LAST 24M",R24)):
  for mode in ('pct','c2c1','c2c2'):
    R.thr=lambda i,md,mode=mode: T(i,mode)
    v0,_=R.signals(24,'x',0,s,e)
    pairs=[]
    for i,d in v0:
        if (C[i]-O[i])*d<=T(i,mode) or i+12>=n: continue
        imm=d*math.log(C[i+6]/C[i])*1e4-10
        hi_=max(H[i-24:i]); lo_=min(L[i-24:i]); lvl=hi_ if d>0 else lo_
        j=i+1; carries=0; out=None
        while j<n-6:
            still=(C[j]>lvl) if d>0 else (C[j]<lvl)
            if not still: out=0.0; break
            if (C[j]-O[j])*d>T(j,mode):
                carries+=1
                if carries>=2: out=0.0; break
                j+=1; continue
            out=d*math.log(C[j+6]/C[j])*1e4-10; break
        if out is None: continue
        pairs.append((T_CLOSE[i],imm,out,out!=0.0))
    k=len(pairs); conv=sum(p[3] for p in pairs)
    mi=sum(p[1] for p in pairs)/k; md=sum(p[2] for p in pairs)/k
    lo,hi=wkboot_diff([(p[0],p[2]) for p in pairs],[(p[0],p[1]) for p in pairs])
    dropped=[p[1] for p in pairs if not p[3]]; kept=[p[1] for p in pairs if p[3]]
    print(f"{lab:8} T={mode:5} signals {k} converted {conv} ({conv/k*100:.0f}%) | per signal: immediate {mi:+6.1f}bp, deferred {md:+6.1f}bp, diff {md-mi:+6.1f} [{lo:+.1f},{hi:+.1f}] | immediate outcome of dropped signals {sum(dropped)/max(1,len(dropped)):+6.1f}bp (n={len(dropped)}), of converted {sum(kept)/max(1,len(kept)):+6.1f}bp")
print("\n=== P3 (post-hoc): V0 vs V1 at larger thresholds (N=24, 24h, 10bp) ===")
for lab,(s,e) in (("FULL",FULL),("LAST 24M",R24)):
  for mode in ('c2c1','c2c2'):
    R.thr=lambda i,md,mode=mode: T(i,mode)
    for v in (0,1):
        sig,_=R.signals(24,'x',v,s,e); R.summ(f"{lab} T={mode} V{v}",sig,6,s,e)
print("\n=== U7 (recorded): Binance BTCUSDT funding per settlement, Oct 2 2024 - Oct 4 2026 ===")
s,e=R24
fv=[v for t,v in zip(f_t,f_v) if s<=t<e]
eq1=sum(1 for v in fv if abs(v-1.0)<1e-6); gt=sum(1 for v in fv if v>1.0+1e-6); lt=sum(1 for v in fv if v<-1.0-1e-6)
mid=sum(1 for v in fv if -1.0-1e-6<=v<1.0-1e-6)
print(f"n={len(fv)}: exactly +1.000 bp {eq1} ({eq1/len(fv)*100:.1f}%); above +1 bp {gt} ({gt/len(fv)*100:.1f}%); in [-1,+1) bp {mid} ({mid/len(fv)*100:.1f}%); below -1 bp {lt} ({lt/len(fv)*100:.1f}%); <= +1 bp {len(fv)-gt} ({(len(fv)-gt)/len(fv)*100:.1f}%)")
print("\n=== U6 (recomputed, Parkinson 6-bar including the issue bar) ===")
for lab,(s,e) in (("FULL",FULL),("LAST 24M",R24),("LAST 6M",R6)):
    idx=[i for i in range(44,n-1) if s<=T_CLOSE[i]<e]
    print(lab, len(idx), " | ".join(f"±{k}σ {sum(1 for i in idx if abs(C[i+1]-C[i])<k*P6I[i])/len(idx)*100:.1f}%" for k in (1.0,1.5,2.0)))
print("\n=== containment record 21/27: Wilson 95% ===", [round(x*100,1) for x in jm.wilson(21,27)])
```

## manifest.py

```python
import sys, json, datetime as dt, hashlib
sys.path.insert(0,'/home/claude/pkg/crypto-desk')
import jbm_archive as ja
from concurrent.futures import ThreadPoolExecutor
st,rows,man=ja.load_klines_span(dt.date(2020,1,1), dt.date(2026,10,4), '4h')
def one(d):
    s,r,rep=ja.load_metrics(d); return {"day":d.isoformat(),"entry":ja.manifest_entry(s,rep)}
days=[dt.date(2024,10,1)+dt.timedelta(days=i) for i in range((dt.date(2026,10,4)-dt.date(2024,10,1)).days+1)]
with ThreadPoolExecutor(12) as ex: mets=list(ex.map(one,days))
out={"code_version":ja.VERSION,"klines_4h":{"state":st,"bars":len(rows),"files":man},"metrics":mets}
b=json.dumps(out,sort_keys=True,separators=(",",":")).encode()
open('data_manifest.json','wb').write(b)
print('klines',st,len(rows),len(man),'metrics days',len(mets),'states',{s:sum(1 for m in mets if m['entry'].get('state')==s) for s in set(m['entry'].get('state') for m in mets)},'sha256',hashlib.sha256(b).hexdigest())
```

## Printed output — run.py, run2.py, run3.py (as saved)

```text
bars 14814: 2020-01-01T00:00:00Z -> 2026-10-05T00:00:00Z; OI rows 209376 (ok days 727); funding 7411

=== PRIMARY: N=24, T=0.353% price, 24h horizon, 10bp cost ===
FULL 2020-03..2026-10 V0                       n=1089 (3.17/wk, 633 non-ovl) hit 48.6%  net   +7.4bp  drift-adj   +5.6bp 95%CI [-23,+32] 
FULL 2020-03..2026-10 V1                       n= 514 (1.49/wk, 431 non-ovl) hit 44.0%  net  -21.5bp  drift-adj  -23.1bp 95%CI [-50,+4] 
LAST 24M V0                                    n= 363 (3.47/wk, 210 non-ovl) hit 49.6%  net  -18.6bp  drift-adj  -19.3bp 95%CI [-52,+14] 
LAST 24M V1                                    n= 170 (1.63/wk, 142 non-ovl) hit 45.9%  net  -25.8bp  drift-adj  -26.1bp 95%CI [-65,+13] 
LAST 24M V2                                    n=  84 (0.80/wk, 74 non-ovl) hit 41.7%  net  -23.4bp  drift-adj  -23.3bp 95%CI [-71,+28] (OI-missing bars 2)
LAST 24M V3                                    n=  84 (0.80/wk, 74 non-ovl) hit 41.7%  net  -23.4bp  drift-adj  -23.3bp 95%CI [-71,+28] (OI-missing bars 2)
=== Q1: S-04 directly. After a bar moving > T, return in the move's direction (no cost) ===
FULL     T=pct h= 4h  big moves: n= 8588 cont 44.7% mean   -1.7bp CI[-5,+1] | all bars: n=14447 cont 45.6% mean   -2.0bp CI[-4,-0]
FULL     T=pct h=24h  big moves: n= 8588 cont 47.8% mean   -2.3bp CI[-9,+4] | all bars: n=14447 cont 48.4% mean   -1.8bp CI[-6,+3]
FULL     T=sig h= 4h  big moves: n= 6965 cont 44.7% mean   -0.8bp CI[-4,+2] | all bars: n=14447 cont 45.6% mean   -2.0bp CI[-4,-0]
FULL     T=sig h=24h  big moves: n= 6965 cont 48.0% mean   +1.1bp CI[-6,+8] | all bars: n=14447 cont 48.4% mean   -1.8bp CI[-6,+3]
LAST 24M T=pct h= 4h  big moves: n= 2425 cont 46.4% mean   -0.0bp CI[-5,+5] | all bars: n= 4392 cont 46.6% mean   -0.6bp CI[-3,+2]
LAST 24M T=pct h=24h  big moves: n= 2425 cont 49.1% mean   -2.2bp CI[-11,+8] | all bars: n= 4392 cont 49.4% mean   +1.3bp CI[-5,+8]
LAST 24M T=sig h= 4h  big moves: n= 2184 cont 46.6% mean   +0.8bp CI[-3,+5] | all bars: n= 4392 cont 46.6% mean   -0.6bp CI[-3,+2]
LAST 24M T=sig h=24h  big moves: n= 2184 cont 49.4% mean   -1.5bp CI[-11,+8] | all bars: n= 4392 cont 49.4% mean   +1.3bp CI[-5,+8]
LAST 6M  T=pct h= 4h  big moves: n=  551 cont 45.4% mean   -3.3bp CI[-10,+3] | all bars: n= 1098 cont 45.1% mean   -3.2bp CI[-8,+1]
LAST 6M  T=pct h=24h  big moves: n=  551 cont 50.3% mean   +3.7bp CI[-18,+30] | all bars: n= 1098 cont 49.4% mean   +2.2bp CI[-9,+16]
LAST 6M  T=sig h= 4h  big moves: n=  530 cont 45.8% mean   -0.0bp CI[-8,+8] | all bars: n= 1098 cont 45.1% mean   -3.2bp CI[-8,+1]
LAST 6M  T=sig h=24h  big moves: n=  530 cont 50.6% mean   +5.6bp CI[-16,+30] | all bars: n= 1098 cont 49.4% mean   +2.2bp CI[-9,+16]

=== What S-04 removed: breakouts on a >T bar, entered immediately vs deferred outcome (N=24, pct, 24h, 10bp) ===
FULL breakouts on big bars (immediate)         n=1052 (3.06/wk, 623 non-ovl) hit 48.2%  net   +6.5bp  drift-adj   +4.8bp 95%CI [-24,+32] 
FULL breakouts on normal bars                  n=  37 (0.11/wk, 36 non-ovl) hit 59.5%  net  +32.6bp  drift-adj  +28.7bp 95%CI [-55,+112] 
FULL deferred-then-converted                   n= 477 (1.39/wk, 412 non-ovl) hit 42.8%  net  -25.7bp  drift-adj  -27.1bp 95%CI [-56,+2] 
LAST 24M breakouts on big bars (immediate)     n= 342 (3.27/wk, 204 non-ovl) hit 48.8%  net  -21.6bp  drift-adj  -22.2bp 95%CI [-56,+11] 
LAST 24M breakouts on normal bars              n=  21 (0.20/wk, 20 non-ovl) hit 61.9%  net  +29.5bp  drift-adj  +28.4bp 95%CI [-60,+100] 
LAST 24M deferred-then-converted               n= 149 (1.42/wk, 131 non-ovl) hit 43.6%  net  -33.6bp  drift-adj  -33.8bp 95%CI [-74,+10] 

=== Sensitivity grid (secondary; 4 x 2 x 2 cells per sample, multiplicity applies) ===
FULL N=24 T=pct h=4h V0                        n=1089 (3.17/wk, 1089 non-ovl) hit 45.5%  net   -5.0bp  drift-adj   -5.3bp 95%CI [-14,+4] 
FULL N=24 T=pct h=4h V1                        n= 514 (1.49/wk, 514 non-ovl) hit 48.6%  net  -12.3bp  drift-adj  -12.5bp 95%CI [-23,-1] 
FULL N=24 T=pct h=24h V0                       n=1089 (3.17/wk, 633 non-ovl) hit 48.6%  net   +7.4bp  drift-adj   +5.6bp 95%CI [-23,+32] 
FULL N=24 T=pct h=24h V1                       n= 514 (1.49/wk, 431 non-ovl) hit 44.0%  net  -21.5bp  drift-adj  -23.1bp 95%CI [-50,+4] 
FULL N=24 T=sig h=4h V0                        n=1089 (3.17/wk, 1089 non-ovl) hit 45.5%  net   -5.0bp  drift-adj   -5.3bp 95%CI [-14,+4] 
FULL N=24 T=sig h=4h V1                        n= 539 (1.57/wk, 539 non-ovl) hit 48.6%  net  -11.8bp  drift-adj  -12.1bp 95%CI [-23,-2] 
FULL N=24 T=sig h=24h V0                       n=1089 (3.17/wk, 633 non-ovl) hit 48.6%  net   +7.4bp  drift-adj   +5.6bp 95%CI [-23,+32] 
FULL N=24 T=sig h=24h V1                       n= 539 (1.57/wk, 447 non-ovl) hit 43.4%  net  -22.4bp  drift-adj  -24.0bp 95%CI [-52,+3] 
FULL N=42 T=pct h=4h V0                        n= 786 (2.28/wk, 786 non-ovl) hit 46.8%  net   -3.3bp  drift-adj   -3.6bp 95%CI [-14,+7] 
FULL N=42 T=pct h=4h V1                        n= 362 (1.05/wk, 362 non-ovl) hit 48.6%  net   -7.7bp  drift-adj   -8.0bp 95%CI [-22,+6] 
FULL N=42 T=pct h=24h V0                       n= 786 (2.28/wk, 458 non-ovl) hit 49.5%  net  +19.4bp  drift-adj  +17.3bp 95%CI [-17,+50] 
FULL N=42 T=pct h=24h V1                       n= 362 (1.05/wk, 308 non-ovl) hit 43.4%  net  -10.9bp  drift-adj  -12.8bp 95%CI [-49,+23] 
FULL N=42 T=sig h=4h V0                        n= 786 (2.28/wk, 786 non-ovl) hit 46.8%  net   -3.3bp  drift-adj   -3.6bp 95%CI [-14,+7] 
FULL N=42 T=sig h=4h V1                        n= 378 (1.10/wk, 378 non-ovl) hit 49.7%  net   -7.3bp  drift-adj   -7.6bp 95%CI [-21,+6] 
FULL N=42 T=sig h=24h V0                       n= 786 (2.28/wk, 458 non-ovl) hit 49.5%  net  +19.4bp  drift-adj  +17.3bp 95%CI [-17,+50] 
FULL N=42 T=sig h=24h V1                       n= 378 (1.10/wk, 319 non-ovl) hit 42.9%  net  -11.6bp  drift-adj  -13.5bp 95%CI [-49,+22] 
LAST 24M N=24 T=pct h=4h V0                    n= 363 (3.47/wk, 363 non-ovl) hit 45.2%  net  -15.0bp  drift-adj  -15.1bp 95%CI [-26,-4] 
LAST 24M N=24 T=pct h=4h V1                    n= 170 (1.63/wk, 170 non-ovl) hit 44.7%  net  -24.5bp  drift-adj  -24.6bp 95%CI [-38,-13] 
LAST 24M N=24 T=pct h=24h V0                   n= 363 (3.47/wk, 210 non-ovl) hit 49.6%  net  -18.6bp  drift-adj  -19.3bp 95%CI [-52,+14] 
LAST 24M N=24 T=pct h=24h V1                   n= 170 (1.63/wk, 142 non-ovl) hit 45.9%  net  -25.8bp  drift-adj  -26.1bp 95%CI [-65,+13] 
LAST 24M N=24 T=sig h=4h V0                    n= 363 (3.47/wk, 363 non-ovl) hit 45.2%  net  -15.0bp  drift-adj  -15.1bp 95%CI [-26,-4] 
LAST 24M N=24 T=sig h=4h V1                    n= 181 (1.73/wk, 181 non-ovl) hit 45.3%  net  -21.3bp  drift-adj  -21.3bp 95%CI [-35,-9] 
LAST 24M N=24 T=sig h=24h V0                   n= 363 (3.47/wk, 210 non-ovl) hit 49.6%  net  -18.6bp  drift-adj  -19.3bp 95%CI [-52,+14] 
LAST 24M N=24 T=sig h=24h V1                   n= 181 (1.73/wk, 148 non-ovl) hit 47.0%  net  -16.0bp  drift-adj  -16.3bp 95%CI [-57,+26] 
LAST 24M N=42 T=pct h=4h V0                    n= 254 (2.43/wk, 254 non-ovl) hit 46.5%  net  -12.3bp  drift-adj  -12.5bp 95%CI [-25,+0] 
LAST 24M N=42 T=pct h=4h V1                    n= 112 (1.07/wk, 112 non-ovl) hit 44.6%  net  -18.5bp  drift-adj  -18.6bp 95%CI [-33,-4] 
LAST 24M N=42 T=pct h=24h V0                   n= 254 (2.43/wk, 145 non-ovl) hit 49.2%  net  -18.6bp  drift-adj  -19.4bp 95%CI [-63,+23] 
LAST 24M N=42 T=pct h=24h V1                   n= 112 (1.07/wk, 96 non-ovl) hit 46.4%  net  -18.1bp  drift-adj  -18.5bp 95%CI [-71,+34] 
LAST 24M N=42 T=sig h=4h V0                    n= 254 (2.43/wk, 254 non-ovl) hit 46.5%  net  -12.3bp  drift-adj  -12.5bp 95%CI [-25,+0] 
LAST 24M N=42 T=sig h=4h V1                    n= 117 (1.12/wk, 117 non-ovl) hit 47.0%  net  -16.4bp  drift-adj  -16.4bp 95%CI [-32,-2] 
LAST 24M N=42 T=sig h=24h V0                   n= 254 (2.43/wk, 145 non-ovl) hit 49.2%  net  -18.6bp  drift-adj  -19.4bp 95%CI [-63,+23] 
LAST 24M N=42 T=sig h=24h V1                   n= 117 (1.12/wk, 100 non-ovl) hit 46.2%  net  -10.5bp  drift-adj  -10.8bp 95%CI [-70,+52] 
LAST 6M N=24 T=pct h=4h V0                     n=  84 (3.21/wk, 84 non-ovl) hit 44.0%  net  -19.3bp  drift-adj  -19.9bp 95%CI [-39,-0] 
LAST 6M N=24 T=pct h=4h V1                     n=  45 (1.72/wk, 45 non-ovl) hit 48.9%  net  -14.5bp  drift-adj  -14.9bp 95%CI [-32,+2] 
LAST 6M N=24 T=pct h=24h V0                    n=  84 (3.21/wk, 52 non-ovl) hit 50.0%  net   +0.7bp  drift-adj   -3.0bp 95%CI [-77,+79] 
LAST 6M N=24 T=pct h=24h V1                    n=  45 (1.72/wk, 37 non-ovl) hit 51.1%  net  +29.1bp  drift-adj  +27.1bp 95%CI [-59,+121] 
LAST 6M N=24 T=sig h=4h V0                     n=  84 (3.21/wk, 84 non-ovl) hit 44.0%  net  -19.3bp  drift-adj  -19.9bp 95%CI [-39,-0] 
LAST 6M N=24 T=sig h=4h V1                     n=  47 (1.80/wk, 47 non-ovl) hit 48.9%  net   -8.5bp  drift-adj   -8.9bp 95%CI [-29,+14] 
LAST 6M N=24 T=sig h=24h V0                    n=  84 (3.21/wk, 52 non-ovl) hit 50.0%  net   +0.7bp  drift-adj   -3.0bp 95%CI [-77,+79] 
LAST 6M N=24 T=sig h=24h V1                    n=  47 (1.80/wk, 37 non-ovl) hit 48.9%  net  +37.9bp  drift-adj  +35.4bp 95%CI [-64,+147] 
LAST 6M N=42 T=pct h=4h V0                     n=  60 (2.30/wk, 60 non-ovl) hit 41.7%  net  -17.4bp  drift-adj  -18.1bp 95%CI [-41,+5] 
LAST 6M N=42 T=pct h=4h V1                     n=  31 (1.19/wk, 31 non-ovl) hit 54.8%  net   -9.7bp  drift-adj  -10.2bp 95%CI [-33,+11] 
LAST 6M N=42 T=pct h=24h V0                    n=  60 (2.30/wk, 38 non-ovl) hit 48.3%  net  +21.5bp  drift-adj  +17.2bp 95%CI [-84,+127] 
LAST 6M N=42 T=pct h=24h V1                    n=  31 (1.19/wk, 26 non-ovl) hit 48.4%  net  +60.2bp  drift-adj  +57.3bp 95%CI [-59,+180] 
LAST 6M N=42 T=sig h=4h V0                     n=  60 (2.30/wk, 60 non-ovl) hit 41.7%  net  -17.4bp  drift-adj  -18.1bp 95%CI [-41,+5] 
LAST 6M N=42 T=sig h=4h V1                     n=  32 (1.22/wk, 32 non-ovl) hit 56.2%  net   -3.9bp  drift-adj   -4.4bp 95%CI [-32,+23] 
LAST 6M N=42 T=sig h=24h V0                    n=  60 (2.30/wk, 38 non-ovl) hit 48.3%  net  +21.5bp  drift-adj  +17.2bp 95%CI [-84,+127] 
LAST 6M N=42 T=sig h=24h V1                    n=  32 (1.22/wk, 26 non-ovl) hit 46.9%  net  +77.9bp  drift-adj  +74.6bp 95%CI [-63,+216] 
max rel diff hand sigma vs jm.sd_c2c (sampled): 3.9755014737176005e-16
FULL share of bars > 0.5*park6: 0.488
FULL N=24 T=0.5*park6 h=24h V0                 n=1089 (3.17/wk, 633 non-ovl) hit 48.6%  net   +7.4bp  drift-adj   +5.6bp 95%CI [-23,+32] 
FULL N=24 T=0.5*park6 h=24h V1                 n= 559 (1.62/wk, 452 non-ovl) hit 43.3%  net  -23.3bp  drift-adj  -25.0bp 95%CI [-54,+5] 
LAST 24M share of bars > 0.5*park6: 0.509
LAST 24M N=24 T=0.5*park6 h=24h V0             n= 363 (3.47/wk, 210 non-ovl) hit 49.6%  net  -18.6bp  drift-adj  -19.3bp 95%CI [-52,+14] 
LAST 24M N=24 T=0.5*park6 h=24h V1             n= 184 (1.76/wk, 149 non-ovl) hit 44.6%  net  -28.6bp  drift-adj  -29.1bp 95%CI [-74,+14] 

=== naive containment: next 4H close within +/-h of the current close ===
FULL     n=14448: ±0.50% 51.8% [51.0,52.6] | ±0.60% 58.1% [57.3,58.9] | ±0.75% 65.4% [64.6,66.2] | ±0.90% 71.3% [70.5,72.0] | ±1.00% 74.4% [73.7,75.1] | ±1.25% 80.9% [80.2,81.5]
         operative-σ bands (Parkinson 6-bar at issue): ±1.0σp6 76.0% | ±1.5σp6 87.4% | ±2.0σp6 92.8%
LAST 24M n=4392: ±0.50% 56.9% [55.5,58.4] | ±0.60% 64.3% [62.8,65.7] | ±0.75% 72.1% [70.8,73.4] | ±0.90% 78.2% [77.0,79.4] | ±1.00% 81.0% [79.8,82.1] | ±1.25% 87.1% [86.0,88.0]
         operative-σ bands (Parkinson 6-bar at issue): ±1.0σp6 74.5% | ±1.5σp6 86.8% | ±2.0σp6 92.3%
LAST 6M  n=1098: ±0.50% 61.8% [58.9,64.7] | ±0.60% 68.9% [66.1,71.6] | ±0.75% 78.0% [75.4,80.3] | ±0.90% 83.4% [81.1,85.5] | ±1.00% 86.0% [83.8,87.9] | ±1.25% 91.2% [89.3,92.7]
         operative-σ bands (Parkinson 6-bar at issue): ±1.0σp6 75.0% | ±1.5σp6 87.7% | ±2.0σp6 92.9%
```

## Printed output — run4.py (post hoc)

```text
=== P1 (post-hoc): continuation after bars > T vs bars <= T (complement), in the bar's direction, no cost ===
FULL     T=pct    h= 4h big n= 8588 cont 44.7% mean   -1.7 | small n= 5859 cont 46.9% mean   -2.3 | diff cont -2.3pp [-3.7,-0.7] mean  +0.6bp [-3.1,+4.5]
FULL     T=pct    h=24h big n= 8588 cont 47.8% mean   -2.3 | small n= 5859 cont 49.2% mean   -1.1 | diff cont -1.3pp [-3.0,+0.3] mean  -1.2bp [-10.2,+7.5]
FULL     T=c2c0.5 h= 4h big n= 7020 cont 44.7% mean   -0.9 | small n= 7427 cont 46.4% mean   -2.9 | diff cont -1.7pp [-3.2,-0.1] mean  +2.0bp [-2.0,+6.0]
FULL     T=c2c0.5 h=24h big n= 7020 cont 48.0% mean   +0.8 | small n= 7427 cont 48.7% mean   -4.2 | diff cont -0.7pp [-2.3,+0.9] mean  +5.0bp [-4.4,+14.4]
FULL     T=p6_0.5 h= 4h big n= 7268 cont 44.9% mean   -1.0 | small n= 7179 cont 46.3% mean   -2.9 | diff cont -1.5pp [-3.0,+0.2] mean  +1.9bp [-1.8,+5.5]
FULL     T=p6_0.5 h=24h big n= 7268 cont 47.9% mean   +0.3 | small n= 7179 cont 48.9% mean   -3.9 | diff cont -1.0pp [-2.7,+0.7] mean  +4.3bp [-5.2,+13.6]
FULL     T=c2c1   h= 4h big n= 3340 cont 45.2% mean   -0.2 | small n=11107 cont 45.7% mean   -2.5 | diff cont -0.5pp [-2.3,+1.6] mean  +2.3bp [-2.3,+6.9]
FULL     T=c2c1   h=24h big n= 3340 cont 47.5% mean   +1.9 | small n=11107 cont 48.7% mean   -2.9 | diff cont -1.2pp [-3.0,+0.7] mean  +4.7bp [-7.5,+17.2]
FULL     T=c2c2   h= 4h big n=  909 cont 49.4% mean   +8.3 | small n=13538 cont 45.3% mean   -2.7 | diff cont +4.1pp [+0.8,+7.1] mean +11.0bp [+1.9,+20.5]
FULL     T=c2c2   h=24h big n=  909 cont 50.7% mean  +16.4 | small n=13538 cont 48.2% mean   -3.0 | diff cont +2.5pp [-1.1,+6.0] mean +19.4bp [-7.0,+47.0]
LAST 24M T=pct    h= 4h big n= 2425 cont 46.4% mean   -0.0 | small n= 1967 cont 46.8% mean   -1.4 | diff cont -0.3pp [-3.1,+2.5] mean  +1.4bp [-4.5,+7.7]
LAST 24M T=pct    h=24h big n= 2425 cont 49.1% mean   -2.2 | small n= 1967 cont 49.7% mean   +5.5 | diff cont -0.6pp [-3.5,+2.4] mean  -7.7bp [-20.6,+5.7]
LAST 24M T=c2c0.5 h= 4h big n= 2198 cont 46.5% mean   +0.6 | small n= 2194 cont 46.7% mean   -1.9 | diff cont -0.2pp [-2.8,+2.5] mean  +2.4bp [-2.7,+7.6]
LAST 24M T=c2c0.5 h=24h big n= 2198 cont 49.3% mean   -2.2 | small n= 2194 cont 49.4% mean   +4.8 | diff cont -0.1pp [-2.8,+2.8] mean  -7.0bp [-19.1,+6.2]
LAST 24M T=p6_0.5 h= 4h big n= 2312 cont 46.5% mean   +1.0 | small n= 2080 cont 46.6% mean   -2.5 | diff cont -0.1pp [-3.2,+3.0] mean  +3.5bp [-2.1,+8.9]
LAST 24M T=p6_0.5 h=24h big n= 2312 cont 49.8% mean   +1.6 | small n= 2080 cont 48.8% mean   +1.0 | diff cont +1.0pp [-1.9,+3.9] mean  +0.6bp [-11.6,+14.0]
LAST 24M T=c2c1   h= 4h big n= 1063 cont 47.7% mean   +0.2 | small n= 3329 cont 46.2% mean   -0.9 | diff cont +1.5pp [-2.0,+4.8] mean  +1.1bp [-4.7,+7.1]
LAST 24M T=c2c1   h=24h big n= 1063 cont 49.9% mean   -1.8 | small n= 3329 cont 49.2% mean   +2.2 | diff cont +0.7pp [-2.6,+3.8] mean  -4.0bp [-16.9,+9.1]
LAST 24M T=c2c2   h= 4h big n=  272 cont 47.1% mean   -3.3 | small n= 4120 cont 46.6% mean   -0.5 | diff cont +0.5pp [-5.8,+6.6] mean  -2.8bp [-14.8,+9.9]
LAST 24M T=c2c2   h=24h big n=  272 cont 49.6% mean  -17.4 | small n= 4120 cont 49.3% mean   +2.5 | diff cont +0.3pp [-6.2,+6.8] mean -20.0bp [-56.7,+16.0]

=== P2 (post-hoc): paired deferral test on the same breakout signals (N=24, 24h, 10 bp) ===
each V0 signal on a bar > T: immediate = enter at that close; deferred = S-04 path (enter at conversion close, else no trade = 0)
FULL     T=pct   signals 1052 converted 655 (62%) | per signal: immediate   +6.5bp, deferred   -7.3bp, diff  -13.8 [-35.2,+7.2] | immediate outcome of dropped signals   +8.6bp (n=397), of converted   +5.2bp
FULL     T=c2c1  signals 847 converted 613 (72%) | per signal: immediate   +5.2bp, deferred   -7.7bp, diff  -12.8 [-33.2,+7.5] | immediate outcome of dropped signals  -36.0bp (n=234), of converted  +20.9bp
FULL     T=c2c2  signals 449 converted 384 (86%) | per signal: immediate  +15.8bp, deferred   +0.9bp, diff  -14.9 [-36.6,+5.9] | immediate outcome of dropped signals -110.5bp (n=65), of converted  +37.2bp
LAST 24M T=pct   signals 342 converted 208 (61%) | per signal: immediate  -21.6bp, deferred  -19.3bp, diff   +2.3 [-21.6,+25.5] | immediate outcome of dropped signals  -14.4bp (n=134), of converted  -26.2bp
LAST 24M T=c2c1  signals 264 converted 192 (73%) | per signal: immediate  -28.9bp, deferred  -12.2bp, diff  +16.7 [-4.4,+38.4] | immediate outcome of dropped signals -107.8bp (n=72), of converted   +0.7bp
LAST 24M T=c2c2  signals 132 converted 110 (83%) | per signal: immediate  -44.9bp, deferred  -30.0bp, diff  +14.8 [-14.0,+41.1] | immediate outcome of dropped signals -106.1bp (n=22), of converted  -32.6bp

=== P3 (post-hoc): V0 vs V1 at larger thresholds (N=24, 24h, 10bp) ===
FULL T=c2c1 V0                                 n=1089 (3.17/wk, 633 non-ovl) hit 48.6%  net   +7.4bp  drift-adj   +5.6bp 95%CI [-23,+32] 
FULL T=c2c1 V1                                 n= 667 (1.94/wk, 498 non-ovl) hit 45.3%  net  -14.9bp  drift-adj  -16.8bp 95%CI [-45,+9] 
FULL T=c2c2 V0                                 n=1089 (3.17/wk, 633 non-ovl) hit 48.6%  net   +7.4bp  drift-adj   +5.6bp 95%CI [-23,+32] 
FULL T=c2c2 V1                                 n= 903 (2.62/wk, 593 non-ovl) hit 45.6%  net   -3.6bp  drift-adj   -5.6bp 95%CI [-33,+20] 
LAST 24M T=c2c1 V0                             n= 363 (3.47/wk, 210 non-ovl) hit 49.6%  net  -18.6bp  drift-adj  -19.3bp 95%CI [-52,+14] 
LAST 24M T=c2c1 V1                             n= 228 (2.18/wk, 165 non-ovl) hit 50.0%  net   -2.7bp  drift-adj   -3.5bp 95%CI [-41,+32] 
LAST 24M T=c2c2 V0                             n= 363 (3.47/wk, 210 non-ovl) hit 49.6%  net  -18.6bp  drift-adj  -19.3bp 95%CI [-52,+14] 
LAST 24M T=c2c2 V1                             n= 303 (2.90/wk, 195 non-ovl) hit 48.5%  net   -5.6bp  drift-adj   -6.4bp 95%CI [-44,+29] 

=== U7 (recorded): Binance BTCUSDT funding per settlement, Oct 2 2024 - Oct 4 2026 ===
n=2196: exactly +1.000 bp 403 (18.4%); above +1 bp 57 (2.6%); in [-1,+1) bp 1727 (78.6%); below -1 bp 9 (0.4%); <= +1 bp 2139 (97.4%)

=== U6 (recomputed, Parkinson 6-bar including the issue bar) ===
FULL 14448 ±1.0σ 76.4% | ±1.5σ 87.8% | ±2.0σ 93.1%
LAST 24M 4392 ±1.0σ 74.7% | ±1.5σ 87.3% | ±2.0σ 92.9%
LAST 6M 1098 ±1.0σ 74.8% | ±1.5σ 88.0% | ±2.0σ 93.1%

=== containment record 21/27: Wilson 95% === [59.2, 89.4]
```
