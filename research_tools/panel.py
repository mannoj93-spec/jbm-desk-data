"""Continuous feature panel (panel-1.0.0, repo 2.29; brief section 10).

A versioned panel on a fixed 15-minute decision grid covering ordinary periods as well as event periods: every grid
time in the window gets a row, whatever the market did, so the panel is never selected from successful signals.
Each feature carries its value or an explicit state, the clocks of the inputs it read, and its family's version.

Decision clock. Row time T is a grid instant (:00, :15, :30, :45 UTC). A feature reads only inputs whose `avail`
(lab/data.Store: max(collector write, source knowability)) is <= T. The price window is the 15 closed minutes ending
at the latest perp bar available at T; its age (T minus that bar's close) is recorded, and a window older than
MAX_INPUT_AGE is 'stale-inputs' - never silently used. Labels are built by labels(), separately, and never enter a
feature.

Supported families (research_tools/catalog.json feature_families):
  flow_liquidity           flow_btc = sum(2*tbv - v) over the window (BTC, + = taker buying);
                           flow_per_depth = flow_btc / Binance USD-M depth within 25 bp (bid + ask, BTC), latest
                           snapshot available at T; depth < MIN_DEPTH_BTC -> insufficient-depth
  price_response           ret_15m_bp = 1e4 ln(close_last / open_first); response_bp_per_100btc = ret / (flow/100),
                           only when |flow| >= MIN_FLOW_BTC (else flow-below-threshold). A PAST response feature,
                           never a future label
  funding_dispersion       predicted (estimated, not settled) rates for Binance, Bybit, Hyperliquid normalized to 8h:
                           funding_mean_bp_8h, funding_dispersion_bp_8h (max - min); needs >= 2 venues
  positioning_interaction  d_oi_1h_pct from Binance 5-minute OI history available at T (latest row vs the row 1h
                           earlier); ret_1h_bp; oi_x_ret = d_oi_1h_pct * ret_1h_bp; d_oi_per_volume = delta OI (BTC) /
                           traded volume (BTC) over the same hour
  spot_perp_basis          basis_bp = 1e4 (Binance USDT perp mark / Binance spot - 1) from the latest snapshot
Gated (explicit, never filled): liquidity_resilience (needs E1 sequence-valid books; uncommissioned) and
options_disagreement (maturity, moneyness, quote age and liquidity filters not yet frozen).

Dependence. Rows overlap and share market shocks: each row carries session_utc (UTC day), block_4h and event
(|ret_15m_bp| >= EVENT_BP). More rows are not more independent evidence (see research_tools/calibration.py).

Fitted preprocessing (fit_transform/apply_transform): scaling and winsorization learned ONLY from rows whose T is
before the declared training cutoff; the artifact records that cutoff, the rows' hash and the panel version, and
apply refuses an artifact fitted on rows at or after it.
"""
import bisect
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lab.common import MINUTE, iso  # noqa: E402
from research_tools import evidence_contract as E  # noqa: E402

VERSION = "panel-1.0.0"
STEP = 15 * MINUTE
WINDOW = 15
MAX_INPUT_AGE = 45 * MINUTE
MIN_DEPTH_BTC = 1.0
MIN_FLOW_BTC = 5.0
EVENT_BP = 50.0
FAMILIES = {"flow_liquidity": "1.0.0", "price_response": "1.0.0", "funding_dispersion": "1.0.0",
            "positioning_interaction": "1.0.0", "spot_perp_basis": "1.0.0",
            "liquidity_resilience": "gated", "options_disagreement": "gated"}
GATED = {"liquidity_resilience": "gated: requires E1 sequence-valid order books (stream recorder not commissioned)",
         "options_disagreement": "gated: maturity, moneyness, quote-age and liquidity filters not frozen"}


