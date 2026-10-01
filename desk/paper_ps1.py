#!/usr/bin/env python3
"""paper_ps1 — the prospective paper sizing experiment PS1 (protocol desk/research/ps1/protocol.json, PS1 v2).

A SIMULATION on captured quotes. It tests whether sizing a synthetic, unlevered BTC spot long by the registered
RC1D B2 4h range forecast beats sizing by trailing Parkinson volatility (primary) and a fixed weight (control),
after costs. It places no order, holds no credential, and its results are never an entry endorsement.

  decide    for the latest 4H decision: read the eligible RC1D 4h forecast (range_reader.read_current) and its
            verified input bundle; compute the three target weights; append the decision record. All arms share
            the decision - if any input is missing, no arm rebalances.
  confirm   after the workflow pushed: verify the decision record on origin/main and store an integrity binding
            (record hash, decision time, version, input snapshot, contract, confirmation time and commit).
  execute   recover any interrupted execution from its immutable snapshot; verify the binding; capture a Binance
            spot depth quote AFTER the decision became executable; validate it; record the snapshot; write all six
            execution rows (3 arms x 2 scenarios) in one atomic replacement; record the execution state.
  report    reports/paper_ps1.{json,md}: lifecycle, coverage, delays, execution states, integrity, duration-weighted
            per-arm statistics, paired differences, evidence block. Open intervals are pending, never marked.
  lifecycle <state> <reason>   operator command (pause, resume, terminate, archive)

v2 (repo 2.21) replaces v1, which was retired before launch with no observation (protocol_v1_retired.json).
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

VERSION = "ps1-job-2.0.0"
PROTOCOL = DESK / "research/ps1/protocol.json"
PROTOCOL_SHA256 = "be015545540d85ae8b9e0733167b9160704e4c8a743c810467cac57af377e560"
PROTOCOL_V1_RETIRED = ("desk/research/ps1/protocol_v1_retired.json",
                       "00acb5bcf3e868e9d2023ff963c256f2fed23d6d2302552f109dab2193a48e8f")
ROOT = "streams/ps1"
DECISIONS, CONFIRMS, QUOTES = f"{ROOT}/decisions.jsonl", f"{ROOT}/confirmations.jsonl", f"{ROOT}/quotes.jsonl"
EXECUTIONS, RUNS, LAUNCH, TERMINATED = f"{ROOT}/executions.jsonl", f"{ROOT}/runs.jsonl", f"{ROOT}/launch.json", f"{ROOT}/terminated.json"
EXEC_STATES = f"{ROOT}/execution_states.jsonl"
ARMS = ("FIXED", "VOL", "B2")
SCENARIOS = ("ordinary", "stressed")
HOURS_PER_YEAR = 8760.0
STEP_H = 4.0
EXEC_STATE_NAMES = ("pending", "running", "completed", "failed", "partially_written", "recovered")
FINAL_OK = ("completed", "recovered")
SYMBOL = "BTCUSDT"
MAX_RTT_MS = 10_000
HTTP_DATE_TOL_MS = 120_000
LIVE = "live request (not a retrospective quote)"
UA = {"User-Agent": "jbm-desk-data/ps1 (research; read-only)"}


class Refused(RuntimeError):
    """The frozen protocol cannot be verified; nothing is decided or executed."""


class DuplicateExecution(RuntimeError):
    """The decision already has an execution (completed, recovered, in progress or failed)."""


# --------------------------------------------------------------------------------------------
# Protocol and lifecycle
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


def check_launch(base) -> None:
    """Refuse if PS1 was launched under another protocol: v2 never continues a v1 ledger. If v1 launched before
    v2 merged, the operator terminates v1 and v2 starts as a new stream (new root, new clock)."""
    p = Path(base) / LAUNCH
    if p.exists():
        got = json.loads(p.read_text()).get("protocol_sha256")
        if got != PROTOCOL_SHA256:
            raise Refused(f"PS1 was launched under protocol {str(got)[:12]}; this job runs {PROTOCOL_SHA256[:12]} and never "
                          f"continues another protocol's ledger")


def constants(proto) -> dict:
    c = dict(proto["calibration"]["constants"])
    c.update(w_max=proto["policy"]["w_max"], band=proto["policy"]["rebalance_band"],
             max_delay_ms=proto["execution"]["max_delay_min"] * 60000)
    return c


def lifecycle(base) -> tuple:
    """(state, last transition row or None) for this protocol."""
    rows = U.lifecycle_rows(base, ROOT, PROTOCOL_SHA256)
    return U.lifecycle_state(base, ROOT, PROTOCOL_SHA256), (rows[-1] if rows else None)


def stage_allowed(base, stage: str) -> tuple:
    """(allowed, state). Decisions and executions run while approved or active, or while paused by the job
    (infrastructure pause - the job keeps trying and resumes itself). An operator pause, termination or
    archiving stops them. Confirmation, scoring and reporting of retained history always run."""
    st, last = lifecycle(base)
    if stage in ("decide", "execute"):
        ok = st in ("approved", "active") or (st == "paused" and (last or {}).get("by") == "job")
        return ok, st
    return True, st


def _activate(base, reason: str, t_ms: int) -> None:
    st, last = lifecycle(base)
    if st == "approved" or (st == "paused" and (last or {}).get("by") == "job"):
        U.transition(base, ROOT, PROTOCOL_SHA256, "active", by="job", reason=reason, t_ms=t_ms)


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
# Market-data validation (pure). Unknown liquidity is never treated as available liquidity.
# --------------------------------------------------------------------------------------------
def _num(x):
    """A decimal string that parses to a finite number, else None (NaN, inf, empty, non-string: None)."""
    if not isinstance(x, str) or not x.strip():
        return None
    try:
        v = float(x)
    except ValueError:
        return None
    return v if math.isfinite(v) else None


def _side(levels, name) -> tuple:
    out, probs = [], []
    if not isinstance(levels, list):
        return [], [f"{name}: missing or not a list"]
    for i, lv in enumerate(levels):
        if not isinstance(lv, (list, tuple)) or len(lv) < 2:
            probs.append(f"{name}[{i}]: malformed level")
            continue
        p, q = _num(lv[0]), _num(lv[1])
        if p is None or q is None:
            probs.append(f"{name}[{i}]: price or size missing, non-numeric or non-finite")
        elif p <= 0 or q <= 0:
            probs.append(f"{name}[{i}]: non-positive price or size")
        else:
            out.append((p, q))
    return out, probs


def validate_book(book: dict) -> list:
    """Problems with a captured depth snapshot (empty list = usable)."""
    if not isinstance(book, dict):
        return ["malformed book"]
    bids, pb = _side(book.get("bids"), "bids")
    asks, pa = _side(book.get("asks"), "asks")
    out = pb + pa
    if pb or pa:
        out.append("non-positive price or size" if any("non-positive" in x for x in pb + pa) else "malformed book")
    if len(book.get("bids") or []) < 5 or len(book.get("asks") or []) < 5:
        out.append("fewer than 5 levels")
    if bids and asks and bids[0][0] >= asks[0][0]:
        out.append("crossed or locked book")
    if any(a[0] <= b[0] for a, b in zip(bids, bids[1:])) or any(b[0] <= a[0] for a, b in zip(asks, asks[1:])):
        out.append("levels out of order")
    return out


def validate_quote(q: dict) -> list:
    """Book checks plus timestamps, symbol and update id."""
    out = validate_book(q)
    if f"symbol={SYMBOL}" not in str(q.get("source", "")):
        out.append(f"source does not name symbol={SYMBOL}")
    lid = q.get("last_update_id")
    if not isinstance(lid, int) or isinstance(lid, bool):
        out.append("lastUpdateId missing or not an integer")
    s, r = q.get("t_sent_ms"), q.get("t_received_ms")
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (s, r)):
        out.append("request/receipt timestamps missing or invalid")
    else:
        if r <= s:
            out.append("receipt not after request")
        elif r - s > MAX_RTT_MS:
            out.append(f"stale: {r - s} ms between request and receipt (max {MAX_RTT_MS})")
        hd = q.get("http_date_ms")
        if hd is not None and (not isinstance(hd, int) or abs(hd - r) > HTTP_DATE_TOL_MS):
            out.append(f"stale: HTTP Date differs from receipt by more than {HTTP_DATE_TOL_MS // 1000} s")
    return out


# --------------------------------------------------------------------------------------------
# Fills and accounting (pure)
# --------------------------------------------------------------------------------------------
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
    probs = validate_book(book)
    if probs:
        raise ValueError(f"invalid book: {'; '.join(probs)}")
    if not all(math.isfinite(x) for x in (state["cash"], state["btc"], w_target)):
        raise ValueError("accounting: non-finite state or target")
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
    """One depth request with its timing. Raises on any HTTP or parse failure (a missing quote is recorded).
    Prices and sizes are kept as the strings Binance sent; validation happens before any use."""
    opener = opener or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=15))
    sent = clock()
    resp = opener(url)
    raw = resp.read()
    received = clock()
    date = resp.headers.get("Date") if hasattr(resp, "headers") else None
    book = json.loads(raw)
    try:
        date_ms = int(email.utils.parsedate_to_datetime(date).timestamp() * 1000) if date else None
    except (TypeError, ValueError):
        date_ms = None
    return {"source": url, "t_sent_ms": sent, "t_received_ms": received, "http_date": date, "http_date_ms": date_ms,
            "last_update_id": book.get("lastUpdateId"), "bids": book.get("bids", [])[:20], "asks": book.get("asks", [])[:20],
            "raw_sha256": hashlib.sha256(raw).hexdigest(), "retrieval": LIVE}


def eligible_quote(q: dict, executable_ms: int, deadline_ms: int) -> tuple:
    """(ok, reason). A quote is usable only if requested after the decision became executable, received before
    the deadline, captured live, and valid."""
    if q.get("retrieval") != LIVE:
        return False, "not a live capture"
    if not isinstance(q.get("t_sent_ms"), int) or q["t_sent_ms"] <= executable_ms:
        return False, "requested before the decision was executable"
    if not isinstance(q.get("t_received_ms"), int) or q["t_received_ms"] > deadline_ms:
        return False, "received after the execution deadline"
    probs = validate_quote(q)
    return (not probs), "; ".join(probs) or "eligible"


def _safe_quote_row(q: dict) -> dict:
    """A quote as recorded: non-finite numbers (which cannot be serialized) are recorded as their repr."""
    def clean(v):
        if isinstance(v, float) and not math.isfinite(v):
            return repr(v)
        if isinstance(v, list):
            return [clean(x) for x in v]
        if isinstance(v, dict):
            return {k: clean(x) for k, x in v.items()}
        return v
    return clean(q)


# --------------------------------------------------------------------------------------------
# Records, bindings and the ledger
# --------------------------------------------------------------------------------------------
def _run_row(base, run, stage, outcome, **extra):
    U.append(Path(base) / RUNS, dict({"run": run, "stage": stage, "outcome": outcome, "t_ms": U.clock_ms(), "job": VERSION}, **extra),
             key=lambda r: (json.dumps(r["run"], sort_keys=True), r["stage"], r["t_ms"], r.get("decision_id")))


def decisions(base) -> dict:
    out = {}
    for r in U.rows(Path(base) / DECISIONS):
        out.setdefault(r["decision_id"], r)                 # first write wins
    return out


def binding(d: dict, confirmed_ms: int, commit: str) -> dict:
    return {"record_sha256": U.sha(d), "decision_id": d["decision_id"], "decision_utc": d["decision_utc"],
            "version": {"protocol": d.get("protocol"), "protocol_sha256": d.get("protocol_sha256"), "job": d.get("job")},
            "input_snapshot": {"rc1d_id": d.get("rc1d_id"), "rc1d_frozen_sha256": d.get("rc1d_frozen_sha256"),
                               "snapshot_hash": d.get("snapshot_hash")},
            "contract": d.get("rc1d_contract"), "confirmed_ms": confirmed_ms, "commit": commit}


def verify_confirmation(conf: dict, d: dict | None) -> tuple:
    """(ok, reason). Recompute the binding from the decision row as it stands now."""
    b = conf.get("binding")
    if not isinstance(b, dict) or conf.get("binding_sha256") != U.sha(b):
        return False, "confirmation binding missing or altered"
    if d is None:
        return False, "decision row missing"
    if conf.get("confirmed_ms") != b.get("confirmed_ms") or conf.get("commit") != b.get("commit"):
        return False, "confirmation time or commit differs from its binding"
    want = binding(d, b.get("confirmed_ms"), b.get("commit"))
    for k in ("record_sha256", "decision_utc", "version", "input_snapshot", "contract"):
        if want[k] != b.get(k):
            return False, f"decision row changed after confirmation ({k})"
    if d.get("protocol_sha256") != PROTOCOL_SHA256:
        return False, "decision made under another protocol"
    return True, "verified"


def verified_confirmations(base, record=True) -> dict:
    """decision_id -> confirmation row, for bindings that verify; failures are recorded and excluded."""
    base = Path(base)
    decs = decisions(base)
    out = {}
    for c in U.rows(base / CONFIRMS):
        if c["decision_id"] in out:
            continue
        ok, why = verify_confirmation(c, decs.get(c["decision_id"]))
        if ok:
            out[c["decision_id"]] = c
        elif record:
            U.integrity_failure(base, ROOT, f"decision {c['decision_id']}", why,
                                expected=(c.get("binding") or {}).get("record_sha256"),
                                found=U.sha(decs[c["decision_id"]]) if c["decision_id"] in decs else None)
    return out


def exec_states(base) -> dict:
    out = {}
    for r in U.rows(Path(base) / EXEC_STATES):
        out.setdefault(r["execution_id"], []).append(r)
    return out


def _state(base, eid, state, t_ms, **extra) -> dict:
    if state not in EXEC_STATE_NAMES:
        raise ValueError(state)
    row = dict({"execution_id": eid, "state": state, "t_ms": t_ms, "job": VERSION}, **extra)
    U.append(Path(base) / EXEC_STATES, row, key=lambda r: (r["execution_id"], r["state"], r["t_ms"]))
    return row


def rows_sha(rows: list) -> str:
    return U.sha(sorted(rows, key=lambda r: (r["scenario"], r["arm"])))


def ledger(base) -> tuple:
    """(execution rows of completed/recovered sets in fill order, integrity failures). A set whose rows do not
    match the hash its final state recorded is a failure; nothing else is read."""
    base = Path(base)
    states = exec_states(base)
    by = {}
    for r in U.rows(base / EXECUTIONS):
        by.setdefault(r.get("execution_id"), []).append(r)
    good, bad = [], []
    for eid, st in states.items():
        fin = st[-1]
        if fin["state"] not in FINAL_OK:
            continue
        rs = by.get(eid, [])
        if len(rs) != len(ARMS) * len(SCENARIOS) or rows_sha(rs) != fin.get("rows_sha256"):
            bad.append({"execution_id": eid, "reason": "execution rows differ from the hash recorded at completion",
                        "expected": fin.get("rows_sha256"), "found": rows_sha(rs) if rs else None})
            continue
        good.extend(rs)
    good.sort(key=lambda r: (r["fill_time_ms"], r["scenario"], r["arm"]))
    return good, bad


def ledger_state(base, proto) -> dict:
    """(scenario, arm) -> {cash, btc} after the last completed execution; start equity otherwise."""
    st = {(s, a): {"cash": float(proto["capital"]["start_equity_usdt"]), "btc": 0.0} for s in SCENARIOS for a in ARMS}
    for r in ledger(base)[0]:
        st[(r["scenario"], r["arm"])] = {"cash": r["cash_after"], "btc": r["btc_after"]}
    return st


def snap_sha(snap: dict) -> str:
    """Hash of a snapshot without its own 'sha256' field."""
    return U.sha({k: v for k, v in snap.items() if k != "sha256"})


def _last_ok_execution(rows: list):
    return rows[-1]["execution_id"] if rows else None


# --------------------------------------------------------------------------------------------
# Decide and confirm
# --------------------------------------------------------------------------------------------
def decide(base=BASE, now=None, clock=U.clock_ms, run=None, read_current=None, proto=None) -> dict | None:
    """Record the paper decision for the latest 4H close (idempotent). Returns the record or None."""
    import range_reader as RR
    base = Path(base)
    now = now or dt.datetime.now(U.UTC)
    run = run if run is not None else U.run_meta()
    proto = proto or load_protocol()
    c = constants(proto)
    check_launch(base)
    if run.get("production") and lifecycle(base)[0] == "proposed":
        U.transition(base, ROOT, PROTOCOL_SHA256, "approved", by="job",
                     reason=f"protocol on main at {run.get('code_commit')} (the operator's merge)")
    ok, st = stage_allowed(base, "decide")
    if not ok:
        _run_row(base, run, "decide", f"refused: lifecycle {st}")
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
                if not (math.isfinite(sd42) and sd42 > 0 and math.isfinite(rc["point_lr"]) and rc["point_lr"] > 0):
                    raise ValueError("non-finite or non-positive sigma input")
                w = weights(rc["point_lr"], sd42, c)
                src = (bundle.get("sources") or {})
                rec.update(data_cutoff_utc=U.iso(decision),
                           source_retrieved_utc={"bars": (src.get("bars") or {}).get("retrieved_utc"),
                                                 "dvol": (src.get("dvol") or {}).get("retrieved_utc")})
                rec.update(action="rebalance", rc1d_id=rc["id"], rc1d_frozen_sha256=entry["sha256"],
                           rc1d_contract=entry.get("contract") or doc.get("contract"),
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
    """Confirm recorded decisions on origin/main (the row must be identical in canonical form) and bind them."""
    base = Path(base)
    have = {r["decision_id"] for r in U.rows(base / CONFIRMS)}
    todo = [r for r in decisions(base).values() if r["decision_id"] not in have and r.get("action") == "rebalance"]
    if not todo:
        return []
    commit, remote_decisions = remote(DECISIONS)
    t = clock()
    there = {}
    for r in remote_decisions:
        there.setdefault(r.get("decision_id"), U.sha(r))
    out = []
    for r in todo:
        if there.get(r["decision_id"]) != U.sha(r):
            continue
        b = binding(r, t, commit)
        row = {"decision_id": r["decision_id"], "commit": commit, "confirmed_ms": t, "binding": b,
               "binding_sha256": U.sha(b), "method": "git fetch origin; decision row identical on origin/main; bound"}
        U.append(base / CONFIRMS, row, key=lambda x: (x["decision_id"],))
        out.append(row)
    return out


# --------------------------------------------------------------------------------------------
# Execution: snapshot -> rows (pure), atomic write, states, recovery
# --------------------------------------------------------------------------------------------
def _prior(rows: list) -> dict:
    """'scenario/arm' -> the last completed row's carry-forward values, or None."""
    out = {f"{s}/{a}": None for s in SCENARIOS for a in ARMS}
    for r in rows:
        out[f"{r['scenario']}/{r['arm']}"] = {k: r[k] for k in ("cash_after", "btc_after", "equity_pre", "fill_time_ms",
                                                                "w_after", "decision_utc", "execution_id")}
    return out


