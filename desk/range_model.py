#!/usr/bin/env python3
"""range_model — the desk's range forecast (runbook §E2) and its evaluation harness (queue O21).

Version: range-11.1.0 (package 11.1, Sep 25 2026). Stdlib only; imports jbm_measure. Status:
implemented and tested offline (test_range_model.py); O21 run once in the build container (results in
baserates.md §3 R-rows); deployed only when a fresh thread runs the tests from the mounted skill folder.

What it forecasts: the log range ln(H/L) of the Binance BTCUSDT perp over the next 4H bar, the next
24h (6 bars), and the next 72h (18 bars), from each 4H close. Units: log range (dimensionless);
points only by explicit conversion at the decision close.

Models (direct, one fit per horizon — ranges do not add, so 4H forecasts are never iterated):
  B0  persistence: mean ln range over the trailing 42 bars (4h), or over the trailing seven
      non-overlapping completed windows of the horizon's length (24h, 72h).
  B1  HAR-range OLS: ln lr_4h(t), ln mean(lr_4h, 6/42/180 bars), Saturday and Sunday shares of the
      horizon, count of scheduled releases (CPI, NFP, PPI, FOMC) inside the horizon.
  B2  B1 + ln of the DVOL-implied 4H sigma known at the decision (DVOL candle admitted at its close).
Refits monthly on an expanding window using only decisions whose targets had closed before the refit.
Interval: fit-residual 10/50/90 quantiles. Coherence: 24h >= 4h and 72h >= 24h, raises counted.

Look-ahead rule: every feature at decision i is computed from bars[0..i] and inputs whose
available_at <= the close of bar i. `features_at` receives only that history.
"""
from __future__ import annotations

import bisect
import csv
import datetime as dt
import hashlib
import json
import math
import os
import random
import statistics

from jbm_measure import VERSION as MEASURE_VERSION

VERSION = "range-11.1.0"
HORIZON_BARS = {"4h": 1, "24h": 6, "72h": 18}
BARS_PER_YEAR_4H = 365 * 6
WARMUP = 180                                     # bars needed for the longest HAR term
NW_MIN_LAG = 6
SPLITS = {"fit_end": "2024-09-22T23:59:59Z", "validation_end": "2025-09-22T23:59:59Z",
          "holdout_end": "2026-09-22T23:59:59Z"}
UTC = dt.timezone.utc


