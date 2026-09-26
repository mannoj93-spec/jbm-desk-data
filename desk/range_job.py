#!/usr/bin/env python3
"""range_job — automated registration of the desk's range forecasts (crypto-desk package 11.2).

Runs from .github/workflows/range.yml a few minutes after every 4H close (00/04/08/12/16/20Z):
  refit     once per calendar month: fit B2 on every target that closed before the month began
            (the frozen walk-forward rule of runbook E2) and write desk/fits/YYYY-MM.json.
  forecast  forecast the log range of the next 4h, 24h and 72h from the last closed 4H bar and
            register three forecasts in registry/ through the repository's own registration.py.
  summary   read registry/scores.jsonl (scored weekly by report.py) and write reports/range.md.

Integrity. The model file must hash to the frozen O21 specification (FROZEN_SPEC) or nothing is
forecast. Each forecast's window starts at the next five-minute boundary after registration
(schema.py requires start > registration), so no forecast can be registered after its window opens.
The model was trained on UTC-aligned windows starting at the 4H close; the registered window starts a
few minutes later (queueing and GitHub cron delay), and the offset is recorded in each forecast's note.
Each forecast carries two range events scored identically by scoring.py: the B2 model and the B0
persistence baseline, so skill is measured on the same windows.

Stdlib only. Network: www.binance.com (4H klines), data.binance.vision (archive, refit only),
www.deribit.com (DVOL).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import sys
import time
import urllib.request
from pathlib import Path

DESK = Path(__file__).resolve().parent
BASE = DESK.parent
for p in (str(DESK), str(BASE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import jbm_archive as A          # noqa: E402
import range_model as R         # noqa: E402

JOB_VERSION = "range-job-11.2.0"
FROZEN_SPEC = "ae6aa254c786d2dd6045fab098c4237dbe8bcc07d6626d20617366d386ff687d"   # O21, Sep 26 2026
SELECTED = {"4h": "B2", "24h": "B2", "72h": "B2"}
HOURS = {"4h": 4, "24h": 24, "72h": 72}
CALENDAR = DESK / "releases_2020_2026.csv"
STATUS = "exploratory, holdout-consistent (O21, Sep 26 2026)"
UTC = dt.timezone.utc
MS_5M = 300_000
MAX_DECISION_AGE_H = 1.0          # window offset from the trained alignment stays near an hour or less
ID_PREFIX = "range-b2-"


class StaleDecision(RuntimeError):
    """The last closed 4H bar is too old to forecast from (the job ran late or out of schedule)."""


def _now():
    return dt.datetime.now(UTC).replace(microsecond=0)


def _ms(t):
    return int(t.timestamp() * 1000)


def _iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def spec_ok(path=DESK / "range_model.py") -> bool:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest() == FROZEN_SPEC


# --------------------------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------------------------
def fetch_recent_bars(now, n=400, opener=None):
    """The last n closed 4H bars from the live API, through the archive loader's validation."""
    end = now.replace(minute=0, second=0) - dt.timedelta(hours=now.hour % 4)      # last 4H boundary
    start = end - dt.timedelta(hours=4 * n)
    url = (f"https://www.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=4h"
           f"&startTime={_ms(start)}&endTime={_ms(end) - 1}&limit=1500")
    opener = opener or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=A.UA), timeout=30).read())
    raw = json.loads(opener(url))
    rows = [dict(zip(A.KLINE_COLS, [str(x) for x in r])) for r in raw if int(r[6]) < _ms(end)]
    state, bars, rep = A.inspect_klines(rows, start, end, "4h")
    if state != "ok":
        raise RuntimeError(f"recent bars not ok: {state} {rep.get('malformed_rows')} missing={rep.get('missing_bars')}")
    return bars, {"url": url, "sha256": _sha(bars), "n": len(bars)}


def fetch_recent_dvol(now, hours=96, opener=None):
    end = now.replace(minute=0, second=0)
    state, rows, rep = A.load_dvol(end - dt.timedelta(hours=hours), end, opener=opener)
    if state == "retrieval_error":
        raise RuntimeError("DVOL retrieval failed")
    return rows, {"state": state, "sha256": rep.get("sha256"), "missing_hours": rep.get("missing_hours")}


