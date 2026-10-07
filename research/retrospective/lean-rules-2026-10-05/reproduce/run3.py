import sys; sys.path.insert(0,'/root/in29/crypto-desk')
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
