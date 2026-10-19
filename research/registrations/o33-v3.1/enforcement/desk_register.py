"""desk_register - registration, admission and scoring of desk calls for O33 v3, as ONE public workflow.

register-2.3.0 (package 12.4.20; 2.2.0 in 12.4.19, 2.1.0 in 12.4.18, 2.0.0 in 12.4.17). An enforcement wrapper over the frozen desk_calls.py (calls-2.0.0) and
desk_calls_freeze.py (calls-freeze-1.0.0). Neither file changes, so the bytes registered in the repository
(research/registrations/o33-v3/) stay exact. Nothing here changes an estimator, a constant or a cohort definition.

Why 2.0.0. In register-1.0.0, unit() and score_v3() accepted separately supplied dictionaries without establishing
that they belonged together. An independent review reproduced four failures:
  - a post-outcome call was counted with another call's eligible verification;
  - a containment unit accepted a baseline labelled calls-1.0.0 / v2 (wrong spec hash, 2020 anchor, 1 h horizon)
    and was still marked "v3 baseline se";
  - an outcome of 2 was accepted;
  - a bound given as text escaped as an uncaught ValueError.
2.0.0 removes those entry points. Units are derived, never supplied.

Public workflow (the only supported path from a registered call to a score)
  prepare(doc)                         bind content and id before the registry write
  verify_readback(written, read_back)  identical canonical content after the registry get
  registration_failure(doc, cause)     an explicit 'unregistered' record when the write cannot happen
  market_from_archive(...)             validated 1m market data from jbm_archive (or market_data(...) for another
                                       named source); it carries symbol, provenance and retrieval time
  evaluate(entry, evaluation_utc, market)
      entry = {"doc", "receipt", "read", "readback"}. Derives, in order:
        1. admission    verify_registration(): the stored document, the registry server's receipt naming this id
                        and content, the read-back and the read record only. Caller flags are ignored.
        2. data         the market's instrument equals the call's; values finite and positive on the minute grid;
                        retrieved no later than the evaluation time.
        3. maturity     pending until the graded close has passed; the outcome close must be in data retrieved at
                        or after that close.
        4. baseline     the registered PRIMARY baseline, computed here from the market (containment:
                        matched_baseline_v3; lean: v3_lean_drift). Bound to o33 v3, the frozen spec hash, the call's
                        anchor and horizon. A secondary baseline never replaces it.
        5. outcome      containment 0/1 only; lean the 1m close at the graded close.
        6. unit         bound to the call's id, content hash, instrument, type, cohort, spec, anchor, horizon,
                        baseline role and data provenance.
      Returns a status: scored | pending | unavailable | not-admitted | invalid, with reasons. It never raises on
      bad input.
  score_v3(entries, evaluation_utc, market)
      Re-derives every unit through evaluate() and applies the registered de-duplication. Each call type is scored
      separately, never pooled. Declared dependence leaves a comparative claim unsupported: no dependence method is
      registered.

Added in 2.1.0 (package 12.4.18; no estimator, constant or cohort changed)
  normalize_numbers(obj)       whole-number floats become ints before hashing (fold F1): the registry stores 82843.0
                               as 82843, which changed the content hash of two Oct 13 documents
  receipt_from_registry(row)   the server receipt from an inline registry query row (id, data, version, updatedAt):
                               version 1's updatedAt is the registry's own write time. Reads saved to files omit
                               updatedAt; that omission was misreported Oct 16-19 as "the registry returns no receipt"
  record_summary(calls, grades)  the registered record by call type and direction, for any read or document that
                               cites it (a lean document on Oct 19 stated the record from memory, wrongly)

Added in 2.2.0 (package 12.4.19; O33 v3.1 - the frozen v3 estimators, constants and cohort are unchanged)
  Conditional calls. A condition a read states ("a 4H close above 81,384 at 00:00Z makes it a lean higher") is
  registered as call_type "conditional" when it is stated, before the read is delivered. It converts at the first
  trigger close inside its window: the issue becomes that close and its price, and it is graded from market data
  alone, with no read needed at the trigger. It expires untriggered when the window passes. It can be withdrawn
  only by a registered withdrawal whose receipt precedes the trigger close; a later withdrawal is void and the call
  is scored. Units are scored as their own call type, never pooled with leans.
    conditional_trigger(doc, closes, now)   triggered | expired | pending | unavailable, from bar closes
    conditional_grade(doc, closes, now)     the plain grade: right | wrong | expired | pending | unavailable
    prepare_withdrawal(call_doc, issue_utc, reason)   a withdrawal document to register
    evaluate() dispatches a conditional entry (optional entry["withdrawal"] = {"doc", "receipt"})
  Order evidence. A read that did not quote its receipt is admitted when an observed delivery record shows the
  read was delivered at or after the receipt: read["order_record"] = {"source": "conversation-record" |
  "operator", "delivered_utc", "ref"}. Delivery before the receipt is "late". The admission names its basis
  ("quote" or "order-record") so every result can be reported with and without the record-admitted calls. The
  rule applies to every order-unverified call whatever its outcome (operator decision, Oct 19 2026).

Changed in 2.3.0 (package 12.4.20; the Oct 19 review's findings A-C reproduced on 2.2.0; frozen v3 arithmetic,
constants and cohort unchanged; the O33 v3.1 manifest names these rules)
  A  every piece of evidence must have been available at the evaluation cutoff (desk_evidence.available_at):
     a withdrawal registered after the cutoff is not known to that evaluation and cannot change it.
  B  a withdrawal is effective only if its receipt precedes the first possible trigger close, or the trigger history
     up to its receipt is complete and shows no trigger. Missing history before the withdrawal is 'unavailable',
     never 'withdrawn before any trigger'. A withdrawal needs its read-back, like a call.
  C  an order record separates the claimed delivery (delivered_utc) from the availability of the record that shows
     it (available_utc: when the conversation record or the operator's statement was obtained). It is admissible to an
     evaluation only when available by its cutoff; a missing available_utc leaves the call order-unverified.
  O33 v3.1 populations: score_v31() recomputes eligibility, de-duplication and scoring separately for each declared
     population (all admitted; quote-only; order-record-only), never by removing rows from a de-duplicated result,
     and reports the conditional usable-opportunity funnel (registered, triggered, expired, withdrawn, unavailable,
     late, pending). Outcomes are named: conditional_grade is the invalidation-path plain grade; a unit's d is the
     terminal-close, drift-adjusted directional return - not the P&L of a strategy that exited at invalidation.

Internal helpers (_unit, _paired) do arithmetic on values already derived by evaluate(). They are not admission
paths.

Trust boundary. The receipt and read-back are evidence from the artifact registry: its version-1 updatedAt and its
get result. Offline, this module cannot prove that a receipt dict came from the server. It checks only that the
receipt names this id and content, is labelled as the server's, precedes the derived window, and agrees with the
read-back. A fixture's receipt is a fixture, never a registry write.

The lean drift has no registered standard error: a lean unit's se is None, and its interval excludes
drift-estimation error. Pure functions; no network, no clock.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math

import desk_calls as D
import desk_calls_freeze as F
import desk_evidence as E

VERSION = "register-2.3.0"
CALLS_VERSION = "calls-2.0.0"
RECEIPT_SOURCE = "registry-server"          # the artifact registry's own version-1 updatedAt, read back after write
LEAN_SE_BASIS = "none: O33 v3 registers no standard error for a lean's drift; intervals exclude drift-estimation error"
CONTAINMENT_SE_BASIS = "v3 primary baseline se"
REQUIRED = {"common": ("id", "version", "instrument", "call_type", "issue_utc", "graded_close_utc", "issue_price"),
            "containment": ("lower", "upper"), "lean": ("direction",)}
IGNORED_CALLER_FIELDS = ("eligible", "status", "cohort", "counted")
MARKET_STATES_OK = ("ok",)
CONDITIONAL_INTERVALS = {"1h": 3_600_000, "4h": 14_400_000}
ORDER_RECORD_SOURCES = ("conversation-record", "operator")
O33_CONDITIONAL = "O33 v3.1 (conditional calls; lean-drift primary baseline from the trigger close)"
OUTCOME_LABELS = {"grade": "invalidation-path plain grade (right/wrong; an hourly close through the invalidation line before the graded close is wrong)",
                  "d": "terminal-close directional return minus the registered lean drift (log units); not the P&L of a strategy that exits at invalidation"}
POPULATIONS = ("all-admitted", "quote-only", "order-record-only")


# ------------------------------------------------------------------------------------------------------- parsing
def _t(x) -> dt.datetime:
    """A timezone-aware instant. Naive strings or datetimes are refused (a naive value would be read in local time)."""
    if isinstance(x, dt.datetime):
        if x.tzinfo is None:
            raise ValueError("naive datetime")
        return x.astimezone(dt.timezone.utc)
    s = str(x)
    t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    if t.tzinfo is None:
        raise ValueError(f"timestamp without a timezone: {s!r}")
    return t.astimezone(dt.timezone.utc)


def _tt(x):
    try:
        return _t(x)
    except (TypeError, ValueError):
        return None


def _finite(x) -> float | None:
    """A finite number (int or float, never bool or text), else None."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return None
    x = float(x)
    return x if math.isfinite(x) else None