def build_rows(snap: dict, d: dict, quote: dict, proto: dict) -> list:
    """The six execution rows of one execution, from its snapshot alone (deterministic)."""
    c = constants(proto)
    fill = quote["t_received_ms"]
    start = float(proto["capital"]["start_equity_usdt"])
    out = []
    for s in SCENARIOS:
        for a in ARMS:
            p = snap["prior"][f"{s}/{a}"]
            state = {"cash": p["cash_after"], "btc": p["btc_after"]} if p else {"cash": start, "btc": 0.0}
            _, rec = rebalance(state, d["w_target"][a], quote, proto["costs"][s], c["band"])
            row = dict(rec, execution_id=snap["execution_id"], decision_id=d["decision_id"], decision_utc=d["decision_utc"],
                       scenario=s, arm=a, quote_id=quote["quote_id"], fill_time_ms=fill,
                       executable_ms=snap["executable_ms"], intended_execution_ms=snap["executable_ms"],
                       quote_sent_ms=quote["t_sent_ms"], delay_from_decision_ms=fill - U.ms(U.parse(d["decision_utc"])),
                       costs_version=proto["costs"]["version"], job=VERSION, snapshot_sha256=snap["sha256"])
            if p:
                steps = (U.parse(d["decision_utc"]) - U.parse(p["decision_utc"])).total_seconds() / 3600 / STEP_H
                row.update(interval_start_decision=p["decision_utc"], interval_start_fill_ms=p["fill_time_ms"],
                           elapsed_h=(fill - p["fill_time_ms"]) / 3.6e6, decision_steps=round(steps, 6),
                           interval_flag="scheduled" if abs(steps - 1) < 1e-9 else f"extended ({steps:g} decision steps)",
                           w_held=p["w_after"], interval_return=rec["equity_pre"] / p["equity_pre"] - 1,
                           interval_log_return=math.log(rec["equity_pre"] / p["equity_pre"]))
            else:
                row.update(interval_start_decision=None, interval_start_fill_ms=None, elapsed_h=None, decision_steps=None,
                           interval_flag="entry", w_held=None, interval_return=None, interval_log_return=None)
            out.append(row)
    return out


