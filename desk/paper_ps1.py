#!/usr/bin/env python3
"""paper_ps1 — the prospective paper sizing experiment PS1 (repo 2.20; protocol desk/research/ps1/protocol.json).

A SIMULATION on captured quotes. It tests whether sizing a synthetic, unlevered BTC spot long by the registered
RC1D B2 4h range forecast beats sizing by trailing Parkinson volatility (primary) and a fixed weight (control),
after costs. It places no order, holds no credential, and its results are never an entry endorsement.

  decide    for the latest 4H decision: read the eligible RC1D 4h forecast (range_reader.read_current) and its
            verified input bundle; compute the three target weights; append the decision record. All arms share
            the decision - if any input is missing, no arm rebalances.
  confirm   after the workflow pushed: verify the decision record on origin/main; the confirmation time makes
            the decision executable.
  execute   capture a Binance spot depth quote AFTER the decision became executable (never an earlier quote or
            a candle), simulate bid/ask-walked fills under ordinary and stressed costs, append one execution
            row per arm and scenario. Missing quotes leave every holding unchanged.
  report    reports/paper_ps1.{json,md}: coverage, delays, per-arm returns, risk, exposure, turnover, drawdown,
            paired differences and - only from 10 blocks of 42 intervals - the bootstrap interval of the primary
            metric. Open intervals are pending, never marked.

The job refuses to run if the protocol, calibration or calibration script differ from the frozen hashes below.
Stdlib only. Network: Binance spot depth (www.binance.com, data-api.binance.vision), git. Records: streams/ps1/.
"""
from __future__ import annotations

import datetime as dt
import email.utils
import hashlib
import json
import math
import random
import sys
import time
import urllib.request
from pathlib import Path

