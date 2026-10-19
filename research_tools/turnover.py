"""Turnover control for a sizing policy (turnover-1.0.0, repo 2.29; brief section 16) - the arithmetic of the prepared
PS1 successor (research/registrations/ps1-t1-prepared/). PS1 itself is untouched.

apply_band(targets, band, every=1) -> holdings: start at 0; at each decision k (every `every`-th decision only) trade
to the target if |target - holding| > band, else hold (a no-trade band; band = 0 reproduces PS1's rebalance-every-time).
simulate(targets, prices, band, fee_bp, slippage_bp, every=1) -> net log returns per interval, costs and turnover, on
the same paper conventions as PS1 (costs on traded notional, charged in the interval a trade opens). Paper only.
"""
import math

VERSION = "turnover-1.0.0"


def apply_band(targets, band, every=1):
    if band < 0 or every < 1:
        raise ValueError("band >= 0 and every >= 1")
    h, out = 0.0, []
    for k, w in enumerate(targets):
        if w is None or not math.isfinite(w):
            out.append(h)                         # a missing target holds (it never invents a trade)
            continue
        if k % every == 0 and abs(w - h) > band:
            h = w
        out.append(h)
    return out


def simulate(targets, prices, band, fee_bp, slippage_bp, every=1):
    """prices: interval-boundary prices p_0..p_n (len n+1 for n targets). Returns per-interval net log returns."""
    if len(prices) != len(targets) + 1:
        raise ValueError("need one more price than targets")
    hold = apply_band(targets, band, every)
    prev, rets, costs, turnover = 0.0, [], 0.0, 0.0
    for k, h in enumerate(hold):
        traded = abs(h - prev)
        c = traded * (fee_bp + slippage_bp) / 1e4
        gross = h * (prices[k + 1] / prices[k] - 1)
        rets.append(math.log(max(1e-12, (1 - c) * (1 + gross))))
        costs += c
        turnover += traded
        prev = h
    return {"version": VERSION, "band": band, "every": every, "net_log_returns": rets, "cost_fraction": costs,
            "turnover": turnover, "trades": sum(1 for a, b in zip([0.0] + hold, hold) if a != b)}
