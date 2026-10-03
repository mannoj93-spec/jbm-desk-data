#!/usr/bin/env python3
"""paper_ps1 — the prospective paper sizing experiment PS1 (protocol desk/research/ps1/protocol.json, PS1 v3).

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
  report    reports/paper_ps1.{json,md}: lifecycle, coverage, delays, execution states, integrity, per-arm statistics
            and paired differences from the VERIFIED ledger only; any integrity failure withholds every performance
            figure. Open intervals are pending, never marked.
  lifecycle <state> <reason>   operator command (pause, resume, terminate, archive)
  checkpoint C1|C2 <note>      operator command after review: the immutable checkpoint record

Every command prints one machine-readable line, OUTCOME {"outcome", "class": done|expected|error, ...}, and exits 3
on class "error" (integrity failures, refusals the run must surface), 0 otherwise.
v3 (repo 2.22) replaces v2 and v1, both retired before launch with no observation (protocol_v2_retired.json,
protocol_v1_retired.json). Data root: $JBM_DESK_BASE if set (tests), else the repository.
The job refuses to run if the protocol, calibration or calibration script differ from the frozen hashes below.
Stdlib only. Network: Binance spot depth (www.binance.com, data-api.binance.vision), git. Records: streams/ps1/.
"""
from __future__ import annotations

import datetime as dt
import email.utils
import hashlib
import json
import math
import os
import random
import sys
import time
import urllib.request
from pathlib import Path