DESK = Path(__file__).resolve().parent
BASE = DESK.parent
for p in (str(DESK), str(BASE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import stream_util as U          # noqa: E402

VERSION = "ps1-job-1.0.0"
PROTOCOL = DESK / "research/ps1/protocol.json"
PROTOCOL_SHA256 = "00acb5bcf3e868e9d2023ff963c256f2fed23d6d2302552f109dab2193a48e8f"
ROOT = "streams/ps1"
DECISIONS, CONFIRMS, QUOTES = f"{ROOT}/decisions.jsonl", f"{ROOT}/confirmations.jsonl", f"{ROOT}/quotes.jsonl"
EXECUTIONS, RUNS, LAUNCH, TERMINATED = f"{ROOT}/executions.jsonl", f"{ROOT}/runs.jsonl", f"{ROOT}/launch.json", f"{ROOT}/terminated.json"
ARMS = ("FIXED", "VOL", "B2")
SCENARIOS = ("ordinary", "stressed")
INTERVALS_PER_YEAR = 365 * 6
UA = {"User-Agent": "jbm-desk-data/ps1 (research; read-only)"}


class Refused(RuntimeError):
    """The frozen protocol cannot be verified; nothing is decided or executed."""


# --------------------------------------------------------------------------------------------
# Protocol
# --------------------------------------------------------------------------------------------
def load_protocol(path=PROTOCOL, want=None) -> dict:
    raw = Path(path).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != (want or PROTOCOL_SHA256):
        raise Refused(f"protocol hash {got[:12]} != frozen {str(want or PROTOCOL_SHA256)[:12]}")
    doc = json.loads(raw)
    for key, rel in (("file_sha256", doc["calibration"]["file"]), ("script_sha256", doc["calibration"]["script"])):
        f = BASE / rel
        if not f.exists() or U.file_sha(f) != doc["calibration"][key]:
            raise Refused(f"calibration artifact {rel} missing or altered")
    cal = json.loads((BASE / doc["calibration"]["file"]).read_text())
    if cal["constants"] != doc["calibration"]["constants"]:
        raise Refused("calibration constants differ from the protocol's")
    return doc


def constants(proto) -> dict:
    c = dict(proto["calibration"]["constants"])
    c.update(w_max=proto["policy"]["w_max"], band=proto["policy"]["rebalance_band"],
             max_delay_ms=proto["execution"]["max_delay_min"] * 60000)
    return c


# --------------------------------------------------------------------------------------------
# Sizing (pure)
# --------------------------------------------------------------------------------------------
def sd_park(bars: list, n: int = 42) -> float:
    """Parkinson 4H sigma over the last n bars, as range_model.features_at's sd_park_42."""
    if len(bars) < n:
        raise ValueError(f"need {n} bars, have {len(bars)}")
    hl = [math.log(float(b["high"]) / float(b["low"])) for b in bars[-n:]]
    return math.sqrt(sum(x * x for x in hl) / n / (4 * math.log(2)))


def weights(point_lr: float, sd42: float, c: dict) -> dict:
    s = c["sigma_star_4h"]
    return {"FIXED": min(c["w_max"], s / c["s_uncond"]),
            "VOL": min(c["w_max"], s / (c["k_vol"] * sd42)),
            "B2": min(c["w_max"], s / (c["k_b2"] * point_lr))}


# --------------------------------------------------------------------------------------------
# Fills and accounting (pure)
# --------------------------------------------------------------------------------------------
def validate_book(book: dict) -> list:
    """Problems with a captured depth snapshot (empty list = usable)."""
    out = []
    try:
        bids = [(float(p), float(q)) for p, q in book["bids"]]
        asks = [(float(p), float(q)) for p, q in book["asks"]]
    except (KeyError, TypeError, ValueError):
        return ["malformed book"]
    if len(bids) < 5 or len(asks) < 5:
        out.append("fewer than 5 levels")
    if any(p <= 0 or q <= 0 for p, q in bids + asks):
        out.append("non-positive price or size")
    if bids and asks and bids[0][0] >= asks[0][0]:
        out.append("crossed or locked book")
    if [p for p, _ in bids] != sorted((p for p, _ in bids), reverse=True) or [p for p, _ in asks] != sorted(p for p, _ in asks):
        out.append("levels out of order")
    return out


def fill_price(book: dict, side: str, qty: float, slippage_bp: float) -> dict:
    """Simulated fill for qty BTC (> 0) on side 'buy' or 'sell': walk the captured levels; any remainder fills at
    the last level with an extra 50 bp; then slippage. Returns price and the depth used."""
    levels = [(float(p), float(q)) for p, q in (book["asks"] if side == "buy" else book["bids"])]
    left, cost = qty, 0.0
    for p, q in levels:
        take = min(left, q)
        cost += take * p
        left -= take
        if left <= 1e-12:
            left = 0.0
            break
    beyond = left
    if beyond > 0:
        last = levels[-1][0] * (1.005 if side == "buy" else 0.995)
        cost += beyond * last
    vwap = cost / qty
    slip = 1 + slippage_bp / 1e4 if side == "buy" else 1 - slippage_bp / 1e4
    return {"price": vwap * slip, "vwap": vwap, "beyond_captured_depth_btc": beyond}


def rebalance(state: dict, w_target: float, book: dict, cost: dict, band: float) -> dict:
    """One arm's execution at a captured book. `state` = {cash, btc}. Returns the new state and the trade record.
    Equity is marked at mid before trading; the arm trades to w_target only outside the band."""
    bid, ask = float(book["bids"][0][0]), float(book["asks"][0][0])
    mid = (bid + ask) / 2
    cash, btc = state["cash"], state["btc"]
    equity = cash + btc * mid
    w_now = btc * mid / equity if equity > 0 else 0.0
    rec = {"mid": mid, "equity_pre": equity, "w_before": w_now, "w_target": w_target, "traded_btc": 0.0,
           "fill_price": None, "fee": 0.0, "notional": 0.0, "beyond_depth_btc": 0.0}
    if abs(w_target - w_now) > band:
        delta = (w_target * equity - btc * mid) / mid
        side = "buy" if delta > 0 else "sell"
        qty = abs(delta)
        if side == "sell":
            qty = min(qty, btc)                          # never short
        f = fill_price(book, side, qty, cost["slippage_bp"])
        if side == "buy" and qty * f["price"] * (1 + cost["taker_fee_bp"] / 1e4) > cash:
            qty = cash / (f["price"] * (1 + cost["taker_fee_bp"] / 1e4)) * (1 - 1e-9)    # no borrowing
            f = fill_price(book, side, qty, cost["slippage_bp"])
            qty = min(qty, cash / (f["price"] * (1 + cost["taker_fee_bp"] / 1e4)) * (1 - 1e-9))
        notional = qty * f["price"]
        fee = notional * cost["taker_fee_bp"] / 1e4
        if side == "buy":
            cash -= notional + fee
            btc += qty
        else:
            cash += notional - fee
            btc -= qty
        rec.update(traded_btc=qty if side == "buy" else -qty, fill_price=f["price"], fee=fee, notional=notional,
                   beyond_depth_btc=f["beyond_captured_depth_btc"])
    if cash < -1e-6 or btc < -1e-12:
        raise ValueError("accounting: negative cash or BTC")
    post = cash + btc * mid
    rec.update(cash_after=cash, btc_after=btc, equity_post=post, w_after=(btc * mid / post) if post > 0 else 0.0,
               cost_vs_mid=(equity - post))
    return {"cash": cash, "btc": btc}, rec


# --------------------------------------------------------------------------------------------
# Quotes
# --------------------------------------------------------------------------------------------
def fetch_depth(url: str, clock=U.clock_ms, opener=None) -> dict:
    """One depth request with its timing. Raises on any HTTP or parse failure (a missing quote is recorded)."""
    opener = opener or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=15))
    sent = clock()
    resp = opener(url)
    raw = resp.read()
    received = clock()
    date = resp.headers.get("Date") if hasattr(resp, "headers") else None
    book = json.loads(raw)
    return {"source": url, "t_sent_ms": sent, "t_received_ms": received, "http_date": date,
            "http_date_ms": int(email.utils.parsedate_to_datetime(date).timestamp() * 1000) if date else None,
            "last_update_id": book.get("lastUpdateId"), "bids": book.get("bids", [])[:20], "asks": book.get("asks", [])[:20],
            "raw_sha256": hashlib.sha256(raw).hexdigest(), "retrieval": "live request (not a retrospective quote)"}


