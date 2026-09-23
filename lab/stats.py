"""Small, dependency-free statistics for dependent, overlapping financial samples.

Nothing here produces a p-value or a significance claim. Intervals are descriptive: a day-block
bootstrap (resampling whole UTC days of independent episodes, fixed seed) so that episodes sharing
a day are not treated as independent, and every result reports how many variants its family has
tested (multiple-testing exposure).
"""
import math
import random

DAY = 86_400_000


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def quantile(xs, q):
    if not xs:
        return None
    s = sorted(xs)
    pos = q * (len(s) - 1)
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def describe(xs):
    if not xs:
        return {"n": 0}
    return {"n": len(xs), "mean": mean(xs), "median": quantile(xs, 0.5), "q10": quantile(xs, 0.1),
            "q90": quantile(xs, 0.9), "share_positive": sum(1 for x in xs if x > 0) / len(xs)}


def block_bootstrap_diff(a, b, reps=1000, seed=7):
    """90% interval for mean(a) - mean(b), where a and b are lists of (t_ms, value); UTC days are
    resampled as blocks, jointly for both groups. Returns None when either side has < 2 days."""
    days = sorted({t // DAY for t, _ in a} | {t // DAY for t, _ in b})
    by_a, by_b = {}, {}
    for t, v in a:
        by_a.setdefault(t // DAY, []).append(v)
    for t, v in b:
        by_b.setdefault(t // DAY, []).append(v)
    if len({t // DAY for t, _ in a}) < 2 or len({t // DAY for t, _ in b}) < 2:
        return None
    rng = random.Random(seed)
    stats = []
    for _ in range(reps):
        pick = [rng.choice(days) for _ in days]
        xa = [v for d in pick for v in by_a.get(d, [])]
        xb = [v for d in pick for v in by_b.get(d, [])]
        if xa and xb:
            stats.append(mean(xa) - mean(xb))
    if len(stats) < reps // 2:
        return None
    return {"lo90": quantile(stats, 0.05), "hi90": quantile(stats, 0.95), "reps": len(stats), "block": "UTC day"}


def ols(X, y):
    """Least squares via normal equations (small k). Returns coefficients or None if singular."""
    k = len(X[0])
    A = [[sum(r[i] * r[j] for r in X) for j in range(k)] for i in range(k)]
    v = [sum(r[i] * yy for r, yy in zip(X, y)) for i in range(k)]
    for i in range(k):                                  # Gauss-Jordan with partial pivoting
        p = max(range(i, k), key=lambda r: abs(A[r][i]))
        if abs(A[p][i]) < 1e-12:
            return None
        A[i], A[p], v[i], v[p] = A[p], A[i], v[p], v[i]
        for r in range(k):
            if r != i:
                f = A[r][i] / A[i][i]
                A[r] = [a - f * b for a, b in zip(A[r], A[i])]
                v[r] -= f * v[i]
    return [v[i] / A[i][i] for i in range(k)]


def residualize(controls, events, keys):
    """Fit outcome ~ 1 + keys on control observations, return event residuals (outcome - fit).
    Measures what an event adds beyond the simple baseline predictors. None if underdetermined."""
    rows = [c for c in controls if all(c.get(k) is not None for k in keys) and c.get("y") is not None]
    if len(rows) < 5 * (len(keys) + 1):
        return None, None
    beta = ols([[1.0] + [r[k] for k in keys] for r in rows], [r["y"] for r in rows])
    if beta is None:
        return None, None
    res = []
    for e in events:
        if all(e.get(k) is not None for k in keys) and e.get("y") is not None:
            res.append((e["t"], e["y"] - beta[0] - sum(b * e[k] for b, k in zip(beta[1:], keys))))
    return res, beta


def nonoverlap(items, horizon_ms):
    """Greedy chronological thinning so no two kept outcomes overlap in time."""
    kept, last = [], None
    for it in sorted(items, key=lambda x: x["t"]):
        if last is None or it["t"] >= last + horizon_ms:
            kept.append(it)
            last = it["t"]
    return kept
