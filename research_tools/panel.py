"""Continuous feature panel (panel-1.1.0, repo 2.30; panel-1.0.0 was repo 2.29, brief section 10).

panel-1.1.0 (Oct 19 2026 review, F2). In 1.0.0 only the perpetual bars had an age limit: a 05:00 row used bars ending
04:45 with depth, funding and basis snapshots from 00:07 and an OI change ending 01:55, all labelled usable, and the OI
change was multiplied by a price return over a different hour. Every source dependency now has a declared policy
(POLICY, hashed into each panel): a maximum age at the decision time, an availability rule (avail <= T) and, where a
feature combines sources, an alignment tolerance. Each feature carries its own state (row["fstate"]): ok, missing,
stale, malformed, misaligned, insufficient-*, gated - a dependent feature inherits the worst state of its inputs, and an
old timestamp next to "ok" no longer happens. Valid zeros are values. Estimated funding stays labelled estimated.
  depth for flow_per_depth   the snapshot whose depth measurement (t_event, else t_ret, else the snapshot slot) is
                             nearest the flow window, within DEPTH_ALIGN of it and no older than DEPTH_MAX_AGE at T
  funding (estimated)        snapshot no older than FUNDING_MAX_AGE at T; venues normalised to bp per 8h
  basis                      mark and spot measured within BASIS_PAIR of each other, no older than BASIS_MAX_AGE
  positioning_interaction    OI change over an aligned hour: the latest OI stamp t_oi (available at T, no older than
                             OI_MAX_AGE) whose row 60 min earlier is available and whose price/volume hour
                             [t_oi - 60 min, t_oi) is complete at T; ret_1h_bp and volume refer to that same hour
freeze()/compare(): an admitted panel is frozen with its rows hash, policy hash and source identities; a rebuild that
differs (later-arriving data, a correction) is reported as a revision, never silently substituted.

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

VERSION = "panel-1.1.0"
STEP = 15 * MINUTE
WINDOW = 15
MAX_INPUT_AGE = 45 * MINUTE                       # perpetual 15-minute window, as in 1.0.0
DEPTH_MAX_AGE = 30 * MINUTE                       # snapshots arrive every ~12 min (median), 26 min at worst (Oct 2026)
DEPTH_ALIGN = 10 * MINUTE                         # depth measured within 10 min of the flow window
FUNDING_MAX_AGE = 60 * MINUTE                     # estimated funding changes slowly; older than 1 h is stale
BASIS_MAX_AGE = 30 * MINUTE
BASIS_PAIR = 60 * 1000                            # mark and spot measured within 60 s of each other
OI_MAX_AGE = 45 * MINUTE                          # OI history lags ~13 min median, 27.5 min max (Oct 2026)
POLICY = {"perp_window": {"max_age_ms": MAX_INPUT_AGE, "bars": WINDOW},
          "depth": {"max_age_ms": DEPTH_MAX_AGE, "align_ms": DEPTH_ALIGN, "measured": "t_event|t_ret|slot"},
          "funding_estimate": {"max_age_ms": FUNDING_MAX_AGE, "units": "bp per 8h (rate * 8 / interval_h * 1e4)",
                               "kind": "estimated (predicted), never settled"},
          "basis": {"max_age_ms": BASIS_MAX_AGE, "pair_ms": BASIS_PAIR},
          "oi": {"max_age_ms": OI_MAX_AGE, "pair_gap_ms": 60 * MINUTE, "price_window": "the same hour as the OI change"},
          "availability": "an input is usable at T only if its first durable availability (avail) is <= T"}
MIN_DEPTH_BTC = 1.0
MIN_FLOW_BTC = 5.0
EVENT_BP = 50.0
FAMILIES = {"flow_liquidity": "1.0.0", "price_response": "1.0.0", "funding_dispersion": "1.0.0",
            "positioning_interaction": "1.0.0", "spot_perp_basis": "1.0.0",
            "liquidity_resilience": "gated", "options_disagreement": "gated"}
GATED = {"liquidity_resilience": "gated: requires E1 sequence-valid order books (stream recorder not commissioned)",
         "options_disagreement": "gated: maturity, moneyness, quote-age and liquidity filters not frozen"}


class _Avail:
    """Items (t, avail, payload) ordered by availability; the ones available at a cutoff, newest first."""
    def __init__(self, items):
        self.items = sorted((x for x in items if x[1] is not None), key=lambda x: x[1])
        self.av = [x[1] for x in self.items]

    def recent(self, cutoff, n=12):
        i = bisect.bisect_right(self.av, cutoff)
        return self.items[max(0, i - n):i][::-1]

    def at(self, cutoff, t_max=None, back=400):
        """Latest by t among items available at cutoff (and t <= t_max)."""
        best = None
        for t, a, p in self.recent(cutoff, back):
            if t_max is not None and t > t_max:
                continue
            if best is None or t > best[0]:
                best = (t, a, p)
        return best


_Latest = _Avail                                    # 1.0.0 name


def _snap_items(store):
    out = []
    for s in store.snaps():
        o = s.get("observed_at")
        o = int(o) if o is not None else None
        out.append((int(s["t"]), o, s))
    return out


def _measured(snap, part):
    """When a snapshot component was measured: its own event stamp, else its retrieval time, else the slot."""
    d = snap.get(part) or {}
    for k in ("t_event", "t_ret"):
        v, st = E.number(d.get(k), "nonneg")
        if st == "ok" and v:
            return int(v)
    return int(snap["t"])


def policy_sha256():
    return hashlib.sha256(E.canon(POLICY).encode()).hexdigest()


def build(store, start_ms, end_ms):
    """Panel rows for every grid time T in [start, end). store: lab/data.Store (its cutoff bounds what exists)."""
    perp = store.bars("binance_klines_1m_BTCUSDT_perp")
    perp_av = sorted((b["avail"], t) for t, b in perp.items())
    av_keys = [a for a, _ in perp_av]
    snaps = _Avail(_snap_items(store))
    oi_rows = [(r["t"], r["avail"], r["f"]) for r in store.series("binance_openInterestHist_5m")]
    oi = _Avail(oi_rows)
    oi_by_t = {t: (t, a, f) for t, a, f in oi_rows}
    rows = []
    t0 = (start_ms + STEP - 1) // STEP * STEP
    for T in range(t0, end_ms, STEP):
        rows.append(_row(T, perp, perp_av, av_keys, snaps, oi, oi_by_t))
    return {"version": VERSION, "families": FAMILIES, "policy": POLICY, "policy_sha256": policy_sha256(),
            "start_utc": iso(t0), "end_utc": iso(end_ms), "store_cutoff_utc": iso(store.cutoff), "rows": rows}


def _latest_bar_end(perp_av, av_keys, T):
    i = bisect.bisect_right(av_keys, T)
    if i == 0:
        return None
    return max(t for _, t in perp_av[max(0, i - 3000):i]) + MINUTE


FEATURES = {"flow_liquidity": ("flow_btc", "ret_15m_bp", "depth_25bp_btc", "flow_per_depth"),
            "price_response": ("response_bp_per_100btc",),
            "funding_dispersion": ("funding_mean_bp_8h", "funding_dispersion_bp_8h"),
            "positioning_interaction": ("d_oi_1h_pct", "ret_1h_bp", "oi_x_ret", "d_oi_per_volume"),
            "spot_perp_basis": ("basis_bp",)}


def _src(row, name, t_ms, avail_ms, T, state):
    row["inputs"].setdefault("sources", {})[name] = {"t_utc": iso(t_ms) if t_ms is not None else None,
                                                    "avail_utc": iso(avail_ms) if avail_ms is not None else None,
                                                    "age_s": (T - t_ms) // 1000 if t_ms is not None else None,
                                                    "state": state}


def _row(T, perp, perp_av, av_keys, snaps, oi, oi_by_t):
    row = {"t_utc": iso(T), "t": T, "session_utc": iso(T)[:10], "block_4h": T // (4 * 60 * MINUTE),
           "features": {}, "state": {}, "fstate": {}, "inputs": {}}
    f, s, fs = row["features"], row["state"], row["fstate"]
    for fam, why in GATED.items():
        s[fam] = why

    def put(fam, state, values=None):
        """A family's state; its features get the values (state ok) or the same state (never a stale number)."""
        s[fam] = state
        for k in FEATURES[fam]:
            if values and k in values and values[k] is not None:
                f[k] = values[k]
                fs[k] = "ok"
            else:
                fs[k] = state if state != "ok" else fs.get(k, "undefined")

    end = _latest_bar_end(perp_av, av_keys, T)
    flow = ret = None
    if end is None:
        for fam in ("flow_liquidity", "price_response", "positioning_interaction"):
            put(fam, "source-missing")
        _src(row, "perp_window", None, None, T, "missing")
    else:
        age = T - end
        row["inputs"]["perp_window_end_utc"] = iso(end)
        row["inputs"]["perp_window_age_s"] = age // 1000
        win = [perp.get(end - (k + 1) * MINUTE) for k in range(WINDOW)][::-1]
        if age > MAX_INPUT_AGE:
            _src(row, "perp_window", end, None, T, "stale")
            for fam in ("flow_liquidity", "price_response"):
                put(fam, f"stale-inputs: latest perp bar closed {age // 60000} min before T")
        elif any(b is None or b["avail"] > T for b in win):
            _src(row, "perp_window", end, None, T, "incomplete")
            for fam in ("flow_liquidity", "price_response"):
                put(fam, "window-incomplete")
        else:
            _src(row, "perp_window", end, max(b["avail"] for b in win), T, "ok")
            flow = sum(2 * b["tbv"] - b["v"] for b in win)
            ret = 1e4 * math.log(win[-1]["c"] / win[0]["o"])
            row["event"] = abs(ret) >= EVENT_BP
            vals = {"flow_btc": round(flow, 4), "ret_15m_bp": round(ret, 3)}
            dstate, depth = _depth(row, snaps, T, end - WINDOW * MINUTE, end)
            if dstate == "ok" and depth < MIN_DEPTH_BTC:
                dstate = f"insufficient-depth ({depth:.3f} BTC)"
            if dstate == "ok":
                vals.update(depth_25bp_btc=round(depth, 3), flow_per_depth=round(flow / depth, 5))
            put("flow_liquidity", dstate, vals)
            for k in ("flow_btc", "ret_15m_bp"):                        # perp-only values stand on their own
                f[k], fs[k] = vals[k], "ok"
            if abs(flow) < MIN_FLOW_BTC:
                put("price_response", "flow-below-threshold")
            else:
                put("price_response", "ok", {"response_bp_per_100btc": round(ret / (flow / 100), 4)})
    _positioning(row, put, perp, oi, oi_by_t, T)
    _funding_and_basis(row, put, snaps, T)
    return row