def eligible_quote(q: dict, executable_ms: int, deadline_ms: int) -> tuple:
    """(ok, reason). A quote is usable only if requested after the decision became executable, received before
    the deadline, captured live, and valid."""
    if q.get("retrieval") != "live request (not a retrospective quote)":
        return False, "not a live capture"
    if not isinstance(q.get("t_sent_ms"), int) or q["t_sent_ms"] <= executable_ms:
        return False, "requested before the decision was executable"
    if q["t_received_ms"] > deadline_ms:
        return False, "received after the execution deadline"
    probs = validate_book(q)
    return (not probs), "; ".join(probs) or "eligible"


# --------------------------------------------------------------------------------------------
# Ledger
# --------------------------------------------------------------------------------------------
def ledger_state(base, proto) -> dict:
    """(scenario, arm) -> {cash, btc} after the last execution; start equity otherwise."""
    st = {(s, a): {"cash": float(proto["capital"]["start_equity_usdt"]), "btc": 0.0} for s in SCENARIOS for a in ARMS}
    for r in U.rows(Path(base) / EXECUTIONS):
        st[(r["scenario"], r["arm"])] = {"cash": r["cash_after"], "btc": r["btc_after"]}
    return st


def _run_row(base, run, stage, outcome, **extra):
    U.append(Path(base) / RUNS, dict({"run": run, "stage": stage, "outcome": outcome, "t_ms": U.clock_ms(), "job": VERSION}, **extra),
             key=lambda r: (json.dumps(r["run"], sort_keys=True), r["stage"], r["t_ms"]))


def decisions(base) -> dict:
    return {r["decision_id"]: r for r in U.rows(Path(base) / DECISIONS)}


