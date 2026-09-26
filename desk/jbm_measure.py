#!/usr/bin/env python3
"""jbm_measure — deterministic measurement functions for the JBM crypto desk.

Version: measure-11.1.0 (package 11.1, Sep 26 2026; 11.1 changes only the default precedence rule). Stdlib only. Status: implemented and tested
offline (test_jbm_measure.py); deployed only when a fresh thread runs the tests from the mounted
skill folder (runbook §D).

Why this module exists: the desk rebuilt these calculations in every thread, and four formula
defects survived rule-text corrections (cases.md §4 roots). One implementation, one version, one
fixture set. A change to any computation here is a new VERSION.

Units convention (methods.md M-10):
  * Every volatility estimator returns a SIGMA of 4H LOG returns (dimensionless, per bar).
  * A range is ln(H/L) of a bar (dimensionless) and is never a sigma. E[range] ~= 1.596 sigma for a
    Brownian bar, so a range in a sigma slot overstates by construction.
  * Comparisons and model scaling happen in log units. Price units (points) are produced only by
    to_points(), at a stated reference price, for reporting.
The Measure class carries kind ('sigma'|'range') and unit ('log'|'points'); functions that need a
log sigma refuse anything else. That refusal is the fixture that catches a range-for-sigma or a
unit substitution.

Thresholds marked PROVISIONAL are operator policy, not measurements (methods.md §0 scope table).
"""
from __future__ import annotations

import datetime as dt
import math
import statistics
from dataclasses import dataclass, field

VERSION = "measure-11.1.0"
BARS_PER_YEAR_4H = 365 * 6
BROWNIAN_RANGE_OVER_SIGMA = 2.0 * math.sqrt(2.0 / math.pi)  # 1.5958


# --------------------------------------------------------------------------------------------
# Tagged measurements
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Measure:
    value: float
    kind: str          # "sigma" | "range"
    unit: str          # "log" | "points"
    name: str
    ref_price: float | None = None   # set when unit == "points"

    def __post_init__(self):
        if self.kind not in ("sigma", "range"):
            raise ValueError(f"kind must be sigma or range, not {self.kind!r}")
        if self.unit not in ("log", "points"):
            raise ValueError(f"unit must be log or points, not {self.unit!r}")
        if not math.isfinite(self.value) or self.value < 0:
            raise ValueError(f"{self.name}: value must be finite and >= 0, got {self.value!r}")


def _require(m: Measure, kind: str, unit: str = "log") -> Measure:
    if not isinstance(m, Measure):
        raise TypeError(f"expected a Measure({kind}, {unit}); got a bare {type(m).__name__} — tag it")
    if m.kind != kind:
        raise TypeError(f"{m.name} is a {m.kind}; a {kind} is required (a range is never a sigma)")
    if m.unit != unit:
        raise TypeError(f"{m.name} is in {m.unit}; {unit} units are required here")
    return m


def to_points(m: Measure, ref_price: float) -> Measure:
    """Log measure -> points at a stated reference price (first order: points = ref x log value).
    The reference is the decision-time close of the series the estimator ran on."""
    _require(m, m.kind, "log")
    if not (math.isfinite(ref_price) and ref_price > 0):
        raise ValueError("ref_price must be finite and > 0")
    return Measure(m.value * ref_price, m.kind, "points", m.name + "_pts", ref_price)


def barrier_prices(ref_price: float, k: float, sigma: Measure) -> tuple[float, float]:
    """Exact barrier prices at +/- k sigma in log space: ref x exp(-k s), ref x exp(+k s)."""
    s = _require(sigma, "sigma").value
    return ref_price * math.exp(-k * s), ref_price * math.exp(k * s)


def sigma_distance(price: float, line: float, sigma: Measure) -> float:
    """Distance of a line from price in sigma units (log): |ln(line/price)| / sigma."""
    s = _require(sigma, "sigma").value
    if s <= 0:
        raise ValueError("sigma must be > 0")
    return abs(math.log(line / price)) / s


