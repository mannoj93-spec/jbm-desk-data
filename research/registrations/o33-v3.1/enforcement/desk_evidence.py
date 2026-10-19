"""desk_evidence - the shared evidence contract (evidence-1.0.0; package 12.4.20, repository research_tools/evidence_contract.py).

One small set of rules that every public entry point reuses, so a new helper cannot implement a weaker copy of a rule
already enforced elsewhere (the recurring failure in the Oct 18-19 reviews: findings A-K). Byte-identical in the
skill package (desk_evidence.py) and the repository (research_tools/evidence_contract.py); both pin its sha256 in a test.

Clocks (all timezone-aware; a naive value is refused, never read as local time):
  event_utc      the instant or window end the evidence describes (a bar close, a fill, a delivery)
  published_utc  when the source published it, when the source says so (often unknown)
  retrieved_utc  when this system fetched it
  durable_utc    first durable availability: when a copy existed that a later reader could rely on
  cutoff         the assessment's information cutoff
Availability is the first of durable_utc, retrieved_utc that is present - never event_utc. Evidence whose
availability is unknown is state 'unknown-availability': it is not admitted as original evidence, and it is never
given the event time to complete a chain.

Boundaries. available_at(..., boundary) takes the contract's own rule: 'inclusive' (available at or before the cutoff;
the default, as the frozen O33 maturity rule reads data retrieved at or after a close) or 'strict' (strictly before;
prior selection: a snapshot recorded at the instant of a read was not available to it). Frozen contracts keep theirs.

Provenance: 'original' (captured at the time), 'reconstructed' (fetched later; never proof of what was available
earlier), 'unknown'. A reconstruction stays a reconstruction through every helper (provenance_after).

Values. number() never accepts bool; text only when the caller says the raw field is text (exchange JSON); NaN and
Infinity are 'malformed', never values; domains are per field, and zero is kept where the domain allows it.

States: ok | missing | malformed | out-of-domain | unavailable | partial | pending | invalid | unknown-availability |
not-yet-assessed. Missing, unavailable and failed are never zero.

A self-consistent hash proves content identity only - not a timestamp, a publication or an approval.
Pure functions, stdlib only, no clock.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math

VERSION = "evidence-1.0.0"
UTC = dt.timezone.utc
STATES = ("ok", "missing", "malformed", "out-of-domain", "unavailable", "partial", "pending", "invalid",
          "unknown-availability", "not-yet-assessed")
PROVENANCE = ("original", "reconstructed", "unknown")
# field domains: (lower, upper, lower_inclusive). None = unbounded.
DOMAINS = {
    "price": (0.0, None, False),          # a usable price is strictly positive
    "nonneg": (0.0, None, True),          # sizes, open interest, volumes: zero is a value
    "share_pct": (0.0, 100.0, True),
    "share": (0.0, 1.0, True),
    "funding_rate": (-0.05, 0.05, True),  # decimal per interval; |r| >= 5% is a unit error (percent passed?)
    "signed": (None, None, True),
    "probability": (0.0, 1.0, True),
}


# ------------------------------------------------------------------------------------------------------- clocks
def instant(x) -> dt.datetime:
    """A timezone-aware UTC instant from an aware datetime or an ISO-8601 string with an offset. Epoch numbers are
    accepted only through epoch_ms(). Raises ValueError on naive or unparseable input."""
    if isinstance(x, dt.datetime):
        if x.tzinfo is None:
            raise ValueError("naive datetime")
        return x.astimezone(UTC)
    if isinstance(x, (int, float, bool)) or x is None:
        raise ValueError(f"not an ISO-8601 instant: {x!r}")
    s = str(x).strip()
    t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    if t.tzinfo is None:
        raise ValueError(f"timestamp without a timezone: {s!r}")
    return t.astimezone(UTC)


def maybe_instant(x):
    """instant(x) or None (never raises)."""
    try:
        return instant(x)
    except (TypeError, ValueError):
        return None


def epoch_ms(x) -> dt.datetime:
    """An instant from integer epoch milliseconds (bool refused)."""
    if isinstance(x, bool) or not isinstance(x, int):
        raise ValueError(f"epoch milliseconds must be an integer, got {x!r}")
    return dt.datetime.fromtimestamp(x / 1000, UTC)


def iso(t) -> str:
    t = instant(t)
    return t.strftime("%Y-%m-%dT%H:%M:%S") + ("Z" if not t.microsecond else f".{t.microsecond:06d}Z")


def availability(ev: dict):
    """(instant | None, which clock). First durable availability, else retrieval. Never the event time."""
    if not isinstance(ev, dict):
        return None, "not an evidence object"
    for k in ("durable_utc", "retrieved_utc"):
        if ev.get(k) is not None:
            t = maybe_instant(ev.get(k))
            return (t, k) if t is not None else (None, f"{k} unparseable or without a timezone")
    return None, "availability unknown (no durable_utc or retrieved_utc)"


def available_at(ev: dict, cutoff, boundary: str = "inclusive") -> tuple[str, str]:
    """('ok' | 'pending' | 'unknown-availability' | 'invalid', reason): was this evidence available to an assessment
    with this cutoff? 'pending' means first available after the cutoff - it cannot change the earlier answer."""
    c = maybe_instant(cutoff)
    if c is None:
        return "invalid", "cutoff missing or without a timezone"
    if boundary not in ("inclusive", "strict"):
        return "invalid", f"boundary {boundary!r}"
    t, which = availability(ev)
    if t is None:
        return ("unknown-availability" if "unknown" in which else "invalid"), which
    e = maybe_instant(ev.get("event_utc")) if ev.get("event_utc") is not None else None
    if ev.get("event_utc") is not None and e is None:
        return "invalid", "event_utc unparseable or without a timezone"
    if e is not None and t < e and not ev.get("forecast"):
        return "invalid", f"{which} {iso(t)} precedes the event it describes {iso(e)}"
    late = t > c if boundary == "inclusive" else t >= c
    if late:
        return "pending", f"first available {iso(t)} ({which}), after the cutoff {iso(c)}"
    return "ok", f"available {iso(t)} ({which})"


def provenance_after(*inputs: str) -> str:
    """The provenance of a value derived from these inputs: any reconstruction makes it reconstructed; any unknown
    makes it unknown; only all-original inputs give an original."""
    ps = [p if p in PROVENANCE else "unknown" for p in inputs]
    if not ps:
        return "unknown"
    if "reconstructed" in ps:
        return "reconstructed"
    if "unknown" in ps:
        return "unknown"
    return "original"


# ------------------------------------------------------------------------------------------------------- values
def number(x, domain: str | None = None, allow_text: bool = False) -> tuple[float | None, str]:
    """(value, state). state: ok | missing | malformed | out-of-domain. Bool is malformed; NaN/Infinity (numbers or
    text) are malformed; text is parsed only with allow_text."""
    if x is None or (isinstance(x, str) and not x.strip()):
        return None, "missing"
    if isinstance(x, bool):
        return None, "malformed"
    if isinstance(x, (int, float)):
        v = float(x)
    elif allow_text and isinstance(x, str):
        try:
            v = float(x.strip())
        except ValueError:
            return None, "malformed"
    else:
        return None, "malformed"
    if not math.isfinite(v):
        return None, "malformed"
    if domain is not None:
        lo, hi, lo_incl = DOMAINS[domain]
        if lo is not None and (v < lo or (v == lo and not lo_incl)):
            return None, "out-of-domain"
        if hi is not None and v > hi:
            return None, "out-of-domain"
    return v, "ok"


def canon(obj) -> str:
    """Canonical JSON; NaN and Infinity are refused (ValueError) - never persisted."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