def decide(base=BASE, now=None, clock=U.clock_ms, run=None, read_current=None, proto=None) -> dict | None:
    """Record the paper decision for the latest 4H close (idempotent). Returns the record or None."""
    import range_reader as RR
    base = Path(base)
    now = now or dt.datetime.now(U.UTC)
    run = run or U.run_meta()
    proto = proto or load_protocol()
    c = constants(proto)
    if (base / TERMINATED).exists():
        _run_row(base, run, "decide", "terminated")
        return None
    decision = U.boundary(now)
    if decision < U.parse(proto["start"]["not_before_utc"]):
        _run_row(base, run, "decide", "not-launched", decision_utc=U.iso(decision))
        return None
    did = f"ps1-{decision:%Y%m%dT%H%MZ}"
    have = decisions(base)
    if did in have:
        return have[did]
    t0 = clock()
    rec = {"decision_id": did, "decision_utc": U.iso(decision), "protocol": f"PS1 v{proto['version']}",
           "protocol_sha256": PROTOCOL_SHA256, "job": VERSION, "code_sha256": U.file_sha(Path(__file__)),
           "computed_start_ms": t0, "run": run}
    if (U.ms(now) - U.ms(decision)) > c["max_delay_ms"]:
        rec.update(action="missed", reason="stale: processed after close + max_delay")
    else:
        rc = (read_current or RR.read_current)(base, now, "4h")
        if rc.get("state") != "valid-current" or rc.get("decision_utc") != U.iso(decision):
            rec.update(action="no-rebalance", reason=f"forecast unavailable ({rc.get('state')}: {rc.get('reason')})"[:300],
                       rc1d_id=rc.get("id"))
        else:
            try:
                doc, entry, pub = U.rc1d_record(base, rc["id"])
                bundle = U.rc1d_bundle(base, doc)
                bars = bundle["bars"]
                if bars[-1]["close_utc"] != U.iso(decision):
                    raise U.RecordUnavailable("bundle does not end at the decision")
                sd42 = sd_park(bars)
                w = weights(rc["point_lr"], sd42, c)
                src = (bundle.get("sources") or {})
                rec.update(data_cutoff_utc=U.iso(decision),
                           source_retrieved_utc={"bars": (src.get("bars") or {}).get("retrieved_utc"),
                                                 "dvol": (src.get("dvol") or {}).get("retrieved_utc")})
                rec.update(action="rebalance", rc1d_id=rc["id"], rc1d_frozen_sha256=entry["sha256"],
                           rc1d_available_ms=rc["available_ms"], rc1d_start_utc=rc["start_utc"],
                           rc1d_made_utc=doc["made_utc"], rc1d_confirmed_ms=(pub or {}).get("confirmed"),
                           snapshot_hash=doc["snapshot_hash"], point_lr=rc["point_lr"], sd_park_42=sd42,
                           sigma_hat={"FIXED": c["s_uncond"], "VOL": c["k_vol"] * sd42, "B2": c["k_b2"] * rc["point_lr"]},
                           w_target=w)
            except (U.RecordUnavailable, OSError, ValueError, KeyError) as exc:
                rec.update(action="no-rebalance", reason=f"inputs unavailable: {exc}"[:300], rc1d_id=rc.get("id"))
    rec["computed_end_ms"] = clock()
    U.append(base / DECISIONS, rec, key=lambda r: (r["decision_id"],))
    _run_row(base, run, "decide", rec["action"], decision_id=did)
    return rec


def confirm(base=BASE, clock=U.clock_ms, remote=U.remote_rows) -> list:
    """Confirm recorded decisions on origin/main (the row must be byte-identical in canonical form)."""
    base = Path(base)
    have = {r["decision_id"] for r in U.rows(base / CONFIRMS)}
    todo = [r for r in decisions(base).values() if r["decision_id"] not in have and r.get("action") == "rebalance"]
    if not todo:
        return []
    commit, remote_decisions = remote(DECISIONS)
    t = clock()
    there = {r.get("decision_id"): U.sha(r) for r in remote_decisions}
    out = []
    for r in todo:
        if there.get(r["decision_id"]) != U.sha(r):
            continue
        row = {"decision_id": r["decision_id"], "commit": commit, "confirmed_ms": t,
               "method": "git fetch origin; decision row identical on origin/main"}
        U.append(base / CONFIRMS, row, key=lambda x: (x["decision_id"],))
        out.append(row)
    return out


