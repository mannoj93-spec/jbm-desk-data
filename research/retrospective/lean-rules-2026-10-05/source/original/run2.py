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