def _depth(row, snaps, T, w0, w1):
    """(state, depth BTC) from the snapshot whose depth measurement is nearest the flow window [w0, w1]."""
    best, seen = None, False
    for t, a, snap in snaps.recent(T):
        d = snap.get("depth_binance_usdt") or {}
        if not d:
            continue
        seen = True
        m = _measured(snap, "depth_binance_usdt")
        dist = 0 if w0 <= m <= w1 else min(abs(m - w0), abs(m - w1))
        if best is None or dist < best[0]:
            best = (dist, m, a, d)
    if best is None:
        _src(row, "depth", None, None, T, "missing")
        return ("source-missing: no depth snapshot available at T" if not seen else "source-missing"), None
    dist, m, a, d = best
    b25, bst = E.number(d.get("bid_btc_25"), "nonneg")
    a25, ast = E.number(d.get("ask_btc_25"), "nonneg")
    row["inputs"]["depth_snapshot_utc"] = iso(m)
    if d.get("st") != "ok" or bst != "ok" or ast != "ok":
        _src(row, "depth", m, a, T, "malformed")
        return f"invalid-capture: depth ({d.get('st')}, bid {bst}, ask {ast})", None
    if T - m > DEPTH_MAX_AGE:
        _src(row, "depth", m, a, T, "stale")
        return f"stale-depth: measured {(T - m) // 60000} min before T (limit {DEPTH_MAX_AGE // 60000})", None
    if dist > DEPTH_ALIGN:
        _src(row, "depth", m, a, T, "misaligned")
        return f"misaligned-depth: measured {dist // 60000} min from the flow window (limit {DEPTH_ALIGN // 60000})", None
    _src(row, "depth", m, a, T, "ok")
    return "ok", b25 + a25