def execute(base=BASE, clock=U.clock_ms, fetch=fetch_depth, proto=None, run=None, pause=time.sleep) -> dict | None:
    """Execute the newest confirmed, unexecuted decision on a quote captured now. Returns the outcome row."""
    base = Path(base)
    proto = proto or load_protocol()
    run = run or U.run_meta()
    c = constants(proto)
    conf = {r["decision_id"]: r for r in U.rows(base / CONFIRMS)}
    done = {r["decision_id"] for r in U.rows(base / EXECUTIONS)} | \
           {r["decision_id"] for r in U.rows(base / RUNS) if r.get("stage") == "execute" and r.get("outcome") == "missed-execution"}
    cands = sorted((d for d in decisions(base).values() if d.get("action") == "rebalance" and d["decision_id"] in conf
                    and d["decision_id"] not in done), key=lambda d: d["decision_utc"])
    if not cands:
        return None
    d = cands[-1]
    for older in cands[:-1]:                             # superseded before execution: never executed late
        _run_row(base, run, "execute", "missed-execution", decision_id=older["decision_id"], reason="superseded by a newer decision")
    executable = max(conf[d["decision_id"]]["confirmed_ms"], d["rc1d_available_ms"], d["computed_end_ms"])
    deadline = U.ms(U.parse(d["decision_utc"])) + c["max_delay_ms"]
    quote, why = None, "no attempt"
    for attempt in range(3):
        if clock() > deadline:
            why = "deadline passed"
            break
        for url in proto["instrument"]["quote_sources"]:
            try:
                q = fetch(url, clock=clock)
            except Exception as exc:                     # noqa: BLE001 - any failure is a missing quote
                why = f"{type(exc).__name__}: {exc}"[:200]
                continue
            ok, why = eligible_quote(q, executable, deadline)
            q.update(decision_id=d["decision_id"], eligible=ok, eligibility=why,
                     quote_id=f"{d['decision_id']}#{q['t_sent_ms']}")
            U.append(base / QUOTES, q, key=lambda r: (r["quote_id"],))
            if ok:
                quote = q
                break
        if quote:
            break
        pause(5)
    if quote is None:
        if clock() > deadline:
            _run_row(base, run, "execute", "missed-execution", decision_id=d["decision_id"], reason=why)
        else:
            _run_row(base, run, "execute", "no-quote-yet", decision_id=d["decision_id"], reason=why)
        return {"decision_id": d["decision_id"], "outcome": "no eligible quote", "reason": why}
    state = ledger_state(base, proto)
    prev = {}
    for r in U.rows(base / EXECUTIONS):
        prev[(r["scenario"], r["arm"])] = r
    first = not (base / LAUNCH).exists()
    rows = []
    for s in SCENARIOS:
        for a in ARMS:
            new, rec = rebalance(state[(s, a)], d["w_target"][a], quote, proto["costs"][s], c["band"])
            p = prev.get((s, a))
            rows.append(dict(rec, decision_id=d["decision_id"], decision_utc=d["decision_utc"], scenario=s, arm=a,
                             quote_id=quote["quote_id"], fill_time_ms=quote["t_received_ms"], executable_ms=executable,
                             intended_execution_ms=executable, quote_sent_ms=quote["t_sent_ms"],
                             delay_from_decision_ms=quote["t_received_ms"] - U.ms(U.parse(d["decision_utc"])),
                             interval_start_decision=(p or {}).get("decision_utc"),
                             interval_return=(rec["equity_pre"] / p["equity_pre"] - 1) if p else None,
                             costs_version=proto["costs"]["version"], job=VERSION))
    for r in rows:
        U.append(base / EXECUTIONS, r, key=lambda x: (x["decision_id"], x["scenario"], x["arm"]))
    if first:
        from storage import atomic_json
        atomic_json(base / LAUNCH, {"first_decision_utc": d["decision_utc"], "first_execution_ms": quote["t_received_ms"],
                                    "protocol_sha256": PROTOCOL_SHA256, "job": VERSION})
    _run_row(base, run, "execute", "executed", decision_id=d["decision_id"], quote_id=quote["quote_id"])
    return {"decision_id": d["decision_id"], "outcome": "executed", "rows": len(rows)}


