"""Module A - flow absorption.

Hypothesis: when heavy aggressive flow meets an unusually weak price response (the flow was
absorbed), subsequent returns in the flow's direction differ from comparable events where price
responded strongly.

Inputs: Binance USD-M BTCUSDT 1-minute bars with taker-buy volume (perp flow), Binance spot BTCUSDT
1-minute bars (comparable spot flow), Binance USD-M depth snapshots (spread and depth, prospective
only, at most 15 minutes old). All at 5-minute decision steps; nothing sub-minute is claimed.
Features at a 5-minute boundary t (window = the five 1-minute bars ending at t):
  nti        net taker flow, sum(2 * taker_buy_volume - volume), BTC
  flow_norm  nti / median 5-minute volume over the prior 24 h (liquidity normalisation)
  resp       ln(close_t / open_{t-5m}) / sigma5, sigma5 = std of 1-minute log returns over the prior
             60 minutes x sqrt(5) (volatility normalisation)
  aligned    sign(nti) * resp; spot_flow_norm the same flow measure on spot
Event: |flow_norm| >= its trailing 7-day quantile q (recomputed hourly from past windows only);
group "weak" if aligned <= weak_max, "strong" if aligned >= strong_min, otherwise "middle".
Controls: every hour on the hour, same features, direction sign(nti).
"""
import math

from lab.common import BASIS_PROSPECTIVE, BASIS_RECONSTRUCTION, DAY, H, MINUTE, PROCESSING_LATENCY_MS, hash_inputs
from lab.events import event_record

ID = "flow_absorption"
VERSION = "A-1"
STEP = 5 * MINUTE
SPEC = {
    "module": "A", "id": ID, "version": VERSION, "title": "Flow absorption",
    "hypothesis": "Heavy aggressive flow met by an unusually weak price response predicts different "
                  "subsequent flow-direction returns than comparable strong-response events.",
    "inputs": ["binance_klines_1m_BTCUSDT_perp (o,h,l,c,v,tbv)", "binance_klines_1m_BTCUSDT_spot (v,tbv)",
               "snap.depth_binance_usdt (prospective only)"],
    "event": "|flow_norm| >= trailing 7-day quantile; weak if aligned response <= weak_max sigma, strong if >= strong_min",
    "outcome": "net log return in the flow direction from the first bar after availability",
    "baseline": "strong-response events of the same size class; hourly controls; regression on prior 60m "
                "return, prior 60m realised volatility and the last settled funding rate",
    "exclusions": ["windows with any missing 1-minute bar", "fewer than 7 days of prior windows",
                   "the middle response group (neither weak nor strong)"],
}


