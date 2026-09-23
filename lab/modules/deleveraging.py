"""Module H - exchange deleveraging stress.

Inputs actually available to this repository:
  OKX BTC-USDT swap liquidation orders (collector since 2.0; OKX retains ~24 h, so history exists
  only as collected). Each order carries bkPx, the BANKRUPTCY price, not an execution price; the
  notional here is size x bkPx and is labelled as such.
  OKX insurance fund, BTC-USDT swap family (collector 2.7): balance rows and every
  liquidation-deposit, bankruptcy-loss and ADL row since the previous run; pool membership is
  the instrument family as returned; publication lag = observed_at - row ts, measured per row.
Not available here (recorded, not substituted): Bybit liquidation / ADL / insurance feeds (HTTP 403
from this environment; the streaming service documents them for an eligible host); Deribit
liquidation flags (hidden from the public for the first hour after a trade); Binance insurance
data (no documented public endpoint used).

Event: 5-minute OKX long (short) liquidation notional >= its trailing 7-day 99th percentile ->
"burst". Test group: bursts with an insurance-fund bankruptcy-loss or ADL row within +-15 minutes
("stressed_burst"); reference: other bursts ("plain_burst"). Direction: -1 for long liquidations,
+1 for short. This asks what insurance/ADL information adds beyond the liquidations themselves.
"""
from lab.common import BASIS_PROSPECTIVE, DAY, MINUTE, PROCESSING_LATENCY_MS, hash_inputs
from lab.events import event_record, hourly_controls

ID = "deleveraging"
VERSION = "H-1"
BUCKET = 5 * MINUTE
SPEC = {"module": "H", "id": ID, "version": VERSION, "title": "Exchange deleveraging stress",
        "hypothesis": "Liquidation bursts accompanied by insurance-fund draws or ADL carry information about "
                      "subsequent returns beyond the liquidations themselves.",
        "inputs": ["data/liq/orders (OKX, bankruptcy price)", "data/okx_insurance"],
        "event": "5-minute OKX long/short liquidation notional >= trailing 7-day p99; split by insurance/ADL rows",
        "outcome": "net log return in the liquidation direction (continuation)",
        "baseline": "plain bursts; hourly controls; regression on prior return, volatility, funding",
        "exclusions": ["buckets before 7 days of collected liquidation history",
                       "Bybit/Deribit/Binance deleveraging data (not available to this collector)"]}


def run(lab, params):
    """Each bucket is judged at T = max(first observation of its orders, bucket close), using only
    orders observed by T - for the bucket itself and for the trailing threshold - so liquidations
    reported late (OKX revises for hours) never leak into an earlier decision, and a bucket is never
    judged before it has ended."""
    import bisect
    orders = lab.store.liq_orders()
    ins = lab.store.okx_insurance()
    bars = lab.store.bars("binance_klines_1m_BTCUSDT_perp")
    per = {}                                      # bucket -> side -> sorted [(avail, notional)]
    for o in orders:
        side = "long" if o.get("posSide") == "long" else "short"
        per.setdefault(o["t"] // BUCKET * BUCKET, {"long": [], "short": []})[side].append(
            (o["avail"], (o.get("btc") or 0) * (o.get("bkPx") or 0)))
    cum = {}
    for t, sides in per.items():
        for side, xs in sides.items():
            xs.sort()
            run_sum, pts = 0.0, []
            for a, v in xs:
                run_sum += v
                pts.append((a, run_sum))
            cum[(t, side)] = pts

    def as_of(t, side, T):
        pts = cum.get((t, side))
        if not pts:
            return 0.0
        i = bisect.bisect_right(pts, (T, float("inf")))
        return pts[i - 1][1] if i else 0.0
    stress = [(r["t"], r["type"]) for r in ins if r["type"] in ("bankruptcy_loss", "adl")]
    lags = [r["observed_at"] - r["t"] for r in ins]
    events = []
    span = (max(per) - min(per)) / DAY if per else 0
    thr_cache = {}
    for t in sorted(per):
        for side, direction in (("long", -1), ("short", 1)):
            pts = cum.get((t, side))
            if not pts:
                continue
            T = max(pts[0][0], t + BUCKET)         # judged once the bucket has closed AND been observed
            value = as_of(t, side, T)
            window = range(t - 2016 * BUCKET, t, BUCKET)
            if t - 2016 * BUCKET < min(per):
                continue
            key = (side, T // 3_600_000)
            if key not in thr_cache:
                vals = sorted(as_of(b, side, T) for b in window)
                thr_cache[key] = vals[int(0.99 * (len(vals) - 1))]
            thr = thr_cache[key]
            if value >= thr and value > 0:
                near = [k for ts, k in stress if abs(ts - (t + BUCKET)) <= 15 * MINUTE]
                ins_avail = [r["observed_at"] for r in ins if abs(r["t"] - (t + BUCKET)) <= 15 * MINUTE
                             and r["type"] in ("bankruptcy_loss", "adl")]
                avail = max([T] + ins_avail)
                events.append(event_record(ID, VERSION, t + BUCKET, T, avail + PROCESSING_LATENCY_MS,
                                           direction, "stressed_burst" if near else "plain_burst",
                                           {"side": side, "notional_usd_at_bankruptcy_px": value, "threshold": thr,
                                            "insurance_rows": near, "late_revision_usd": as_of(t, side, float("inf")) - value},
                                           hash_inputs([t, side, value, near]), BASIS_PROSPECTIVE, {},
                                           {"price_basis": "bankruptcy price"}, lab.code))
    controls = hourly_controls(bars, ID, VERSION, lab.code, BASIS_PROSPECTIVE)
    need = 7
    state = "available" if span >= need and ins else "insufficient_data"
    reasons = []
    if span < need:
        reasons.append(f"{span:.1f} days of collected OKX liquidation history; the p99 threshold needs {need}")
    if not ins:
        reasons.append("no OKX insurance-fund rows stored yet (collector 2.7)")
    return {"module": ID, "passes": [{"basis": "prospective", "events": events, "controls": controls,
                                      "coverage": {"liquidation_orders": len(orders), "buckets": len(per),
                                                   "insurance_rows": len(ins), "stress_rows": len(stress),
                                                   "publication_lag_ms_median": sorted(lags)[len(lags) // 2] if lags else None,
                                                   "unavailable_sources": ["bybit (HTTP 403 here)", "deribit liquidation flag (1h public delay)",
                                                                           "binance insurance fund"]},
                                      "bars": bars, "state": state, "reasons": reasons}]}