# --------------------------------------------------------------------------------------------
# Volatility estimators (4H bars, closed bars only — the caller drops the forming bar)
# --------------------------------------------------------------------------------------------
def _finite_pos(xs, what):
    xs = list(xs)
    for x in xs:
        if not (isinstance(x, (int, float)) and math.isfinite(x) and x > 0):
            raise ValueError(f"{what}: every value must be finite and > 0, got {x!r}")
    return xs


def sd_c2c(closes, name="sd_c2c_4h_7d", min_returns=42) -> Measure:
    """Sample sd (ddof=1) of close-to-close log returns. 43 closes -> 42 returns = 7d of 4H bars."""
    c = _finite_pos(closes, name)
    r = [math.log(b / a) for a, b in zip(c, c[1:])]
    if len(r) < min_returns:
        raise ValueError(f"{name}: {len(r)} returns < floor {min_returns}")
    return Measure(statistics.stdev(r), "sigma", "log", name)


def sd_parkinson(highs, lows, name="sd_parkinson_4h_7d", min_bars=1) -> Measure:
    """Parkinson: sqrt(mean(ln(H/L)^2) / (4 ln 2)). Log units."""
    h, l = _finite_pos(highs, name), _finite_pos(lows, name)
    if len(h) != len(l) or len(h) < min_bars:
        raise ValueError(f"{name}: need >= {min_bars} paired bars")
    if any(a < b for a, b in zip(h, l)):
        raise ValueError(f"{name}: a high below its low")
    return Measure(math.sqrt(sum(math.log(a / b) ** 2 for a, b in zip(h, l)) / len(h) / (4 * math.log(2))),
                   "sigma", "log", name)


def log_range(high: float, low: float) -> float:
    h, l = _finite_pos([high, low], "log_range")
    if h < l:
        raise ValueError("high below low")
    return math.log(h / l)


def range_realized(highs, lows, name="range_realized_4h_6") -> Measure:
    """Median ln(H/L) over the bars given. A RANGE — its own field, never a denominator."""
    return Measure(statistics.median(log_range(a, b) for a, b in zip(highs, lows)), "range", "log", name)


def implied_sigma_4h(dvol_pct: float, name="implied_4h") -> Measure:
    """DVOL (annualised %, 30-day) -> 4H log sigma = DVOL/100 / sqrt(365*6). Uniform variance:
    blind to variance concentrated in one release."""
    if not (math.isfinite(dvol_pct) and dvol_pct > 0):
        raise ValueError("dvol_pct must be finite and > 0")
    return Measure(dvol_pct / 100.0 / math.sqrt(BARS_PER_YEAR_4H), "sigma", "log", name)


def range_in_expected_ranges(rng: Measure, sigma: Measure) -> float:
    """A live or trailing range expressed as a multiple of the range a Brownian bar at `sigma`
    would print (1.596 sigma). This is how a range is reported beside a sigma — never instead of it."""
    return _require(rng, "range").value / (BROWNIAN_RANGE_OVER_SIGMA * _require(sigma, "sigma").value)


# Used only by rule="house-10.2" (the pre-O21 house rule, kept for reproduction).
COMPRESSION_RATIO = 2.0


def operative_sigma(c2c: Measure, park6: Measure, implied: Measure | None = None,
                    print_within_24h: bool = False, rule: str = "o21") -> tuple[Measure, str]:
    """M-10 precedence. Every input must be a log sigma; a range raises TypeError.
    rule="o21" (default from 11.1): O21 stage 1 ranked sd_parkinson_4h_6 first for the next-4H range on
    validation and holdout, so it is the default; inside 24h of a print the implied figure still governs
    (policy pending O7 — stage 1 did not isolate release bars). rule="house-10.2" reproduces the old rule."""
    if rule not in ("o21", "house-10.2"):
        raise ValueError("rule must be o21 or house-10.2")
    _require(c2c, "sigma"); _require(park6, "sigma")
    if implied is not None:
        _require(implied, "sigma")
    if print_within_24h:
        if implied is None:
            raise ValueError("inside 24h of a scheduled print the implied figure is required")
        return implied, "implied: scheduled print inside 24h"
    if rule == "o21":
        return park6, "default: Parkinson 6-bar (O21 stage 1)"
    if park6.value > 0 and c2c.value > COMPRESSION_RATIO * park6.value:
        return park6, f"compression: c2c/park6 = {c2c.value / park6.value:.2f} > {COMPRESSION_RATIO}"
    return c2c, "default: close-to-close 7d"