def build(bars_perp, bars_spot, start, end, params, basis, snaps=(), funding=(), code=""):
    """Returns (events, controls, coverage). Pure function of its inputs."""
    q, weak_max, strong_min = params["flow_quantile"], params["weak_max"], params["strong_min"]
    first = (start // STEP) * STEP
    n = (end - first) // MINUTE
    ts = [first + i * MINUTE for i in range(n)]
    perp = [bars_perp.get(t) for t in ts]
    spot = [bars_spot.get(t) for t in ts]
    lr = [math.log(b["c"] / b["o"]) if b else None for b in perp]      # within-bar return (open->close)
    events, controls = [], []
    flow_hist, vol5_hist, spot_vol5_hist = [], [], []
    threshold, thr_at = None, None
    cov = {"steps": 0, "skipped_missing": 0, "skipped_history": 0, "events": 0, "controls": 0}
    fund = sorted(funding)
    fi = 0
    snap_i = 0
    snaps = list(snaps)
    for i in range(65, n):
        t_close = ts[i] + MINUTE                   # a 5-minute window ends when bar i closes
        if t_close % STEP:
            continue
        cov["steps"] += 1
        win = perp[i - 4:i + 1]
        prior = lr[i - 64:i - 4]
        if any(b is None for b in win) or any(x is None for x in prior):
            cov["skipped_missing"] += 1
            flow_hist.append(None)
            continue
        vol5 = sum(b["v"] for b in win)
        nti = sum(2 * b["tbv"] - b["v"] for b in win)
        mu = sum(prior) / len(prior)
        sd = math.sqrt(sum((x - mu) ** 2 for x in prior) / (len(prior) - 1))
        med = sorted(vol5_hist[-288:])[len(vol5_hist[-288:]) // 2] if len(vol5_hist) >= 144 else None
        vol5_hist.append(vol5)
        swin = spot[i - 4:i + 1]
        spot_ok = all(b is not None for b in swin)
        spot_nti = sum(2 * b["tbv"] - b["v"] for b in swin) if spot_ok else None
        if spot_ok:
            spot_vol5_hist.append(sum(b["v"] for b in swin))
        smed = sorted(spot_vol5_hist[-288:])[len(spot_vol5_hist[-288:]) // 2] if len(spot_vol5_hist) >= 144 else None
        if med is None or sd <= 0:
            cov["skipped_history"] += 1
            flow_hist.append(None)
            continue
        flow_norm = nti / med
        resp = math.log(win[-1]["c"] / win[0]["o"]) / (sd * math.sqrt(5))
        direction = 1 if nti >= 0 else -1
        aligned = direction * resp
        past = [abs(x) for x in flow_hist[-2016:] if x is not None]
        if thr_at is None or t_close - thr_at >= H:
            threshold = sorted(past)[int(q * (len(past) - 1))] if len(past) >= 2016 * 0.9 else None
            thr_at = t_close
        flow_hist.append(flow_norm)
        avail_inputs = max(b["avail"] for b in win)
        t_available = avail_inputs + PROCESSING_LATENCY_MS
        prior_ret = direction * math.log(win[0]["o"] / perp[i - 64]["o"]) if perp[i - 64] else None
        while fi < len(fund) and fund[fi][0] <= t_close:
            fi += 1
        funding_last = fund[fi - 1][1] if fi else None
        half_spread = depth50 = None
        if snaps:
            while snap_i + 1 < len(snaps) and snaps[snap_i + 1]["t"] <= t_close:
                snap_i += 1
            s = snaps[snap_i]
            d = s.get("depth_binance_usdt") or {}
            if s["t"] <= t_close and t_close - s["t"] <= 15 * MINUTE and d.get("st") == "ok" and d.get("best_bid"):
                mid = (d["best_bid"] + d["best_ask"]) / 2
                half_spread = (d["best_ask"] - d["best_bid"]) / 2 / mid * 1e4
                depth50 = (d.get("bid_btc_50") or 0) + (d.get("ask_btc_50") or 0)
        feats = {"nti_btc": round(nti, 4), "flow_norm": round(flow_norm, 4), "resp_sigma": round(resp, 4),
                 "aligned_resp": round(aligned, 4), "sigma5": sd * math.sqrt(5), "vol5_btc": round(vol5, 3),
                 "spot_flow_norm": round(spot_nti / smed, 4) if spot_nti is not None and smed else None,
                 "prior_ret_60m_aligned": prior_ret, "prior_rv_60m": sd * math.sqrt(60),
                 "funding_last": funding_last, "half_spread_bp": half_spread, "depth_50pt_btc": depth50,
                 "threshold": threshold}
        quality = {"spot": "ok" if spot_ok else "missing", "spread": "snapshot" if half_spread is not None else "absent"}
        in_hash = hash_inputs([[b["t"], b["o"], b["c"], b["v"], b["tbv"]] for b in win])
        if t_close % H == 0:
            controls.append(event_record(ID + ":control", VERSION, t_close, avail_inputs, t_available, direction,
                                         "control", feats, in_hash, basis, {"window_bars": 5}, quality, code))
            cov["controls"] += 1
        if threshold is not None and abs(flow_norm) >= threshold:
            group = "weak" if aligned <= weak_max else ("strong" if aligned >= strong_min else "middle")
            events.append(event_record(ID, VERSION, t_close, avail_inputs, t_available, direction, group, feats,
                                       in_hash, basis, {"window_bars": 5}, quality, code))
            cov["events"] += 1
    return events, controls, cov


def run(lab, params):
    """Prospective pass over stored bars, and a reconstruction pass when history was fetched."""
    out = {"module": ID, "passes": []}
    stored_perp = lab.store.bars("binance_klines_1m_BTCUSDT_perp")
    stored_spot = lab.store.bars("binance_klines_1m_BTCUSDT_spot")
    funding = lab.store.funding_events()
    if stored_perp:
        start, end = min(stored_perp), max(stored_perp) + MINUTE
        ev, ctl, cov = build(stored_perp, stored_spot, start, end, params, BASIS_PROSPECTIVE,
                             lab.store.snaps(), funding, lab.code)
        state = "available" if cov["events"] or cov["controls"] else "insufficient_data"
        reasons = [] if (end - start) >= 7 * DAY else [f"{(end - start) / DAY:.1f} days of stored 1-minute bars; "
                                                       "the event threshold needs 7 days of prior windows"]
        out["passes"].append({"basis": "prospective", "events": ev, "controls": ctl, "coverage": cov,
                              "bars": stored_perp, "state": state if not reasons else "insufficient_data",
                              "reasons": reasons})
    else:
        out["passes"].append({"basis": "prospective", "events": [], "controls": [], "coverage": {},
                              "bars": {}, "state": "insufficient_data",
                              "reasons": ["no stored 1-minute bars yet (collector 2.7 stores them from deployment)"]})
    if lab.history.get("binance_klines_1m_BTCUSDT_perp"):
        hp, hs = lab.history["binance_klines_1m_BTCUSDT_perp"], lab.history.get("binance_klines_1m_BTCUSDT_spot", {})
        start, end = min(hp), max(hp) + MINUTE
        ev, ctl, cov = build(hp, hs, start, end, params, BASIS_RECONSTRUCTION, (), funding, lab.code)
        out["passes"].append({"basis": "reconstruction", "events": ev, "controls": ctl, "coverage": cov,
                              "bars": hp, "state": "available", "reasons": [],
                              "data_sha256": {k: lab.history_sha[k] for k in lab.history_sha if "BTCUSDT" in k}})
    return out