class _Latest:
    """Latest item with avail <= cutoff (and t <= t_max) from (t, avail, payload) triples."""
    def __init__(self, items):
        self.items = sorted((x for x in items if x[1] is not None), key=lambda x: x[1])
        self.av = [x[1] for x in self.items]

    def at(self, cutoff, t_max=None, back=400):
        i = bisect.bisect_right(self.av, cutoff)
        best = None
        for j in range(i - 1, max(i - 1 - back, -1), -1):
            t, a, p = self.items[j]
            if t_max is not None and t > t_max:
                continue
            if best is None or t > best[0]:
                best = (t, a, p)
        return best


def _snap_items(store):
    out = []
    for s in store.snaps():
        o = s.get("observed_at")
        o = int(o) if o is not None else None
        out.append((int(s["t"]), o, s))
    return out


def build(store, start_ms, end_ms):
    """Panel rows for every grid time T in [start, end). store: lab/data.Store (its cutoff bounds what exists)."""
    perp = store.bars("binance_klines_1m_BTCUSDT_perp")
    perp_av = sorted((b["avail"], t) for t, b in perp.items())
    av_keys = [a for a, _ in perp_av]
    snaps = _Latest(_snap_items(store))
    oi_rows = [(r["t"], r["avail"], r["f"]) for r in store.series("binance_openInterestHist_5m")]
    oi = _Latest(oi_rows)
    oi_by_t = sorted(oi_rows)
    rows = []
    t0 = (start_ms + STEP - 1) // STEP * STEP
    for T in range(t0, end_ms, STEP):
        rows.append(_row(T, perp, perp_av, av_keys, snaps, oi, oi_by_t))
    return {"version": VERSION, "families": FAMILIES, "start_utc": iso(t0), "end_utc": iso(end_ms),
            "store_cutoff_utc": iso(store.cutoff), "rows": rows}


def _latest_bar_end(perp_av, av_keys, T):
    i = bisect.bisect_right(av_keys, T)
    if i == 0:
        return None
    return max(t for _, t in perp_av[max(0, i - 3000):i]) + MINUTE