def _positioning(row, put, perp, oi, oi_by_t, T):
    """OI change over an aligned hour, with the price return and volume of that same hour."""
    cands = oi.recent(T, 24)
    if not cands:
        _src(row, "oi", None, None, T, "missing")
        return put("positioning_interaction", "source-missing: no OI history available at T")
    why = None
    for t_oi, a_oi, f_oi in sorted(cands, key=lambda x: -x[0]):
        if T - t_oi > OI_MAX_AGE:
            why = why or f"stale-oi: newest usable OI stamp {(T - t_oi) // 60000} min before T (limit {OI_MAX_AGE // 60000})"
            break
        then = oi_by_t.get(t_oi - 60 * MINUTE)
        if then is None or then[1] is None or then[1] > T:
            why = "source-missing: OI 1h earlier not available"
            continue
        hour = [perp.get(t_oi - (k + 1) * MINUTE) for k in range(60)][::-1]
        if any(b is None or b["avail"] > T for b in hour):
            why = "window-incomplete (price/volume for the OI hour)"
            continue
        o1, st1 = E.number(f_oi.get("sumOpenInterest"), "nonneg")
        o0, st0 = E.number(then[2].get("sumOpenInterest"), "nonneg")
        _src(row, "oi", t_oi, a_oi, T, "ok" if st1 == st0 == "ok" else "malformed")
        if st1 != "ok" or st0 != "ok" or not o0:
            return put("positioning_interaction", "invalid-capture")
        r1 = 1e4 * math.log(hour[-1]["c"] / hour[0]["o"])
        vol = sum(b["v"] for b in hour)
        d_pct = 100 * (o1 / o0 - 1)
        row["inputs"]["oi_stamp_utc"] = iso(t_oi)
        row["inputs"]["oi_window_utc"] = [iso(t_oi - 60 * MINUTE), iso(t_oi)]
        put("positioning_interaction", "ok" if vol > 0 else "ok (zero volume: per-volume undefined)",
            {"d_oi_1h_pct": round(d_pct, 4), "ret_1h_bp": round(r1, 3), "oi_x_ret": round(d_pct * r1, 4),
             "d_oi_per_volume": round((o1 - o0) / vol, 5) if vol > 0 else None})
        if vol <= 0:
            row["fstate"]["d_oi_per_volume"] = "undefined: zero volume"
        return None
    _src(row, "oi", None, None, T, "stale" if why and why.startswith("stale") else "missing")
    return put("positioning_interaction", why or "source-missing")