def _write_rows(base, rows) -> int:
    """All rows of one execution in one atomic file replacement (storage.append_unique)."""
    from storage import append_unique
    return append_unique(Path(base) / EXECUTIONS, rows, key=lambda x: (x["execution_id"], x["scenario"], x["arm"]))


def _quote_row(base, qid):
    for r in U.rows(Path(base) / QUOTES):
        if r.get("quote_id") == qid:
            return r
    return None


def verify_snapshot(base, snap: dict, ledger_rows: list) -> tuple:
    """(ok, reason, decision, quote). The snapshot's inputs must be exactly as recorded."""
    base = Path(base)
    d = decisions(base).get(snap.get("decision_id"))
    if d is None or U.sha(d) != snap.get("decision_sha256"):
        return False, "decision row missing or changed since the snapshot", None, None
    q = _quote_row(base, snap.get("quote_id"))
    if q is None or U.sha(q) != snap.get("quote_sha256"):
        return False, "quote row missing or changed since the snapshot", None, None
    if _last_ok_execution(ledger_rows) != snap.get("prior_execution_id"):
        return False, "ledger moved on since the snapshot", None, None
    if U.sha(_prior(ledger_rows)) != snap.get("prior_sha256"):
        return False, "prior ledger state differs from the snapshot", None, None
    return True, "verified", d, q


