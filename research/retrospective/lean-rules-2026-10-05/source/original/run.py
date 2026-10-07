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
