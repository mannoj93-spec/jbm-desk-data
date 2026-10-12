"""O34 v1 runner — tight close-basis exits against the R-09 stop alone.

Implements research/o34/protocol.json (frozen; sha256 checked at start). Written after the freeze.
Usage (from the package root):  python3 research/o34/run_o34.py [--cache rows.json] > out.txt
Writes research/o34/results_v1.json.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
import jbm_archive as ja  # noqa: E402
import jbm_measure as jm  # noqa: E402
import range_contract as rc  # noqa: E402

PROTOCOL_SHA256 = "8b7fb0f1dc295b8aaed11bd746e7672f6a2304213ffd37df7178727ed3adc2c4"
KS = (0.7, 1.0, 1.5)
HS = (2, 6, 18)
PRIMARY = (0.7, 6)
STOP_SIGMA = 2.0
FEE_BP_SIDE = 4.0
TICK = 0.1
WARMUP = 42
RESAMPLES = 10_000
SEED = 20261012
STEP_MS = 4 * 3600 * 1000
PERIODS = {
    "pre": ("2023-09-23T00:00:00Z", "2024-09-23T00:00:00Z"),
    "validation": ("2024-09-23T00:00:00Z", "2025-09-23T00:00:00Z"),
    "holdout": ("2025-09-23T00:00:00Z", "2026-09-23T00:00:00Z"),
}


def _ts(s: str) -> int:
    return int(dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() * 1000)


def check_protocol():
    h = hashlib.sha256((HERE / "protocol.json").read_bytes()).hexdigest()
    if h != PROTOCOL_SHA256:
        raise SystemExit(f"protocol hash mismatch: {h}")
    return h


def load(cache: str | None):
    if cache and Path(cache).exists():
        blob = json.loads(Path(cache).read_text())
        return blob["rows"], blob["manifest"], blob["worst"]
    worst, rows, manifest = ja.load_klines_span(dt.date(2023, 8, 1), dt.date(2026, 9, 30), "4h")
    if cache:
        Path(cache).write_text(json.dumps({"rows": rows, "manifest": manifest, "worst": worst}))
    return rows, manifest, worst


def prepare(rows, manifest):
    bad = {m["sha256"] for m in manifest if m.get("state") != "ok"}
    keep = {}
    for r in rows:
        if r.get("source_sha256") in bad:
            continue
        keep[_ts(r["open_utc"])] = r
    t = sorted(keep)
    o = np.array([keep[x]["open"] for x in t], float)
    h = np.array([keep[x]["high"] for x in t], float)
    lo = np.array([keep[x]["low"] for x in t], float)
    c = np.array([keep[x]["close"] for x in t], float)
    t = np.array(t, np.int64)
    contig = np.zeros(len(t), bool)            # contig[i]: bar i follows bar i-1 by exactly 4h
    contig[1:] = (t[1:] - t[:-1]) == STEP_MS
    return t, o, h, lo, c, contig, len(bad)


def sigmas(h, lo):
    sig = np.full(len(h), np.nan)
    for i in range(5, len(h)):
        sig[i] = jm.sd_parkinson(list(h[i - 5:i + 1]), list(lo[i - 5:i + 1]), name="sd_parkinson_4h_6",
                                 min_bars=6).value
    return sig


def eligible(i, H, n, contig, sig):
    if i - WARMUP + 1 < 0 or i + H >= n:
        return False
    if not contig[i - WARMUP + 2:i + H + 1].all():
        return False
    return bool(np.isfinite(sig[i]) and sig[i] > 0)


def simulate(i, d, k, H, o, h, lo, c, sig, rule_b):
    p0 = c[i]
    s = p0 * math.exp(-d * STOP_SIGMA * sig[i])
    x = p0 * math.exp(-d * k * sig[i])
    for j in range(1, H + 1):
        b = i + j
        if d > 0 and lo[b] <= s:
            ex = s if o[b] > s else o[b]
            return ex, j, "stop"
        if d < 0 and h[b] >= s:
            ex = s if o[b] < s else o[b]
            return ex, j, "stop"
        if rule_b and j < H and ((d > 0 and c[b] <= x) or (d < 0 and c[b] >= x)):
            return c[b], j, "close_exit"
    return c[i + H], H, "horizon"


def net_bp(d, p0, ex):
    return 1e4 * d * math.log(ex / p0) - 2 * FEE_BP_SIDE - 2 * 1e4 * TICK / p0


def stationary_bootstrap(x, mean_block, reps, seed):
    rng = np.random.default_rng(seed)
    n = len(x)
    p = 1.0 / mean_block
    idx = np.empty((reps, n), np.int64)
    idx[:, 0] = rng.integers(0, n, reps)
    jump = rng.random((reps, n)) < p
    fresh = rng.integers(0, n, (reps, n))
    for j in range(1, n):
        idx[:, j] = np.where(jump[:, j], fresh[:, j], (idx[:, j - 1] + 1) % n)
    return x[idx].mean(axis=1)


def summarize(vals):
    a = np.array(vals, float)
    return {"mean": round(float(a.mean()), 2), "median": round(float(np.median(a)), 2),
            "p05": round(float(np.percentile(a, 5)), 2)} if len(a) else None


def run(cache=None):
    proto = check_protocol()
    rows, manifest, worst = load(cache)
    t, o, h, lo, c, contig, nbad = prepare(rows, manifest)
    sig = sigmas(h, lo)
    n = len(t)
    close_ms = t + STEP_MS
    out = {"protocol_sha256": proto, "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "run_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "data": {"bars": int(n), "files": len(manifest), "files_not_ok": nbad, "worst_state": worst,
                    "first_open": rows and min(r["open_utc"] for r in rows), "last_open": rows and max(r["open_utc"] for r in rows),
                    "manifest": manifest},
           "variants": {}}
    pvals_val = {}
    for k in KS:
        for H in HS:
            name = f"k{k}_H{H}"
            res = {}
            for per, (a, b) in PERIODS.items():
                a_ms, b_ms = _ts(a), _ts(b)
                D, RA, RB, dirs = [], [], [], {1: [], -1: []}
                fired = blocked = trades = 0
                excluded = 0
                for i in range(n):
                    if not (a_ms <= close_ms[i] and i + H < n and close_ms[min(i + H, n - 1)] <= b_ms):
                        continue
                    if not eligible(i, H, n, contig, sig):
                        excluded += 1
                        continue
                    dt_vals = []
                    for d in (1, -1):
                        ea, ja_, wa = simulate(i, d, k, H, o, h, lo, c, sig, False)
                        eb, jb, wb = simulate(i, d, k, H, o, h, lo, c, sig, True)
                        ra, rb = net_bp(d, c[i], ea), net_bp(d, c[i], eb)
                        RA.append(ra); RB.append(rb); trades += 1
                        if wb == "close_exit":
                            fired += 1
                            if ra > rb:
                                blocked += 1
                        dt_vals.append(rb - ra)
                        dirs[d].append(rb - ra)
                    D.append(sum(dt_vals) / 2)
                Darr = np.array(D, float)
                boot = stationary_bootstrap(Darr, max(H, 6), RESAMPLES, SEED) if len(Darr) else np.array([0.0])
                lo95, hi95 = np.percentile(boot, [2.5, 97.5])
                p = min(1.0, 2 * min(float((boot <= 0).mean()), float((boot >= 0).mean())))
                res[per] = {"decision_times": len(D), "excluded": excluded, "trades": trades,
                            "mean_D_bp": round(float(Darr.mean()), 3) if len(D) else None,
                            "ci95_bp": [round(float(lo95), 3), round(float(hi95), 3)], "p_two_sided": round(p, 5),
                            "early_exit_rate": round(fired / trades, 4) if trades else None,
                            "blocked_recovery_share_of_fired": round(blocked / fired, 4) if fired else None,
                            "R_A": summarize(RA), "R_B": summarize(RB),
                            "mean_D_long_bp": round(float(np.mean(dirs[1])), 3) if dirs[1] else None,
                            "mean_D_short_bp": round(float(np.mean(dirs[-1])), 3) if dirs[-1] else None}
                if per == "validation":
                    pvals_val[name] = p
            out["variants"][name] = res
    holm = rc.holm(pvals_val)
    for name, adj in holm.items():
        out["variants"][name]["validation"]["p_holm"] = round(adj, 5)
    pv = out["variants"][f"k{PRIMARY[0]}_H{PRIMARY[1]}"]
    v, ho = pv["validation"], pv["holdout"]
    excl0 = lambda r: r["ci95_bp"][0] > 0 or r["ci95_bp"][1] < 0  # noqa: E731
    if not excl0(v):
        status = "no demonstrated difference"
    elif excl0(ho) and math.copysign(1, v["mean_D_bp"]) == math.copysign(1, ho["mean_D_bp"]):
        status = f"exploratory, holdout-consistent (D {'<' if v['mean_D_bp'] < 0 else '>'} 0)"
    else:
        status = "validation only, not holdout-consistent"
    out["primary"] = {"variant": f"k{PRIMARY[0]}_H{PRIMARY[1]}", "filing_status": status}
    return out


if __name__ == "__main__":
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    res = run(cache)
    (HERE / "results_v1.json").write_text(json.dumps(res, indent=1))
    slim = {k: v for k, v in res.items() if k != "data"}
    slim["data"] = {k: v for k, v in res["data"].items() if k != "manifest"}
    print(json.dumps(slim, indent=1))
