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


# ---- lab-2.0: interval-based overlap and dependence blocks --------------------------------------
def nonoverlap_intervals(items):
    """Deterministic chronological thinning on ACTUAL label intervals [entry_t, exit_t).

    Items are sorted by (entry_t, t_event, event_id) - never by outcome - and an item is kept only
    if its entry is at or after the exit of the last kept item. Touching intervals (next entry ==
    previous exit) share one price print but no return and are both kept. Two decisions that enter
    at the same executable bar have identical intervals, so only the first is kept. Returns
    (kept, dropped_count). Non-overlap does NOT make observations statistically independent;
    dependence is handled by the blocks below."""
    kept, last_exit = [], None
    for it in sorted(items, key=lambda x: (x["entry_t"], x.get("t_event", 0), x.get("event_id", ""))):
        if last_exit is None or it["entry_t"] >= last_exit:
            kept.append(it)
            last_exit = it["exit_t"]
    return kept, len(items) - len(kept)


def dependence_blocks(items, block_ms=DAY):
    """Assign a block id to every item: items are in one block when their label intervals overlap
    (strictly) or their entries fall in the same UTC day (volatility clustering makes same-day
    outcomes dependent even without overlap), chained transitively across groups. Returns the
    number of blocks; each item gets item['block']."""
    order = sorted(range(len(items)), key=lambda i: (items[i]["entry_t"], items[i]["exit_t"]))
    block, cur_end, cur_day = -1, None, None
    for i in order:
        it = items[i]
        day = it["entry_t"] // block_ms
        if cur_end is None or not (it["entry_t"] < cur_end or day == cur_day):
            block += 1
            cur_end = it["exit_t"]
        else:
            cur_end = max(cur_end, it["exit_t"])
        cur_day = day
        it["block"] = block
    return block + 1


def block_bootstrap(test, ref, alphas=(0.10,), reps=2000, seed=7):
    """Intervals for mean(test.y) - mean(ref.y), resampling whole dependence blocks jointly.
    `test`/`ref` items carry 'block' and 'y'. Returns {alpha: (lo, hi)} or None when fewer than 2
    blocks hold each group."""
    blocks = sorted({x["block"] for x in test} | {x["block"] for x in ref})
    tb = {}
    for x in test:
        tb.setdefault(x["block"], [0.0, 0])
        tb[x["block"]][0] += x["y"]
        tb[x["block"]][1] += 1
    rb = {}
    for x in ref:
        rb.setdefault(x["block"], [0.0, 0])
        rb[x["block"]][0] += x["y"]
        rb[x["block"]][1] += 1
    if len(tb) < 2 or len(rb) < 2:
        return None
    rng = random.Random(seed)
    diffs = []
    for _ in range(reps):
        ts = tn = rs = rn = 0
        for _ in blocks:
            b = blocks[rng.randrange(len(blocks))]
            if b in tb:
                ts += tb[b][0]
                tn += tb[b][1]
            if b in rb:
                rs += rb[b][0]
                rn += rb[b][1]
        if tn and rn:
            diffs.append(ts / tn - rs / rn)
    if len(diffs) < reps // 2:
        return None
    return {a: (quantile(diffs, a / 2), quantile(diffs, 1 - a / 2)) for a in alphas}