def _row(T, perp, perp_av, av_keys, snaps, oi, oi_by_t):
    row = {"t_utc": iso(T), "t": T, "session_utc": iso(T)[:10], "block_4h": T // (4 * 60 * MINUTE),
           "features": {}, "state": {}, "inputs": {}}
    f, s = row["features"], row["state"]
    for fam, why in GATED.items():
        s[fam] = why
    end = _latest_bar_end(perp_av, av_keys, T)
    if end is None:
        for fam in ("flow_liquidity", "price_response", "positioning_interaction"):
            s[fam] = "source-missing"
    else:
        age = T - end
        row["inputs"]["perp_window_end_utc"] = iso(end)
        row["inputs"]["perp_window_age_s"] = age // 1000
        win = [perp.get(end - (k + 1) * MINUTE) for k in range(WINDOW)][::-1]
        hour = [perp.get(end - (k + 1) * MINUTE) for k in range(60)][::-1]
        if age > MAX_INPUT_AGE:
            for fam in ("flow_liquidity", "price_response", "positioning_interaction"):
                s[fam] = f"stale-inputs: latest perp bar closed {age // 60000} min before T"
        elif any(b is None or b["avail"] > T for b in win):
            for fam in ("flow_liquidity", "price_response"):
                s[fam] = "window-incomplete"
        else:
            flow = sum(2 * b["tbv"] - b["v"] for b in win)
            ret = 1e4 * math.log(win[-1]["c"] / win[0]["o"])
            f["flow_btc"], f["ret_15m_bp"] = round(flow, 4), round(ret, 3)
            row["event"] = abs(ret) >= EVENT_BP
            sn = snaps.at(T)
            depth = None
            if sn is not None:
                d = (sn[2].get("depth_binance_usdt") or {})
                b25, _ = E.number(d.get("bid_btc_25"), "nonneg")
                a25, _ = E.number(d.get("ask_btc_25"), "nonneg")
                if d.get("st") == "ok" and b25 is not None and a25 is not None:
                    depth = b25 + a25
                    row["inputs"]["depth_snapshot_utc"] = iso(sn[0])
            if depth is None:
                s["flow_liquidity"] = "source-missing: no valid depth snapshot available at T"
            elif depth < MIN_DEPTH_BTC:
                s["flow_liquidity"] = f"insufficient-depth ({depth:.3f} BTC)"
            else:
                f["depth_25bp_btc"] = round(depth, 3)
                f["flow_per_depth"] = round(flow / depth, 5)
                s["flow_liquidity"] = "ok"
            if abs(flow) < MIN_FLOW_BTC:
                s["price_response"] = "flow-below-threshold"
            else:
                f["response_bp_per_100btc"] = round(ret / (flow / 100), 4)
                s["price_response"] = "ok"
        if age <= MAX_INPUT_AGE:
            if any(b is None or b["avail"] > T for b in hour):
                s["positioning_interaction"] = "window-incomplete (1h price/volume)"
            else:
                now_oi = oi.at(T)
                if now_oi is None:
                    s["positioning_interaction"] = "source-missing: no OI history available at T"
                else:
                    t_then = now_oi[0] - 60 * MINUTE
                    k = bisect.bisect_left(oi_by_t, (t_then, -1, {}))
                    then = oi_by_t[k] if k < len(oi_by_t) and oi_by_t[k][0] == t_then else None
                    if then is None or then[1] is None or then[1] > T:
                        s["positioning_interaction"] = "source-missing: OI 1h earlier not available"
                    else:
                        o1, st1 = E.number(now_oi[2].get("sumOpenInterest"), "nonneg")
                        o0, st0 = E.number(then[2].get("sumOpenInterest"), "nonneg")
                        if st1 != "ok" or st0 != "ok" or not o0:
                            s["positioning_interaction"] = "invalid-capture"
                        else:
                            r1 = 1e4 * math.log(hour[-1]["c"] / hour[0]["o"])
                            vol = sum(b["v"] for b in hour)
                            d_pct = 100 * (o1 / o0 - 1)
                            f.update(d_oi_1h_pct=round(d_pct, 4), ret_1h_bp=round(r1, 3),
                                     oi_x_ret=round(d_pct * r1, 4),
                                     d_oi_per_volume=round((o1 - o0) / vol, 5) if vol > 0 else None)
                            s["positioning_interaction"] = "ok" if vol > 0 else "ok (zero volume: per-volume undefined)"
                            row["inputs"]["oi_stamp_utc"] = iso(now_oi[0])
    sn = snaps.at(T)
    if sn is None:
        s["funding_dispersion"] = s["spot_perp_basis"] = "source-missing: no snapshot available at T"
    else:
        snap = sn[2]
        row["inputs"]["snapshot_utc"] = iso(sn[0])
        hl = snap.get("hl_predicted_fundings") or {}
        rates = []
        if hl.get("st") == "ok":
            for venue, v in sorted((hl.get("venues") or {}).items()):
                r, st = E.number((v or {}).get("rate"), "funding_rate")
                ih, st2 = E.number((v or {}).get("interval_h"), "price")
                if st == "ok" and st2 == "ok":
                    rates.append((venue, 1e4 * r * 8 / ih))
        if len(rates) < 2:
            s["funding_dispersion"] = f"insufficient-venues ({len(rates)})"
        else:
            vals = [x for _, x in rates]
            f["funding_mean_bp_8h"] = round(sum(vals) / len(vals), 4)
            f["funding_dispersion_bp_8h"] = round(max(vals) - min(vals), 4)
            row["inputs"]["funding_venues"] = [v for v, _ in rates]
            s["funding_dispersion"] = "ok (estimated rates)"
        mark, mst = E.number((snap.get("binance_usdt_prem") or {}).get("mark"), "price")
        spot, sst = E.number((snap.get("premium_parts") or {}).get("binance_spot_btcusdt"), "price")
        if mst == "ok" and sst == "ok":
            f["basis_bp"] = round(1e4 * (mark / spot - 1), 3)
            s["spot_perp_basis"] = "ok"
        else:
            s["spot_perp_basis"] = f"source-missing (mark {mst}, spot {sst})"
    return row


