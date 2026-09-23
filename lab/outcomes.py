"""Idempotent outcome labels with an explicit, versioned cost model.

Entry convention (never earlier than the decision could have been made):
  entry bar = the first 1-minute bar whose OPEN time is >= t_available rounded up to the minute;
  entry price = that bar's open (Binance USD-M BTCUSDT last-trade bars).
Exit at horizon h: the open of the bar starting at entry + h, i.e. the close of the last bar inside
the horizon. All bars in [entry, entry + h] must be stored; otherwise the label is
  immature   the horizon (or its bars) has not arrived yet: retry later, nothing stored;
  incomplete the time has passed but bars are missing: unscorable, nothing stored, retried later.
Measures for direction d (+1 long, -1 short), all in natural-log units:
  ret        d * ln(exit / entry)
  range      ln(max high / min low) over the horizon's bars
  mfe / mae  best favourable / worst adverse excursion, d-aware, from highs and lows
  rv         realised volatility: sqrt(sum of squared 1-minute close-to-close log returns)
  ret_net    ret - fees - spread - slippage + funding (funding: settled events in (entry, exit];
             longs pay positive rates)
COST_MODEL values are ASSUMPTIONS stated for review, not venue quotes verified in this release:
taker fee 5.0 bp per side (Binance USD-M regular-tier taker rate as commonly published; not
re-verified here - the fee page did not render for automated retrieval on 2026-09-23), slippage
1.0 bp per side, half-spread from the nearest prior depth snapshot (<= 15 min old; else 0.5 bp).
"""
import math

from lab.common import H, HORIZONS_MIN, MINUTE, ceil_minute

COST_MODEL = {"version": "costs-1", "taker_fee_bp_per_side": 5.0, "slippage_bp_per_side": 1.0,
              "default_half_spread_bp": 0.5, "max_spread_age_ms": 15 * MINUTE,
              "funding": "Binance BTCUSDT settled 8h rates in (entry, exit]; longs pay positive",
              "status": "assumption; verify fees before relying on net figures"}


def half_spread_bp(snaps, t):
    """Half-spread in basis points from the Binance USD-M depth snapshot nearest before t."""
    best = None
    for s in snaps:
        if s["t"] > t:
            break
        best = s
    if best is None or t - best["t"] > COST_MODEL["max_spread_age_ms"]:
        return COST_MODEL["default_half_spread_bp"], "default"
    d = best.get("depth_binance_usdt") or {}
    bid, ask = d.get("best_bid"), d.get("best_ask")
    if d.get("st") != "ok" or not bid or not ask or ask <= bid:
        return COST_MODEL["default_half_spread_bp"], "default"
    mid = (bid + ask) / 2
    return (ask - bid) / 2 / mid * 1e4, "snapshot"


def label(t_available, direction, bars, now, horizons=HORIZONS_MIN, funding=(), half_spread=None):
    """Labels for each horizon: {h: {...}} with status complete / immature / incomplete."""
    entry_t = ceil_minute(t_available)
    out = {}
    entry = bars.get(entry_t)
    latest = max(bars) if bars else None          # bars not yet written by the collector are not "missing"
    for hmin in horizons:
        end_t = entry_t + hmin * MINUTE
        if end_t + MINUTE > now or latest is None or end_t > latest:
            out[hmin] = {"status": "immature"}
            continue
        seq = [bars.get(entry_t + i * MINUTE) for i in range(hmin + 1)]
        if entry is None or any(b is None for b in seq):
            out[hmin] = {"status": "incomplete", "missing": sum(1 for b in seq if b is None)}
            continue
        inside = seq[:-1]
        exit_px = seq[-1]["o"]
        px0 = entry["o"]
        hi, lo = max(b["h"] for b in inside), min(b["l"] for b in inside)
        ret = direction * math.log(exit_px / px0)
        fav = math.log(hi / px0) if direction > 0 else -math.log(lo / px0)
        adv = math.log(lo / px0) if direction > 0 else -math.log(hi / px0)
        closes = [px0] + [b["c"] for b in inside]
        rv = math.sqrt(sum(math.log(b / a) ** 2 for a, b in zip(closes, closes[1:])))
        fees = 2 * COST_MODEL["taker_fee_bp_per_side"] / 1e4
        slip = 2 * COST_MODEL["slippage_bp_per_side"] / 1e4
        hs = half_spread if half_spread is not None else COST_MODEL["default_half_spread_bp"]
        spread = 2 * hs / 1e4
        fund = -direction * sum(rate for t, rate in funding if entry_t < t <= end_t)
        out[hmin] = {"status": "complete", "entry_t": entry_t, "entry_px": px0, "exit_t": end_t, "exit_px": exit_px,
                     "ret": ret, "range": math.log(hi / lo), "mfe": fav, "mae": adv, "rv": rv,
                     "costs": {"fees": fees, "slippage": slip, "spread": spread, "funding_pnl": fund},
                     "ret_net": ret - fees - slip - spread + fund}
    return out


def mature_by(t_available, horizon_min):
    return ceil_minute(t_available) + (horizon_min + 1) * MINUTE


__all__ = ["COST_MODEL", "label", "half_spread_bp", "mature_by", "H"]
