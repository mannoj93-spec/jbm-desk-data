"""desk_calls_freeze - enforcement of the O33 v3 freeze (package 12.4.13, added after fresh-context runs found the
freeze rule enforced only in text). Kept apart from desk_calls.py so the frozen module's bytes stay exactly those
registered in the repository (research/registrations/o33-v3/registration.json).

  v3_cohort(receipt_utc)   'v3' only for a registry receipt strictly after the freeze; else 'pre-freeze'
  frozen_ok(folder)        verifies desk_calls.py / test_desk_calls.py bytes and every V3 constant against the record
"""
from __future__ import annotations

import datetime as dt
import hashlib
import os

VERSION = "calls-freeze-1.0.0"
V3_FREEZE_UTC = "2026-10-07T23:07:56Z"     # first push of the record to main (merge 730c06c5, GitHub activity API)
V3_FILES_SHA256 = {"desk_calls.py": "7cd1f3b61d0fdfea7819e848f314573c3af4cb815f8d586a7e72535059748fb4",
                   "test_desk_calls.py": "d1acb8a1bd040de14167bfc76a36ae1d1b01ede383e555af060db1a8f86414e3"}
V3_SPEC_SHA256 = "7c884dc65da1ed7da072a0f6709e89ad7c3fdb5bfdcafaaa0c7dc60f50262d56"
V3_CONSTANTS = {"V3_LOOKBACK_DAYS": 730, "V3_MIN_H": 15, "V3_MAX_H": 4320, "V3_K_RANGE": (0.05, 8.0),
                "V3_MIN_WINDOWS": 2000, "V3_MIN_USABLE": 0.95, "V3_SECONDARY_MIN": 300, "V3_TOD_HOURS": 2,
                "COST_BP": 10.0, "COMPARE": {"resampling_unit": "ISO week of the graded close", "B": 10_000, "seed": 33,
                                             "min_blocks": 10, "min_units": 30, "claim_blocks": 20, "claim_units": 60,
                                             "level": 0.95}}


def _t(x) -> dt.datetime:
    return x.astimezone(dt.timezone.utc) if isinstance(x, dt.datetime) else \
        dt.datetime.fromisoformat(str(x).replace("Z", "+00:00")).astimezone(dt.timezone.utc)


def v3_cohort(receipt_utc) -> str:
    """'v3' for a server receipt strictly later than the freeze, 'pre-freeze' otherwise (never v3 evidence)."""
    if receipt_utc is None:
        return "unregistered"
    return "v3" if _t(receipt_utc) > _t(V3_FREEZE_UTC) else "pre-freeze"


def frozen_ok(folder=None) -> list:
    """Problems ([] = intact): file bytes against the registered sha256 and every V3 constant against its frozen value."""
    folder = folder or os.path.dirname(os.path.abspath(__file__))
    probs = []
    for f, want in V3_FILES_SHA256.items():
        got = hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
        if got != want:
            probs.append(f"{f} sha256 {got[:12]} differs from the frozen {want[:12]}: a change to v3 is v4")
    import desk_calls as D
    if D.v3_spec_sha256() != V3_SPEC_SHA256:
        probs.append("V3 specification text differs from the frozen record")
    for k, v in V3_CONSTANTS.items():
        if getattr(D, k) != v:
            probs.append(f"{k} = {getattr(D, k)!r}, frozen {v!r}")
    return probs