def calendar():
    rel = R.load_calendar(str(CALENDAR))
    return rel, hashlib.sha256(CALENDAR.read_bytes()).hexdigest()


# --------------------------------------------------------------------------------------------
# Monthly refit
# --------------------------------------------------------------------------------------------
def fit_path(month: dt.date, base=BASE) -> Path:
    return Path(base) / "desk/fits" / f"{month:%Y-%m}.json"


def refit(now=None, base=BASE, history=None):
    """Write desk/fits/YYYY-MM.json for the current month if missing. `history` (bars, dvol) may be
    supplied (tests); otherwise pulled from the archive and the API."""
    now = now or _now()
    m0 = dt.datetime(now.year, now.month, 1, tzinfo=UTC)
    path = fit_path(m0.date(), base)
    if path.exists():
        print(f"refit: {path.name} exists; nothing to do")
        return path
    if not spec_ok():
        raise SystemExit("refit refused: range_model.py does not match the frozen specification")
    if history is None:
        st, bars, manifest = A.load_klines_span(dt.date(2020, 1, 1), (m0 - dt.timedelta(days=1)).date(), "4h")
        have = {b["open_utc"] for b in bars}
        want_last = _iso(m0 - dt.timedelta(hours=4))
        if want_last not in have:                     # archive for the last day(s) not yet published
            gap_start = R._t(bars[-1]["open_utc"]) + dt.timedelta(hours=4)
            n = int((m0 - gap_start).total_seconds() // 14400)
            recent, _ = fetch_recent_bars(m0, n=max(n, 1))
            bars += [b for b in recent if b["open_utc"] >= _iso(gap_start)]
        dstate, dvol, drep = A.load_dvol(dt.datetime(2021, 3, 24, tzinfo=UTC), m0)
        data = {"klines_files": len(manifest), "klines_manifest_sha256": _sha([m["sha256"] for m in manifest]),
                "klines_worst_state": st, "dvol_state": dstate, "dvol_sha256": drep.get("sha256")}
    else:
        bars, dvol = history
        data = {"supplied": True}
    times = [R._t(b["open_utc"]) for b in bars]
    gaps = sum(1 for a, b in zip(times, times[1:]) if b - a != dt.timedelta(hours=4))
    if gaps or times[-1] != m0 - dt.timedelta(hours=4):
        raise RuntimeError(f"refit history not contiguous to the month start (gaps={gaps}, last={times[-1]})")
    rel, cal_sha = calendar()
    panel = R.build_panel(bars, rel, dvol)
    fits, b0q = {}, {}
    for h, model in SELECTED.items():
        fm = R.fit(panel[h], model, m0)
        if fm is None:
            raise RuntimeError(f"refit: too few rows for {h}")
        fits[h] = {k: fm[k] for k in ("model", "beta", "terms", "n", "dropped_terms", "resid_q", "refit_utc")}
        res0 = [r["y"] - r["b0"] for r in panel[h] if r["y"] is not None and r["target_close_utc"] <= _iso(m0)]
        b0q[h] = R._quantiles(res0)
    doc = {"month": f"{m0:%Y-%m}", "refit_utc": _iso(m0), "spec_sha256": FROZEN_SPEC, "range_model": R.VERSION,
           "job": JOB_VERSION, "fits": fits, "b0_resid_q": b0q, "calendar_sha256": cal_sha,
           "bars": len(bars), "first_bar": bars[0]["open_utc"], "last_bar": bars[-1]["open_utc"], "data": data}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n")
    print(f"refit: wrote {path.name} (n={ {h: f['n'] for h, f in fits.items()} })")
    return path


# --------------------------------------------------------------------------------------------
# Forecast and register
# --------------------------------------------------------------------------------------------
def build_forecasts(bars, dvol, fits_doc, fits_sha, now, inputs_meta):
    """Three registry documents (4h, 24h, 72h) for the decision at the close of bars[-1]."""
    rel, cal_sha = calendar()
    decision = R._t(bars[-1]["close_utc"])
    age_h = (now - decision).total_seconds() / 3600
    if age_h > MAX_DECISION_AGE_H or age_h < 0:
        raise StaleDecision(f"decision close {decision} is {age_h:.2f}h from now (> {MAX_DECISION_AGE_H}h); not forecasting a stale bar")
    panel = R.build_panel(bars, rel, dvol)
    ref = bars[-1]["close"]
    cal_end = rel[-1]
    start = dt.datetime.fromtimestamp(((_ms(now) + 60_000) // MS_5M + 1) * MS_5M / 1000, tz=UTC)
    offset_min = int((start - decision).total_seconds() // 60)
    docs = []
    for h, model in SELECTED.items():
        row = panel[h][-1]
        if row["decision_utc"] != _iso(decision):
            raise RuntimeError("panel does not end at the decision bar")
        f = fits_doc["fits"][h]
        fitted = {"model": model, "beta": f["beta"]}
        if any(row.get(t) is None for t in R.MODEL_TERMS[model]):
            raise RuntimeError(f"{h}: a B2 input is missing at the decision (DVOL?)")
        p = R.predict(fitted, row)
        q = sorted(math.exp(p + r) for r in f["resid_q"])
        q0 = sorted(math.exp(row["b0"] + r) for r in fits_doc["b0_resid_q"][h])
        horizon = start + dt.timedelta(hours=HOURS[h])
        inside = [r for r in rel if start <= r < horizon]
        regime = ("releases inside the window: " + ", ".join(_iso(r) for r in inside)) if inside else \
            "no CPI/NFP/PPI/FOMC release inside the window (desk calendar)"
        if horizon > cal_end:
            regime += f"; calendar coverage ends {_iso(cal_end)} — later releases unknown"
        note = (f"Desk range model {R.VERSION} (frozen spec {FROZEN_SPEC[:12]}, {STATUS}); job {JOB_VERSION}. "
                f"Decision at the {_iso(decision)} 4H close; registered window starts {offset_min} min later "
                f"(model trained on windows starting at the close). Point ln(lr) {p:.5f}; B0 ln(lr) {row['b0']:.5f}. "
                f"Fit {fits_doc['month']} sha256 {fits_sha[:12]}. Quantiles are ln(high/low) from fit residuals. "
                f"Ref close {ref}; q50 range ≈ {ref * (math.exp(q[1]) - 1):.0f} pts. Not a direction or a probability.")
        docs.append({
            "id": f"{ID_PREFIX}{h}-{decision:%Y%m%dT%H%MZ}",
            "code_version": f"{R.VERSION} / {JOB_VERSION}",
            "snapshot_hash": _sha({"inputs": inputs_meta, "fit": fits_sha, "calendar": cal_sha}),
            "instrument": "BTCUSDT perp, Binance last price",
            "reference_price": ref,
            "start_utc": _iso(start),
            "horizon_utc": _iso(horizon),
            "made_utc": _iso(now),
            "package": "crypto-desk 11.2",
            "event_regime": regime[:2000],
            "note": note[:2000],
            "events": [
                {"name": f"B2 range model {R.VERSION}", "type": "range",
                 "q10": round(q[0], 8), "q50": round(q[1], 8), "q90": round(q[2], 8)},
                {"name": "B0 persistence baseline", "type": "range",
                 "q10": round(q0[0], 8), "q50": round(q0[1], 8), "q90": round(q0[2], 8)},
            ],
        })
    return docs


def forecast(now=None, base=BASE, bars=None, dvol=None, register_fn=None, validate_fn=None, clock=None):
    """Build, validate, write and register the three forecasts. Idempotent per decision."""
    now = now or _now()
    clock = clock or (lambda: int(time.time() * 1000))
    if not spec_ok():
        raise SystemExit("forecast refused: range_model.py does not match the frozen specification")
    if register_fn is None or validate_fn is None:
        from registration import register as register_fn  # noqa: F811
        from schema import validate as validate_fn         # noqa: F811
    inputs = {}
    if bars is None:
        bars, inputs["bars"] = fetch_recent_bars(now)
    if dvol is None:
        dvol, inputs["dvol"] = fetch_recent_dvol(now)
    decision = R._t(bars[-1]["close_utc"])
    fp = fit_path(dt.date(decision.year, decision.month, 1), base)
    if not fp.exists():
        raise RuntimeError(f"no fit file {fp.name}; run refit first")
    fits_bytes = fp.read_bytes()
    docs = build_forecasts(bars, dvol, json.loads(fits_bytes), hashlib.sha256(fits_bytes).hexdigest(), now, inputs)
    written = []
    for doc in docs:
        path = Path(base) / "registry" / f"{doc['id']}.json"
        if path.exists():
            print(f"forecast: {doc['id']} already written; skipping")
            continue
        errors = validate_fn(doc, clock())
        if errors:
            raise RuntimeError(f"{doc['id']} invalid: {errors}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode() + b"\n")
        written.append(doc["id"])
    if written:
        rat = clock()
        for doc in docs:
            if doc["id"] in written and _ms(R._t(doc["start_utc"])) <= rat:
                raise RuntimeError(f"{doc['id']}: registration would be at or after start; aborting")
        new, errors = register_fn(base, rat)
        if errors:
            raise RuntimeError("registration errors: " + "; ".join(errors))
        print(f"forecast: registered {written} at {rat}")
    return docs, written


# --------------------------------------------------------------------------------------------
# Summary of scored forecasts
# --------------------------------------------------------------------------------------------
def summary(base=BASE, out="reports/range.md"):
    path = Path(base) / "registry/scores.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []
    mine = [r for r in rows if str(r.get("id", "")).startswith(ID_PREFIX)]
    stats = {}
    for r in mine:
        h = r["id"][len(ID_PREFIX):].split("-")[0]
        s = stats.setdefault(h, {"scored": 0, "late": 0, "other": 0, "b2": [], "b0": [], "c2": [], "c0": []})
        if r.get("status") != "scored":
            s["late" if "late" in str(r.get("status")) else "other"] += 1
            continue
        ev = {e["name"].split(" ")[0]: e for e in r.get("events", [])}
        if "B2" not in ev or "B0" not in ev or ev["B2"].get("abs_error_log_lr") is None:
            s["other"] += 1
            continue
        s["scored"] += 1
        s["b2"].append(ev["B2"]["abs_error_log_lr"]); s["b0"].append(ev["B0"]["abs_error_log_lr"])
        s["c2"].append(ev["B2"]["covered_80"]); s["c0"].append(ev["B0"]["covered_80"])
    lines = ["# Range forecasts — prospective scores", "",
             f"Generated {_iso(_now())} by {JOB_VERSION} from `registry/scores.jsonl` (scored weekly by `report.py`). "
             f"Model {R.VERSION}, frozen spec `{FROZEN_SPEC[:12]}`, status before these scores: {STATUS}.", "",
             "Skill = 1 − MAE(B2) ÷ MAE(B0) on |ln q50 − ln realized ln(high/low)|, the same windows for both. "
             "Coverage is the share of realized ranges inside q10–q90 (nominal 80%). Windows overlap within a "
             "horizon (a 72h window every 4h), so independent n is far below the count; nothing here is "
             "eligible for forecast status below ~100 independent windows.", "",
             "| horizon | scored | late / unscorable | MAE B2 | MAE B0 | skill | coverage B2 | coverage B0 |",
             "|---|---|---|---|---|---|---|---|"]
    for h in ("4h", "24h", "72h"):
        s = stats.get(h)
        if not s or not s["scored"]:
            lines.append(f"| {h} | 0 | {(s or {}).get('late', 0)} / {(s or {}).get('other', 0)} | — | — | — | — | — |")
            continue
        m2, m0 = sum(s["b2"]) / len(s["b2"]), sum(s["b0"]) / len(s["b0"])
        lines.append(f"| {h} | {s['scored']} | {s['late']} / {s['other']} | {m2:.4f} | {m0:.4f} | "
                     f"{(1 - m2 / m0) * 100:.1f}% | {sum(s['c2']) / len(s['c2']) * 100:.0f}% | "
                     f"{sum(s['c0']) / len(s['c0']) * 100:.0f}% |")
    target = Path(base) / out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n")
    print(f"summary: {sum(s['scored'] for s in stats.values())} scored range forecasts -> {out}")
    return stats


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "refit":
        refit()
    elif cmd == "forecast":
        import os
        try:
            forecast()
        except StaleDecision as exc:
            # A manual run between closes is a plumbing check, not a failure; a scheduled run that
            # starts this late is a failure worth seeing.
            print(f"forecast skipped: {exc}")
            if os.environ.get("GITHUB_EVENT_NAME") == "schedule":
                raise SystemExit(1)
    elif cmd == "summary":
        summary()
    else:
        raise SystemExit("usage: range_job.py refit|forecast|summary")