def _funding_and_basis(row, put, snaps, T):
    rec = snaps.recent(T, 1)
    if not rec:
        _src(row, "snapshot", None, None, T, "missing")
        put("funding_dispersion", "source-missing: no snapshot available at T")
        return put("spot_perp_basis", "source-missing: no snapshot available at T")
    t, a, snap = rec[0]
    row["inputs"]["snapshot_utc"] = iso(t)
    hl = snap.get("hl_predicted_fundings") or {}
    m = _measured(snap, "hl_predicted_fundings")
    rates = []
    if hl.get("st") == "ok":
        for venue, v in sorted((hl.get("venues") or {}).items()):
            r, st = E.number((v or {}).get("rate"), "funding_rate")
            ih, st2 = E.number((v or {}).get("interval_h"), "price")
            if st == "ok" and st2 == "ok":
                rates.append((venue, 1e4 * r * 8 / ih))
    if T - m > FUNDING_MAX_AGE:
        _src(row, "funding_estimate", m, a, T, "stale")
        put("funding_dispersion", f"stale-funding: estimated {(T - m) // 60000} min before T (limit {FUNDING_MAX_AGE // 60000})")
    elif len(rates) < 2:
        _src(row, "funding_estimate", m, a, T, "insufficient")
        put("funding_dispersion", f"insufficient-venues ({len(rates)})")
    else:
        _src(row, "funding_estimate", m, a, T, "ok")
        vals = [x for _, x in rates]
        row["inputs"]["funding_venues"] = [v for v, _ in rates]
        put("funding_dispersion", "ok (estimated rates)", {"funding_mean_bp_8h": round(sum(vals) / len(vals), 4),
                                                            "funding_dispersion_bp_8h": round(max(vals) - min(vals), 4)})
    mark, mst = E.number((snap.get("binance_usdt_prem") or {}).get("mark"), "price")
    spot, sst = E.number((snap.get("premium_parts") or {}).get("binance_spot_btcusdt"), "price")
    mm, ms = _measured(snap, "binance_usdt_prem"), _measured(snap, "premium_parts")
    if mst != "ok" or sst != "ok":
        _src(row, "basis", None, a, T, "missing" if "missing" in (mst, sst) else "malformed")
        return put("spot_perp_basis", f"source-missing (mark {mst}, spot {sst})")
    if T - min(mm, ms) > BASIS_MAX_AGE:
        _src(row, "basis", min(mm, ms), a, T, "stale")
        return put("spot_perp_basis", f"stale-basis: measured {(T - min(mm, ms)) // 60000} min before T")
    if abs(mm - ms) > BASIS_PAIR:
        _src(row, "basis", min(mm, ms), a, T, "misaligned")
        return put("spot_perp_basis", f"misaligned-basis: mark and spot {abs(mm - ms) // 1000} s apart")
    _src(row, "basis", min(mm, ms), a, T, "ok")
    return put("spot_perp_basis", "ok", {"basis_bp": round(1e4 * (mark / spot - 1), 3)})