def recover(base=BASE, proto=None, clock=U.clock_ms, run=None, writer=None) -> list:
    """Finish or close every execution left pending or running. Never captures a quote."""
    base = Path(base)
    proto = proto or load_protocol()
    run = run if run is not None else U.run_meta()
    writer = writer or _write_rows
    out = []
    for eid, st in exec_states(base).items():
        if st[-1]["state"] not in ("pending", "running"):
            continue
        first = st[0]
        snap = first.get("snapshot") or {}
        written = [r for r in U.rows(base / EXECUTIONS) if r.get("execution_id") == eid]
        t = clock()
        if snap_sha(snap) != first.get("snapshot_sha256") or snap.get("sha256") != first.get("snapshot_sha256"):
            out.append(_state(base, eid, "failed", t, reason="snapshot altered", rows_written=len(written)))
            _run_row(base, run, "execute", "missed-execution", decision_id=snap.get("decision_id"), reason="recovery failed: snapshot altered")
            continue
        if U.lifecycle_state(base, ROOT, PROTOCOL_SHA256) in ("terminated", "archived"):
            out.append(_state(base, eid, "failed", t, reason="terminated before recovery", rows_written=len(written)))
            _run_row(base, run, "execute", "missed-execution", decision_id=snap["decision_id"], reason="terminated")
            continue
        good, _ = ledger(base)
        ok, why, d, q = verify_snapshot(base, snap, good)
        if not ok:
            out.append(_state(base, eid, "failed", t, reason=f"recovery impossible: {why}", rows_written=len(written)))
            _run_row(base, run, "execute", "missed-execution", decision_id=snap["decision_id"], reason=f"recovery failed: {why}")
            continue
        rows = build_rows(snap, d, q, proto)
        if not written:
            writer(base, rows)
            out.append(_state(base, eid, "recovered", clock(), rows_sha256=rows_sha(rows), n_rows=len(rows),
                              recovered_from=eid, note="no row had been written; rebuilt from the snapshot"))
        elif len(written) == len(rows) and rows_sha(written) == rows_sha(rows):
            out.append(_state(base, eid, "recovered", clock(), rows_sha256=rows_sha(rows), n_rows=len(rows),
                              recovered_from=eid, note="every row had been written; verified against the snapshot"))
        else:
            _state(base, eid, "partially_written", t, rows_written=len(written),
                   note="partial rows preserved in place; excluded from the ledger")
            eid2 = f"{eid}~r1"
            snap2 = dict(snap, execution_id=eid2)
            snap2["sha256"] = snap_sha(snap2)
            rows2 = build_rows(snap2, d, q, proto)
            _state(base, eid2, "pending", clock(), snapshot=snap2, snapshot_sha256=snap2["sha256"],
                   decision_id=snap["decision_id"], recovers=eid)
            writer(base, rows2)
            out.append(_state(base, eid2, "recovered", clock(), rows_sha256=rows_sha(rows2), n_rows=len(rows2),
                              recovered_from=eid, note="rebuilt from the original snapshot under a new id"))
        _activate(base, f"execution {eid} recovered", clock())
        _launch(base, d, q)
        _run_row(base, run, "execute", "recovered", decision_id=snap["decision_id"], execution_id=eid)
    return out


