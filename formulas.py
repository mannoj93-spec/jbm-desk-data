"""formulas.py — the desk's closed-form arithmetic, one implementation, fixture-tested.

Each function is the subject of a runbook.md §G numerical fixture; test_fixtures.py must pass
before any of them is quoted as `tested` (runbook §D states). Stdlib only. The path model
(runbook §F, requirement 40) is not here: it gets its own versioned module and fixtures.
"""
import datetime as dt
import math

VERSION = "formulas-1.0-2026-09-22"


def parse_iso(s):
    d = dt.datetime.fromisoformat(s.strip().replace("Z", "+00:00"))
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return int(d.timestamp() * 1000)


def share_from_ratio(r):
    """Binance longShortRatio → long share. Shares are composition, not contract counts."""
    return r / (1.0 + r)


def synthetic_index(oi, long_share, short_share):
    """S = OI × (a − b). Labelled synthetic; not a flow."""
    return oi * (long_share - short_share)


def size_concentration(notional_long_share, account_long_share):
    """Mean long size ÷ mean short size within one cohort = ratio of odds.
    Assumes both shares describe the same cohort. The retired p/a is not this ratio."""
    p, a = notional_long_share, account_long_share
    return (p / (1 - p)) / (a / (1 - a))


def zero_of_n_upper(n, alpha=0.05, two_sided=False):
    """Exact upper limit for 0 successes in n trials."""
    a = alpha / 2 if two_sided else alpha
    return 1 - a ** (1.0 / n)


def rule_of_three(n):
    return 3.0 / n


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def hyperliquid_funding(premium, interest=0.0001, band=0.0005, hourly_cap=0.04):
    """Hyperliquid: 8h formula, paid hourly at one eighth. Returns (formula_rate_8h, cash_rate_1h).
    The API `funding` field is already the hourly cash rate — never ÷8 it again."""
    f8 = premium + clamp(interest - premium, -band, band)
    h = clamp(f8 / 8.0, -hourly_cap, hourly_cap)
    return f8, h


def binance_family_funding(premium, interest=0.0001, band=0.0005):
    """Binance/Bybit/Bitget/Gate 8h form, before outer caps."""
    return premium + clamp(interest - premium, -band, band)


def premium_identifiable(rate, interest=0.0001, band=0.0005, tol=1e-9):
    """False when the rate sits on the dead-zone pin (the premium is not identified by the rate)."""
    return abs(rate - interest) > tol


def countdown(start_iso, end_iso):
    m = (parse_iso(end_iso) - parse_iso(start_iso)) // 60000
    return f"{m // 60}h {m % 60:02d}m"


def gaussian_range_over_sigma():
    """E[high − low] of a Brownian bar ÷ σ = 2·sqrt(2/π) ≈ 1.596. Why a range never enters a σ slot."""
    return 2.0 * math.sqrt(2.0 / math.pi)


def add_valuation(outside_cash, margin, add, paths, yield_annual=0.0, hours=0.0):
    """Wealth-consistent margin-add valuation (A-09). Total wealth held constant across branches.
    paths: list of dicts {hold_pnl, hold_liq, add_pnl, add_liq}, equiprobable.
    A liquidated branch loses its whole margin (margin, or margin+add). Collateral incurs no funding;
    funding belongs in the path P&L (charged on notional over survival). Yield foregone is on `add`."""
    n = len(paths)
    w0 = outside_cash + margin
    wh = [w0 + (-margin if p["hold_liq"] else p["hold_pnl"]) for p in paths]
    wa = [w0 + (-(margin + add) if p["add_liq"] else p["add_pnl"]) for p in paths]
    e_h, e_a = sum(wh) / n, sum(wa) / n
    p_liq_add = sum(1 for p in paths if p["add_liq"]) / n
    avoided = sum((p["add_pnl"] - (-margin)) for p in paths if p["hold_liq"] and not p["add_liq"]) / n
    yield_foregone = add * yield_annual * hours / 8760.0
    other = (e_a - e_h) - (-add * p_liq_add + avoided)
    return {"E_hold": e_h, "E_add": e_a, "marginal_before_yield": e_a - e_h,
            "minus_C_Pliq": -add * p_liq_add, "loss_avoided": avoided, "other_paths": other,
            "yield_foregone": yield_foregone, "marginal_after_yield": e_a - e_h - yield_foregone}
