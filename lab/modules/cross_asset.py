"""Module G - cross-asset stress propagation (bounded ETH/SOL subset).

Inputs: Binance USD-M 1-minute bars for BTCUSDT, ETHUSDT, SOLUSDT (one venue, one exchange clock,
USDT quote for all three, so no quote or unit conversion is needed for returns); the cross-asset
snapshot sources (Hyperliquid and Binance ETH/SOL, normalised in the collector); sampled Hyperliquid
account positions in ETH and SOL (hl-sample-v2 detail coins).

Timing limits, stated rather than assumed away: bars share open times, so the finest ordering this
data supports is one minute. "Leadership" is only reported as lagged correlation at lags of one or
more whole minutes; same-minute co-movement is never called leadership, and nothing sub-minute is
claimed. 15-minute snapshots support no sequencing at all.

Event at a 5-minute boundary: an alt (ETH or SOL) 5-minute log return beyond -k sigma (its own
prior-60-minute volatility) while BTC's 5-minute return is within +-1 sigma -> "alt_stress",
direction -1 (propagation hypothesis); mirror image "alt_squeeze", direction +1. Reference: hourly
controls. Lead-lag diagnostics (correlations of BTC returns with alt returns at lags -3..+3
minutes) are reported with the result.
"""
import math

from lab.common import BASIS_PROSPECTIVE, BASIS_RECONSTRUCTION, MINUTE, PROCESSING_LATENCY_MS, hash_inputs
from lab.events import event_record

ID = "cross_asset"
VERSION = "G-1"
SERIES = {"BTC": "binance_klines_1m_BTCUSDT_perp", "ETH": "binance_klines_1m_ETHUSDT_perp",
          "SOL": "binance_klines_1m_SOLUSDT_perp"}
SPEC = {"module": "G", "id": ID, "version": VERSION, "title": "Cross-asset stress propagation",
        "hypothesis": "Sharp ETH/SOL stress while BTC is still calm predicts BTC moving the same way over the "
                      "following hours more often than controls.",
        "inputs": list(SERIES.values()) + ["snap.cross_* sources", "data/hl_accounts ETH/SOL positions"],
        "event": "alt 5m return beyond -k sigma with BTC within 1 sigma (and mirror image)",
        "outcome": "net log return of BTC in the alt's direction",
        "baseline": "hourly controls; regression on prior return, volatility, funding",
        "exclusions": ["windows with any missing bar in any of the three series",
                       "sub-minute ordering (not identifiable from 1-minute bars)"]}


def lead_lag(rets, lags=range(-3, 4)):
    """corr(BTC_t, ALT_{t-lag}): positive lag = the alt moved first by `lag` minutes."""
    out = {}
    for alt in ("ETH", "SOL"):
        for lag in lags:
            pairs = [(rets["BTC"][i], rets[alt][i - lag]) for i in range(max(0, lag), len(rets["BTC"]) - max(0, -lag))
                     if rets["BTC"][i] is not None and rets[alt][i - lag] is not None]
            if len(pairs) < 100:
                continue
            xs, ys = zip(*pairs)
            mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
            sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
            sy = math.sqrt(sum((y - my) ** 2 for y in ys))
            out[f"{alt}_lag{lag}"] = round(sum((x - mx) * (y - my) for x, y in pairs) / (sx * sy), 4) if sx and sy else None
    return out