def scale_factor_k(operative: Measure, full_sample: Measure) -> float:
    """Path/range model scaling k = operative sigma / full-sample sigma, both log sigmas."""
    return _require(operative, "sigma").value / _require(full_sample, "sigma").value


# --------------------------------------------------------------------------------------------
# Calendar arithmetic
# --------------------------------------------------------------------------------------------
def roll_off_exit(bar_open: dt.datetime, window_bars: int = 42, bar_hours: int = 4) -> dt.datetime:
    """A bar leaves a trailing window at the close of the bar that opens window x bar_hours after
    it: open + window*bar_hours + bar_hours (the 42-bar 4H window: open + 7d + 4h)."""
    return bar_open + dt.timedelta(hours=window_bars * bar_hours + bar_hours)


def countdown(now: dt.datetime, event: dt.datetime) -> tuple[int, int]:
    """(hours, minutes) from now to a verified event timestamp; never recalled."""
    s = int((event - now).total_seconds())
    if s < 0:
        raise ValueError("event is in the past")
    return s // 3600, (s % 3600) // 60


# --------------------------------------------------------------------------------------------
# Small-sample uncertainty
# --------------------------------------------------------------------------------------------
def upper_limit_zero(n: int, conf: float = 0.95) -> float:
    """One-sided exact upper limit for 0 successes in n: 1 - (1-conf)^(1/n)."""
    return 1.0 - (1.0 - conf) ** (1.0 / n)