def eligible(row, features):
    """(True, []) when every named feature has a value with state ok at this row; otherwise (False, reasons). The
    research API and DIR1 use this, never "any number they find"."""
    why = []
    for k in features:
        st = (row.get("fstate") or {}).get(k)
        if st is None and "fstate" not in row:                   # a fixture row without per-feature states
            st = "ok" if row.get("features", {}).get(k) is not None else "missing"
        if st != "ok" or row.get("features", {}).get(k) is None:
            why.append(f"{k}: {st or 'missing'}")
    return (not why), why


def freeze(panel, sources=None):
    """The admitted identity of a panel: version, policy hash, rows hash, window and source identities."""
    return {"schema": "panel-admitted/1", "version": panel["version"], "policy_sha256": panel.get("policy_sha256"),
            "start_utc": panel["start_utc"], "end_utc": panel["end_utc"], "store_cutoff_utc": panel["store_cutoff_utc"],
            "rows": len(panel["rows"]), "rows_sha256": rows_sha256(panel["rows"]), "sources": sources or {},
            "row_sha256": {r["t_utc"]: hashlib.sha256(E.canon(r).encode()).hexdigest()[:16] for r in panel["rows"]}}


def compare(admitted, rebuilt):
    """Rows whose content differs between an admitted panel and a rebuild: a revision to report, never a silent
    replacement of the admitted version."""
    now = freeze(rebuilt)
    changed = sorted(t for t, h in admitted["row_sha256"].items() if now["row_sha256"].get(t) not in (None, h))
    missing = sorted(t for t in admitted["row_sha256"] if t not in now["row_sha256"])
    return {"identical": now["rows_sha256"] == admitted["rows_sha256"] and admitted["policy_sha256"] == now["policy_sha256"],
            "changed_rows": changed, "missing_rows": missing, "policy_changed": admitted["policy_sha256"] != now["policy_sha256"],
            "rule": "the admitted panel stays the evidence; a rebuild that differs is a new panel version"}


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