def _launch(base, d, quote):
    if not (Path(base) / LAUNCH).exists():
        from storage import atomic_json
        atomic_json(Path(base) / LAUNCH, {"first_decision_utc": d["decision_utc"], "first_execution_ms": quote["t_received_ms"],
                                          "protocol_sha256": PROTOCOL_SHA256, "job": VERSION})


def start_execution(base, d, conf, quote, proto, clock, run, writer=None) -> dict:
    """Execute one verified decision on one eligible, recorded quote. Raises DuplicateExecution if the decision
    already has any execution state."""
    base = Path(base)
    writer = writer or _write_rows
    states = exec_states(base)
    if any((st[0].get("decision_id") == d["decision_id"]) for st in states.values()):
        raise DuplicateExecution(f"{d['decision_id']} already has an execution")
    good, bad = ledger(base)
    if bad:
        raise RuntimeError("ledger integrity failure; execution refused")
    eid = f"{d['decision_id']}#x{quote['t_sent_ms']}"
    executable = max(conf["confirmed_ms"], d["rc1d_available_ms"], d["computed_end_ms"])
    prior = _prior(good)
    snap = {"execution_id": eid, "decision_id": d["decision_id"], "decision_sha256": U.sha(d),
            "binding_sha256": conf["binding_sha256"], "quote_id": quote["quote_id"], "quote_sha256": U.sha(quote),
            "prior": prior, "prior_sha256": U.sha(prior), "prior_execution_id": _last_ok_execution(good),
            "protocol_sha256": PROTOCOL_SHA256, "job": VERSION, "executable_ms": executable}
    snap["sha256"] = snap_sha(snap)
    _state(base, eid, "pending", clock(), snapshot=snap, snapshot_sha256=snap["sha256"], decision_id=d["decision_id"])
    _state(base, eid, "running", clock())
    rows = build_rows(snap, d, quote, proto)
    ok, st = stage_allowed(base, "execute")
    if not ok:
        return _state(base, eid, "failed", clock(), reason=f"lifecycle {st} during execution; no ledger row written", rows_written=0)
    writer(base, rows)
    done = _state(base, eid, "completed", clock(), rows_sha256=rows_sha(rows), n_rows=len(rows))
    _activate(base, f"execution {eid} completed", clock())
    _launch(base, d, quote)
    return done


def execute(base=BASE, clock=U.clock_ms, fetch=fetch_depth, proto=None, run=None, pause=time.sleep, writer=None) -> dict | None:
    """Recover interrupted executions, then execute the newest confirmed, unexecuted decision on a quote captured
    now. Returns the outcome."""
    base = Path(base)
    proto = proto or load_protocol()
    run = run if run is not None else U.run_meta()
    c = constants(proto)
    check_launch(base)
    ok, st = stage_allowed(base, "execute")
    if not ok:
        _run_row(base, run, "execute", f"refused: lifecycle {st}")
        return {"outcome": "refused", "reason": f"lifecycle {st}"}
    recover(base, proto, clock, run, writer)
    good, bad = ledger(base)
    for b in bad:
        U.integrity_failure(base, ROOT, f"execution {b['execution_id']}", b["reason"], b["expected"], b["found"])
    if bad:
        _run_row(base, run, "execute", "refused: ledger integrity failure")
        return {"outcome": "refused", "reason": "ledger integrity failure"}
    conf = verified_confirmations(base)
    started = {st_[0].get("decision_id") for st_ in exec_states(base).values()}
    done = started | {r["decision_id"] for r in U.rows(base / RUNS)
                      if r.get("stage") == "execute" and r.get("outcome") == "missed-execution" and r.get("decision_id")}
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
            ok_q, why = eligible_quote(q, executable, deadline)
            q = _safe_quote_row(dict(q, decision_id=d["decision_id"], eligible=ok_q, eligibility=why,
                                     quote_id=f"{d['decision_id']}#q{q.get('t_sent_ms')}"))
            U.append(base / QUOTES, q, key=lambda r: (r["quote_id"],))
            if ok_q:
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
    try:
        res = start_execution(base, d, conf[d["decision_id"]], quote, proto, clock, run, writer)
    except DuplicateExecution as exc:
        _run_row(base, run, "execute", "refused: duplicate", decision_id=d["decision_id"], reason=str(exc))
        return {"decision_id": d["decision_id"], "outcome": "refused", "reason": str(exc)}
    if res["state"] != "completed":
        _run_row(base, run, "execute", "missed-execution", decision_id=d["decision_id"], reason=res.get("reason"))
        return {"decision_id": d["decision_id"], "outcome": res["state"], "reason": res.get("reason")}
    _run_row(base, run, "execute", "executed", decision_id=d["decision_id"], quote_id=quote["quote_id"],
             execution_id=res["execution_id"])
    return {"decision_id": d["decision_id"], "outcome": "executed", "rows": res["n_rows"], "execution_id": res["execution_id"]}