def build(bars, basis, params, code, funding=()):
    btc = bars["BTC"]
    if not btc:
        return [], [], {"steps": 0}, {}
    start, end = min(btc), max(btc) + MINUTE
    ts = list(range(start, end, MINUTE))
    rets = {a: [math.log(bars[a][t]["c"] / bars[a][t]["o"]) if t in bars[a] else None for t in ts] for a in SERIES}
    k = params["k_sigma"]
    events, controls = [], []
    cov = {"steps": 0, "skipped_missing": 0}
    fund = sorted(funding)
    for i in range(65, len(ts)):
        t_close = ts[i] + MINUTE
        if t_close % (5 * MINUTE):
            continue
        cov["steps"] += 1
        vals = {}
        ok = True
        for a in SERIES:
            win, prior = rets[a][i - 4:i + 1], rets[a][i - 64:i - 4]
            if any(x is None for x in win + prior):
                ok = False
                break
            mu = sum(prior) / len(prior)
            sd = math.sqrt(sum((x - mu) ** 2 for x in prior) / (len(prior) - 1)) * math.sqrt(5)
            vals[a] = (sum(win) / sd if sd > 0 else None, sd)
        if not ok or any(v[0] is None for v in vals.values()):
            cov["skipped_missing"] += 1
            continue
        avail = max(bars[a][ts[i]]["avail"] for a in SERIES)
        prior_ret = math.log(bars["BTC"][ts[i - 4]]["o"] / bars["BTC"][ts[i - 64]]["o"])
        funding_last = next((r for t, r in reversed(fund) if t <= t_close), None)
        feats = {f"{a}_z5": round(vals[a][0], 3) for a in SERIES}
        feats.update(prior_rv_60m=vals["BTC"][1] / math.sqrt(5) * math.sqrt(60), funding_last=funding_last)
        ih = hash_inputs([[a, ts[i], bars[a][ts[i]]["c"]] for a in SERIES])
        btc_calm = abs(vals["BTC"][0]) <= 1.0
        for alt in ("ETH", "SOL"):
            z = vals[alt][0]
            for group, cond, direction in (("alt_stress", z <= -k, -1), ("alt_squeeze", z >= k, 1)):
                if cond and btc_calm:
                    f = dict(feats, alt=alt, prior_ret_60m_aligned=direction * prior_ret)
                    events.append(event_record(ID, VERSION, t_close, avail, avail + PROCESSING_LATENCY_MS, direction,
                                               group, f, ih, basis, {"assets": 3}, {"clock": "Binance bar open times"},
                                               code))
        if t_close % 3_600_000 == 0:
            f = dict(feats, prior_ret_60m_aligned=-prior_ret)
            controls.append(event_record(ID + ":control", VERSION, t_close, avail, avail + PROCESSING_LATENCY_MS, -1,
                                         "control", f, ih, basis, {}, {}, code))
    return events, controls, cov, lead_lag(rets)


def hl_cross_exposure(store):
    """Share of sampled BTC notional held by accounts whose ETH+SOL notional exceeds their BTC notional."""
    recs = store.hl_accounts()
    if not recs:
        return None
    rec = recs[-1]
    by = {}
    for p in rec.get("positions", []):
        by.setdefault(p[0], {}).setdefault(p[1], 0.0)
        by[p[0]][p[1]] += abs(p[7] or 0.0)
    btc = sum(v.get("BTC", 0) for v in by.values())
    heavy = sum(v.get("BTC", 0) for v in by.values() if v.get("ETH", 0) + v.get("SOL", 0) > v.get("BTC", 0))
    return {"t": rec["t"], "btc_notional_usd": btc, "share_in_alt_heavy_accounts": heavy / btc if btc else None}


def run(lab, params):
    passes = []
    stored = {a: lab.store.bars(n) for a, n in SERIES.items()}
    ev, ctl, cov, ll = build(stored, BASIS_PROSPECTIVE, params, lab.code, lab.store.funding_events())
    days = (max(stored["BTC"]) - min(stored["BTC"])) / 86_400_000 if stored["BTC"] else 0
    need = params.get("min_days", 14)
    passes.append({"basis": "prospective", "events": ev, "controls": ctl, "coverage": dict(cov, lead_lag=ll,
                   hl_cross_exposure=hl_cross_exposure(lab.store)), "bars": stored["BTC"],
                   "state": "available" if days >= need else "insufficient_data",
                   "reasons": [] if days >= need else [f"{days:.1f} days of stored bars; the design needs {need}"]})
    if all(lab.history.get(n) for n in SERIES.values()):
        hist = {a: lab.history[n] for a, n in SERIES.items()}
        ev, ctl, cov, ll = build(hist, BASIS_RECONSTRUCTION, params, lab.code, lab.store.funding_events())
        passes.append({"basis": "reconstruction", "events": ev, "controls": ctl, "coverage": dict(cov, lead_lag=ll),
                       "bars": hist["BTC"], "state": "available", "reasons": [],
                       "data_sha256": {n: lab.history_sha.get(n) for n in SERIES.values()}})
    return {"module": ID, "passes": passes}