def content_sha256(obj) -> str:
    return hashlib.sha256(canon(obj).encode()).hexdigest()


def loads_strict(text: str):
    """json.loads that refuses NaN/Infinity constants."""
    def bad(c):
        raise ValueError(f"non-finite constant {c} in stored JSON")
    return json.loads(text, parse_constant=bad)


# ---------------------------------------------------------------------------------------------- record identity
IDENTITY = ("instrument", "venue", "metric", "cohort", "unit")


def identity_mismatch(a: dict, b: dict, fields=IDENTITY) -> list[str]:
    """Fields on which two records' identities differ (both present and unequal). A missing field on either side is
    reported as unverified rather than assumed equal."""
    out = []
    for f in fields:
        x, y = (a or {}).get(f), (b or {}).get(f)
        if x is None or y is None:
            if x is not None or y is not None:
                out.append(f"{f}: unverified ({x!r} vs {y!r})")
        elif x != y:
            out.append(f"{f}: {x!r} != {y!r}")
    return out


def dedupe_by_identity(records: list[dict], key) -> tuple[list[dict], list[tuple]]:
    """(unique, conflicts). Records with the same key and identical canonical content collapse to one (reprocessing
    an identified event cannot double-count it); same key with different content is a conflict, returned - never
    silently resolved. Order-independent."""
    by, conflicts = {}, []
    for r in sorted(records or [], key=lambda r: canon(r)):
        k = key(r)
        if k in by:
            if canon(by[k]) != canon(r):
                conflicts.append((k, by[k], r))
            continue
        by[k] = r
    return [by[k] for k in sorted(by, key=lambda k: canon(list(k) if isinstance(k, tuple) else k))], conflicts


# --------------------------------------------------------------------------------------------- property helpers
def monotone_in_evidence(evaluate, base_inputs, later_inputs, cutoff) -> bool:
    """Property check used by tests: adding evidence first available after `cutoff` cannot change the answer of an
    assessment at `cutoff`."""
    return canon(evaluate(base_inputs, cutoff)) == canon(evaluate(base_inputs + later_inputs, cutoff))