def labels(store, panel, horizon_min=60):
    """Forward log return (bp) from the open of the first minute at or after T to the close h minutes later, with the
    label's availability (the exit bar's avail). Separate from features; a label never enters a feature."""
    perp = store.bars("binance_klines_1m_BTCUSDT_perp")
    out = []
    for r in panel["rows"]:
        a, b = perp.get(r["t"]), perp.get(r["t"] + (horizon_min - 1) * MINUTE)
        if a is None or b is None:
            out.append({"t": r["t"], "h": horizon_min, "label_bp": None, "state": "incomplete", "label_available": None})
        else:
            out.append({"t": r["t"], "h": horizon_min, "label_bp": round(1e4 * math.log(b["c"] / a["o"]), 3),
                        "state": "ok", "label_available": b["avail"]})
    return out


def coverage(panel):
    """Per family: counts by state (ok vs each exclusion reason, reasons truncated at ':'), ordinary vs event rows."""
    out = {}
    for r in panel["rows"]:
        for fam, st in r["state"].items():
            key = st.split(":")[0].split(" (")[0]
            out.setdefault(fam, {}).setdefault(key, 0)
            out[fam][key] += 1
    n = len(panel["rows"])
    ev = sum(1 for r in panel["rows"] if r.get("event"))
    return {"version": VERSION, "rows": n, "event_rows": ev, "ordinary_rows": n - ev, "families": out}


def rows_sha256(rows):
    return hashlib.sha256(E.canon(rows).encode()).hexdigest()


def fit_transform(rows, features, train_cutoff_ms, winsor=0.01):
    """Fit mean/sd and winsor bounds on rows with t < train_cutoff only. Returns a versioned artifact."""
    train = [r for r in rows if r["t"] < train_cutoff_ms]
    art = {"schema": "panel-transform/1", "panel_version": VERSION, "train_cutoff_utc": iso(train_cutoff_ms),
           "train_rows": len(train), "train_rows_sha256": rows_sha256(train), "max_train_t": max((r["t"] for r in train),
                                                                                                default=None),
           "params": {}}
    for k in features:
        xs = sorted(r["features"][k] for r in train if r["features"].get(k) is not None)
        if len(xs) < 10:
            art["params"][k] = None
            continue
        lo, hi = xs[int(winsor * (len(xs) - 1))], xs[int((1 - winsor) * (len(xs) - 1))]
        cl = [min(max(x, lo), hi) for x in xs]
        m = sum(cl) / len(cl)
        sd = math.sqrt(sum((x - m) ** 2 for x in cl) / (len(cl) - 1)) or None
        art["params"][k] = {"lo": lo, "hi": hi, "mean": m, "sd": sd, "n": len(xs)}
    art["sha256"] = hashlib.sha256(json.dumps(art, sort_keys=True).encode()).hexdigest()
    return art


def apply_transform(art, rows):
    """Standardized, winsorized features; refuses an artifact whose training rows reach its own cutoff."""
    if art.get("max_train_t") is not None and iso(art["max_train_t"]) >= art["train_cutoff_utc"]:
        raise ValueError("artifact was fitted on rows at or after its training cutoff")
    body = {k: v for k, v in art.items() if k != "sha256"}
    if hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() != art.get("sha256"):
        raise ValueError("transform artifact altered")
    out = []
    for r in rows:
        z = {}
        for k, p in art["params"].items():
            x = r["features"].get(k)
            z[k] = None if (p is None or x is None or not p["sd"]) else (min(max(x, p["lo"]), p["hi"]) - p["mean"]) / p["sd"]
        out.append({"t": r["t"], "z": z})
    return out
