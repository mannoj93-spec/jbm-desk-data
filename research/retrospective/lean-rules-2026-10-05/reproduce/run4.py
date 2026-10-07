"""POST-HOC additions (written Oct 6 ~01:30Z, after the primary results and the independent review).
Not part of SPEC.md. Labelled post-hoc wherever cited."""
import sys; sys.path.insert(0,'/root/in29/crypto-desk')
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