# --------------------------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------------------------
def _sharpe(xs):
    if len(xs) < 2:
        return None
    m = sum(xs) / len(xs)
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))
    return m / sd * math.sqrt(INTERVALS_PER_YEAR) if sd > 0 else None


def _quantile(xs, q):
    xs = sorted(xs)
    if not xs:
        return None
    i = (len(xs) - 1) * q
    lo = int(i)
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (i - lo)


def bootstrap_sharpe_diff(a: list, b: list, block=42, reps=5000, seed=20261003) -> list:
    """Moving-block bootstrap of paired intervals: 90% interval of Sharpe(a) - Sharpe(b)."""
    n = len(a)
    rng = random.Random(seed)
    starts = n - block + 1
    k = -(-n // block)
    out = []
    for _ in range(reps):
        idx = []
        for _ in range(k):
            s0 = rng.randrange(starts)
            idx.extend(range(s0, s0 + block))
        idx = idx[:n]
        sa, sb = _sharpe([a[i] for i in idx]), _sharpe([b[i] for i in idx])
        if sa is not None and sb is not None:
            out.append(sa - sb)
    return [_quantile(out, 0.05), _quantile(out, 0.95)]


def arm_stats(rows: list) -> dict:
    """rows: one arm's executions in order."""
    rets = [r["interval_return"] for r in rows if r["interval_return"] is not None]
    marks = [r["equity_pre"] for r in rows]
    peak, mdd = -1.0, 0.0
    for m in marks:
        peak = max(peak, m)
        mdd = min(mdd, m / peak - 1)
    mean_eq = sum(marks) / len(marks) if marks else None
    years = len(rets) / INTERVALS_PER_YEAR if rets else None
    return {"intervals": len(rets), "net_return": (marks[-1] / marks[0] - 1) if len(marks) > 1 else None,
            "sharpe_ann": _sharpe(rets),
            "vol_ann": (math.sqrt(sum((x - sum(rets) / len(rets)) ** 2 for x in rets) / (len(rets) - 1)) * math.sqrt(INTERVALS_PER_YEAR))
            if len(rets) > 1 else None,
            "max_drawdown_marks": mdd,
            "turnover_ann": (sum(abs(r["notional"]) for r in rows) / mean_eq / years) if mean_eq and years else None,
            "exposure_mean": (sum(r["w_after"] for r in rows[:-1]) / (len(rows) - 1)) if len(rows) > 1 else None,
            "fees_and_costs_usdt": sum(r["cost_vs_mid"] for r in rows),
            "worst_interval": min(rets) if rets else None,
            "es5": (lambda s: sum(s[:max(1, len(s) // 20)]) / max(1, len(s) // 20))(sorted(rets)) if rets else None}


def schedule(start: dt.datetime, now: dt.datetime) -> list:
    out, t = [], start
    while t <= U.boundary(now):
        out.append(t)
        t += dt.timedelta(hours=4)
    return out


def report(base=BASE, now=None, proto=None) -> dict:
    base = Path(base)
    now = now or dt.datetime.now(U.UTC)
    proto = proto or json.loads(PROTOCOL.read_text())
    launch = json.loads((base / LAUNCH).read_text()) if (base / LAUNCH).exists() else None
    ex = U.rows(base / EXECUTIONS)
    decs = decisions(base)
    runs = U.rows(base / RUNS)
    doc = {"generated_utc": U.iso_ms(U.ms(now)), "job": VERSION, "protocol": f"PS1 v{proto['version']}",
           "protocol_sha256": PROTOCOL_SHA256, "label": proto["label"], "launch": launch}
    if not launch:
        doc.update(status="not launched", reason=f"no executed decision yet (not before {proto['start']['not_before_utc']})",
                   decisions_recorded=len(decs))
    else:
        sched = schedule(U.parse(launch["first_decision_utc"]), now)
        executed = {r["decision_id"] for r in ex}
        missed_exec = {r["decision_id"]: r.get("reason") for r in runs if r.get("stage") == "execute" and r.get("outcome") == "missed-execution"}
        reasons = {}
        for t in sched:
            did = f"ps1-{t:%Y%m%dT%H%MZ}"
            d = decs.get(did)
            if did in executed:
                k = "executed"
            elif d is None:
                k = "missed: no run" if (now - t) > dt.timedelta(minutes=proto["execution"]["max_delay_min"]) else "pending"
            elif d["action"] != "rebalance":
                k = f"{d['action']}: {str(d.get('reason', '')).split(' (')[0]}"
            elif did in missed_exec:
                k = "missed-execution"
            else:
                k = "confirmed, not yet executed" if d else "pending"
            reasons[k] = reasons.get(k, 0) + 1
        tail = [f"ps1-{t:%Y%m%dT%H%MZ}" for t in sched[-6:]]
        paused = len(tail) == 6 and not any(t in executed for t in tail)
        per = {}
        for s in SCENARIOS:
            per[s] = {a: arm_stats([r for r in ex if r["scenario"] == s and r["arm"] == a]) for a in ARMS}
        ordered = sorted({r["decision_utc"] for r in ex})
        def series(s, a):
            m = {r["decision_utc"]: r["interval_return"] for r in ex if r["scenario"] == s and r["arm"] == a}
            return [m[t] for t in ordered if m.get(t) is not None]
        paired = {}
        for s in SCENARIOS:
            b2, vol, fx = series(s, "B2"), series(s, "VOL"), series(s, "FIXED")
            n = len(b2)
            blocks = n // 42
            e = {"n_intervals": n, "blocks": blocks,
                 "sharpe_diff_B2_minus_VOL": (per[s]["B2"]["sharpe_ann"] - per[s]["VOL"]["sharpe_ann"])
                 if per[s]["B2"]["sharpe_ann"] is not None and per[s]["VOL"]["sharpe_ann"] is not None else None,
                 "mean_diff_B2_minus_VOL": (sum(x - y for x, y in zip(b2, vol)) / n) if n else None,
                 "mean_diff_B2_minus_FIXED": (sum(x - y for x, y in zip(b2, fx)) / n) if n else None,
                 "B2_better_intervals_vs_VOL": sum(x > y for x, y in zip(b2, vol))}
            if blocks >= 10:
                e["sharpe_diff_ci90"] = bootstrap_sharpe_diff(b2, vol)
            else:
                e["sharpe_diff_ci90"] = None
                e["uncertainty"] = f"unavailable: {blocks} complete block(s) of 42 intervals; PS1 needs 10"
            paired[s] = e
        delays = sorted(r["delay_from_decision_ms"] / 60000 for r in ex if r["arm"] == "B2" and r["scenario"] == "ordinary")
        days = (now - U.parse(launch["first_decision_utc"])).total_seconds() / 86400
        open_since = ordered[-1] if ordered else None
        doc.update(
            status="paused" if paused else "collecting (descriptive)",
            days_since_launch=round(days, 2), scheduled_decisions=len(sched), outcomes=reasons,
            coverage=round(reasons.get("executed", 0) / len(sched), 4) if sched else None,
            execution_delay_min={"median": _quantile(delays, 0.5), "max": delays[-1] if delays else None},
            arms=per, paired=paired,
            open_interval={"since_decision_utc": open_since, "state": "pending - not marked until the next executed rebalance"},
            checkpoints={"C1": {"due_after_days": 180, "needs_blocks": 10}, "C2": {"due_after_days": 365, "needs_blocks": 20},
                         "progress": f"{days:.1f} days, {paired['ordinary']['blocks']} complete block(s)"},
            note="Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. "
                 "No status here is a trading edge or an entry endorsement.")
    from storage import atomic_bytes
    atomic_bytes(base / "reports/paper_ps1.json", (json.dumps(doc, indent=1, sort_keys=True, default=str) + "\n").encode())
    atomic_bytes(base / "reports/paper_ps1.md", markdown(doc).encode())
    return doc


def _f(x, fmt="{:.4f}"):
    return "—" if x is None else fmt.format(x)


def markdown(doc: dict) -> str:
    L = ["# Paper sizing experiment PS1", "",
         f"Generated {doc['generated_utc']} by {doc['job']} ({doc['protocol']}, protocol sha256 {doc['protocol_sha256'][:12]}).", "",
         f"> {doc['label']}", "", f"**Status: {doc['status']}**", ""]
    if not doc.get("launch"):
        L += [doc.get("reason", ""), "", "Protocol: [desk/research/ps1/protocol.json](../desk/research/ps1/protocol.json)", ""]
        return "\n".join(L)
    L += [f"Launched at decision {doc['launch']['first_decision_utc']}; {doc['days_since_launch']} days; "
          f"{doc['scheduled_decisions']} scheduled decisions; coverage {_f(doc['coverage'], '{:.1%}')}; "
          f"execution delay after the 4H close: median {_f(doc['execution_delay_min']['median'], '{:.1f}')} min, "
          f"max {_f(doc['execution_delay_min']['max'], '{:.1f}')} min.", "",
          "Outcomes: " + "; ".join(f"{k} {v}" for k, v in sorted(doc["outcomes"].items())), "",
          "| scenario | arm | intervals | net return | Sharpe (ann.) | vol (ann.) | exposure | turnover (ann.) | max DD | worst | ES5% |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for s, arms in doc["arms"].items():
        for a, st in arms.items():
            L.append(f"| {s} | {a} | {st['intervals']} | {_f(st['net_return'], '{:.2%}')} | {_f(st['sharpe_ann'], '{:.2f}')} | "
                     f"{_f(st['vol_ann'], '{:.1%}')} | {_f(st['exposure_mean'], '{:.2f}')} | {_f(st['turnover_ann'], '{:.1f}')} | "
                     f"{_f(st['max_drawdown_marks'], '{:.2%}')} | {_f(st['worst_interval'], '{:.2%}')} | {_f(st['es5'], '{:.2%}')} |")
    L += ["", "| scenario | paired intervals | blocks | Sharpe B2−VOL | 90% interval | mean interval diff B2−VOL | B2−FIXED |",
          "|---|---|---|---|---|---|---|"]
    for s, e in doc["paired"].items():
        ci = e.get("sharpe_diff_ci90")
        L.append(f"| {s} | {e['n_intervals']} | {e['blocks']} | {_f(e['sharpe_diff_B2_minus_VOL'], '{:.3f}')} | "
                 f"{('[' + ', '.join(f'{x:.3f}' for x in ci) + ']') if ci else e.get('uncertainty')} | "
                 f"{_f(e['mean_diff_B2_minus_VOL'], '{:.5f}')} | {_f(e['mean_diff_B2_minus_FIXED'], '{:.5f}')} |")
    L += ["", f"Open interval since {doc['open_interval']['since_decision_utc']}: {doc['open_interval']['state']}.",
          f"Checkpoints: C1 after 180 days with ≥10 blocks; C2 after 365 days with ≥20 blocks. Progress: {doc['checkpoints']['progress']}.",
          "", doc["note"], ""]
    return "\n".join(L)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        if cmd == "decide":
            decide()
        elif cmd == "confirm":
            confirm()
        elif cmd == "execute":
            print(execute())
        elif cmd == "report":
            report()
        else:
            raise SystemExit("usage: paper_ps1.py decide|confirm|execute|report")
    except Refused as exc:
        _run_row(BASE, U.run_meta(), cmd, "refused", reason=str(exc))
        raise SystemExit(f"PS1 refused: {exc}")