def _binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def clopper_pearson(k: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    """Two-sided exact interval by bisection on the binomial CDF."""
    a = (1 - conf) / 2

    def solve(f, lo=0.0, hi=1.0):
        for _ in range(200):
            mid = (lo + hi) / 2
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve(lambda p: a - (1 - _binom_cdf(k - 1, n, p)))
    upper = 1.0 if k == n else solve(lambda p: _binom_cdf(k, n, p) - a)
    return lower, upper


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


# --------------------------------------------------------------------------------------------
# Positioning arithmetic (M-04, methods §6)
# --------------------------------------------------------------------------------------------
def share_from_ratio(r: float) -> float:
    """Long/short ratio -> long share r/(1+r). Domain: finite r >= 0 (0 is legitimate: no longs)."""
    if isinstance(r, bool) or not isinstance(r, (int, float)) or not math.isfinite(r):
        raise ValueError(f"ratio must be a finite number, got {r!r}")
    if r < 0:
        raise ValueError(f"ratio must be >= 0, got {r!r}")
    return r / (1.0 + r)


def synthetic_index(oi: float, a: float, b: float) -> float:
    """S = OI x (a - b). A composition index, not a flow; it scales with OI."""
    return oi * (a - b)


def size_concentration(p: float, a: float) -> float:
    """Mean long size / mean short size within one cohort = [p/(1-p)] / [a/(1-a)]."""
    for x, nm in ((p, "p"), (a, "a")):
        if not (0 < x < 1):
            raise ValueError(f"{nm} must be in (0, 1)")
    return (p / (1 - p)) / (a / (1 - a))


# --------------------------------------------------------------------------------------------
# Funding adapters (methods §5; runbook §B)
# --------------------------------------------------------------------------------------------
def funding_binance_family(premium: float, interest: float = 0.0001, cap: float = 0.0005) -> float:
    """F = P + clamp(interest - P, -cap, +cap), per 8h, as fractions."""
    return premium + max(-cap, min(cap, interest - premium))


def premium_from_rate(f: float, interest: float = 0.0001, cap: float = 0.0005, tol: float = 1e-12):
    """Invert F to P only where unique: outside the dead zone. Returns None when F is pinned."""
    if abs(f - interest) <= tol:
        return None
    return f - cap if f < interest else f + cap


def hyperliquid_rates(premium: float) -> tuple[float, float]:
    """Hyperliquid computes an 8h rate and pays one eighth hourly: (F_8h, hourly cash rate)."""
    f8 = funding_binance_family(premium)
    return f8, f8 / 8.0


# --------------------------------------------------------------------------------------------
# Position arithmetic (methods A-06, A-09)
# --------------------------------------------------------------------------------------------
def implied_add_price(q0: float, e0: float, q1: float, e1: float) -> float:
    if q1 == q0:
        raise ValueError("no size change")
    return (q1 * e1 - q0 * e0) / (q1 - q0)


def add_valuation(outside_cash: float, margin: float, add: float, hold_pnl, add_pnl, probs=None) -> dict:
    """Wealth-constant comparison of a margin-only add (A-09). Paths are P&L per path; a path whose
    P&L <= -margin is liquidated (equity floored at zero). Returns E[W_hold], E[W_add], marginal and
    its two deterministic components: -C x P(liq|add) and the loss avoided on converted paths."""
    n = len(hold_pnl)
    if n != len(add_pnl) or n == 0:
        raise ValueError("paths must pair")
    probs = probs or [1.0 / n] * n
    w_hold = [outside_cash + max(margin + x, 0.0) for x in hold_pnl]
    w_add = [outside_cash - add + max(margin + add + x, 0.0) for x in add_pnl]
    liq_add = [margin + add + x <= 0 for x in add_pnl]
    liq_hold = [margin + x <= 0 for x in hold_pnl]
    e_hold = sum(p * w for p, w in zip(probs, w_hold))
    e_add = sum(p * w for p, w in zip(probs, w_add))
    avoided = sum(p * (wa - wh) for p, wa, wh, lh, la in zip(probs, w_add, w_hold, liq_hold, liq_add)
                  if lh and not la)
    return {"E_W_hold": e_hold, "E_W_add": e_add, "marginal": e_add - e_hold,
            "minus_C_Pliq_add": -add * sum(p for p, l in zip(probs, liq_add) if l),
            "loss_avoided": avoided}


def cash_yield_foregone(amount: float, annual_rate: float, hours: float) -> float:
    return amount * annual_rate * hours / 8760.0


def ratio_stress_pnl(qty: float, entry: float, analysed_line: float, ratio: float) -> float:
    """Cross-asset position P&L if the analysed asset sits at its line and the ratio is stressed."""
    return (analysed_line * ratio - entry) * qty


# --------------------------------------------------------------------------------------------
# Cross-venue OI deltas: concentration and the venue hold-out (methods R-03)
# --------------------------------------------------------------------------------------------
def _valid(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x >= 0


def gross_net(deltas: dict) -> dict:
    gross = sum(abs(v) for v in deltas.values())
    net = sum(deltas.values())
    out = {"gross": gross, "net": net, "gross_share": {}, "net_contribution": {}}
    for k, v in deltas.items():
        out["gross_share"][k] = abs(v) / gross if gross else 0.0
        out["net_contribution"][k] = v / net if net else None   # unstable near zero: reported as None at 0
    if deltas:
        top = max(deltas, key=lambda k: abs(deltas[k]))
        out["largest"] = top
        out["net_ex_largest"] = net - deltas[top]
    return out


@dataclass
class _Hold:
    ref_level: float
    jump: float
    session: str
    confirms: int = 0
    for_session: bool = False


@dataclass
class VenueHoldout:
    """Operational hold-out rule for a book that swings without a price cause (methods R-03).

    Policy (PROVISIONAL unless noted):
      anomaly    = gross share > GROSS_SHARE (rule, 10.2) AND |ln price change between the two
                   snapshots| < PRICE_CAUSE_SIGMA x operative 4H log sigma x sqrt(interval / 4h).
                   With no sigma supplied the price leg cannot be decided: the gross-share leg alone
                   applies and the report says so.
      reference  = the venue's level in the last snapshot before the flag.
      persistence= at each of the next PERSIST_SNAPSHOTS snapshots the level stays on the jump's side
                   of the reference by >= PERSIST_FRACTION x |jump|. Persisted -> restored, and its
                   cumulative change since the reference enters the net once, at restoration.
                   Otherwise -> resolved as noise and re-based at the current level; the jump never
                   enters the net.
      session    = UTC calendar day. A venue flagged twice in one session is held for the rest of it
                   and re-based at its first snapshot of the next session.
      coverage   = included books / valid books, and included OI / valid OI, every step.
    """
    GROSS_SHARE: float = 0.45
    PRICE_CAUSE_SIGMA: float = 0.5
    PERSIST_FRACTION: float = 0.5
    PERSIST_SNAPSHOTS: int = 2
    holds: dict = field(default_factory=dict)
    flags: dict = field(default_factory=dict)     # (venue, session) -> count

    @staticmethod
    def session_of(ts: dt.datetime) -> str:
        return ts.astimezone(dt.timezone.utc).date().isoformat()

    def step(self, ts: dt.datetime, prev: dict, cur: dict, log_price_change: float | None = None,
             sigma_4h_log: float | None = None, interval_hours: float | None = None) -> dict:
        sess = self.session_of(ts)
        inter = sorted(v for v in cur if v in prev and _valid(prev[v]) and _valid(cur[v]))
        excluded = sorted(set(prev) ^ set(cur) | {v for v in cur if v in prev and v not in inter})
        deltas = {v: cur[v] - prev[v] for v in inter}
        g = gross_net(deltas)
        report = {"session": sess, "intersection": inter, "excluded_invalid_or_missing": excluded,
                  "held": {}, "restored": {}, "resolved_noise": [], "flagged": [], "price_leg": None}
        contrib = {}
        # 1. venues already held
        for v in list(self.holds):
            h = self.holds[v]
            if v not in inter:
                report["held"][v] = "held; missing this snapshot"
                continue
            if h.for_session:
                if sess != h.session:
                    del self.holds[v]
                    report["resolved_noise"].append(v + " (session ended; re-based)")
                else:
                    report["held"][v] = "held for session (flagged twice)"
                continue
            d = cur[v] - h.ref_level
            same_side = d * h.jump > 0 and abs(d) >= self.PERSIST_FRACTION * abs(h.jump)
            if not same_side:
                del self.holds[v]
                report["resolved_noise"].append(v)
                continue
            h.confirms += 1
            if h.confirms >= self.PERSIST_SNAPSHOTS:
                contrib[v] = d
                report["restored"][v] = d
                del self.holds[v]
            else:
                report["held"][v] = f"persistence {h.confirms}/{self.PERSIST_SNAPSHOTS}"
        # 2. new anomalies among venues not held and not just restored/resolved
        price_leg = None
        if log_price_change is not None and sigma_4h_log and interval_hours:
            thr = self.PRICE_CAUSE_SIGMA * sigma_4h_log * math.sqrt(interval_hours / 4.0)
            price_leg = abs(log_price_change) < thr
            report["price_leg"] = f"|r|={abs(log_price_change):.5f} vs {thr:.5f}: " + (
                "no price cause" if price_leg else "price cause present")
        else:
            report["price_leg"] = "undetermined (no sigma/interval) — gross-share leg only"
        touched = set(report["restored"]) | {x.split(" ")[0] for x in report["resolved_noise"]}
        for v in inter:
            if v in self.holds or v in touched:
                continue
            if g["gross"] and g["gross_share"][v] > self.GROSS_SHARE and price_leg is not False:
                key = (v, sess)
                self.flags[key] = self.flags.get(key, 0) + 1
                self.holds[v] = _Hold(prev[v], deltas[v], sess, for_session=self.flags[key] >= 2)
                report["flagged"].append(v)
                report["held"][v] = "held for session (flagged twice)" if self.flags[key] >= 2 else "flagged"
                continue
            contrib[v] = deltas[v]
        # venues resolved as noise this step re-enter next step; their delta this step is excluded
        included = [v for v in inter if v in contrib]
        valid_oi = sum(cur[v] for v in inter)
        report.update(
            net_all=g["net"], gross_all=g["gross"],
            net_ex_held=sum(contrib.values()),
            coverage_books=f"{len(included)}/{len(inter)}",
            coverage_oi=(sum(cur[v] for v in included) / valid_oi) if valid_oi else None,
            code_version=VERSION)
        return report