# --------------------------------------------------------------------------------------------
# Statistics (duration-weighted; protocol v2 metrics.time_accounting)
# --------------------------------------------------------------------------------------------
def dw_stats(rs: list, dts: list) -> dict:
    """Duration-weighted mean and variance of interval log returns rs over elapsed hours dts."""
    n, T = len(rs), sum(dts)
    if n == 0 or T <= 0:
        return {"mu_h": None, "var_h": None}
    mu = sum(rs) / T
    if n < 2:
        return {"mu_h": mu, "var_h": None}
    var = sum((r - mu * h) ** 2 for r, h in zip(rs, dts)) / (T * (n - 1) / n)
    return {"mu_h": mu, "var_h": var}


def sharpe_dw(rs: list, dts: list):
    s = dw_stats(rs, dts)
    if s["var_h"] is None or s["var_h"] <= 0:
        return None
    return (s["mu_h"] * HOURS_PER_YEAR) / math.sqrt(s["var_h"] * HOURS_PER_YEAR)


def _quantile(xs, q):
    xs = sorted(xs)
    if not xs:
        return None
    i = (len(xs) - 1) * q
    lo = int(i)
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (i - lo)


def bootstrap_sharpe_diff(a: list, b: list, dts: list = None, block=42, reps=5000, seed=20261003) -> list:
    """Moving-block bootstrap of paired intervals ((a, b, dt) resampled together): 90% interval of
    SR_dw(a) - SR_dw(b). dts defaults to equal 4h intervals."""
    n = len(a)
    dts = dts or [STEP_H] * n
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
        h = [dts[i] for i in idx]
        sa, sb = sharpe_dw([a[i] for i in idx], h), sharpe_dw([b[i] for i in idx], h)
        if sa is not None and sb is not None:
            out.append(sa - sb)
    return [_quantile(out, 0.05), _quantile(out, 0.95)]