DESK = Path(__file__).resolve().parent
CODE = DESK.parent                                   # code and frozen research artifacts
BASE = Path(os.environ.get("JBM_DESK_BASE") or CODE)  # records (streams/, registry/, state/)
for p in (str(DESK), str(CODE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import stream_util as U          # noqa: E402

VERSION = "ps1-job-3.2.0"
PROTOCOL = DESK / "research/ps1/protocol.json"
PROTOCOL_SHA256 = "d0e8c837be9c3a1e51c8a4836d44e73851f488305b2748cb770f35ff1d909952"
PROTOCOL_V1_RETIRED = ("desk/research/ps1/protocol_v1_retired.json",
                       "00acb5bcf3e868e9d2023ff963c256f2fed23d6d2302552f109dab2193a48e8f")
PROTOCOL_V2_RETIRED = ("desk/research/ps1/protocol_v2_retired.json",
                       "be015545540d85ae8b9e0733167b9160704e4c8a743c810467cac57af377e560")
PROTOCOLS_RETIRED = (PROTOCOL_V2_RETIRED, PROTOCOL_V1_RETIRED)
ROOT = "streams/ps1"
DECISIONS, CONFIRMS, QUOTES = f"{ROOT}/decisions.jsonl", f"{ROOT}/confirmations.jsonl", f"{ROOT}/quotes.jsonl"
EXECUTIONS, RUNS, LAUNCH, TERMINATED = f"{ROOT}/executions.jsonl", f"{ROOT}/runs.jsonl", f"{ROOT}/launch.json", f"{ROOT}/terminated.json"
EXEC_STATES, CHECKPOINTS = f"{ROOT}/execution_states.jsonl", f"{ROOT}/checkpoints.jsonl"
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
    """The decision already has an execution (completed, recovered, in progress or failed) or ledger rows."""


class LifecycleHold(RuntimeError):
    """The lifecycle does not permit a fill to be written now (operator pause, termination, archiving)."""


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
        f = CODE / rel
        if not f.exists() or U.file_sha(f) != doc["calibration"][key]:
            raise Refused(f"calibration artifact {rel} missing or altered")
    cal = json.loads((CODE / doc["calibration"]["file"]).read_text())
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
# Records and bindings
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


def verify_confirmation(conf: dict | None, d: dict | None) -> tuple:
    """(ok, reason). The confirmation must be present, its binding intact, and the decision row as it stands
    now must reproduce the binding recorded at confirmation (not merely hash to something)."""
    if not isinstance(conf, dict):
        return False, "confirmation missing"
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


def confirmations(base) -> dict:
    out = {}
    for c in U.rows(Path(base) / CONFIRMS):
        out.setdefault(c.get("decision_id"), c)
    return out


def verified_confirmations(base, record=True) -> dict:
    """decision_id -> confirmation row, for bindings that verify; failures are recorded and excluded."""
    base = Path(base)
    decs = decisions(base)
    out = {}
    for did, c in confirmations(base).items():
        ok, why = verify_confirmation(c, decs.get(did))
        if ok:
            out[did] = c
        elif record:
            U.integrity_failure(base, ROOT, f"decision {did}", why,
                                expected=(c.get("binding") or {}).get("record_sha256"),
                                found=U.sha(decs[did]) if did in decs else None)
    return out


def exec_states(base) -> dict:
    """execution_id -> its journal rows in file order. A row that is not an object or has no string execution_id
    is grouped under None, which account() treats as a malformed journal (repo 2.24: never dropped or crashed on)."""
    out = {}
    for r in U.rows(Path(base) / EXEC_STATES):
        eid = r.get("execution_id") if isinstance(r, dict) else None
        out.setdefault(eid if isinstance(eid, str) else None, []).append(r)
    return out


# Allowed journal transitions (the writers: start_execution, recover). Terminal states take no later row.
TRANSITIONS = {"pending": {"running", "recovered", "failed", "partially_written"},
               "running": {"completed", "failed", "recovered", "partially_written"},
               "completed": set(), "recovered": set(), "failed": set(), "partially_written": set()}


def history_problem(st: list):
    """Why one execution's journal history is invalid, else None (repo 2.24, validated on every read): every row an
    object with a recognized state name and an integer time; the first row 'pending' carrying the snapshot; each
    step an allowed transition; nothing after a terminal state; a failed or partial state records its row count."""
    if not st:
        return "empty state history"
    for i, r in enumerate(st):
        if not isinstance(r, dict):
            return f"journal row {i} is not an object"
        if r.get("state") not in EXEC_STATE_NAMES:
            return f"unknown or missing state {r.get('state')!r} at journal row {i}"
        if not isinstance(r.get("t_ms"), int) or isinstance(r.get("t_ms"), bool):
            return f"journal row {i} ({r.get('state')}) has no integer time"
    if st[0]["state"] != "pending":
        return f"history starts at {st[0]['state']!r}, not pending"
    for a, b in zip(st, st[1:]):
        if b["state"] not in TRANSITIONS[a["state"]]:
            return f"invalid transition {a['state']} -> {b['state']}"
    last = st[-1]
    if last["state"] in ("failed", "partially_written"):
        n = last.get("rows_written", 0 if last["state"] == "failed" else None)
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            return f"{last['state']} state without a valid rows_written count"
    if last["state"] in FINAL_OK and not isinstance(last.get("rows_sha256"), str):
        return f"{last['state']} state without its rows hash"
    return None


def _state(base, eid, state, t_ms, **extra) -> dict:
    if state not in EXEC_STATE_NAMES:
        raise ValueError(state)
    row = dict({"execution_id": eid, "state": state, "t_ms": t_ms, "job": VERSION}, **extra)
    U.append(Path(base) / EXEC_STATES, row, key=lambda r: (r["execution_id"], r["state"], r["t_ms"]))
    return row


def rows_sha(rows: list) -> str:
    return U.sha(sorted(rows, key=lambda r: (r["scenario"], r["arm"])))


def snap_sha(snap: dict) -> str:
    """Hash of a snapshot without its own 'sha256' field."""
    return U.sha({k: v for k, v in snap.items() if k != "sha256"})


def _last_ok_execution(rows: list):
    return rows[-1]["execution_id"] if rows else None


def _quotes(base) -> dict:
    out = {}
    for r in U.rows(Path(base) / QUOTES):
        out.setdefault(r.get("quote_id"), r)
    return out


def _proto_unchecked() -> dict:
    """The protocol as frozen in this checkout (the job's own load_protocol() checks the hash)."""
    return json.loads(PROTOCOL.read_text())


# --------------------------------------------------------------------------------------------
# The one verified consumption path: execution, recovery and reporting all read the ledger through it
# --------------------------------------------------------------------------------------------
def verify_inputs(snap: dict, first_state: dict, decs: dict, confs: dict, quotes: dict, proto: dict,
                  prev_rows: list) -> tuple:
    """(ok, reason, decision, quote) for one execution's immutable inputs, before or after its rows exist:
    snapshot, protocol, decision, present and verified confirmation bound into the snapshot, quote and its
    eligibility, and the predecessor state it was built on. Missing evidence is a failure."""
    if not isinstance(snap, dict) or not snap:
        return False, "snapshot missing", None, None
    if snap_sha(snap) != first_state.get("snapshot_sha256") or snap.get("sha256") != first_state.get("snapshot_sha256"):
        return False, "snapshot altered", None, None
    if snap.get("protocol_sha256") != PROTOCOL_SHA256:
        return False, "snapshot made under another protocol", None, None
    d = decs.get(snap.get("decision_id"))
    if d is None or U.sha(d) != snap.get("decision_sha256"):
        return False, "decision row missing or changed since the snapshot", None, None
    conf = confs.get(snap.get("decision_id"))
    ok, why = verify_confirmation(conf, d)
    if not ok:
        return False, why, None, None
    if conf.get("binding_sha256") != snap.get("binding_sha256"):
        return False, "confirmation differs from the one the execution was bound to", None, None
    q = quotes.get(snap.get("quote_id"))
    if q is None or U.sha(q) != snap.get("quote_sha256"):
        return False, "quote row missing or changed since the snapshot", None, None
    executable = max(conf["confirmed_ms"], d["rc1d_available_ms"], d["computed_end_ms"])
    if executable != snap.get("executable_ms"):
        return False, "executable time differs from the snapshot", None, None
    deadline = U.ms(U.parse(d["decision_utc"])) + constants(proto)["max_delay_ms"]
    ok_q, why_q = eligible_quote(q, executable, deadline)
    if not ok_q or q.get("eligible") is not True:
        return False, f"quote not eligible on re-validation ({why_q})", None, None
    if snap.get("prior_execution_id") != _last_ok_execution(prev_rows) or snap.get("prior_sha256") != U.sha(_prior(prev_rows)):
        return False, "predecessor state differs from the snapshot", None, None
    return True, "verified", d, q


def _rows_by_execution(base) -> dict:
    by = {}
    for r in U.rows(Path(base) / EXECUTIONS):
        by.setdefault(r.get("execution_id"), []).append(r)
    return by


EXCLUDED = "excluded: no ledger row; the decision counts as not executed; original records preserved"
QUARANTINED = "quarantined: partial rows preserved in place, outside the ledger"


def account(states: dict, by: dict) -> dict:
    """Reconcile physical ledger rows with the execution-state journal, in both directions (repo 2.23).

    Every physical row must belong to exactly one execution with a state history: a final completed/recovered
    execution (verified by verify_chain), a recognized recoverable partial (pending/running, finished by
    recover()), a quarantined partial set (partially_written) or an explicit exclusion (failed, with the row count
    its state recorded). Rows with no state history, row counts that differ from the recorded state, rows naming
    another decision, incomplete state histories and two live executions of one decision are failures."""
    failures, exclusions, quarantined, in_progress, live = [], [], [], [], {}
    fail = lambda eid, why, rows=None: failures.append(                                   # noqa: E731
        {"execution_id": eid, "reason": why, "expected": None, "found": rows_sha(rows) if rows else None})
    for eid in sorted(set(by) - set(states), key=str):
        fail(eid, f"{len(by[eid])} ledger row(s) with no execution state history (unknown execution id)", by[eid])
    for eid, st in states.items():
        rows = by.get(eid, [])
        if eid is None:
            fail(None, f"{len(st)} malformed journal row(s) without an execution id", rows)
            continue
        why = history_problem(st)
        if why:
            fail(eid, f"execution state history invalid: {why}; {len(rows)} ledger row(s) unassigned", rows)
            continue
        first, last = st[0], st[-1]
        snap = first.get("snapshot") or {}
        did = first.get("decision_id")
        if first.get("state") != "pending" or snap.get("execution_id") != eid or snap.get("decision_id") != did:
            if last.get("state") not in FINAL_OK:                  # final ones fail inside verify_chain itself
                fail(eid, "execution state history incomplete (pending state with its snapshot missing)", rows)
            continue
        if any(r.get("decision_id") != did for r in rows):
            fail(eid, "ledger rows name another decision than the execution's snapshot", rows)
            continue
        state = last.get("state")
        if state in FINAL_OK or state in ("pending", "running"):
            live.setdefault(did, []).append(eid)
        if state in ("pending", "running"):
            in_progress.append({"execution_id": eid, "decision_id": did, "state": state, "rows": len(rows),
                                "disposition": "recoverable: recover() finishes or closes it from its snapshot"})
        elif state == "partially_written":
            if last.get("rows_written") != len(rows):
                fail(eid, f"quarantined execution records {last.get('rows_written')} row(s) but {len(rows)} exist", rows)
            else:
                quarantined.append({"execution_id": eid, "decision_id": did, "rows": len(rows), "disposition": QUARANTINED})
        elif state == "failed":
            n = last.get("rows_written", 0)
            if n != len(rows):
                fail(eid, f"failed execution records {n} row(s) but {len(rows)} exist", rows)
            else:
                exclusions.append({"decision_id": did, "execution_id": eid, "reason": last.get("reason"),
                                   "integrity": bool(last.get("integrity")), "rows_preserved": n,
                                   "t_ms": last.get("t_ms"),
                                   "disposition": EXCLUDED if not n else EXCLUDED + "; " + QUARANTINED})
    for did, eids in sorted(live.items()):
        if len(eids) > 1:
            for eid in eids[1:]:
                fail(eid, f"duplicate execution of decision {did} (also {eids[0]})", by.get(eid))
    return {"failures": failures, "exclusions": exclusions, "quarantined": quarantined, "in_progress": in_progress}


def verify_chain(base, proto=None) -> dict:
    """Verify every completed or recovered execution in fill order, and account for every physical ledger row
    (account()). A failed execution invalidates every later one (their balances derive from it); any unaccounted
    row fails the whole chain. Returns {rows, verified, failures, ok, exclusions, quarantined, in_progress,
    ledger_rows}."""
    base = Path(base)
    proto = proto or _proto_unchecked()
    states, decs, confs, quotes = exec_states(base), decisions(base), confirmations(base), _quotes(base)
    by = _rows_by_execution(base)
    acc = account(states, by)
    finals = [(eid, st) for eid, st in states.items()
              if eid is not None and not history_problem(st) and st[-1]["state"] in FINAL_OK]

    def order(item):
        snap = item[1][0].get("snapshot") or {}
        return ((quotes.get(snap.get("quote_id")) or {}).get("t_received_ms") or 0, item[0])
    good, verified, failures, broken = [], [], [], None
    expected = {(s, a) for s in SCENARIOS for a in ARMS}
    for eid, st in sorted(finals, key=order):
        fin, rows = st[-1], by.get(eid, [])
        if broken:
            failures.append({"execution_id": eid, "reason": f"depends on {broken}, which failed verification",
                             "expected": None, "found": None})
            continue
        why = None
        if st[0].get("state") != "pending" or (st[0].get("snapshot") or {}).get("execution_id") != eid:
            why = "pending state with its snapshot missing"
        else:
            ok, why_in, d, q = verify_inputs(st[0]["snapshot"], st[0], decs, confs, quotes, proto, good)
            if not ok:
                why = why_in
            elif len(rows) != len(expected) or {(r.get("scenario"), r.get("arm")) for r in rows} != expected \
                    or any(r.get("execution_id") != eid for r in rows):
                why = "execution rows are not exactly the six arm/scenario identities"
            elif rows_sha(rows) != fin.get("rows_sha256"):
                why = "execution rows differ from the hash recorded at completion"
            elif rows_sha(build_rows(st[0]["snapshot"], d, q, proto)) != fin.get("rows_sha256"):
                why = "execution rows are not reproducible from the snapshot"
        if why:
            failures.append({"execution_id": eid, "reason": why, "expected": fin.get("rows_sha256"),
                             "found": rows_sha(rows) if rows else None})
            broken = eid
            continue
        good.extend(sorted(rows, key=lambda r: (r["scenario"], r["arm"])))
        verified.append(eid)
    failures = acc["failures"] + failures
    physical = sum(len(v) for v in by.values())
    counted = {"verified": len(good), "quarantined": sum(q["rows"] for q in acc["quarantined"]),
               "excluded": sum(x["rows_preserved"] for x in acc["exclusions"]),
               "in_progress": sum(p["rows"] for p in acc["in_progress"])}
    unaccounted = physical - sum(counted.values())
    if not failures and unaccounted != 0:                     # conservation: every physical row exactly once
        failures.append({"execution_id": None, "reason": f"ledger conservation failed: {physical} physical rows, "
                         f"{sum(counted.values())} assigned ({counted})", "expected": physical, "found": sum(counted.values())})
    ledger_rows = dict(counted, physical=physical, unaccounted=unaccounted if not failures else None)
    return {"rows": good, "verified": verified, "failures": failures, "ok": not failures,
            "exclusions": acc["exclusions"], "quarantined": acc["quarantined"], "in_progress": acc["in_progress"],
            "ledger_rows": ledger_rows}


def ledger(base, proto=None) -> tuple:
    """(verified execution rows in fill order, failures) - the verified chain, in the 2.21 call shape."""
    ch = verify_chain(base, proto)
    return ch["rows"], ch["failures"]


def ledger_state(base, proto) -> dict:
    """(scenario, arm) -> {cash, btc} after the last verified execution; start equity otherwise. Refuses when the
    chain has any failure: balances derived from an invalid or unaccounted predecessor are never usable."""
    st = {(s, a): {"cash": float(proto["capital"]["start_equity_usdt"]), "btc": 0.0} for s in SCENARIOS for a in ARMS}
    rows, failures = ledger(base, proto)
    if failures:
        raise RuntimeError("ledger integrity failure; balances are unavailable: " + failures[0]["reason"])
    for r in rows:
        st[(r["scenario"], r["arm"])] = {"cash": r["cash_after"], "btc": r["btc_after"]}
    return st


def record_failures(base, failures: list) -> None:
    for f in failures:
        U.integrity_failure(base, ROOT, f"execution {f['execution_id']}", f["reason"], f.get("expected"), f.get("found"))


def expected_launch(chain: dict) -> dict | None:
    """The launch record the earliest verified execution implies: its own decision and fill time, never a retry
    time and never a later decision."""
    if not chain["verified"]:
        return None
    first = [r for r in chain["rows"] if r["execution_id"] == chain["verified"][0]][0]
    return {"first_decision_utc": first["decision_utc"], "first_execution_ms": first["fill_time_ms"],
            "protocol_sha256": PROTOCOL_SHA256, "job": VERSION}


def reconcile(base, chain: dict) -> dict:
    """Idempotent completion bookkeeping from the verified ledger: the launch record and the lifecycle
    activation. Safe to run on every pass; converges to what a clean run writes. A launch record that conflicts
    with the earliest verified execution is flagged, never overwritten."""
    base = Path(base)
    want = expected_launch(chain)
    out = {"launch": "none", "conflict": None}
    if want is None:
        if (base / LAUNCH).exists():
            have = json.loads((base / LAUNCH).read_text())
            if have.get("protocol_sha256") == PROTOCOL_SHA256:
                out.update(launch="conflict", conflict="launch record exists but no execution verifies")
        return out
    if (base / LAUNCH).exists():
        have = json.loads((base / LAUNCH).read_text())
        keys = ("first_decision_utc", "first_execution_ms", "protocol_sha256")
        if any(have.get(k) != want[k] for k in keys):
            out.update(launch="conflict", conflict=f"launch record {[have.get(k) for k in keys]} conflicts with the "
                                                   f"earliest verified execution {[want[k] for k in keys]}")
            U.integrity_failure(base, ROOT, "launch.json", "launch record conflicts with the earliest verified execution",
                                expected=want["first_decision_utc"], found=have.get("first_decision_utc"))
            return out
        out["launch"] = "present"
    else:
        from storage import atomic_json
        atomic_json(base / LAUNCH, want)
        out["launch"] = "written"
    # lifecycle: active from the first verified fill; a job pause ends at the first verified fill after it
    st, last = lifecycle(base)
    fills = sorted({r["fill_time_ms"] for r in chain["rows"]})
    if st == "approved":
        U.transition(base, ROOT, PROTOCOL_SHA256, "active", by="job", reason="first verified execution", t_ms=fills[0])
    elif st == "paused" and (last or {}).get("by") == "job":
        later = [f for f in fills if f > last["t_ms"]]
        if later:
            U.transition(base, ROOT, PROTOCOL_SHA256, "active", by="job", reason="verified execution after a job pause",
                         t_ms=later[0])
    return out

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
                       costs_version=proto["costs"]["version"], job=snap.get("job", VERSION),
                       snapshot_sha256=snap["sha256"])
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


def _guarded_write(base, rows, writer) -> None:
    """The execution write boundary (repo 2.23): the lifecycle is re-read immediately before any fill row is
    written, so an operator pause or termination that lands after the quote is honoured."""
    ok, st = stage_allowed(base, "execute")
    if not ok:
        raise LifecycleHold(st)
    writer(base, rows)


def _lifecycle_label(base) -> str:
    st, last = lifecycle(base)
    return f"{st} (by {(last or {}).get('by')})" if st == "paused" else st


def recover(base=BASE, proto=None, clock=U.clock_ms, run=None, writer=None) -> list:
    """Finish, close or hold every execution left pending or running, from its snapshot only (never a new quote,
    never a later fill time). Every input is verified BEFORE anything is written.

    Two different things are kept apart (repo 2.23):
      bookkeeping  all six rows were already persisted and reproduce from the snapshot: the fill happened, so the
                   state is closed as 'recovered' whatever the lifecycle is now (history is recorded, not created);
      completion   zero or some rows were written: writing the fill is new ledger activity, so it runs only while
                   the lifecycle permits execution. Under an operator pause the execution is HELD (left pending,
                   nothing written, resumed later from the same snapshot and its original quote timestamp); under
                   termination or archiving it is closed as failed with its rows preserved.
    A verification failure writes no ledger row and marks the execution failed (its decision is excluded).
    Returns one dict per execution handled: its state ('recovered', 'failed', 'held') and the action taken."""
    base = Path(base)
    proto = proto or load_protocol()
    run = run if run is not None else U.run_meta()
    writer = writer or _write_rows
    out = []
    for eid, st in exec_states(base).items():
        if eid is None or history_problem(st) or st[-1]["state"] not in ("pending", "running"):
            continue                                   # invalid histories fail verify_chain; nothing is rebuilt
        first = st[0]
        snap = first.get("snapshot") or {}
        written = [r for r in U.rows(base / EXECUTIONS) if r.get("execution_id") == eid]
        t = clock()
        chain = verify_chain(base, proto)
        if not chain["ok"]:
            why = "the verified ledger has failures; nothing is rebuilt on it"
        else:
            ok, why, d, q = verify_inputs(snap, first, decisions(base), confirmations(base), _quotes(base), proto,
                                          chain["rows"])
            why = None if ok else why
        if why:
            out.append(dict(_state(base, eid, "failed", t, reason=f"recovery impossible: {why}", rows_written=len(written),
                                   integrity=True), action="failed verification; no row written"))
            U.integrity_failure(base, ROOT, f"execution {eid}", f"recovery refused: {why}")
            _run_row(base, run, "execute", "missed-execution", decision_id=snap.get("decision_id"), reason=f"recovery failed: {why}")
            continue
        rows = build_rows(snap, d, q, proto)
        if written and len(written) == len(rows) and rows_sha(written) == rows_sha(rows):
            out.append(dict(_state(base, eid, "recovered", clock(), rows_sha256=rows_sha(rows), n_rows=len(rows),
                                   recovered_from=eid, note="every row had been written; verified against the snapshot"),
                            action="bookkeeping: rows already persisted; state closed"))
            reconcile(base, verify_chain(base, proto))
            _run_row(base, run, "execute", "recovered", decision_id=snap["decision_id"], execution_id=eid,
                     action="bookkeeping")
            continue
        life = U.lifecycle_state(base, ROOT, PROTOCOL_SHA256)
        if life in ("terminated", "archived"):
            out.append(dict(_state(base, eid, "failed", t, reason=f"{life} before recovery", rows_written=len(written),
                                   integrity=False), action=f"closed: lifecycle {life}; nothing written"))
            _run_row(base, run, "execute", "missed-execution", decision_id=snap.get("decision_id"), reason=life)
            continue
        allowed, _ = stage_allowed(base, "execute")
        if not allowed:
            label = _lifecycle_label(base)
            out.append({"execution_id": eid, "state": "held", "decision_id": snap.get("decision_id"),
                        "rows_written": len(written),
                        "action": f"held: lifecycle {label}; nothing written; resumes from the same snapshot"})
            _run_row(base, run, "execute", "held", decision_id=snap.get("decision_id"), execution_id=eid,
                     reason=f"lifecycle {label}")
            continue
        try:
            if not written:
                _guarded_write(base, rows, writer)
                out.append(dict(_state(base, eid, "recovered", clock(), rows_sha256=rows_sha(rows), n_rows=len(rows),
                                       recovered_from=eid, note="no row had been written; rebuilt from the snapshot"),
                                action="completed from the snapshot (original quote and fill time)"))
            else:
                eid2 = f"{eid}~r1"
                snap2 = dict(snap, execution_id=eid2)
                snap2["sha256"] = snap_sha(snap2)
                rows2 = build_rows(snap2, d, q, proto)
                ok_now, _ = stage_allowed(base, "execute")
                if not ok_now:
                    raise LifecycleHold(U.lifecycle_state(base, ROOT, PROTOCOL_SHA256))
                _state(base, eid, "partially_written", t, rows_written=len(written),
                       note="partial rows preserved in place; excluded from the ledger")
                _state(base, eid2, "pending", clock(), snapshot=snap2, snapshot_sha256=snap2["sha256"],
                       decision_id=snap["decision_id"], recovers=eid)
                _guarded_write(base, rows2, writer)
                out.append(dict(_state(base, eid2, "recovered", clock(), rows_sha256=rows_sha(rows2), n_rows=len(rows2),
                                       recovered_from=eid, note="rebuilt from the original snapshot under a new id"),
                                action="completed under a new id from the original snapshot; partial rows quarantined"))
        except LifecycleHold as hold:
            out.append({"execution_id": eid, "state": "held", "decision_id": snap.get("decision_id"),
                        "rows_written": len(written), "action": f"held at the write boundary: lifecycle {hold}"})
            _run_row(base, run, "execute", "held", decision_id=snap.get("decision_id"), execution_id=eid,
                     reason=f"lifecycle {hold} at the write boundary")
            continue
        reconcile(base, verify_chain(base, proto))
        _run_row(base, run, "execute", "recovered", decision_id=snap["decision_id"], execution_id=eid,
                 action="completion")
    return out


def start_execution(base, d, conf, quote, proto, clock, run, writer=None) -> dict:
    """Execute one verified decision on one eligible, recorded quote. Raises DuplicateExecution if the decision
    already has any execution state OR any physical ledger row (repo 2.23: duplicate prevention does not depend
    on the state journal alone). Order: snapshot -> six rows (one atomic write, lifecycle re-checked at the
    boundary) -> completed -> reconcile (launch, lifecycle); every step after the write is idempotent."""
    base = Path(base)
    writer = writer or _write_rows
    states = exec_states(base)
    if any(isinstance(r, dict) and r.get("decision_id") == d["decision_id"] for st in states.values() for r in st):
        raise DuplicateExecution(f"{d['decision_id']} already has an execution")
    if any(r.get("decision_id") == d["decision_id"] for r in U.rows(base / EXECUTIONS)):
        raise DuplicateExecution(f"{d['decision_id']} already has ledger rows")
    chain = verify_chain(base, proto)
    if not chain["ok"]:
        raise RuntimeError("ledger integrity failure; execution refused")
    good = chain["rows"]
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
    try:
        _guarded_write(base, rows, writer)
    except LifecycleHold as hold:
        return _state(base, eid, "failed", clock(), reason=f"lifecycle {hold} during execution; no ledger row written",
                      rows_written=0, integrity=False)
    done = _state(base, eid, "completed", clock(), rows_sha256=rows_sha(rows), n_rows=len(rows))
    reconcile(base, verify_chain(base, proto))
    return done


def _result(outcome: str, klass: str, **extra) -> dict:
    """A machine-readable stage outcome: class 'done' (work performed), 'expected' (a protocol state such as
    pre-launch, pause, nothing new, missing market data) or 'error' (integrity or refusal the run must surface)."""
    return dict({"outcome": outcome, "class": klass, "job": VERSION}, **extra)


def execute(base=BASE, clock=U.clock_ms, fetch=fetch_depth, proto=None, run=None, pause=time.sleep, writer=None) -> dict:
    """Recover interrupted executions, verify the ledger, reconcile launch/lifecycle, then execute the newest
    confirmed, unexecuted decision on a quote captured now. Returns a machine-readable outcome."""
    base = Path(base)
    proto = proto or load_protocol()
    run = run if run is not None else U.run_meta()
    c = constants(proto)
    check_launch(base)
    rec = recover(base, proto, clock, run, writer)
    actions = [{k: r.get(k) for k in ("execution_id", "state", "action")} for r in rec]
    failed_rec = [r for r in rec if r["state"] == "failed" and r.get("integrity")]
    chain = verify_chain(base, proto)
    if not chain["ok"] or failed_rec:
        record_failures(base, chain["failures"])
        _run_row(base, run, "execute", "refused: ledger integrity failure")
        return _result("refused: ledger integrity failure", "error",
                       failures=[f["reason"] for f in chain["failures"]] + [r["reason"] for r in failed_rec],
                       recovery=actions, ledger_rows=chain["ledger_rows"])
    rc = reconcile(base, chain)
    if rc["launch"] == "conflict":
        _run_row(base, run, "execute", "refused: launch record conflict")
        return _result("refused: launch record conflict", "error", reason=rc["conflict"])
    excl = [{k: x[k] for k in ("decision_id", "reason", "disposition")} for x in chain["exclusions"]]
    ok, st = stage_allowed(base, "execute")
    if not ok:
        _run_row(base, run, "execute", f"refused: lifecycle {st}")
        return _result(f"refused: lifecycle {st}", "expected", recovery=actions, exclusions=excl)
    recovered = [r["execution_id"] for r in rec if r["state"] == "recovered"]
    conf = verified_confirmations(base)
    bad_conf = set(confirmations(base)) - set(conf)
    if bad_conf:
        _run_row(base, run, "execute", "refused: confirmation integrity failure")
        return _result("refused: confirmation integrity failure", "error", decisions=sorted(bad_conf))
    started = {r.get("decision_id") for st_ in exec_states(base).values() for r in st_ if isinstance(r, dict)}
    in_ledger = {r.get("decision_id") for r in U.rows(base / EXECUTIONS)}
    done = started | in_ledger | {r["decision_id"] for r in U.rows(base / RUNS)
                                  if r.get("stage") == "execute" and r.get("outcome") == "missed-execution" and r.get("decision_id")}
    cands = sorted((d for d in decisions(base).values() if d.get("action") == "rebalance" and d["decision_id"] in conf
                    and d["decision_id"] not in done), key=lambda d: d["decision_utc"])
    if not cands:
        tail = f" ({len(excl)} excluded decision(s) on record)" if excl else ""
        return _result(("recovered" if recovered else "nothing to execute") + tail, "done" if recovered else "expected",
                       recovered=recovered, recovery=actions, exclusions=excl)
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
        return _result("no eligible quote", "expected", decision_id=d["decision_id"], reason=why)
    try:
        res = start_execution(base, d, conf[d["decision_id"]], quote, proto, clock, run, writer)
    except DuplicateExecution as exc:
        _run_row(base, run, "execute", "refused: duplicate", decision_id=d["decision_id"], reason=str(exc))
        return _result("refused: duplicate execution", "error", decision_id=d["decision_id"], reason=str(exc))
    if res["state"] != "completed":
        _run_row(base, run, "execute", "missed-execution", decision_id=d["decision_id"], reason=res.get("reason"))
        return _result(res["state"], "expected", decision_id=d["decision_id"], reason=res.get("reason"))
    _run_row(base, run, "execute", "executed", decision_id=d["decision_id"], quote_id=quote["quote_id"],
             execution_id=res["execution_id"])
    return _result("executed", "done", decision_id=d["decision_id"], rows=res["n_rows"], execution_id=res["execution_id"])


# --------------------------------------------------------------------------------------------
# Statistics (protocol v3 metrics.time_accounting)
# --------------------------------------------------------------------------------------------
def dw_stats(rs: list, dts: list) -> dict:
    """Drift and variance RATES (per hour) of interval log returns under the protocol's working model:
    independent increments r_i = mu*h_i + sigma*sqrt(h_i)*e_i, E[e]=0, Var[e]=1.
      mu_h  = sum(r_i) / sum(h_i)                          (weighted least squares with weights 1/h_i)
      var_h = sum((r_i - mu_h*h_i)^2 / h_i) / (n - 1)       (unbiased for sigma^2 under the model, any h_i)
    v2's var_h = sum((r_i - mu_h*h_i)^2) / (T*(n-1)/n) is unbiased only for equal durations (its expectation is
    sigma^2 * (T - sum(h^2)/T) / (T*(n-1)/n)). Durations must be finite and > 0."""
    n = len(rs)
    if n != len(dts) or any((not isinstance(h, (int, float))) or not math.isfinite(h) or h <= 0 for h in dts) \
            or any(not math.isfinite(r) for r in rs):
        return {"mu_h": None, "var_h": None, "invalid": True}
    T = sum(dts)
    if n == 0:
        return {"mu_h": None, "var_h": None}
    mu = sum(rs) / T
    if n < 2:
        return {"mu_h": mu, "var_h": None}
    var = sum((r - mu * h) ** 2 / h for r, h in zip(rs, dts)) / (n - 1)
    return {"mu_h": mu, "var_h": var}


def sharpe_dw(rs: list, dts: list):
    """Annualized log-return Sharpe: (8760*mu_h) / sqrt(8760*var_h) = sqrt(8760)*mu_h/sigma_h (cash yield 0).
    A ratio of log-return drift to log-return volatility, not a simple-return Sharpe."""
    s = dw_stats(rs, dts)
    if s.get("var_h") is None or s["var_h"] <= 0:
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
    """Moving-block bootstrap of paired intervals ((a, b, h) resampled together; blocks are a resampling device
    for serial dependence, not a measured effective sample size): 90% interval of SR(a) - SR(b)."""
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
    """One arm's verified executions in fill order. Returns and risk use CLOSED intervals only (the interval
    opened by the latest trade is pending). Costs and turnover are reported for the same closed scope - the
    trades that opened closed intervals, rows[:-1] - and separately including the latest (open) trade."""
    iv = [r for r in rows if r.get("interval_log_return") is not None]
    rs, dts = [r["interval_log_return"] for r in iv], [r["elapsed_h"] for r in iv]
    T = sum(dts)
    s = dw_stats(rs, dts)
    marks = [r["equity_pre"] for r in rows]
    peak, mdd = -1.0, 0.0
    for m in marks:
        peak = max(peak, m)
        mdd = min(mdd, m / peak - 1)
    closed = rows[:-1] if len(rows) > 1 else []
    closed_marks = marks[:len(closed)] or []
    mean_eq = sum(closed_marks) / len(closed_marks) if closed_marks else None
    years = T / HOURS_PER_YEAR if T > 0 else None
    srt = sorted(rs)
    k = max(1, len(srt) // 20)
    return {"intervals": len(iv), "elapsed_hours": T if iv else 0.0,
            "extended_intervals": sum(1 for r in iv if r.get("interval_flag", "").startswith("extended")),
            "longest_interval_h": max(dts) if dts else None,
            "net_return_closed": (marks[-1] / marks[0] - 1) if len(marks) > 1 else None,
            "log_return_ann": s["mu_h"] * HOURS_PER_YEAR if s.get("mu_h") is not None else None,
            "vol_ann": math.sqrt(s["var_h"] * HOURS_PER_YEAR) if s.get("var_h") is not None else None,
            "sharpe_ann": sharpe_dw(rs, dts),
            "max_drawdown_marks": mdd,
            "turnover_ann_closed": (sum(abs(r["notional"]) for r in closed) / mean_eq / years) if mean_eq and years else None,
            "exposure_mean": (sum(r["w_held"] * r["elapsed_h"] for r in iv) / T) if T > 0 else None,
            "costs_usdt_closed": sum(r["cost_vs_mid"] for r in closed),
            "costs_usdt_incl_open_trade": sum(r["cost_vs_mid"] for r in rows),
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
    """Job pause when the last six scheduled decisions WHOSE DEADLINES HAVE PASSED were all unexecuted.
    Decisions still inside their execution window are pending and never count as misses. Only an active stream
    is paused; an operator pause is never touched."""
    st, _ = lifecycle(base)
    expired = [t for t in sched if U.ms(t) + max_delay_ms < now_ms]
    tail = expired[-6:]
    if st == "active" and len(tail) == 6 and not any(f"ps1-{t:%Y%m%dT%H%MZ}" in executed for t in tail):
        U.transition(base, ROOT, PROTOCOL_SHA256, "paused", by="job",
                     reason=f"six expired scheduled decisions not executed ({U.iso(tail[0])} .. {U.iso(tail[-1])})",
                     t_ms=U.ms(tail[-1]) + max_delay_ms)


# --------------------------------------------------------------------------------------------
# Checkpoints (C1, C2): operator-reviewed, immutable records
# --------------------------------------------------------------------------------------------
def c2_status(paired: dict, arms: dict, coverage) -> tuple:
    """The protocol's C2 rule applied mechanically, for the operator's review: (status, criteria)."""
    o, s = paired["ordinary"], paired["stressed"]
    ci = o.get("sharpe_diff_ci90")
    crit = {"a_ci90_above_0_ordinary": bool(ci and ci[0] > 0),
            "b_point_above_0_stressed": bool(s.get("sharpe_diff_B2_minus_VOL") is not None and s["sharpe_diff_B2_minus_VOL"] > 0),
            "c_coverage_at_least_80pct": bool(coverage is not None and coverage >= 0.8),
            "d_vol_10_to_20pct_both_arms": all((arms["ordinary"][a].get("vol_ann") or -1) >= 0.10
                                               and (arms["ordinary"][a].get("vol_ann") or 99) <= 0.20 for a in ("B2", "VOL"))}
    if all(crit.values()):
        return "paper-supported (sizing, simulated)", crit
    if ci and ci[1] < 0:
        return "paper-unfavourable", crit
    return "paper-inconclusive", crit


def checkpoints(base) -> dict:
    out = {}
    for r in U.rows(Path(base) / CHECKPOINTS):
        out.setdefault(r.get("checkpoint"), r)
    return out


def record_checkpoint(name: str, by: str, note: str, base=BASE, now=None, proto=None) -> dict:
    """Write the immutable C1 or C2 record after the operator's review. Refused unless the registered
    conditions are met (days since launch, complete blocks, verified ledger). C1 never changes the status;
    C2 applies the protocol's rule. The job never writes a checkpoint on its own."""
    base = Path(base)
    if by != "operator":
        raise U.LifecycleError("checkpoints are recorded by the operator after review")
    if name not in ("C1", "C2"):
        raise ValueError("checkpoint must be C1 or C2")
    if name in checkpoints(base):
        raise ValueError(f"{name} already recorded; checkpoint records are immutable")
    doc = report(base, now=now, proto=proto)
    if not doc.get("launch"):
        raise ValueError("not launched")
    if not doc["integrity"]["ok"]:
        raise ValueError("integrity failure: no checkpoint can be recorded")
    need_days, need_blocks = {"C1": (180, 10), "C2": (365, 20)}[name]
    blocks = doc["paired"]["ordinary"]["blocks"]
    if doc["days_since_launch"] < need_days or blocks < need_blocks:
        raise ValueError(f"{name} not due: {doc['days_since_launch']:.1f} days and {blocks} blocks "
                         f"(needs {need_days} days and {need_blocks} blocks)")
    if name == "C1":
        status, crit = "collecting (descriptive)", {"note": "C1 is descriptive; no status change"}
    else:
        status, crit = c2_status(doc["paired"], doc["arms"], doc["coverage"])
    row = {"checkpoint": name, "status": status, "criteria": crit, "by": by, "note": note, "t_ms": U.clock_ms(),
           "protocol_sha256": PROTOCOL_SHA256, "days_since_launch": doc["days_since_launch"], "blocks": blocks,
           "ledger_sha256": U.sha([r["execution_id"] for r in ledger(base, proto)[0]]),
           "figures": {"paired": doc["paired"], "coverage": doc["coverage"]}}
    U.append(base / CHECKPOINTS, row, key=lambda r: (r["checkpoint"],))
    return row


# --------------------------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------------------------
WITHHELD = "withheld: integrity failure (records preserved; see integrity.failures)"


def report(base=BASE, now=None, proto=None) -> dict:
    base = Path(base)
    now = now or dt.datetime.now(U.UTC)
    proto = proto or _proto_unchecked()
    check_launch(base)
    chain = verify_chain(base, proto)
    record_failures(base, chain["failures"])
    rc = reconcile(base, chain)
    conf = verified_confirmations(base)
    bad_conf = sorted(set(confirmations(base)) - set(conf))
    ex = chain["rows"]
    launch = json.loads((base / LAUNCH).read_text()) if (base / LAUNCH).exists() else None
    decs = decisions(base)
    runs = U.rows(base / RUNS)
    states = exec_states(base)
    integrity_rows = U.rows(base / ROOT / "integrity.jsonl")
    final_states = {}
    for eid, st in states.items():
        k = st[-1].get("state") if eid is not None and not history_problem(st) else "invalid history"
        final_states[k] = final_states.get(k, 0) + 1
    integrity_ok = chain["ok"] and not bad_conf and rc["launch"] != "conflict"
    excluded = {x["decision_id"]: x for x in chain["exclusions"]}
    if launch and integrity_ok:
        sched = schedule(U.parse(launch["first_decision_utc"]), now)
        auto_pause(base, sched, {r["decision_id"] for r in ex}, U.ms(now), proto["execution"]["max_delay_min"] * 60000)
    life, last = lifecycle(base)
    cps = checkpoints(base)
    observed = [r["fill_time_ms"] for r in ex] + [U.ms(U.parse(d["data_cutoff_utc"])) for d in decs.values()
                                                     if d.get("data_cutoff_utc")]
    processed = [d.get("computed_end_ms") or 0 for d in decs.values()] + [st[-1].get("t_ms") or 0 for st in states.values()]
    source_cutoff, processed_ms = max(observed or [0]), max(processed or [0])
    doc = {"report": "paper_ps1", "schema": "ps1-report-4", "generated_utc": U.iso_ms(U.ms(now)), "job": VERSION,
           "processed_utc": U.iso_ms(processed_ms) if processed_ms else None,
           "clocks": {"generated_utc": "when this report file was written",
                      "processed_utc": "latest decision computation or execution-state record (processing)",
                      "source_cutoff_utc": "latest market observation used: the 4H close a rebalance decision read, "
                                           "or a captured quote's receipt (repo 2.23; 2.22 also counted computation "
                                           "time); null before the first decision - expected pre-launch, not a "
                                           "collection failure"},
           "protocol": f"PS1 v{proto['version']}", "protocol_sha256": PROTOCOL_SHA256, "label": proto["label"],
           "source_cutoff_utc": U.iso_ms(source_cutoff) if source_cutoff else None,
           "launch": launch,
           "lifecycle": {"state": life, "paused_by": (last or {}).get("by") if life == "paused" else None, "last": last,
                         "authority": "termination and archiving: operator only; pause: operator or job (infrastructure)"},
           "retired_protocols": [{"file": f, "sha256": h, "state": "retired before launch, zero observations"}
                                 for f, h in PROTOCOLS_RETIRED],
           "execution_states": final_states,
           "integrity": {"ok": integrity_ok,
                         "state": ("failed" if not integrity_ok else
                                   "verified with exclusions" if chain["exclusions"] or chain["quarantined"] else "verified"),
                         "verified_executions": len(chain["verified"]),
                         "failed_executions": [f["execution_id"] for f in chain["failures"]],
                         "failures": [f["reason"] for f in chain["failures"]] + [f"confirmation {d}" for d in bad_conf]
                         + ([rc["conflict"]] if rc["launch"] == "conflict" else []),
                         "excluded_decisions": chain["exclusions"],
                         "quarantined_executions": chain["quarantined"],
                         "in_progress_executions": chain["in_progress"],
                         "ledger_rows": chain["ledger_rows"],
                         "scope": ("every physical ledger row is accounted for: verified, quarantined, excluded or in "
                                   "progress" if chain["ok"] else "ledger reconciliation failed; see failures"),
                         "recorded_failures": len(integrity_rows),
                         "recorded_failures_note": "integrity.jsonl is the append-only history of every failure ever "
                                                   "recorded; current status is 'state' (resolved exclusions stay listed "
                                                   "in excluded_decisions)"},
           "checkpoints": {k: {"status": v["status"], "t_ms": v["t_ms"], "by": v["by"]} for k, v in cps.items()}}
    if not launch:
        status = "not launched"
        doc.update(status=status, reason=f"no verified execution yet (not before {proto['start']['not_before_utc']})",
                   decisions_recorded=len(decs))
    else:
        executed = {r["decision_id"] for r in ex}
        missed_exec = {r["decision_id"]: r.get("reason") for r in runs if r.get("stage") == "execute" and r.get("outcome") == "missed-execution"}
        reasons = {}
        sched = schedule(U.parse(launch["first_decision_utc"]), now)
        for t in sched:
            did = f"ps1-{t:%Y%m%dT%H%MZ}"
            d = decs.get(did)
            pending = (now - t) <= dt.timedelta(minutes=proto["execution"]["max_delay_min"])
            if did in executed:
                k = "executed"
            elif d is None:
                k = "pending" if pending else "missed: no run"
            elif d["action"] != "rebalance":
                k = f"{d['action']}: {str(d.get('reason', '')).split(' (')[0]}"
            elif did in bad_conf:
                k = "excluded: integrity failure"
            elif did in excluded:
                k = ("excluded: integrity failure" if excluded[did]["integrity"] else "excluded: lifecycle")
            elif did in missed_exec:
                k = "missed-execution"
            else:
                k = "pending" if pending else "confirmed, not executed"
            reasons[k] = reasons.get(k, 0) + 1
        per = {s: {a: arm_stats([r for r in ex if r["scenario"] == s and r["arm"] == a]) for a in ARMS} for s in SCENARIOS}
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
            rb, rv = per[s]["B2"]["log_return_ann"], per[s]["VOL"]["log_return_ann"]
            e = {"n_intervals": n, "blocks": blocks, "elapsed_hours": sum(dts),
                 "dependence": "adjacent, non-overlapping intervals that are serially dependent (volatility clusters); "
                               "42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size",
                 "baselines": {"primary": "VOL", "control": "FIXED"},
                 "sharpe_diff_B2_minus_VOL": (sb - sv) if sb is not None and sv is not None else None,
                 "log_return_ann_diff_B2_minus_VOL": (rb - rv) if rb is not None and rv is not None else None,
                 "mean_log_diff_B2_minus_VOL": (sum(diffs) / n) if n else None,
                 "standardized_diff_B2_minus_VOL": (sum(diffs) / n / sd) if sd else None,
                 "mean_log_diff_B2_minus_FIXED": (sum(x - y for x, y in zip(b2, fx)) / n) if n else None,
                 "B2_better_intervals_vs_VOL": sum(x > y for x, y in zip(b2, vol)),
                 "uncertainty_method": proto["uncertainty"]["method"]}
            if blocks >= 10:
                e["sharpe_diff_ci90"] = bootstrap_sharpe_diff(b2, vol, dts)
            else:
                e["sharpe_diff_ci90"] = None
                e["uncertainty"] = f"unavailable: {blocks} complete block(s) of 42 intervals; PS1 needs 10"
            paired[s] = e
        if not integrity_ok:                                  # every affected performance figure, not just the arms
            per = {s: {a: {"withheld": WITHHELD} for a in ARMS} for s in SCENARIOS}
            paired = {s: {"withheld": WITHHELD, "n_intervals": paired[s]["n_intervals"], "blocks": paired[s]["blocks"]}
                      for s in SCENARIOS}
        delays = sorted(r["delay_from_decision_ms"] / 60000 for r in ex if r["arm"] == "B2" and r["scenario"] == "ordinary")
        days = (now - U.parse(launch["first_decision_utc"])).total_seconds() / 86400
        ordered = sorted({r["decision_utc"] for r in ex})
        status = cps["C2"]["status"] if "C2" in cps else ("paused" if life == "paused" else "collecting (descriptive)")
        doc.update(
            status=status,
            days_since_launch=round(days, 2), scheduled_decisions=len(sched), outcomes=reasons,
            coverage=round(reasons.get("executed", 0) / len(sched), 4) if sched else None,
            execution_delay_min={"median": _quantile(delays, 0.5), "max": delays[-1] if delays else None},
            time_accounting={"basis": "elapsed hours between fills; 8760 h/yr; drift and variance rates per hour "
                                      "(protocol v3); no interpolation; the interval opened by the latest trade is pending",
                             "intervals": paired["ordinary"]["n_intervals"],
                             "elapsed_hours": paired["ordinary"].get("elapsed_hours"),
                             "extended_intervals": per["ordinary"]["B2"].get("extended_intervals")},
            arms=per, paired=paired,
            open_interval={"since_decision_utc": ordered[-1] if ordered else None,
                           "state": "pending - not marked until the next executed rebalance"},
            checkpoint_progress={"C1": {"due_after_days": 180, "needs_blocks": 10, "recorded": "C1" in cps},
                                 "C2": {"due_after_days": 365, "needs_blocks": 20, "recorded": "C2" in cps},
                                 "owner": "operator (paper_ps1.py checkpoint C1|C2 \"<note>\"); the job never records one",
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
         f"Generated {doc['generated_utc']} by {doc['job']} ({doc['protocol']}, protocol sha256 {doc['protocol_sha256'][:12]}); "
         f"source cutoff {doc['source_cutoff_utc'] or '—'}.", "",
         f"> {doc['label']}", "",
         f"**Status: {doc['status']}** · lifecycle {doc['lifecycle']['state']}"
         + (f" (by {doc['lifecycle']['paused_by']})" if doc['lifecycle'].get('paused_by') else "")
         + f" · evidence class: {doc['evidence_class']} · integrity: {'ok' if doc['integrity']['ok'] else 'FAILED'}", ""]
    L += ["Retired before launch, zero observations: " + ", ".join(f"`{r['file']}` ({r['sha256'][:12]})" for r in doc["retired_protocols"]), ""]
    if not doc["integrity"]["ok"]:
        L += ["Integrity failed: every performance figure is withheld; the records stay as found. "
              + "; ".join(doc["integrity"]["failures"][:5]), ""]
    lr = doc["integrity"].get("ledger_rows") or {}
    if lr.get("physical"):
        L += [f"Ledger rows: {lr['physical']} physical; {lr['verified']} verified, {lr['quarantined']} quarantined, "
              f"{lr['excluded']} excluded, {lr['in_progress']} in progress"
              + (f", {lr['unaccounted']} unaccounted" if lr.get("unaccounted") else "") + ".", ""]
    for x in doc["integrity"].get("excluded_decisions") or []:
        L += [f"Excluded decision {x['decision_id']} ({'integrity' if x['integrity'] else 'lifecycle'}): {x['reason']}. "
              f"{x['disposition']}.", ""]
    if not doc.get("launch"):
        L += [doc.get("reason", ""), "", "Protocol: [desk/research/ps1/protocol.json](../desk/research/ps1/protocol.json)", ""]
        return "\n".join(L)
    ta = doc["time_accounting"]
    L += [f"Launched at decision {doc['launch']['first_decision_utc']}; {doc['days_since_launch']} days; "
          f"{doc['scheduled_decisions']} scheduled decisions; coverage {_f(doc['coverage'], '{:.1%}')}; "
          f"execution delay after the 4H close: median {_f(doc['execution_delay_min']['median'], '{:.1f}')} min, "
          f"max {_f(doc['execution_delay_min']['max'], '{:.1f}')} min.", "",
          f"Time accounting: {ta['basis']}. {ta['intervals']} closed intervals over {_f(ta['elapsed_hours'], '{:.1f}')} h; "
          f"extended intervals {ta['extended_intervals'] if ta['extended_intervals'] is not None else '—'}.", "",
          "Outcomes: " + "; ".join(f"{k} {v}" for k, v in sorted(doc["outcomes"].items())), "",
          "Execution states: " + ("; ".join(f"{k} {v}" for k, v in sorted(doc["execution_states"].items())) or "none"), ""]
    if doc["integrity"]["ok"]:
        L += ["| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for s, arms in doc["arms"].items():
            for a, st in arms.items():
                L.append(f"| {s} | {a} | {st['intervals']} | {_f(st['elapsed_hours'], '{:.0f}')} | {_f(st['net_return_closed'], '{:.2%}')} | "
                         f"{_f(st['log_return_ann'], '{:.1%}')} | {_f(st['vol_ann'], '{:.1%}')} | {_f(st['sharpe_ann'], '{:.2f}')} | "
                         f"{_f(st['exposure_mean'], '{:.2f}')} | {_f(st['turnover_ann_closed'], '{:.1f}')} | "
                         f"{_f(st['costs_usdt_closed'], '{:.2f}')} / {_f(st['costs_usdt_incl_open_trade'], '{:.2f}')} | "
                         f"{_f(st['max_drawdown_marks'], '{:.2%}')} | {_f(st['worst_interval_log'], '{:.2%}')} | {_f(st['es5_log'], '{:.2%}')} |")
        L += ["", "| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |",
              "|---|---|---|---|---|---|---|---|---|"]
        for s, e in doc["paired"].items():
            ci = e.get("sharpe_diff_ci90")
            L.append(f"| {s} | {e['n_intervals']} | {e['blocks']} | {_f(e['sharpe_diff_B2_minus_VOL'], '{:.3f}')} | "
                     f"{('[' + ', '.join(f'{x:.3f}' for x in ci) + ']') if ci else e.get('uncertainty')} | "
                     f"{_f(e['log_return_ann_diff_B2_minus_VOL'], '{:.2%}')} | {_f(e['mean_log_diff_B2_minus_VOL'], '{:.5f}')} | "
                     f"{_f(e['standardized_diff_B2_minus_VOL'], '{:.3f}')} | {_f(e['mean_log_diff_B2_minus_FIXED'], '{:.5f}')} |")
        o = doc["paired"]["ordinary"]
        L += ["", f"Dependence: {o['dependence']}. Uncertainty: {o['uncertainty_method']}. Baseline: VOL (primary), FIXED (control)."]
    cp = doc["checkpoint_progress"]
    L += [f"Open interval since {doc['open_interval']['since_decision_utc']}: {doc['open_interval']['state']}.",
          f"Checkpoints: C1 after 180 days with ≥10 blocks (recorded: {cp['C1']['recorded']}); C2 after 365 days with ≥20 blocks "
          f"(recorded: {cp['C2']['recorded']}). Owner: {cp['owner']}. Progress: {cp['progress']}.",
          "", doc["note"], ""]
    return "\n".join(L)


def operator_lifecycle(new: str, reason: str, base=BASE) -> dict:
    """The operator's command: pause, resume (active), terminate, archive. Recorded with by='operator'."""
    return U.transition(base, ROOT, PROTOCOL_SHA256, new, by="operator", reason=reason)


def main(argv) -> int:
    cmd = argv[1] if len(argv) > 1 else ""
    try:
        if cmd == "decide":
            rec = decide()
            if rec is None:
                last = (U.rows(BASE / RUNS) or [{}])[-1]
                res = _result(last.get("outcome", "no decision"), "expected")
            else:
                res = _result(f"decided: {rec['action']}", "done", decision_id=rec["decision_id"])
        elif cmd == "confirm":
            rows = confirm()
            res = _result(f"confirmed {len(rows)}", "done" if rows else "expected")
        elif cmd == "execute":
            res = execute()
        elif cmd == "report":
            doc = report()
            res = _result(f"report: {doc['status']}", "done" if doc["integrity"]["ok"] else "error",
                          integrity=doc["integrity"])
        elif cmd == "checkpoint" and len(argv) >= 4:
            row = record_checkpoint(argv[2], "operator", " ".join(argv[3:]))
            res = _result(f"checkpoint {row['checkpoint']}: {row['status']}", "done")
        elif cmd == "lifecycle" and len(argv) >= 4:
            row = operator_lifecycle(argv[2], " ".join(argv[3:]))
            res = _result(f"lifecycle {row['state']}", "done")
        else:
            print("usage: paper_ps1.py decide|confirm|execute|report | lifecycle <state> <reason> | checkpoint C1|C2 <note>")
            return 2
    except Refused as exc:
        _run_row(BASE, U.run_meta(), cmd, "refused", reason=str(exc))
        res = _result(f"refused: {exc}", "error")
    except (U.LifecycleError, RuntimeError, ValueError) as exc:
        _run_row(BASE, U.run_meta(), cmd, "failed", reason=str(exc)[:300])
        res = _result(f"failed: {exc}", "error")
    return U.emit(res)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