def _t(s: str) -> dt.datetime:
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def _iso(t: dt.datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------------------------
def load_calendar(path: str) -> list:
    """Release timestamps (UTC) from data/releases_*.csv; comment lines start with '#'."""
    with open(path, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(line for line in f if not line.startswith("#"))]
    return sorted(_t(r["release_utc"]) for r in rows)


def dvol_series(dvol_rows) -> tuple:
    """(available_at list, dvol list) sorted, for as-of lookup."""
    pairs = sorted((_t(r["available_at_utc"]), float(r["dvol"])) for r in dvol_rows)
    return [p[0] for p in pairs], [p[1] for p in pairs]


def dvol_as_of(series, when: dt.datetime):
    avail, vals = series
    k = bisect.bisect_right(avail, when) - 1
    if k < 0 or (when - avail[k]) > dt.timedelta(hours=6):   # stale beyond 6h -> missing
        return None
    return vals[k]


# --------------------------------------------------------------------------------------------
# Features and targets
# --------------------------------------------------------------------------------------------
def _lr(b):
    return math.log(b["high"] / b["low"])


def features_at(history, releases, dvol, horizon: str):
    """Features for the decision at the close of history[-1]. `history` holds bars 0..i only."""
    if len(history) < WARMUP:
        return None
    lr = [max(_lr(b), 1e-6) for b in history[-WARMUP:]]
    close_t = _t(history[-1]["close_utc"])
    n = HORIZON_BARS[horizon]
    opens = [close_t + dt.timedelta(hours=4 * k) for k in range(n)]
    end_t = close_t + dt.timedelta(hours=4 * n)
    lo = bisect.bisect_left(releases, close_t)
    hi = bisect.bisect_left(releases, end_t)
    closes = [b["close"] for b in history[-43:]]
    rets = [math.log(b / a) for a, b in zip(closes, closes[1:])]
    hl42 = [math.log(b["high"] / b["low"]) for b in history[-42:]]
    hl6 = hl42[-6:]
    d = dvol_as_of(dvol, close_t) if dvol else None
    f = {
        "decision_utc": _iso(close_t),
        "ln_lr_last": math.log(lr[-1]),
        "ln_m6": math.log(statistics.fmean(lr[-6:])),
        "ln_m42": math.log(statistics.fmean(lr[-42:])),
        "ln_m180": math.log(statistics.fmean(lr)),
        "sat_share": sum(o.weekday() == 5 for o in opens) / n,
        "sun_share": sum(o.weekday() == 6 for o in opens) / n,
        "releases": hi - lo,
        "release_within_24h": bisect.bisect_left(releases, close_t + dt.timedelta(hours=24)) - lo > 0,
        "sd_c2c_42": statistics.stdev(rets),
        "sd_park_42": math.sqrt(sum(x * x for x in hl42) / 42 / (4 * math.log(2))),
        "sd_park_6": math.sqrt(sum(x * x for x in hl6) / 6 / (4 * math.log(2))),
        "sd_implied": (d / 100.0 / math.sqrt(BARS_PER_YEAR_4H)) if d else None,
        "ref_close": history[-1]["close"],
    }
    f["ln_implied_h"] = math.log(f["sd_implied"] * math.sqrt(n)) if f["sd_implied"] else None
    # B0 for this horizon
    if n == 1:
        f["b0"] = statistics.fmean(math.log(x) for x in lr[-42:])
    else:
        wins = []
        for k in range(7):
            seg = history[len(history) - n * (k + 1): len(history) - n * k]
            if len(seg) < n:
                return None
            wins.append(math.log(max(math.log(max(b["high"] for b in seg) / min(b["low"] for b in seg)), 1e-6)))
        f["b0"] = statistics.fmean(wins)
    return f


def target_at(bars, i: int, horizon: str):
    n = HORIZON_BARS[horizon]
    seg = bars[i + 1: i + 1 + n]
    if len(seg) < n:
        return None
    lr = math.log(max(b["high"] for b in seg) / min(b["low"] for b in seg))
    return math.log(max(lr, 1e-6)), seg[-1]["close_utc"]          # the target is ln(lr), as B0 and B1 are


def build_panel(bars, releases, dvol_rows=None, horizons=("4h", "24h", "72h")):
    """{horizon: [row]} with features, target, and the target's close time."""
    dvol = dvol_series(dvol_rows) if dvol_rows else None
    panel = {h: [] for h in horizons}
    for i in range(len(bars)):
        hist = bars[max(0, i + 1 - WARMUP): i + 1]     # the features need at most WARMUP bars of history
        for h in horizons:
            f = features_at(hist, releases, dvol, h)
            if f is None:
                continue
            tg = target_at(bars, i, h)
            f["y"], f["target_close_utc"] = (tg if tg else (None, None))
            panel[h].append(f)
    return panel


# --------------------------------------------------------------------------------------------
# OLS (normal equations, Gauss-Jordan with partial pivoting)
# --------------------------------------------------------------------------------------------
def ols(X, y):
    k = len(X[0])
    A = [[0.0] * k for _ in range(k)]
    b = [0.0] * k
    for row, yi in zip(X, y):
        for a in range(k):
            ra = row[a]
            b[a] += ra * yi
            Aa = A[a]
            for c in range(a, k):
                Aa[c] += ra * row[c]
    for a in range(k):
        for c in range(a):
            A[a][c] = A[c][a]
    M = [A[r][:] + [b[r]] for r in range(k)]
    for col in range(k):
        piv = max(range(col, k), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            raise ValueError("singular design")
        M[col], M[piv] = M[piv], M[col]
        p = M[col][col]
        M[col] = [v / p for v in M[col]]
        for r in range(k):
            if r != col and M[r][col]:
                fct = M[r][col]
                M[r] = [a - fct * c for a, c in zip(M[r], M[col])]
    return [M[r][k] for r in range(k)]


MODEL_TERMS = {
    "B1": ("ln_lr_last", "ln_m6", "ln_m42", "ln_m180", "sat_share", "sun_share", "releases"),
    "B2": ("ln_lr_last", "ln_m6", "ln_m42", "ln_m180", "sat_share", "sun_share", "releases", "ln_implied_h"),
}


def design(row, model):
    return [1.0] + [float(row[t]) for t in MODEL_TERMS[model]]


def usable(row, model):
    return row["y"] is not None and all(row.get(t) is not None for t in MODEL_TERMS.get(model, ()))


def _quantiles(xs, qs=(0.1, 0.5, 0.9)):
    s = sorted(xs)
    out = []
    for q in qs:
        pos = q * (len(s) - 1)
        lo, hi = int(math.floor(pos)), int(math.ceil(pos))
        out.append(s[lo] + (s[hi] - s[lo]) * (pos - lo))
    return out


def fit(rows, model, refit_time: dt.datetime, start_utc: str | None = None):
    """Fit on decisions whose targets closed at or before refit_time."""
    cut = _iso(refit_time)
    tr = [r for r in rows if usable(r, model) and r["target_close_utc"] <= cut
          and (start_utc is None or r["decision_utc"] >= start_utc)]
    if len(tr) < 200:
        return None
    X = [design(r, model) for r in tr]
    y = [r["y"] for r in tr]
    terms = ("const",) + MODEL_TERMS[model]
    # a term with no variation in the training window (e.g. no release yet) is dropped, not faked
    keep = [0] + [j for j in range(1, len(terms)) if max(x[j] for x in X) > min(x[j] for x in X)]
    bk = ols([[x[j] for j in keep] for x in X], y)
    beta = [0.0] * len(terms)
    for j, b in zip(keep, bk):
        beta[j] = b
    res = [yi - sum(b * x for b, x in zip(beta, xi)) for xi, yi in zip(X, y)]
    return {"model": model, "beta": beta, "terms": terms, "n": len(tr),
            "dropped_terms": [terms[j] for j in range(len(terms)) if j not in keep],
            "resid_q": _quantiles(res), "refit_utc": cut}


def predict(fitted, row):
    return sum(b * x for b, x in zip(fitted["beta"], design(row, fitted["model"])))


def month_starts(t0: dt.datetime, t1: dt.datetime):
    cur = dt.datetime(t0.year, t0.month, 1, tzinfo=UTC)
    out = []
    while cur <= t1:
        out.append(cur)
        cur = dt.datetime(cur.year + (cur.month == 12), cur.month % 12 + 1, 1, tzinfo=UTC)
    return out


def walk_forward(rows, model, eval_start: str, eval_end: str, start_utc: str | None = None):
    """Pseudo-out-of-sample forecasts over [eval_start, eval_end]: refit at each month start using
    targets closed before it; coefficients frozen within the month."""
    ev = [r for r in rows if eval_start <= r["decision_utc"] <= eval_end and r["y"] is not None
          and (model == "B0" or usable(r, model))]
    out = []
    if model == "B0":
        return [{"decision_utc": r["decision_utc"], "y": r["y"], "f": r["b0"], "q": None} for r in ev]
    fits = {}
    for r in ev:
        t = _t(r["decision_utc"])
        m0 = dt.datetime(t.year, t.month, 1, tzinfo=UTC)
        if m0 not in fits:
            fits[m0] = fit(rows, model, m0, start_utc)
        fm = fits[m0]
        if fm is None:
            continue
        p = predict(fm, r)
        out.append({"decision_utc": r["decision_utc"], "y": r["y"], "f": p,
                    "q": [p + q for q in fm["resid_q"]]})
    return out


# --------------------------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------------------------
def mae(fc):
    return statistics.fmean(abs(r["y"] - r["f"]) for r in fc)


def qlike(fc):
    vals = []
    for r in fc:
        ratio = math.exp(2 * (r["y"] - r["f"]))
        vals.append(ratio - math.log(ratio) - 1)
    return statistics.fmean(vals)


def _phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def newey_west_var(d, lag):
    n = len(d)
    m = statistics.fmean(d)
    e = [x - m for x in d]
    g0 = sum(x * x for x in e) / n
    s = g0
    for L in range(1, lag + 1):
        g = sum(e[t] * e[t - L] for t in range(L, n)) / n
        s += 2 * (1 - L / (lag + 1)) * g
    return s


def diebold_mariano(loss_a, loss_b, lag):
    """d = loss_a - loss_b; negative mean favours a. Returns (mean_d, z, two-sided p)."""
    d = [a - b for a, b in zip(loss_a, loss_b)]
    v = newey_west_var(d, lag)
    if v <= 0:
        return statistics.fmean(d), 0.0, 1.0
    z = statistics.fmean(d) / math.sqrt(v / len(d))
    return statistics.fmean(d), z, 2 * (1 - _phi(abs(z)))


def block_bootstrap_skill(loss_m, loss_b, block=42, reps=1000, seed=20260925):
    """Moving-block bootstrap 95% interval for skill = 1 - mean(loss_m)/mean(loss_b)."""
    n = len(loss_m)
    rnd = random.Random(seed)
    starts = max(1, n - block + 1)
    sk = []
    for _ in range(reps):
        sm = sb = 0.0
        cnt = 0
        while cnt < n:
            s0 = rnd.randrange(starts)
            for j in range(s0, min(s0 + block, n)):
                sm += loss_m[j]; sb += loss_b[j]; cnt += 1
                if cnt >= n:
                    break
        sk.append(1 - sm / sb)
    sk.sort()
    return sk[int(0.025 * reps)], sk[int(0.975 * reps) - 1]


def compare(fc_m, fc_b, horizon):
    """Align on decision time and report skill (MAE of ln range), DM/HAC, bootstrap interval."""
    bmap = {r["decision_utc"]: r for r in fc_b}
    pairs = [(r, bmap[r["decision_utc"]]) for r in fc_m if r["decision_utc"] in bmap]
    lm = [abs(a["y"] - a["f"]) for a, _ in pairs]
    lb = [abs(b["y"] - b["f"]) for _, b in pairs]
    lag = max(HORIZON_BARS[horizon], NW_MIN_LAG)
    md, z, p = diebold_mariano(lm, lb, lag)
    lo, hi = block_bootstrap_skill(lm, lb)
    cov = [a["q"][0] <= a["y"] <= a["q"][2] for a, _ in pairs if a["q"]]
    return {"n": len(pairs), "mae_model": statistics.fmean(lm), "mae_base": statistics.fmean(lb),
            "skill": 1 - statistics.fmean(lm) / statistics.fmean(lb), "skill_ci95": (lo, hi),
            "dm_mean_diff": md, "dm_z": z, "dm_p": p, "nw_lag": lag,
            "qlike_model": qlike([a for a, _ in pairs]), "qlike_base": qlike([b for _, b in pairs]),
            "coverage_10_90": (sum(cov) / len(cov)) if cov else None}


# --------------------------------------------------------------------------------------------
# Stage 1: the sigma-estimator race (O21 stage 1, absorbs O10)
# --------------------------------------------------------------------------------------------
STAGE1 = ("sd_c2c_42", "sd_park_42", "sd_park_6", "sd_implied", "m10_composite")


def stage1_sigma(row, name):
    if name != "m10_composite":
        return row[name]
    if row["release_within_24h"]:
        return row["sd_implied"]
    return row["sd_park_6"] if row["sd_c2c_42"] > 2 * row["sd_park_6"] else row["sd_c2c_42"]


def stage1(rows4h, fit_start, fit_end, eval_start, eval_end):
    """Forecast ln lr_4h = ln sigma_e + c_e, c_e fitted on the fit period (so the range/sigma scale is
    estimated, not assumed). Common sample: rows where every estimator exists."""
    common = [r for r in rows4h if r["y"] is not None and r["sd_implied"]]
    fitrows = [r for r in common if fit_start <= r["decision_utc"] <= fit_end]
    evrows = [r for r in common if eval_start <= r["decision_utc"] <= eval_end]
    out = {}
    for e in STAGE1:
        c = statistics.fmean(r["y"] - math.log(stage1_sigma(r, e)) for r in fitrows)
        fc = [{"decision_utc": r["decision_utc"], "y": r["y"], "f": math.log(stage1_sigma(r, e)) + c, "q": None}
              for r in evrows]
        out[e] = {"c": c, "n_fit": len(fitrows), "forecasts": fc, "mae": mae(fc)}
    return out


# --------------------------------------------------------------------------------------------
# Live use and registration
# --------------------------------------------------------------------------------------------
def coherent(f4, f24, f72):
    raises = 0
    if f24 < f4:
        f24, raises = f4, raises + 1
    if f72 < f24:
        f72, raises = f24, raises + 1
    return f4, f24, f72, raises


def forecast_now(bars, releases, dvol_rows, selected: dict, status: str):
    """Forecast from the last closed bar with the selected model per horizon, refit at the current
    month start (as in evaluation). Returns the registry document body (unregistered)."""
    panel = build_panel(bars[-400:], releases, dvol_rows)
    full = build_panel(bars, releases, dvol_rows)
    last_close = _t(bars[-1]["close_utc"])
    m0 = dt.datetime(last_close.year, last_close.month, 1, tzinfo=UTC)
    out = {}
    for h, model in selected.items():
        row = panel[h][-1]
        if model == "B0":
            out[h] = {"model": "B0", "point": row["b0"], "q": None}
        else:
            fm = fit(full[h], model, m0)
            p = predict(fm, row)
            out[h] = {"model": model, "point": p, "q": [p + q for q in fm["resid_q"]], "fit_n": fm["n"],
                      "refit_utc": fm["refit_utc"]}
    f4, f24, f72, raises = coherent(out["4h"]["point"], out["24h"]["point"], out["72h"]["point"])
    for h, v in zip(("4h", "24h", "72h"), (f4, f24, f72)):
        out[h]["point_coherent"] = v
        # forecasts are ln(lr); lr = exp(v); points at the decision close = ref x (e^lr - 1)
        out[h]["log_range"] = math.exp(v)
        out[h]["range_points"] = row_ref(panel) * (math.exp(math.exp(v)) - 1)
        if out[h]["q"]:
            out[h]["range_points_q10_50_90"] = [row_ref(panel) * (math.exp(math.exp(q)) - 1) for q in out[h]["q"]]
    body = {"model": "range_model", "code_version": VERSION, "measure_version": MEASURE_VERSION,
            "decision_utc": _iso(last_close), "target": "ln(H/L) Binance BTCUSDT perp, last price",
            "horizons": out, "coherence_raises": raises, "status": status,
            "ref_close": row_ref(panel)}
    body["content_sha256"] = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
    body["id"] = f"RANGE-LR-{last_close.strftime('%Y%m%dT%H%MZ')}"
    return body


def row_ref(panel):
    return panel["4h"][-1]["ref_close"]


def spec_sha256() -> str:
    """Hash of this file's bytes: the frozen specification a holdout result belongs to."""
    with open(os.path.abspath(__file__), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# --------------------------------------------------------------------------------------------
# O21 runner
# --------------------------------------------------------------------------------------------
def run_o21(panel, open_holdout: bool = False, stage1_fit_start: str = "2021-03-24T00:00:00Z"):
    """Stage 1 and stage 2 of O21 on the validation period; with open_holdout, also the holdout —
    which the specification allows once per frozen spec (the caller records spec_sha256 first).
    Selection rule (fixed before running): per horizon, B1 is kept over B0 only if its validation MAE
    is lower with DM two-sided p < 0.05; B2 is kept over the kept model under the same rule."""
    fit_end = SPLITS["fit_end"]
    val = ("2024-09-23T00:00:00Z", SPLITS["validation_end"])
    hol = ("2025-09-23T00:00:00Z", SPLITS["holdout_end"])
    res = {"code_version": VERSION, "spec_sha256": spec_sha256(), "splits": SPLITS, "variants_counted": 0,
           "stage1": {}, "stage2": {}, "holdout_opened": open_holdout}
    s1 = stage1(panel["4h"], stage1_fit_start, fit_end, *val)
    res["stage1"]["validation"] = {e: {"mae": v["mae"], "c": v["c"], "n": len(v["forecasts"])} for e, v in s1.items()}
    ref = s1["sd_c2c_42"]["forecasts"]
    for e, v in s1.items():
        if e != "sd_c2c_42":
            res["stage1"]["validation"][e]["vs_c2c"] = compare(v["forecasts"], ref, "4h")
    res["variants_counted"] += len(STAGE1)
    if open_holdout:
        s1h = stage1(panel["4h"], stage1_fit_start, fit_end, *hol)
        refh = s1h["sd_c2c_42"]["forecasts"]
        res["stage1"]["holdout"] = {e: {"mae": v["mae"], "n": len(v["forecasts"]),
                                        **({"vs_c2c": compare(v["forecasts"], refh, "4h")} if e != "sd_c2c_42" else {})}
                                    for e, v in s1h.items()}
    for h, rows in panel.items():
        out = {"validation": {}, "selected": "B0"}
        fc = {m: walk_forward(rows, m, *val) for m in ("B0", "B1", "B2")}
        res["variants_counted"] += 3
        c10 = compare(fc["B1"], fc["B0"], h)
        c21 = compare(fc["B2"], fc["B1"], h)
        c20 = compare(fc["B2"], fc["B0"], h)
        out["validation"] = {"B1_vs_B0": c10, "B2_vs_B1": c21, "B2_vs_B0": c20}
        sel = "B0"
        if c10["skill"] > 0 and c10["dm_p"] < 0.05:
            sel = "B1"
        base_cmp = c21 if sel == "B1" else c20
        if base_cmp["skill"] > 0 and base_cmp["dm_p"] < 0.05:
            sel = "B2"
        out["selected"] = sel
        if open_holdout:
            fh = {m: walk_forward(rows, m, *hol) for m in {"B0", sel}}
            out["holdout"] = {"selected_vs_B0": compare(fh[sel], fh["B0"], h) if sel != "B0" else None,
                              "n_B0": len(fh["B0"]), "mae_B0": mae(fh["B0"])}
        # the reported fit never uses holdout-period targets until the holdout has been opened
        cut = SPLITS["holdout_end"] if open_holdout else SPLITS["validation_end"]
        latest = fit(rows, sel, _t(cut)) if sel != "B0" else None
        out["latest_fit"] = latest
        res["stage2"][h] = out
    return res


if __name__ == "__main__":
    print(VERSION, spec_sha256())