def arm_stats(rows: list) -> dict:
    """rows: one arm's completed executions in fill order."""
    iv = [r for r in rows if r.get("interval_log_return") is not None]
    rs, dts = [r["interval_log_return"] for r in iv], [r["elapsed_h"] for r in iv]
    T = sum(dts)
    s = dw_stats(rs, dts)
    marks = [r["equity_pre"] for r in rows]
    peak, mdd = -1.0, 0.0
    for m in marks:
        peak = max(peak, m)
        mdd = min(mdd, m / peak - 1)
    mean_eq = sum(marks) / len(marks) if marks else None
    years = T / HOURS_PER_YEAR if T > 0 else None
    srt = sorted(rs)
    k = max(1, len(srt) // 20)
    return {"intervals": len(iv), "elapsed_hours": T if iv else 0.0,
            "extended_intervals": sum(1 for r in iv if r.get("interval_flag", "").startswith("extended")),
            "longest_interval_h": max(dts) if dts else None,
            "net_return": (marks[-1] / marks[0] - 1) if len(marks) > 1 else None,
            "return_ann": s["mu_h"] * HOURS_PER_YEAR if s["mu_h"] is not None else None,
            "vol_ann": math.sqrt(s["var_h"] * HOURS_PER_YEAR) if s["var_h"] is not None else None,
            "sharpe_ann": sharpe_dw(rs, dts),
            "max_drawdown_marks": mdd,
            "turnover_ann": (sum(abs(r["notional"]) for r in rows) / mean_eq / years) if mean_eq and years else None,
            "exposure_mean": (sum(r["w_held"] * r["elapsed_h"] for r in iv) / T) if T > 0 else None,
            "fees_and_costs_usdt": sum(r["cost_vs_mid"] for r in rows),
            "worst_interval_log": min(rs) if rs else None,
            "es5_log": (sum(srt[:k]) / k) if rs else None}


def schedule(start: dt.datetime, now: dt.datetime) -> list:
    out, t = [], start
    while t <= U.boundary(now):
        out.append(t)
        t += dt.timedelta(hours=4)
    return out


EVIDENCE_CLASSES = ("descriptive", "hypothesis", "exploratory", "prospectively supported", "inconclusive",
                    "unavailable", "retired")


def evidence_class(status: str, life: str, integrity_ok: bool) -> str:
    if not integrity_ok:
        return "unavailable"
    if life in ("terminated", "archived") and status in ("not launched", "collecting (descriptive)", "paused"):
        return "retired"
    return {"not launched": "hypothesis", "collecting (descriptive)": "descriptive", "paused": "descriptive",
            "paper-inconclusive": "inconclusive", "paper-supported (sizing, simulated)": "prospectively supported",
            "paper-unfavourable": "prospectively supported"}.get(status, "unavailable")


def auto_pause(base, sched: list, executed: set, now_ms: int, max_delay_ms: int) -> None:
    """Job pause when the last 6 scheduled decisions are all past their deadline with none executed."""
    st, _ = lifecycle(base)
    tail = sched[-6:]
    if st == "active" and len(tail) == 6 and not any(f"ps1-{t:%Y%m%dT%H%MZ}" in executed for t in tail) \
            and now_ms > U.ms(tail[-1]) + max_delay_ms:
        U.transition(base, ROOT, PROTOCOL_SHA256, "paused", by="job", reason="last 6 scheduled decisions not executed", t_ms=now_ms)


def report(base=BASE, now=None, proto=None) -> dict:
    base = Path(base)
    now = now or dt.datetime.now(U.UTC)
    proto = proto or json.loads(PROTOCOL.read_text())
    check_launch(base)
    launch = json.loads((base / LAUNCH).read_text()) if (base / LAUNCH).exists() else None
    ex, bad = ledger(base)
    for b in bad:
        U.integrity_failure(base, ROOT, f"execution {b['execution_id']}", b["reason"], b["expected"], b["found"])
    conf = verified_confirmations(base)
    bad_conf = {r["decision_id"] for r in U.rows(base / CONFIRMS)} - set(conf)
    decs = decisions(base)
    runs = U.rows(base / RUNS)
    states = exec_states(base)
    integrity = U.rows(base / ROOT / "integrity.jsonl")
    final_states = {}
    for eid, st in states.items():
        final_states[st[-1]["state"]] = final_states.get(st[-1]["state"], 0) + 1
    if launch:
        sched = schedule(U.parse(launch["first_decision_utc"]), now)
        auto_pause(base, sched, {r["decision_id"] for r in ex},
                   U.ms(now), proto["execution"]["max_delay_min"] * 60000)
    life, last = lifecycle(base)
    integrity_ok = not bad and not (bad_conf & {r["decision_id"] for r in ex})
    doc = {"generated_utc": U.iso_ms(U.ms(now)), "job": VERSION, "protocol": f"PS1 v{proto['version']}",
           "protocol_sha256": PROTOCOL_SHA256, "label": proto["label"], "launch": launch,
           "lifecycle": {"state": life, "last": last,
                         "authority": "termination and archiving: operator only; pause: operator or job (infrastructure)"},
           "retired_protocol": {"file": PROTOCOL_V1_RETIRED[0], "sha256": PROTOCOL_V1_RETIRED[1],
                                "state": "retired before launch, zero observations"},
           "execution_states": final_states,
           "integrity": {"ok": integrity_ok, "failures": len(integrity), "recent": integrity[-5:]}}
    if not launch:
        status = "not launched"
        doc.update(status=status, reason=f"no executed decision yet (not before {proto['start']['not_before_utc']})",
                   decisions_recorded=len(decs))
    else:
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
            elif did in bad_conf:
                k = "excluded: integrity failure"
            elif did in missed_exec:
                k = "missed-execution"
            else:
                k = "confirmed, not yet executed"
            reasons[k] = reasons.get(k, 0) + 1
        per = {}
        for s in SCENARIOS:
            per[s] = {a: arm_stats([r for r in ex if r["scenario"] == s and r["arm"] == a]) for a in ARMS}
        paired = {}
        for s in SCENARIOS:
            m = {a: {r["decision_utc"]: r for r in ex if r["scenario"] == s and r["arm"] == a} for a in ARMS}
            keys = [t for t in sorted(m["B2"]) if m["B2"][t].get("interval_log_return") is not None]
            b2 = [m["B2"][t]["interval_log_return"] for t in keys]
            vol = [m["VOL"][t]["interval_log_return"] for t in keys]
            fx = [m["FIXED"][t]["interval_log_return"] for t in keys]
            dts = [m["B2"][t]["elapsed_h"] for t in keys]
            n = len(b2)
            blocks = n // 42
            diffs = [x - y for x, y in zip(b2, vol)]
            sd = math.sqrt(sum((x - sum(diffs) / n) ** 2 for x in diffs) / (n - 1)) if n > 1 else None
            sb, sv = per[s]["B2"]["sharpe_ann"], per[s]["VOL"]["sharpe_ann"]
            rb, rv = per[s]["B2"]["return_ann"], per[s]["VOL"]["return_ann"]
            e = {"n_intervals": n, "blocks": blocks, "elapsed_hours": sum(dts),
                 "independent_observations": f"{blocks} complete block(s) of 42 intervals (the dependence unit); "
                                             f"{n} adjacent intervals are not independent",
                 "overlap_warning": "intervals are adjacent, not overlapping, but serially dependent (volatility clusters)",
                 "baselines": {"primary": "VOL", "control": "FIXED"},
                 "sharpe_diff_B2_minus_VOL": (sb - sv) if sb is not None and sv is not None else None,
                 "return_ann_diff_B2_minus_VOL": (rb - rv) if rb is not None and rv is not None else None,
                 "mean_log_diff_B2_minus_VOL": (sum(diffs) / n) if n else None,
                 "standardized_diff_B2_minus_VOL": (sum(diffs) / n / sd) if sd else None,
                 "mean_log_diff_B2_minus_FIXED": (sum(x - y for x, y in zip(b2, fx)) / n) if n else None,
                 "B2_better_intervals_vs_VOL": sum(x > y for x, y in zip(b2, vol)),
                 "uncertainty_method": proto["uncertainty"]["method"]}
            if blocks >= 10 and integrity_ok:
                e["sharpe_diff_ci90"] = bootstrap_sharpe_diff(b2, vol, dts)
            else:
                e["sharpe_diff_ci90"] = None
                e["uncertainty"] = (f"unavailable: {blocks} complete block(s) of 42 intervals; PS1 needs 10"
                                    if integrity_ok else "unavailable: integrity failure")
            paired[s] = e
        if not integrity_ok:
            per = {s: {a: {"withheld": "integrity failure; originals preserved"} for a in ARMS} for s in SCENARIOS}
        delays = sorted(r["delay_from_decision_ms"] / 60000 for r in ex if r["arm"] == "B2" and r["scenario"] == "ordinary")
        days = (now - U.parse(launch["first_decision_utc"])).total_seconds() / 86400
        ordered = sorted({r["decision_utc"] for r in ex})
        status = "paused" if life == "paused" else "collecting (descriptive)"
        doc.update(
            status=status,
            days_since_launch=round(days, 2), scheduled_decisions=len(sched), outcomes=reasons,
            coverage=round(reasons.get("executed", 0) / len(sched), 4) if sched else None,
            execution_delay_min={"median": _quantile(delays, 0.5), "max": delays[-1] if delays else None},
            time_accounting={"basis": "elapsed hours between fills; 8760 h/yr; duration-weighted; no interpolation",
                             "intervals": paired["ordinary"]["n_intervals"],
                             "elapsed_hours": paired["ordinary"]["elapsed_hours"],
                             "extended_intervals": per["ordinary"]["B2"].get("extended_intervals") if integrity_ok else None},
            arms=per, paired=paired,
            open_interval={"since_decision_utc": ordered[-1] if ordered else None,
                           "state": "pending - not marked until the next executed rebalance"},
            checkpoints={"C1": {"due_after_days": 180, "needs_blocks": 10}, "C2": {"due_after_days": 365, "needs_blocks": 20},
                         "progress": f"{days:.1f} days, {paired['ordinary']['blocks']} complete block(s)"},
            note="Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. "
                 "No status here is a trading edge or an entry endorsement.")
    doc["evidence_class"] = evidence_class(doc["status"], life, integrity_ok)
    doc["evidence_vocabulary"] = list(EVIDENCE_CLASSES)
    from storage import atomic_bytes
    atomic_bytes(base / "reports/paper_ps1.json", (json.dumps(doc, indent=1, sort_keys=True, default=str) + "\n").encode())
    atomic_bytes(base / "reports/paper_ps1.md", markdown(doc).encode())
    return doc


def _f(x, fmt="{:.4f}"):
    return "—" if x is None else fmt.format(x)


def markdown(doc: dict) -> str:
    L = ["# Paper sizing experiment PS1", "",
         f"Generated {doc['generated_utc']} by {doc['job']} ({doc['protocol']}, protocol sha256 {doc['protocol_sha256'][:12]}).", "",
         f"> {doc['label']}", "",
         f"**Status: {doc['status']}** · lifecycle {doc['lifecycle']['state']} · evidence class: {doc['evidence_class']}", "",
         f"PS1 v1 ({doc['retired_protocol']['sha256'][:12]}) was {doc['retired_protocol']['state']}; preserved at "
         f"`{doc['retired_protocol']['file']}`.", ""]
    if not doc["integrity"]["ok"] or doc["integrity"]["failures"]:
        L += [f"Integrity: {'FAILED - affected records excluded, metrics withheld' if not doc['integrity']['ok'] else 'ok'}; "
              f"{doc['integrity']['failures']} failure record(s) in streams/ps1/integrity.jsonl (originals preserved).", ""]
    if not doc.get("launch"):
        L += [doc.get("reason", ""), "", "Protocol: [desk/research/ps1/protocol.json](../desk/research/ps1/protocol.json)", ""]
        return "\n".join(L)
    ta = doc["time_accounting"]
    L += [f"Launched at decision {doc['launch']['first_decision_utc']}; {doc['days_since_launch']} days; "
          f"{doc['scheduled_decisions']} scheduled decisions; coverage {_f(doc['coverage'], '{:.1%}')}; "
          f"execution delay after the 4H close: median {_f(doc['execution_delay_min']['median'], '{:.1f}')} min, "
          f"max {_f(doc['execution_delay_min']['max'], '{:.1f}')} min.", "",
          f"Time accounting: {ta['basis']}. {ta['intervals']} intervals over {_f(ta['elapsed_hours'], '{:.1f}')} h; "
          f"extended intervals {ta['extended_intervals'] if ta['extended_intervals'] is not None else '—'}.", "",
          "Outcomes: " + "; ".join(f"{k} {v}" for k, v in sorted(doc["outcomes"].items())), "",
          "Execution states: " + ("; ".join(f"{k} {v}" for k, v in sorted(doc["execution_states"].items())) or "none"), ""]
    if doc["integrity"]["ok"]:
        L += ["| scenario | arm | intervals | hours | net return | return (ann.) | vol (ann.) | Sharpe (ann.) | exposure | turnover (ann.) | max DD | worst (log) | ES5% (log) |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for s, arms in doc["arms"].items():
            for a, st in arms.items():
                L.append(f"| {s} | {a} | {st['intervals']} | {_f(st['elapsed_hours'], '{:.0f}')} | {_f(st['net_return'], '{:.2%}')} | "
                         f"{_f(st['return_ann'], '{:.1%}')} | {_f(st['vol_ann'], '{:.1%}')} | {_f(st['sharpe_ann'], '{:.2f}')} | "
                         f"{_f(st['exposure_mean'], '{:.2f}')} | {_f(st['turnover_ann'], '{:.1f}')} | "
                         f"{_f(st['max_drawdown_marks'], '{:.2%}')} | {_f(st['worst_interval_log'], '{:.2%}')} | {_f(st['es5_log'], '{:.2%}')} |")
    L += ["", "| scenario | paired intervals | blocks | Sharpe B2−VOL | 90% interval | ann. return B2−VOL | mean log diff B2−VOL | standardized | B2−FIXED |",
          "|---|---|---|---|---|---|---|---|---|"]
    for s, e in doc["paired"].items():
        ci = e.get("sharpe_diff_ci90")
        L.append(f"| {s} | {e['n_intervals']} | {e['blocks']} | {_f(e['sharpe_diff_B2_minus_VOL'], '{:.3f}')} | "
                 f"{('[' + ', '.join(f'{x:.3f}' for x in ci) + ']') if ci else e.get('uncertainty')} | "
                 f"{_f(e['return_ann_diff_B2_minus_VOL'], '{:.2%}')} | {_f(e['mean_log_diff_B2_minus_VOL'], '{:.5f}')} | "
                 f"{_f(e['standardized_diff_B2_minus_VOL'], '{:.3f}')} | {_f(e['mean_log_diff_B2_minus_FIXED'], '{:.5f}')} |")
    o = doc["paired"]["ordinary"]
    L += ["", f"Independent observations: {o['independent_observations']}. {o['overlap_warning'].capitalize()}. "
              f"Uncertainty: {o['uncertainty_method']}. Baseline: VOL (primary), FIXED (control).",
          f"Open interval since {doc['open_interval']['since_decision_utc']}: {doc['open_interval']['state']}.",
          f"Checkpoints: C1 after 180 days with ≥10 blocks; C2 after 365 days with ≥20 blocks. Progress: {doc['checkpoints']['progress']}.",
          "", doc["note"], ""]
    return "\n".join(L)


def operator_lifecycle(new: str, reason: str, base=BASE) -> dict:
    """The operator's command: pause, resume (active), terminate, archive. Recorded with by='operator'."""
    return U.transition(base, ROOT, PROTOCOL_SHA256, new, by="operator", reason=reason)


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
        elif cmd == "lifecycle" and len(sys.argv) >= 4:
            print(operator_lifecycle(sys.argv[2], " ".join(sys.argv[3:])))
        else:
            raise SystemExit("usage: paper_ps1.py decide|confirm|execute|report | lifecycle <state> <reason>")
    except Refused as exc:
        _run_row(BASE, U.run_meta(), cmd, "refused", reason=str(exc))
        raise SystemExit(f"PS1 refused: {exc}")
    except (U.LifecycleError, RuntimeError) as exc:
        _run_row(BASE, U.run_meta(), cmd, "failed", reason=str(exc)[:300])
        raise SystemExit(f"PS1 {cmd} failed: {exc}")