def _ms(t: dt.datetime) -> int:
    return int(t.timestamp() * 1000)


# ------------------------------------------------------------------------------------------------ registration
def registration_failure(doc: dict | None, cause: str, at_utc=None) -> dict:
    """An explicit failure record. 'cause' names it (tool missing, write refused, read-back mismatch, timeout)."""
    if not cause:
        raise ValueError("an unregistered call names its cause")
    return {"status": "unregistered", "cause": cause, "at_utc": at_utc, "id": (doc or {}).get("id"),
            "note": "analysis may continue under this label; a later write is not a prospective registration",
            "version": VERSION}


def normalize_numbers(obj):
    """Whole-number floats to int, recursively (bools untouched). Applied before hashing so that the content the
    registry stores (it drops a trailing .0) hashes to the content registered (F1)."""
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, float) and math.isfinite(obj) and obj.is_integer():
        return int(obj)
    if isinstance(obj, dict):
        return {k: normalize_numbers(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize_numbers(v) for v in obj]
    return obj


def prepare(doc: dict) -> dict:
    """Bind content and identity before writing: content_sha256 over the canonical content, the id from it.
    Whole-number floats are normalized first (2.1.0)."""
    doc = normalize_numbers(doc)
    body = {k: v for k, v in doc.items() if k not in ("id", "content_sha256") + IGNORED_CALLER_FIELDS}
    body.setdefault("version", 1)
    sha = D.content_sha256(dict(body, id=None))
    out = dict(body)
    out["id"] = _call_id(body["instrument"], body["issue_utc"], body["call_type"], sha)
    out["content_sha256"] = D.content_sha256(out)
    return out


def _call_id(instrument, issue_utc, call_type, sha) -> str:
    """The frozen id for leans and containment; conditional calls use the letter K (desk_calls stays frozen).
    A withdrawal uses W."""
    if call_type in ("conditional", "withdrawal"):
        t = _t(issue_utc)
        return f"DESK-{instrument.upper()}-{t:%Y%m%dT%H%M%S}Z-{'K' if call_type == 'conditional' else 'W'}-{sha[:8]}"
    return D.call_id(instrument, issue_utc, call_type, sha)


def verify_readback(written: dict, read_back: dict | None) -> tuple[bool, str]:
    """After the registry write and get: identical canonical content, or the registration failed."""
    if not isinstance(read_back, dict):
        return False, "read-back returned nothing"
    if D.content_sha256(written) != D.content_sha256(read_back):
        return False, "read-back content differs from what was written"
    return True, "read-back matches"


def receipt_from_registry(row: dict | None) -> tuple[dict | None, str]:
    """(receipt, reason) from one row of an inline registry query - {"id", "data", "version", "updatedAt"}.
    Only version 1 carries the write time; a later version's updatedAt is an edit time and gives no receipt.
    The receipt's content hash is computed from the stored data, never copied from a field."""
    if not isinstance(row, dict) or not isinstance(row.get("data"), dict):
        return None, "no registry row"
    if row.get("version") != 1:
        return None, f"registry version {row.get('version')!r}: the version-1 write time is no longer readable"
    t = _tt(row.get("updatedAt"))
    if t is None:
        return None, "updatedAt missing or without a timezone (a file read omits it: use an inline query)"
    data = row["data"]
    return {"id": row.get("id"), "receipt_utc": D.iso(t),
            "source": RECEIPT_SOURCE, "content_sha256": D.content_sha256(data)}, "version-1 updatedAt"


def record_summary(calls: list[dict], grades: list[dict]) -> dict:
    """The registered record: counts by call type and direction from the stored documents and their grade
    documents (result 'right...' / 'wrong...'); a call with no grade document is pending. Plain grades only -
    never a score, never a hit rate."""
    res = {}
    for g in grades or []:
        r = str(g.get("result", "")).strip().lower()
        res[g.get("forecast_id")] = next((k for k in ("right", "wrong", "expired", "withdrawn") if r.startswith(k)),
                                         "other")
    out = {}
    for c in calls or []:
        if not isinstance(c, dict) or c.get("call_type") not in ("lean", "containment", "conditional"):
            continue
        lab = c.get('direction_label') or ('higher' if c.get('direction') == 1 else 'lower')
        key = c["call_type"] if c["call_type"] == "containment" else f"{c['call_type']} {lab}"
        b = out.setdefault(key, {"right": 0, "wrong": 0, "pending": 0, "expired": 0, "withdrawn": 0, "other": 0,
                                 "ids": []})
        b[res.get(c.get("id"), "pending")] += 1
        b["ids"].append(c.get("id"))
    out["line"] = "; ".join(f"{k}: {v['right']} right, {v['wrong']} wrong, {v['pending']} pending"
                            + (f", {v['expired']} expired, {v['withdrawn']} withdrawn" if k.startswith("conditional")
                               else "")
                            for k, v in sorted(out.items()) if isinstance(v, dict))
    return out


def _shape(doc) -> list[str]:
    """Every problem with a stored call document; never raises."""
    if not isinstance(doc, dict):
        return ["document is not an object"]
    probs = [f"missing field {k}" for k in REQUIRED["common"] if doc.get(k) in (None, "")]
    ct = doc.get("call_type")
    if ct not in ("containment", "lean"):
        return probs + [f"call_type {ct!r}"]
    probs += [f"missing field {k}" for k in REQUIRED[ct] if doc.get(k) in (None, "")]
    if probs:
        return probs
    if not isinstance(doc["instrument"], str) or not doc["instrument"].strip():
        probs.append("instrument must be a non-empty string")
    if not isinstance(doc["id"], str):
        probs.append("id must be a string")
    if isinstance(doc.get("version"), bool) or not isinstance(doc.get("version"), int):
        probs.append("version must be an integer")
    p = _finite(doc["issue_price"])
    if p is None:
        probs.append("issue_price is not a finite number")
    elif not p > 0:
        probs.append("issue price not positive")
    issue, graded = _tt(doc["issue_utc"]), _tt(doc["graded_close_utc"])
    if issue is None or graded is None:
        probs.append("issue_utc and graded_close_utc must be timezone-aware ISO-8601 instants")
    elif graded <= issue:
        probs.append("graded close not after issue")
    if ct == "containment":
        lo, hi = _finite(doc["lower"]), _finite(doc["upper"])
        if lo is None or hi is None:
            probs.append("bounds are not finite numbers")
        elif p is not None and not (0 < lo < p < hi):
            probs.append("bounds do not bracket the issue price")
    if ct == "lean":
        d = doc["direction"]
        if isinstance(d, bool) or not isinstance(d, int) or d not in (1, -1):
            probs.append("lean direction must be the integer +1 or -1")
    return probs


def verify_registration(doc: dict, receipt: dict | None, read: dict | None = None,
                        readback: dict | None = None, evaluation_utc=None) -> dict:
    """Admission for O33 v3, from the stored document, the server receipt, the read-back and the read record only.

    receipt   {"id": the registry key, "receipt_utc": server time of version 1, "source": "registry-server",
              "content_sha256": the hash the registry held at that receipt} - or None, or registration_failure()
    read      {"quotes_receipt": bool, "sent_utc": optional delivery time supplied by the operator}
    readback  the document as the registry returned it after the write (optional here; evaluate() requires it)
    evaluation_utc  the assessment cutoff (2.3.0). When given, an order record must have been available by it
              (available_utc <= cutoff); evaluate() always passes it. Without it, availability is not checked and
              the result says so (availability_checked False).
    Statuses: eligible | unregistered | unverifiable | invalid | content-changed | backdated | late |
    order-unverified | post-outcome | pre-freeze. Never raises."""
    read = read if isinstance(read, dict) else {}
    doc_d = doc if isinstance(doc, dict) else {}
    out = {"version": VERSION, "id": doc_d.get("id"), "eligible": False, "reasons": [], "cohort": None,
           "derived_start_utc": None, "content_sha256": None,
           "ignored_caller_fields": sorted(k for k in IGNORED_CALLER_FIELDS if k in doc_d)}

    def done(status, reason):
        out["status"] = status
        out["reasons"].append(reason)
        return out

    if not isinstance(receipt, dict) or receipt.get("status") == "unregistered":
        return done("unregistered", (receipt or {}).get("cause") if isinstance(receipt, dict) else "no server receipt")
    if receipt.get("source") != RECEIPT_SOURCE or not receipt.get("receipt_utc"):
        return done("unverifiable", "receipt is not the registry server's version-1 time")
    r = _tt(receipt.get("receipt_utc"))
    if r is None:
        return done("unverifiable", "receipt time unparseable or without a timezone")
    conditional = isinstance(doc, dict) and doc.get("call_type") == "conditional"
    shape = _cond_shape(doc) if conditional else _shape(doc)
    if shape:
        return done("invalid", "; ".join(shape))
    if receipt.get("id") != doc["id"]:
        return done("unverifiable", f"receipt names {receipt.get('id')!r}, not this call {doc['id']!r}")
    sha = D.content_sha256(doc)
    out["content_sha256"] = sha
    if receipt.get("content_sha256") != sha or (doc.get("content_sha256") and doc["content_sha256"] != sha):
        return done("content-changed", "stored content does not hash to the content registered at the receipt")
    body_sha = D.content_sha256({k: v for k, v in doc.items() if k != "id"} | {"id": None})
    if doc["id"] != _call_id(doc["instrument"], doc["issue_utc"], doc["call_type"], body_sha):
        return done("content-changed", "id does not bind this content (instrument, issue time, type, content hash)")
    if readback is not None:
        ok, why = verify_readback(doc, readback)
        if not ok:
            return done("unverifiable", why)
    if read.get("sent_utc") is not None and _tt(read["sent_utc"]) is None:
        return done("invalid", "read sent_utc unparseable or without a timezone")
    rec = read.get("order_record")
    sent = read.get("sent_utc")
    cutoff = _tt(evaluation_utc) if evaluation_utc is not None else None
    if evaluation_utc is not None and cutoff is None:
        return done("invalid", "evaluation time without a timezone")
    out["availability_checked"] = cutoff is not None
    if rec is not None:
        if (not isinstance(rec, dict) or rec.get("source") not in ORDER_RECORD_SOURCES
                or _tt(rec.get("delivered_utc")) is None or not rec.get("ref")):
            return done("invalid", "order_record needs source (conversation-record | operator), a timezone-aware "
                                   "delivered_utc and a ref")
        if rec.get("available_utc") is not None and _tt(rec.get("available_utc")) is None:
            return done("invalid", "order_record available_utc without a timezone")
        if cutoff is not None:
            ev = {"event_utc": rec["delivered_utc"], "retrieved_utc": rec.get("available_utc")}
            st, why_av = E.available_at(ev, cutoff)
            if _t(rec["delivered_utc"]) > cutoff:
                st, why_av = "pending", (f"claimed delivery {D.iso(_t(rec['delivered_utc']))} is after this evaluation's "
                                         f"cutoff {D.iso(cutoff)}")
            if st != "ok":
                out["order_record_availability"] = why_av
                rec = None                                       # not evidence this evaluation could have used
                if not read.get("quotes_receipt"):
                    out["reasons"].append(f"order record not admissible at this cutoff: {why_av}")
        if rec is not None:
            d_rec = _t(rec["delivered_utc"])
            sent = d_rec if sent is None else min(_t(sent), d_rec)
    status, why = D.registration_status(doc, r, bool(read.get("quotes_receipt")), sent)
    out["admission_basis"] = "quote" if read.get("quotes_receipt") else None
    if status == "order-unverified" and rec is not None:
        status, why = "eligible", (f"order-record (O33 v3.1): delivered {D.iso(_t(rec['delivered_utc']))} at or "
                                   f"after the receipt {D.iso(r)}; source {rec['source']}, ref {rec['ref']}")
        out["admission_basis"] = "order-record"
    start = D.derived_start(r)
    out["derived_start_utc"] = D.iso(start)
    out["receipt_utc"] = D.iso(r)
    if status != "eligible":
        return done(status, why)
    if r < _t(doc["issue_utc"]):
        return done("invalid", "receipt precedes the stated issue time")
    if conditional and _t(doc["trigger"]["first_close_utc"]) <= start:
        return done("post-outcome", f"trigger window opens {doc['trigger']['first_close_utc']}, at or before the "
                                    f"derived start {D.iso(start)}: a condition is registered before its window")
    if _t(doc["graded_close_utc"]) <= start:
        return done("post-outcome", f"graded close {doc['graded_close_utc']} is at or before the derived start "
                                    f"{D.iso(start)}: the outcome could be known before the window opened")
    cohort = F.v3_cohort(r)
    out["cohort"] = cohort
    if cohort != "v3":
        return done("pre-freeze", f"receipt {D.iso(r)} is not after the v3 freeze {F.V3_FREEZE_UTC}: v1 cohort, "
                                  "never v3 evidence")
    out["eligible"] = True
    out["status"] = "eligible"
    out["reasons"].append(why)
    return out


# ------------------------------------------------------------------------------------------- conditional calls
def _on_grid(t: dt.datetime, step_ms: int) -> bool:
    return _ms(t) % step_ms == 0


def _cond_shape(doc) -> list[str]:
    """Every problem with a stored conditional call; never raises.
    Fields: id, version, instrument, call_type "conditional", issue_utc (when the condition was stated and
    registered), issue_price (the price then; reference only), direction +1/-1, graded_close_utc,
    trigger {interval "1h"|"4h", side "above"|"below", level, first_close_utc, last_close_utc},
    invalidation {side, level} on 1H closes after the trigger (below for a lean higher, above for a lean lower)."""
    if not isinstance(doc, dict):
        return ["document is not an object"]
    probs = [f"missing field {k}" for k in REQUIRED["common"] + ("direction", "trigger", "invalidation")
             if doc.get(k) in (None, "")]
    if probs:
        return probs
    if doc.get("call_type") != "conditional":
        return [f"call_type {doc.get('call_type')!r}"]
    if not isinstance(doc["instrument"], str) or not doc["instrument"].strip():
        probs.append("instrument must be a non-empty string")
    if isinstance(doc.get("version"), bool) or not isinstance(doc.get("version"), int):
        probs.append("version must be an integer")
    d = doc["direction"]
    if isinstance(d, bool) or d not in (1, -1):
        probs.append("direction must be the integer +1 or -1")
    p = _finite(doc["issue_price"])
    if p is None or not p > 0:
        probs.append("issue_price is not a finite positive number")
    tr, inv = doc["trigger"], doc["invalidation"]
    if not isinstance(tr, dict) or not isinstance(inv, dict):
        return probs + ["trigger and invalidation must be objects"]
    step = CONDITIONAL_INTERVALS.get(tr.get("interval"))
    if step is None:
        probs.append(f"trigger interval {tr.get('interval')!r} (1h or 4h)")
    if tr.get("side") not in ("above", "below"):
        probs.append(f"trigger side {tr.get('side')!r}")
    if _finite(tr.get("level")) is None or not _finite(tr.get("level")) > 0:
        probs.append("trigger level is not a finite positive number")
    want = "below" if d == 1 else "above"
    if inv.get("side") != want:
        probs.append(f"invalidation side {inv.get('side')!r}: a lean {'higher' if d == 1 else 'lower'} is "
                     f"invalidated by a close {want} its line")
    if _finite(inv.get("level")) is None or not _finite(inv.get("level")) > 0:
        probs.append("invalidation level is not a finite positive number")
    issue, graded = _tt(doc["issue_utc"]), _tt(doc["graded_close_utc"])
    first, last = _tt(tr.get("first_close_utc")), _tt(tr.get("last_close_utc"))
    if None in (issue, graded, first, last):
        probs.append("issue_utc, graded_close_utc and the trigger window must be timezone-aware ISO-8601 instants")
        return probs
    if step is not None and not (_on_grid(first, step) and _on_grid(last, step)):
        probs.append(f"trigger window is not on the {tr.get('interval')} close grid")
    if not _on_grid(graded, 3_600_000):
        probs.append("graded close is not on an hourly close")
    if not issue < first <= last < graded:
        probs.append("need issue < first trigger close <= last trigger close < graded close")
    return probs


def _bar_closes(doc: dict) -> list[int]:
    tr = doc["trigger"]
    step = CONDITIONAL_INTERVALS[tr["interval"]]
    a, b = _ms(_t(tr["first_close_utc"])), _ms(_t(tr["last_close_utc"]))
    return list(range(a, b + 1, step))


def conditional_trigger(doc: dict, closes: dict, now=None) -> dict:
    """The first bar close in the window beyond the trigger level. closes: {close_ms: price} (1m or coarser; a bar
    close at T is the price keyed T). now (optional): closes after it are not yet known. A missing close before any
    trigger makes the state unavailable - it is never read as 'not triggered'."""
    probs = _cond_shape(doc)
    if probs:
        return {"state": "invalid", "reasons": probs}
    tr = doc["trigger"]
    lvl, above = float(tr["level"]), tr["side"] == "above"
    lim = _ms(_t(now)) if _tt(now) is not None else None
    for T in _bar_closes(doc):
        if lim is not None and T > lim:
            return {"state": "pending", "reasons": [f"window still open at {D.iso(_t(now))}"]}
        c = _finite(closes.get(T)) if isinstance(closes, dict) else None
        if c is None:
            return {"state": "unavailable",
                    "reasons": [f"no close at {D.iso(dt.datetime.fromtimestamp(T / 1000, dt.timezone.utc))}"]}
        if (c > lvl) if above else (c < lvl):
            return {"state": "triggered", "close_utc": D.iso(dt.datetime.fromtimestamp(T / 1000, dt.timezone.utc)),
                    "price": c, "reasons": [f"{tr['interval']} close {c} {tr['side']} {lvl}"]}
    return {"state": "expired", "reasons": [f"no {tr['interval']} close {tr['side']} {lvl} from "
                                            f"{tr['first_close_utc']} to {tr['last_close_utc']}"]}


def _as_lean(doc: dict, trig: dict) -> dict:
    """The lean a triggered conditional became: issue at the trigger close, at its price."""
    return {"version": 1, "instrument": doc["instrument"], "call_type": "lean", "direction": doc["direction"],
            "issue_utc": trig["close_utc"], "issue_price": trig["price"], "graded_close_utc": doc["graded_close_utc"]}


def conditional_grade(doc: dict, closes: dict, now=None) -> dict:
    """Plain grade of a conditional call from market data alone: right if the graded close is beyond the trigger
    close in the call's direction and no 1H close after the trigger and before the graded close crossed the
    invalidation line; wrong otherwise. Never a score; admission is separate (evaluate)."""
    trig = conditional_trigger(doc, closes, now)
    out = {"version": VERSION, "id": doc.get("id") if isinstance(doc, dict) else None, "trigger": trig}
    if trig["state"] != "triggered":
        return dict(out, result=trig["state"])
    g = _ms(_t(doc["graded_close_utc"]))
    lim = _ms(_t(now)) if _tt(now) is not None else None
    if lim is not None and g > lim:
        return dict(out, result="pending")
    t0 = _ms(_t(trig["close_utc"]))
    inv = doc["invalidation"]
    lvl, below = float(inv["level"]), inv["side"] == "below"
    for T in range(t0 + 3_600_000, g, 3_600_000):
        c = _finite(closes.get(T))
        if c is None:
            return dict(out, result="unavailable", reasons=[f"no 1H close at {D.iso(_t(dt.datetime.fromtimestamp(T / 1000, dt.timezone.utc)))}"])
        if (c < lvl) if below else (c > lvl):
            return dict(out, result="wrong", invalidated_utc=D.iso(dt.datetime.fromtimestamp(T / 1000, dt.timezone.utc)),
                        invalidation_close=c, issue_price=trig["price"])
    cg = _finite(closes.get(g))
    if cg is None:
        return dict(out, result="unavailable", reasons=["no close at the graded close"])
    right = (cg - trig["price"]) * doc["direction"] > 0
    return dict(out, result="right" if right else "wrong", issue_price=trig["price"], graded_close=cg)


def prepare_withdrawal(call_doc: dict, issue_utc, reason: str) -> dict:
    """A withdrawal document for a registered conditional call. It takes effect only if its own registry receipt
    precedes the trigger close; it never edits the call."""
    if not isinstance(call_doc, dict) or call_doc.get("call_type") != "conditional":
        raise ValueError("only a conditional call can be withdrawn")
    if not reason:
        raise ValueError("a withdrawal states its reason")
    return prepare({"version": 1, "instrument": call_doc["instrument"], "call_type": "withdrawal",
                    "withdraws": call_doc["id"], "issue_utc": D.iso(_t(issue_utc)), "reason": reason})


def _withdrawal_effective(doc: dict, w: dict | None, call_receipt_utc, closes: dict, cutoff: dt.datetime
                          ) -> tuple[bool | None, str, str]:
    """(effective, state, why). effective: True (withdrawn), False (void or not known to this evaluation), None (no
    withdrawal, or its effect cannot be established - state 'unavailable').
    Rules (2.3.0): the withdrawal names this call, carries its own registry receipt and matching read-back, was
    registered after the call and was available by the cutoff. It takes effect if its receipt precedes the first
    possible trigger close; otherwise only when every trigger close up to the receipt is present and none triggered.
    A trigger close at or before the receipt makes it void."""
    if not w:
        return None, "none", ""
    wd, wr = w.get("doc"), w.get("receipt")
    if not isinstance(wd, dict) or wd.get("call_type") != "withdrawal" or wd.get("withdraws") != doc.get("id"):
        return False, "void", "withdrawal does not name this call"
    if not isinstance(wr, dict) or wr.get("source") != RECEIPT_SOURCE or wr.get("id") != wd.get("id"):
        return False, "void", "withdrawal has no registry receipt naming it"
    if wr.get("content_sha256") != D.content_sha256(wd):
        return False, "void", "withdrawal content differs from what was registered"
    ok, why = verify_readback(wd, w.get("readback"))
    if not ok:
        return False, "void", f"withdrawal read-back: {why}"
    rt = _tt(wr.get("receipt_utc"))
    if rt is None:
        return False, "void", "withdrawal receipt time unparseable"
    st, why = E.available_at({"retrieved_utc": wr["receipt_utc"]}, cutoff)
    if st != "ok":
        return False, "not-known", f"withdrawal registered {D.iso(rt)}, after this evaluation's cutoff: not considered"
    wi = _tt(wd.get("issue_utc"))
    if wi is None or wi > rt:
        return False, "void", "withdrawal issue time missing or after its receipt"
    cr = _tt(call_receipt_utc)
    if cr is None or rt <= cr:
        return False, "void", "withdrawal receipt not after the call's receipt"
    tr = doc["trigger"]
    lvl, above = float(tr["level"]), tr["side"] == "above"
    if rt < _t(tr["first_close_utc"]):
        return True, "withdrawn", f"withdrawn {D.iso(rt)}, before the first possible trigger close {tr['first_close_utc']}"
    for T in _bar_closes(doc):
        if T > _ms(rt):
            break
        c = _finite(closes.get(T)) if isinstance(closes, dict) else None
        tiso = D.iso(dt.datetime.fromtimestamp(T / 1000, dt.timezone.utc))
        if c is None:
            return None, "unavailable", (f"withdrawal at {D.iso(rt)}: the {tr['interval']} close at {tiso} is missing, "
                                         "so a trigger before the withdrawal cannot be ruled out")
        if (c > lvl) if above else (c < lvl):
            return False, "void", (f"withdrawal registered {D.iso(rt)}, at or after the trigger close {tiso}: void, "
                                   "the call is scored")
    return True, "withdrawn", f"withdrawn {D.iso(rt)}; every trigger close up to it present and none triggered"


def _evaluate_conditional(entry: dict, now: dt.datetime, market: dict, releases) -> dict:
    doc = entry.get("doc")
    eid = doc.get("id") if isinstance(doc, dict) else None
    if entry.get("readback") is None:
        return _result(eid, "not-admitted", ["no registry read-back: registration is unverified"])
    adm = verify_registration(doc, entry.get("receipt"), entry.get("read"), entry.get("readback"), now)
    base = {"admission": adm, "protocol": O33_CONDITIONAL, "outcome_labels": OUTCOME_LABELS}
    if not adm["eligible"]:
        return _result(eid, "invalid" if adm["status"] == "invalid" else "not-admitted",
                       [f"{adm['status']}: " + "; ".join(adm["reasons"])], **base)
    if _t(adm["receipt_utc"]) > now:
        return _result(eid, "not-admitted", ["the registry receipt is later than the evaluation time"], **base)
    if not isinstance(market, dict) or market.get("problems") is None:
        return _result(eid, "unavailable", ["market data not built by market_data()/market_from_archive()"], **base)
    market = market_data(market.get("symbol"), market.get("closes"), market.get("source"))
    if market["problems"]:
        return _result(eid, "unavailable", ["market data invalid: " + "; ".join(market["problems"])], **base)
    if market.get("symbol") != doc["instrument"]:
        return _result(eid, "invalid", [f"market data is {market.get('symbol')!r}, the call is on "
                                        f"{doc['instrument']!r}"], **base)
    retrieved = _t(market["source"]["retrieved_utc"])
    if retrieved > now:
        return _result(eid, "unavailable", [f"market data retrieved {D.iso(retrieved)}, after the evaluation time"],
                       **base)
    closes = market["closes"]
    known = min(now, retrieved)
    visible = {k: v for k, v in closes.items() if k <= _ms(known)}
    trig = conditional_trigger(doc, visible, known)
    base["trigger"] = trig
    w_ok, w_state, w_why = _withdrawal_effective(doc, entry.get("withdrawal"), adm["receipt_utc"], visible, now)
    if w_ok:
        return _result(eid, "withdrawn", [w_why, "recorded, never scored"], **base)
    if w_state == "unavailable":
        base["withdrawal"] = w_why
        return _result(eid, "unavailable", [w_why], **base)
    if w_ok is False:
        base["withdrawal"] = w_why
    if trig["state"] == "expired":
        return _result(eid, "expired", trig["reasons"] + ["recorded in the record as expired, never scored"], **base)
    if trig["state"] in ("pending", "unavailable", "invalid"):
        return _result(eid, trig["state"], trig["reasons"], **base)
    lean = _as_lean(doc, trig)
    graded = _t(doc["graded_close_utc"])
    if now < graded:
        return _result(eid, "pending", [f"triggered {trig['close_utc']} at {trig['price']}; graded close "
                                        f"{doc['graded_close_utc']} not yet passed"], **base)
    g = _ms(graded)
    if g not in closes:
        return _result(eid, "unavailable", ["the 1m close at the graded close is not in the market data"], **base)
    if retrieved < graded:
        return _result(eid, "invalid", ["the outcome close is in data retrieved before that close existed"], **base)
    b = v3_lean_drift(lean, closes)
    base["baseline"] = {"available": bool(b.get("available")), "reason": b.get("reason"), "role": "primary",
                        "o33": b.get("o33"), "spec_sha256": b.get("spec_sha256"), "anchor_utc": b.get("anchor_utc"),
                        "horizon_min": b.get("horizon_min"), "windows": b.get("windows"),
                        "candidate_windows": b.get("candidate_windows"), "lean_drift": b.get("lean_drift"), "se": None}
    if not b.get("available"):
        return _result(eid, "unavailable", [f"registered primary baseline unavailable: {b.get('reason')}"], **base)
    bind = _bind_baseline(lean, b)
    if bind:
        return _result(eid, "invalid", ["baseline binding: " + "; ".join(bind)], **base)
    if _finite(b.get("lean_drift")) is None:
        return _result(eid, "invalid", ["lean drift is not finite"], **base)
    base["grade"] = conditional_grade(doc, closes, known)
    base["outcome"] = {"close_utc": doc["graded_close_utc"], "close": closes[g], "value": closes[g]}
    u = _unit(dict(doc, issue_utc=trig["close_utc"], issue_price=trig["price"]), adm, b, closes[g], market, now)
    u.update(registered_issue_utc=doc["issue_utc"], trigger_close_utc=trig["close_utc"], protocol=O33_CONDITIONAL)
    return dict(_result(eid, "scored", ["eligible, triggered, matured, baseline and outcome derived"], **base), unit=u)


# ------------------------------------------------------------------------------------------------- market data
def market_data(symbol: str, closes: dict, source: dict) -> dict:
    """Validated 1m closes for one instrument. source: {"provider", "interval": "1m", "state", "retrieved_utc"} -
    retrieved_utc is when the data was obtained (a historical evaluation may not use data retrieved after it).
    Returns {"symbol", "closes", "source", "closes_sha256", "problems"}; a market with problems is never used."""
    probs = []
    src = dict(source or {})
    if not isinstance(symbol, str) or not symbol:
        probs.append("symbol missing")
    if src.get("interval") != "1m":
        probs.append(f"interval {src.get('interval')!r}, the v3 baseline uses 1m closes")
    if src.get("state") not in MARKET_STATES_OK:
        probs.append(f"source state {src.get('state')!r} (only validated 'ok' data is admissible)")
    if not src.get("provider"):
        probs.append("provider missing")
    if _tt(src.get("retrieved_utc")) is None:
        probs.append("retrieved_utc missing or without a timezone")
    clean = {}
    if not isinstance(closes, dict) or not closes:
        probs.append("no closes")
    else:
        for k, v in closes.items():
            if isinstance(k, bool) or not isinstance(k, int) or k % D.MINUTE_MS:
                probs.append(f"close time {k!r} is not an integer millisecond on the minute grid")
                break
            x = _finite(v)
            if x is None or x <= 0:
                probs.append(f"close at {k} is not a finite positive number")
                break
            clean[k] = x
    h = hashlib.sha256(json.dumps(sorted(clean.items()), separators=(",", ":")).encode()).hexdigest() if clean else None
    return {"symbol": symbol, "closes": clean, "source": src, "closes_sha256": h, "problems": probs,
            "version": VERSION}


def market_from_archive(state: str, closes: dict, manifest: list, symbol: str = "BTCUSDT") -> dict:
    """From desk_calls.load_closes_1m(...) -> (state, closes, manifest): the archive's own validation state and its
    per-file retrieval times; retrieved_utc is the latest file retrieval."""
    times = [_tt(m.get("retrieved_at_utc")) for m in manifest or [] if isinstance(m, dict)]
    rt = max((t for t in times if t is not None), default=None)
    src = {"provider": "binance-usdm-archive (jbm_archive)", "interval": "1m", "state": state,
           "retrieved_utc": D.iso(rt) if rt else None,
           "manifest_sha256": hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()}
    return market_data(symbol, closes, src)


# ------------------------------------------------------------------------------------------- v3 lean drift path
def v3_lean_support(call: dict) -> tuple[bool, str]:
    if call.get("call_type") != "lean":
        return False, "not a lean"
    p, issue, graded = _finite(call.get("issue_price")), _tt(call.get("issue_utc")), _tt(call.get("graded_close_utc"))
    direction = call.get("direction")
    if p is None or issue is None or graded is None:
        return False, "missing or invalid issue, price or graded close"
    if isinstance(direction, bool) or direction not in (1, -1) or not p > 0:
        return False, "direction must be +1/-1 and the issue price positive"
    if graded.second or graded.microsecond:
        return False, "graded close is not on a whole minute"
    h = (_ms(graded) - D._floor_minute_ms(issue)) // D.MINUTE_MS
    if not (D.V3_MIN_H <= h <= D.V3_MAX_H):
        return False, f"horizon {h} min outside {D.V3_MIN_H}-{D.V3_MAX_H}"
    return True, f"{h} min"


def _v3_windows(a: int, h_min: int, closes: dict):
    """The primary window set exactly as matched_baseline_v3 builds it (same start alignment, same sigma
    requirement, same lookback): returns (candidates, used, returns)."""
    hm = h_min * D.MINUTE_MS

    def sigma_ok(t):
        pts = [closes.get(t - j * D.HOUR_MS) for j in range(25)]
        if any(x is None for x in pts):
            return False
        r = [math.log(pts[j] / pts[j + 1]) for j in range(24)]
        return bool(D._sd(r) * math.sqrt(h_min / 60))
    first = a - D.V3_LOOKBACK_DAYS * 86_400_000 + 24 * D.HOUR_MS
    cand, rets = 0, []
    t = a - hm
    t -= ((t - a) % D.HOUR_MS)
    while t >= first:
        cand += 1
        c0, c1 = closes.get(t), closes.get(t + hm)
        if c0 is not None and c1 is not None and sigma_ok(t):
            rets.append(math.log(c1 / c0))
        t -= D.HOUR_MS
    return cand, len(rets), rets


def v3_lean_drift(call: dict, closes: dict) -> dict:
    """Measurement helper: the registered v3 lean drift for one lean (closes: {close_ms: close} 1m; nothing after
    the anchor is read). Not an admission path - evaluate() calls it on validated market data."""
    out = {"version": VERSION, "o33": "v3", "spec_sha256": D.v3_spec_sha256(), "se": None, "se_basis": LEAN_SE_BASIS,
           "role": "primary"}
    ok, why = v3_lean_support(call)
    if not ok:
        return dict(out, available=False, reason=why)
    a = D._floor_minute_ms(_t(call["issue_utc"]))
    if a not in closes:
        return dict(out, available=False, reason="no 1m close at the anchor (data cutoff)")
    h_min = (_ms(_t(call["graded_close_utc"])) - a) // D.MINUTE_MS
    past = {k: v for k, v in closes.items() if k <= a}
    cand, used, rets = _v3_windows(a, h_min, past)
    out.update(anchor_utc=D.iso(dt.datetime.fromtimestamp(a / 1000, dt.timezone.utc)), horizon_min=h_min,
               candidate_windows=cand, windows=used)
    if used < D.V3_MIN_WINDOWS or used < D.V3_MIN_USABLE * cand:
        return dict(out, available=False, reason=f"{used} of {cand} windows usable")
    return dict(out, available=True, lean_drift=sum(rets) / used)


# ------------------------------------------------------------------------------------------- the public workflow
def _result(entry_id, status, reasons, **kw) -> dict:
    return {"version": VERSION, "id": entry_id, "status": status, "reasons": list(reasons), "unit": None, **kw}


def _bind_baseline(call: dict, b: dict) -> list[str]:
    """Invariants the derived baseline must satisfy (it is computed here, so a failure is a defect, not input)."""
    probs = []
    a = D._floor_minute_ms(_t(call["issue_utc"]))
    h = (_ms(_t(call["graded_close_utc"])) - a) // D.MINUTE_MS
    if b.get("o33") != "v3":
        probs.append(f"baseline o33 {b.get('o33')!r}")
    if b.get("spec_sha256") != F.V3_SPEC_SHA256:
        probs.append("baseline spec hash is not the frozen v3 specification")
    if call["call_type"] == "containment" and b.get("version") != CALLS_VERSION:
        probs.append(f"baseline module {b.get('version')!r}, registered {CALLS_VERSION}")
    if b.get("anchor_utc") != D.iso(dt.datetime.fromtimestamp(a / 1000, dt.timezone.utc)):
        probs.append(f"baseline anchor {b.get('anchor_utc')} is not the call's anchor")
    if b.get("horizon_min") != h:
        probs.append(f"baseline horizon {b.get('horizon_min')} min, the call's is {h}")
    return probs


def evaluate(entry: dict, evaluation_utc, market: dict, releases: list[int] | None = None) -> dict:
    """The supported path from one registered call to a scoring unit (see the module docstring). Never raises."""
    entry = entry if isinstance(entry, dict) else {}
    doc = entry.get("doc")
    eid = doc.get("id") if isinstance(doc, dict) else None
    now = _tt(evaluation_utc)
    if now is None:
        return _result(eid, "invalid", ["evaluation time missing or without a timezone"])
    if isinstance(doc, dict) and doc.get("call_type") == "conditional":
        return _evaluate_conditional(entry, now, market, releases)
    if entry.get("readback") is None:
        return _result(eid, "not-admitted", ["no registry read-back: registration is unverified"])
    adm = verify_registration(doc, entry.get("receipt"), entry.get("read"), entry.get("readback"), now)
    base = {"admission": adm}
    if not adm["eligible"]:
        return _result(eid, "invalid" if adm["status"] == "invalid" else "not-admitted",
                       [f"{adm['status']}: " + "; ".join(adm["reasons"])], **base)
    if _t(adm["receipt_utc"]) > now:
        return _result(eid, "not-admitted", ["the registry receipt is later than the evaluation time"], **base)
    graded = _t(doc["graded_close_utc"])
    if now < graded:
        return _result(eid, "pending", [f"not matured: graded close {doc['graded_close_utc']} is after the "
                                        f"evaluation time {D.iso(now)}"], **base)
    if not isinstance(market, dict) or market.get("problems") is None:
        return _result(eid, "unavailable", ["market data not built by market_data()/market_from_archive()"], **base)
    if market["problems"]:
        return _result(eid, "unavailable", ["market data invalid: " + "; ".join(market["problems"])], **base)
    market = market_data(market.get("symbol"), market.get("closes"), market.get("source"))      # edited since? re-check
    if market["problems"]:
        return _result(eid, "unavailable", ["market data invalid: " + "; ".join(market["problems"])], **base)
    if market.get("symbol") != doc["instrument"]:
        return _result(eid, "invalid", [f"market data is {market.get('symbol')!r}, the call is on "
                                        f"{doc['instrument']!r}"], **base)
    retrieved = _t(market["source"]["retrieved_utc"])
    if retrieved > now:
        return _result(eid, "unavailable", [f"market data retrieved {D.iso(retrieved)}, after the evaluation time: "
                                            "not available to this evaluation"], **base)
    closes = market["closes"]
    g = _ms(graded)
    if g not in closes:
        return _result(eid, "unavailable", ["the 1m close at the graded close is not in the market data"], **base)
    if retrieved < graded:
        return _result(eid, "invalid", ["the outcome close is in data retrieved before that close existed"], **base)
    if doc["call_type"] == "containment":
        b = D.matched_baseline_v3(doc, closes, releases)
        role_value = "rate"
    else:
        b = v3_lean_drift(doc, closes)
        role_value = "lean_drift"
    summary = {"available": bool(b.get("available")), "reason": b.get("reason"), "role": "primary",
               "o33": b.get("o33"), "spec_sha256": b.get("spec_sha256"), "module": b.get("version"),
               "anchor_utc": b.get("anchor_utc"), "horizon_min": b.get("horizon_min"), "windows": b.get("windows"),
               "candidate_windows": b.get("candidate_windows"), role_value: b.get(role_value), "se": b.get("se")}
    base["baseline"] = summary
    if not b.get("available"):
        return _result(eid, "unavailable", [f"registered primary baseline unavailable: {b.get('reason')}"], **base)
    bind = _bind_baseline(doc, b)
    if bind:
        return _result(eid, "invalid", ["baseline binding: " + "; ".join(bind)], **base)
    if doc["call_type"] == "containment":
        if _finite(b.get("rate")) is None or not 0 <= b["rate"] <= 1:
            return _result(eid, "invalid", ["baseline rate outside [0, 1]"], **base)
        se = _finite(b.get("se"))
        if se is None or se < 0:
            return _result(eid, "unavailable", ["containment baseline has no valid standard error: refusing to "
                                                "substitute zero"], **base)
        outcome = D.containment_outcome_v3(doc, closes)
        if outcome not in (0, 1):
            return _result(eid, "invalid", [f"containment outcome {outcome!r} is not binary"], **base)
    else:
        if _finite(b.get("lean_drift")) is None:
            return _result(eid, "invalid", ["lean drift is not finite"], **base)
        outcome = closes[g]
    base["outcome"] = {"close_utc": doc["graded_close_utc"], "close": closes[g],
                       "value": outcome if doc["call_type"] == "containment" else closes[g]}
    u = _unit(doc, adm, b, outcome, market, now)
    return dict(_result(eid, "scored", ["eligible, matured, baseline and outcome derived"], **base), unit=u)


def _unit(call: dict, adm: dict, baseline: dict, outcome, market: dict, now: dt.datetime) -> dict:
    """Internal: one scoring unit from values evaluate() derived and checked."""
    u = {"id": call["id"], "content_sha256": adm["content_sha256"], "instrument": call["instrument"],
         "call_type": call["call_type"], "issue_utc": call["issue_utc"], "graded_close_utc": call["graded_close_utc"],
         "receipt_utc": adm["receipt_utc"], "status": "eligible", "cohort": adm["cohort"], "o33": "v3",
         "spec_sha256": baseline["spec_sha256"], "anchor_utc": baseline["anchor_utc"],
         "horizon_min": baseline["horizon_min"], "baseline_role": "primary",
         "source": {"symbol": market["symbol"], "provider": market["source"].get("provider"),
                    "retrieved_utc": market["source"].get("retrieved_utc"), "closes_sha256": market["closes_sha256"]},
         "depends_on": call.get("depends_on"), "evaluated_utc": D.iso(now), "wrapper": VERSION,
         "admission_basis": adm.get("admission_basis")}
    if call["call_type"] == "containment":
        u.update(outcome=int(outcome), baseline=baseline["rate"], d=int(outcome) - baseline["rate"],
                 se=float(baseline["se"]), se_basis=CONTAINMENT_SE_BASIS)
    else:
        u.update(outcome=float(outcome), baseline=baseline["lean_drift"],
                 d=D.lean_outcome(int(call["direction"]), float(call["issue_price"]), float(outcome),
                                  baseline["lean_drift"]), se=None, se_basis=LEAN_SE_BASIS)
    return u


def _paired(units: list[dict]) -> dict:
    """Internal: the frozen paired statistic for one cohort and call type of units derived by evaluate()."""
    if not units:
        return {"version": VERSION, "status": "no units"}
    kinds = {(u.get("cohort"), u.get("call_type")) for u in units}
    if len(kinds) != 1:
        raise ValueError(f"mixed cohorts {sorted(map(str, kinds))}: score each cohort separately, never pooled")
    cohort, call_type = next(iter(kinds))
    if cohort != "v3":
        raise ValueError(f"cohort {cohort!r} is not v3 evidence")
    for u in units:
        if call_type == "containment" and (u.get("se") is None or u.get("se_basis") != CONTAINMENT_SE_BASIS):
            raise ValueError(f"{u.get('id')}: containment unit without its primary baseline se")
        if call_type in ("lean", "conditional") and u.get("se") is not None:
            raise ValueError(f"{u.get('id')}: a lean unit carries no se (none is registered)")
        if not u.get("receipt_utc"):
            raise ValueError(f"{u.get('id')}: receipt needed for the registered de-duplication order")
    # The registered rule counts the first receipt per key and is silent on equal receipts; the frozen function
    # then keeps input order, so a tie would depend on arrival order. Ties are broken by call id and reported.
    ordered = sorted(units, key=lambda u: (_t(u["receipt_utc"]), u["id"]))
    keys = {}
    for u in ordered:
        keys.setdefault((u["instrument"], u["call_type"], round(D.horizon_h(u)), u["graded_close_utc"],
                         _t(u["receipt_utc"])), []).append(u["id"])
    ties = sorted(v for v in keys.values() if len(v) > 1)
    counted, rest = D.scoring_units(ordered)
    res = D.paired([dict(u, se=u["se"] if u["se"] is not None else 0.0) for u in counted])
    dependent = sorted(u["id"] for u in counted if u.get("depends_on"))
    res.update(cohort=cohort, call_type=call_type, counted=[u["id"] for u in counted],
               not_counted=[(u["id"], u.get("why")) for u in rest], wrapper=VERSION, se_basis=units[0]["se_basis"])
    if ties:
        res["receipt_ties"] = {"groups": ties, "rule": "same key and receipt time: the lowest call id counts "
                                                       "(the registered rule is silent on ties)"}
    by_basis = {}
    for u in counted:
        by_basis[u.get("admission_basis") or "unknown"] = by_basis.get(u.get("admission_basis") or "unknown", 0) + 1
    res["admission_basis_counts"] = by_basis
    if call_type in ("lean", "conditional"):
        res["interval_note"] = "excludes lean-drift estimation error (no registered standard error)"
    if dependent:
        res["dependence"] = {"units": dependent, "method": "none registered",
                             "effect": "comparative claim unsupported until a dependence method is registered "
                                       "prospectively (O33 v4 proposal)"}
        if res.get("status", "").startswith("comparative"):
            res["status"] = "unsupported: declared dependence between units, no registered method"
    return res


def score_v3(entries: list[dict], evaluation_utc, market: dict, releases: list[int] | None = None) -> dict:
    """Score registered calls: every unit is re-derived by evaluate(); nothing is accepted as a pre-built unit.
    Repeats of the same call id count once; each call type is scored separately."""
    results, seen, repeats = [], set(), []
    for e in entries or []:
        r = evaluate(e, evaluation_utc, market, releases)
        if r["status"] == "scored" and r["id"] in seen:
            repeats.append(r["id"])
            continue
        if r["status"] == "scored":
            seen.add(r["id"])
        results.append(r)
    units = [r["unit"] for r in results if r["status"] == "scored"]
    by_type = {}
    for ct in ("containment", "lean", "conditional"):
        us = [u for u in units if u["call_type"] == ct]
        if us:
            by_type[ct] = _paired(us)
    return {"version": VERSION, "evaluated_utc": D.iso(_t(evaluation_utc)) if _tt(evaluation_utc) else None,
            "by_type": by_type, "repeated_entries": repeats,
            "not_scored": [(r["id"], r["status"], r["reasons"]) for r in results if r["status"] != "scored"]}


# ------------------------------------------------------------------------------- O33 v3.1 population sensitivity
def _basis_of(entry: dict, evaluation_utc) -> str | None:
    """The admission basis evaluate() derives for an entry at this cutoff (None when not admitted)."""
    doc = entry.get("doc") if isinstance(entry, dict) else None
    adm = verify_registration(doc, entry.get("receipt") if isinstance(entry, dict) else None,
                              entry.get("read") if isinstance(entry, dict) else None,
                              entry.get("readback") if isinstance(entry, dict) else None, evaluation_utc)
    return adm.get("admission_basis") if adm.get("eligible") else None


def evidence_class(result: dict, v31_effective_utc=None) -> str:
    """Which of the three O33 v3.1 evidence classes a scored result belongs to:
    'original-rule' (admitted on its quoted receipt, as v3 required), 'retrospective-reassessment' (newly eligible
    under the order-record rule, registered before the verifiable v3.1 effective time), 'prospective-v3.1'
    (registered at or after that time). Without a verified effective time nothing is prospective v3.1."""
    unit = result.get("unit") or {}
    basis = unit.get("admission_basis")
    r = _tt(unit.get("receipt_utc"))
    eff = _tt(v31_effective_utc) if v31_effective_utc is not None else None
    if eff is not None and r is not None and r >= eff:
        return "prospective-v3.1"
    if basis == "quote":
        return "original-rule"
    if basis == "order-record":
        return "retrospective-reassessment"
    return "unclassified"


def conditional_funnel(entries: list[dict], evaluation_utc, market: dict, releases=None) -> dict:
    """Every registered conditional with its state at this cutoff, so a triggered-only score cannot hide a low
    usable-opportunity rate. Counts: registered (submitted), not-admitted, invalid, late, pending, expired,
    withdrawn, unavailable, scored."""
    counts = {k: 0 for k in ("registered", "not-admitted", "invalid", "late", "pending", "expired", "withdrawn",
                             "unavailable", "scored")}
    rows = []
    for e in entries or []:
        doc = (e or {}).get("doc") if isinstance(e, dict) else None
        if not (isinstance(doc, dict) and doc.get("call_type") == "conditional"):
            continue
        counts["registered"] += 1
        r = evaluate(e, evaluation_utc, market, releases)
        st = r["status"]
        if st == "not-admitted" and (r.get("admission") or {}).get("status") == "late":
            st = "late"
        counts[st] = counts.get(st, 0) + 1
        rows.append({"id": r["id"], "state": st, "reasons": r["reasons"][:2]})
    n = counts["registered"]
    counts["usable_rate"] = None if not n else round(counts["scored"] / n, 4)
    return {"version": VERSION, "counts": counts, "rows": rows, "outcome_labels": OUTCOME_LABELS}


def score_v31(entries: list[dict], evaluation_utc, market: dict, releases=None, v31_effective_utc=None) -> dict:
    """O33 v3.1 sensitivity: each declared population is scored by a complete, separate run of evaluate() and the
    registered de-duplication over only that population's entries (de-duplication can change which call counts,
    so rows are never removed from an already de-duplicated result). Call types stay separate."""
    entries = list(entries or [])
    basis = [(_basis_of(e, evaluation_utc), e) for e in entries]
    pops = {"all-admitted": [e for b, e in basis],
            "quote-only": [e for b, e in basis if b == "quote"],
            "order-record-only": [e for b, e in basis if b == "order-record"]}
    out = {"version": VERSION, "protocol": "O33 v3.1", "evaluated_utc": D.iso(_t(evaluation_utc)) if _tt(evaluation_utc) else None,
           "populations": {}, "outcome_labels": OUTCOME_LABELS,
           "effective_utc": v31_effective_utc,
           "note": "populations are separately recomputed; their counts need not add up after de-duplication"}
    for name, es in pops.items():
        sc = score_v3(es, evaluation_utc, market, releases)
        classes = {}
        for e in es:
            r = evaluate(e, evaluation_utc, market, releases)
            if r["status"] == "scored":
                c = evidence_class(r, v31_effective_utc)
                classes[c] = classes.get(c, 0) + 1
        sc["entries"] = len(es)
        sc["evidence_classes"] = classes
        out["populations"][name] = sc
    out["conditional_funnel"] = conditional_funnel(entries, evaluation_utc, market, releases)["counts"]
    return out
