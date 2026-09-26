#!/usr/bin/env python3
"""range_job — the desk's automated range forecasts (crypto-desk package 12.0, repo revision 2.15).

Commands (workflow .github/workflows/range.yml, a few minutes after every 4H close):
  refit     once per calendar month: validate or build desk/fits/YYYY-MM.json from the retained history
            chain (desk/research/o21/inputs + desk/inputs/refit/*) plus the months since, fitted on every
            target that matured before the month began.
  forecast  prepare, validate and freeze one batch (4h, 24h, 72h) under contract RC1D
            (desk/range_contract.py) and register it through registration.register_batch - one logical
            transaction. Every attempt is logged in state/range_attempts.jsonl, whatever its outcome.
  confirm   after the workflow pushed: verify the manifest entries are on the remote branch and record the
            confirmation time in state/range_publications.jsonl. Prospective eligibility = local freeze
            before the window start AND remote confirmation before the window start.
  status    reports/range_status.json (machine-readable, read by the skill) and reports/range.md.
  replay    `replay <forecast id>`: rebuild a registered forecast from its retained input bundle, offline.

Stdlib only. Network: www.binance.com (4H klines), data.binance.vision (refit only), www.deribit.com (DVOL).
"""
from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import json
import math
import os
import subprocess
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
import range_contract as C      # noqa: E402

JOB_VERSION = "range-job-12.0.0"
PACKAGE = "crypto-desk 12.0"
FROZEN_SPEC = "ae6aa254c786d2dd6045fab098c4237dbe8bcc07d6626d20617366d386ff687d"   # O21, Sep 26 2026
CONTRACT = "RC1D"
ID_PREFIX = "range-rc1d-"
LEGACY_PREFIX = "range-b2-"                       # repo 2.14 records (q50-scored, pre-contract)
CALENDAR = DESK / "releases_2020_2026.csv"
STATUS = "exploratory, holdout-consistent (O21 under RC1); RC1D prospective record only"
UTC = dt.timezone.utc
MAX_DECISION_AGE_H = 1.0
ATTEMPTS, PUBLICATIONS = "state/range_attempts.jsonl", "state/range_publications.jsonl"
INPUTS = "desk/inputs"
CHAIN_ROOT = DESK / "research/o21/inputs"
BUNDLE_BARS = R.WARMUP                            # features never read more than the last 180 bars
BUNDLE_DVOL_H = 8


class StaleDecision(RuntimeError):
    """The last closed 4H bar is too old to forecast from."""


class AttemptRefused(RuntimeError):
    """This decision already has a recorded window; a retry would move it."""


def _now():
    return dt.datetime.now(UTC).replace(microsecond=0)


_ms, _iso, _sha = C.ms, C.iso, C.sha256_json


def spec_ok(path=DESK / "range_model.py") -> bool:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest() == FROZEN_SPEC


def run_meta() -> dict:
    env = os.environ
    production = (env.get("GITHUB_ACTIONS") == "true" and env.get("GITHUB_REPOSITORY") == "mannoj93-spec/jbm-desk-data"
                   and env.get("GITHUB_REF") == "refs/heads/main")
    return {"event": env.get("GITHUB_EVENT_NAME", "local"), "run_id": env.get("GITHUB_RUN_ID"),
            "code_commit": env.get("GITHUB_SHA", "local"), "production": production}


# --------------------------------------------------------------------------------------------
# Append-only logs
# --------------------------------------------------------------------------------------------
def _rows(base, rel):
    from storage import read_rows
    return read_rows(Path(base) / rel)


def _append(base, rel, row):
    from storage import append_unique
    append_unique(Path(base) / rel, [row], lambda r: json.dumps(r, sort_keys=True))


def record(base, attempt, decision, state, run, t, **extra):
    row = {"attempt": attempt, "decision_utc": decision, "contract": C.contract_id(CONTRACT), "state": state,
           "t": t, "job": JOB_VERSION, "run": run, **extra}
    _append(base, ATTEMPTS, row)
    print(f"attempt {attempt}: {state}" + (f" ({extra['reason']})" if extra.get("reason") else ""))
    return row


def attempts_for(base, decision: str) -> list:
    return [r for r in _rows(base, ATTEMPTS) if r.get("decision_utc") == decision]


# --------------------------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------------------------
def last_boundary(now):
    return now.replace(minute=0, second=0, microsecond=0) - dt.timedelta(hours=now.hour % 4)


def fetch_recent_bars(now, n=400, opener=None):
    """The last n closed 4H bars from the live API, through the archive loader's validation; must be ok."""
    end = last_boundary(now)
    start = end - dt.timedelta(hours=4 * n)
    url = (f"https://www.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=4h"
           f"&startTime={_ms(start)}&endTime={_ms(end) - 1}&limit=1500")
    opener = opener or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=A.UA), timeout=30).read())
    blob = opener(url)
    raw = json.loads(blob)
    rows = [dict(zip(A.KLINE_COLS, [str(x) for x in r])) for r in raw if int(r[6]) < _ms(end)]
    state, bars, rep = A.inspect_klines(rows, start, end, "4h")
    if state != "ok":
        raise RuntimeError(f"recent bars not admissible: {state} {rep.get('malformed_rows')} missing={rep.get('missing_bars')}")
    return bars, {"url": url, "response_sha256": hashlib.sha256(blob).hexdigest(), "state": state,
                  "retrieved_utc": _iso(_now()), "n": len(bars)}


def fetch_recent_dvol(now, hours=96, opener=None):
    end = now.replace(minute=0, second=0, microsecond=0)
    state, rows, rep = A.load_dvol(end - dt.timedelta(hours=hours), end, opener=opener)
    return state, rows, {"state": state, "requests": rep.get("requests"), "sha256": rep.get("sha256"),
                         "missing_hours": rep.get("missing_hours"), "conflicts": rep.get("conflicts", 0),
                         "retrieved_utc": rep.get("retrieved_at_utc")}


def calendar():
    return R.load_calendar(str(CALENDAR)), hashlib.sha256(CALENDAR.read_bytes()).hexdigest()


def write_blob(base, rel_dir, obj) -> tuple:
    """Content-addressed gzip JSON (deterministic bytes). Returns (sha256 of canonical JSON, relative path)."""
    raw = C.canonical(obj)
    sha = hashlib.sha256(raw).hexdigest()
    rel = f"{rel_dir}/{sha}.json.gz"
    path = Path(base) / rel
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_bytes(gzip.compress(raw, 9, mtime=0))
        os.replace(tmp, path)
    return sha, rel


def read_blob(path) -> tuple:
    raw = gzip.decompress(Path(path).read_bytes())
    return hashlib.sha256(raw).hexdigest(), json.loads(raw)


# --------------------------------------------------------------------------------------------
# Monthly refit (retained history chain)
# --------------------------------------------------------------------------------------------
def fit_path(month: dt.date, base=BASE) -> Path:
    return Path(base) / "desk/fits" / f"{month:%Y-%m}.json"


def load_fit(base, month_start):
    path = fit_path(month_start.date(), base)
    if not path.exists():
        raise C.FitInvalid(f"no fit file {path.name}; run refit first")
    raw = path.read_bytes()
    doc = json.loads(raw)
    C.validate_fit(doc, month_start, CALENDAR, FROZEN_SPEC)
    return doc, hashlib.sha256(raw).hexdigest()


def history_chain(base=BASE):
    """Bars and DVOL rows retained in the repository: the O21 inputs plus every refit delta, in order."""
    root_k, root_d = CHAIN_ROOT / "klines_4h.json.gz", CHAIN_ROOT / "dvol_1h.json.gz"
    if not root_k.exists():
        return [], [], []
    k = json.loads(gzip.decompress(root_k.read_bytes()))
    d = json.loads(gzip.decompress(root_d.read_bytes()))
    bars, dvol, links = list(k["rows"]), list(d["rows"]), ["o21-inputs"]
    deltas = [(read_blob(p), p.name) for p in (Path(base) / INPUTS / "refit").glob("*.json.gz")]
    for (sha, delta), name in sorted(deltas, key=lambda x: x[0][1]["month"]):
        if name != f"{sha}.json.gz":
            raise ValueError(f"refit delta {name} altered: content hash {sha[:12]}")
        bars += [b for b in delta["bars"] if b["open_utc"] > bars[-1]["open_utc"]]
        dvol += [r for r in delta["dvol"] if r["open_utc"] > dvol[-1]["open_utc"]]
        links.append(name)
    return bars, dvol, links


def refit(now=None, base=BASE, history=None):
    """Validate this month's fit if it exists; otherwise build it once. `history` (bars, dvol) for tests."""
    now = now or _now()
    m0 = dt.datetime(now.year, now.month, 1, tzinfo=UTC)
    path = fit_path(m0.date(), base)
    if path.exists():
        load_fit(base, m0)                              # raises FitInvalid on any mismatch
        print(f"refit: {path.name} exists and validates")
        return path
    if not spec_ok():
        raise SystemExit("refit refused: range_model.py does not match the frozen specification")
    releases, cal_sha = calendar()
    if history is None:
        bars, dvol, links = history_chain(base)
        bars = [b for b in bars if R._t(b["open_utc"]) < m0]
        dvol = [r for r in dvol if R._t(r["open_utc"]) < m0]
        last = R._t(bars[-1]["open_utc"])
        delta = {"bars": [], "dvol": [], "manifest": [], "dvol_report": None}
        if last < m0 - dt.timedelta(hours=4):
            first = (last + dt.timedelta(hours=4)).date()
            st, new, manifest = A.load_klines_span(first, (m0 - dt.timedelta(days=1)).date(), "4h")
            if st != "ok":
                raise RuntimeError(f"refit klines not admissible: {st}")
            new = [b for b in new if last < R._t(b["open_utc"]) < m0]
            want = int((m0 - last).total_seconds() // 14400) - 1
            if len(new) < want:                     # archive for the last day(s) not yet published
                recent, meta = fetch_recent_bars(m0, n=want)
                new = sorted({b["open_utc"]: b for b in new + [b for b in recent if R._t(b["open_utc"]) > last]}.values(),
                             key=lambda b: b["open_utc"])
                manifest = manifest + [meta]
            dlast = R._t(dvol[-1]["open_utc"])
            dstate, dnew, drep = A.load_dvol(dlast + dt.timedelta(hours=1), m0)
            admit = C.admit_dvol(dstate, dnew, m0, drep, "history")
            delta = {"bars": new, "dvol": dnew, "manifest": manifest, "dvol_report": drep, "dvol_admissibility": admit}
            bars, dvol = bars + new, dvol + dnew
        dsha, drel = write_blob(base, f"{INPUTS}/refit", dict(delta, month=f"{m0:%Y-%m}")) if delta["bars"] else (None, None)
        data = {"chain": links + ([Path(drel).name] if drel else []), "klines_worst_state": "ok",
                "dvol_state": (delta.get("dvol_admissibility") or {}).get("state", "ok"),
                "dvol_override": (delta.get("dvol_admissibility") or {}).get("override"), "delta_sha256": dsha}
    else:
        bars, dvol = history
        data = {"supplied": True}
    times = [R._t(b["open_utc"]) for b in bars]
    gaps = sum(1 for a, b in zip(times, times[1:]) if b - a != dt.timedelta(hours=4))
    if gaps or times[-1] != m0 - dt.timedelta(hours=4):
        raise RuntimeError(f"refit history not contiguous to the month start (gaps={gaps}, last={times[-1]})")
    panel = R.build_panel(bars, releases, dvol)
    fits, b0q = {}, {}
    for h, model in C.SELECTED.items():
        fm = R.fit(panel[h], model, m0)
        if fm is None:
            raise RuntimeError(f"refit: too few rows for {h}")
        fits[h] = {k: fm[k] for k in ("model", "beta", "terms", "n", "dropped_terms", "resid_q", "refit_utc")}
        fits[h]["terms"] = list(fits[h]["terms"])
        res0 = [r["y"] - r["b0"] for r in panel[h] if r["y"] is not None and r["target_close_utc"] <= _iso(m0)]
        b0q[h] = R._quantiles(res0)
    doc = {"month": f"{m0:%Y-%m}", "refit_utc": _iso(m0), "spec_sha256": FROZEN_SPEC, "range_model": R.VERSION,
           "job": JOB_VERSION, "contract": C.contract_id(CONTRACT), "fits": fits, "b0_resid_q": b0q,
           "calendar_sha256": cal_sha, "calendar_prefix_sha256": C.calendar_prefix_sha(CALENDAR, m0),
           "bars": len(bars), "first_bar": bars[0]["open_utc"], "last_bar": bars[-1]["open_utc"], "data": data}
    C.validate_fit(doc, m0, CALENDAR, FROZEN_SPEC)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n")
    print(f"refit: wrote {path.name} (n={ {h: f['n'] for h, f in fits.items()} })")
    return path


# --------------------------------------------------------------------------------------------
# Forecast: prepare -> freeze (one transaction) -> [workflow push] -> confirm
# --------------------------------------------------------------------------------------------
def build(bars, dvol_rows, fit_doc, fit_sha, prepared: dt.datetime, sources: dict):
    """The input bundle and the three forecast documents (RC1D). Pure: no I/O."""
    releases, cal_sha = calendar()
    decision = R._t(bars[-1]["close_utc"])
    keep = bars[-BUNDLE_BARS:]
    dv = [r for r in dvol_rows if decision - dt.timedelta(hours=BUNDLE_DVOL_H) <= R._t(r["available_at_utc"]) <= decision]
    bundle = {"schema": "range-input-bundle/1", "decision_utc": _iso(decision), "prepared_utc": _iso(prepared),
              "contract": C.contract_id(CONTRACT), "range_model": R.VERSION, "spec_sha256": FROZEN_SPEC,
              "bars": [{k: b[k] for k in ("open_utc", "close_utc", "open", "high", "low", "close")} for b in keep],
              "dvol": [{k: r[k] for k in ("open_utc", "available_at_utc", "dvol")} for r in dv],
              "availability": {"bars": "closed 4H bars with close <= decision",
                               "dvol": "candle stamped T admitted at T+1h; stale beyond 6h = missing"},
              "sources": sources, "calendar_sha256": cal_sha,
              "fit": {"month": fit_doc["month"], "sha256": fit_sha}, "features": {}}
    docs, points = [], {}
    ref = keep[-1]["close"]
    for h in C.HOURS:
        start, end = C.window(CONTRACT, decision, h, prepared)
        row = C.decision_row(keep, releases, dv, h, start, end)
        if row is None:
            raise RuntimeError(f"{h}: too little history for features")
        vals = C.values(fit_doc["fits"][h], fit_doc["b0_resid_q"][h], row)
        points[h] = vals["B2"]["point"]
        bundle["features"][h] = {k: row[k] for k in (*R.MODEL_TERMS["B2"], "b0", "start_utc", "end_utc")}
        inside = [r for r in releases if start <= r < end]
        regime = ("releases inside the window: " + ", ".join(_iso(r) for r in inside)) if inside else \
            "no CPI/NFP/PPI/FOMC release inside the window (desk calendar)"
        if end > releases[-1]:
            regime += f"; calendar coverage ends {_iso(releases[-1])} - later releases unknown"
        docs.append({"h": h, "start": start, "end": end, "vals": vals, "regime": regime})
    bsha = _sha(bundle)
    viol = C.coherence_violations(points)
    out = []
    for d in docs:
        v = d["vals"]
        note = (f"Contract {C.contract_id(CONTRACT)}: point = OLS fit value (loss-bearing); q10/q50/q90 = point + fit "
                f"residual quantiles. Decision {_iso(decision)} (inputs cut there); window starts "
                f"{int((d['start'] - decision).total_seconds() // 60)} min later; calendar terms describe the window. "
                f"Model {R.VERSION} (spec {FROZEN_SPEC[:12]}), fit {fit_doc['month']} sha256 {fit_sha[:12]}, job {JOB_VERSION}. "
                f"Status: {STATUS}. Coherence diagnostic (not applied): {', '.join(viol) or 'none'}. "
                f"Ref close {ref}; point range ~{ref * (math.exp(math.exp(v['B2']['point'])) - 1):.0f} pts over the full window. "
                f"Not a direction, not a probability, not a remaining-range forecast once the window has started.")
        out.append({
            "id": f"{ID_PREFIX}{d['h']}-{decision:%Y%m%dT%H%MZ}", "code_version": f"{R.VERSION} / {C.VERSION} / {JOB_VERSION}",
            "contract": C.contract_id(CONTRACT), "decision_utc": _iso(decision), "input_bundle": bsha, "snapshot_hash": bsha,
            "instrument": "BTCUSDT perp, Binance last price", "reference_price": ref,
            "start_utc": _iso(d["start"]), "horizon_utc": _iso(d["end"]), "made_utc": _iso(prepared), "package": PACKAGE,
            "event_regime": d["regime"][:2000], "note": note[:2000],
            "events": [C.event(f"B2 range model {R.VERSION}", v["B2"]), C.event("B0 persistence baseline", v["B0"])],
        })
    return bundle, bsha, out


def _raw(doc) -> bytes:
    return json.dumps(doc, sort_keys=True, separators=(",", ":")).encode() + b"\n"


def reconcile(base, now_ms, run):
    """Roll forward sources of registered range forecasts; mark frozen attempts whose window started without a
    publication confirmation as unconfirmed (ineligible). Never backdates, never re-times a window."""
    from registration import restore_sources
    from storage import read_json
    manifest = read_json(Path(base) / "state/forecast_manifest.json", {})
    mine = [fid for fid, e in manifest.items() if fid.startswith(ID_PREFIX)]
    if mine:
        fixed = restore_sources(base, mine)
        if fixed:
            print(f"reconcile: restored sources {fixed}")
    pubs = {r["attempt"] for r in _rows(base, PUBLICATIONS)}
    latest = {}
    for r in _rows(base, ATTEMPTS):
        latest[r["attempt"]] = r
    for att, r in latest.items():
        if r["state"] == "frozen" and att not in pubs and r.get("start_ms") and now_ms >= r["start_ms"]:
            record(base, att, r["decision_utc"], "unconfirmed", run, now_ms, ids=r.get("ids"), start_ms=r["start_ms"],
                   reason="window started without a recorded publication confirmation; ineligible")


def forecast(now=None, base=BASE, bars=None, dvol=None, clock=None, run=None, hooks=None, dvol_state="ok",
             dvol_report=None, sources=None, opener=None):
    """One attempt for the last closed 4H decision. Returns (state, ids). Every outcome is logged."""
    from registration import register_batch
    from storage import read_json
    now = now or _now()
    clock = clock or (lambda: int(time.time() * 1000))
    run = run or run_meta()
    if not spec_ok():
        raise SystemExit("forecast refused: range_model.py does not match the frozen specification")
    reconcile(base, clock(), run)
    decision_guess = _iso(last_boundary(now))
    attempt = f"{decision_guess}#{run.get('run_id') or clock()}"
    try:
        if bars is None:
            bars, bmeta = fetch_recent_bars(now, opener=opener)
            sources = dict(sources or {}, bars=bmeta)
        if dvol is None:
            dvol_state, dvol, dmeta = fetch_recent_dvol(now, opener=opener)
            dvol_report = dmeta
            sources = dict(sources or {}, dvol=dmeta)
    except Exception as exc:
        record(base, attempt, decision_guess, "failed", run, clock(), reason=f"input retrieval: {type(exc).__name__}: {exc}"[:300])
        raise
    decision = R._t(bars[-1]["close_utc"])
    dstr = _iso(decision)
    attempt = f"{dstr}#{run.get('run_id') or clock()}"
    manifest = read_json(Path(base) / "state/forecast_manifest.json", {})
    ids = [f"{ID_PREFIX}{h}-{decision:%Y%m%dT%H%MZ}" for h in C.HOURS]
    if all(i in manifest for i in ids):
        from registration import restore_sources
        restore_sources(base, ids)
        print(f"forecast: {dstr} already registered ({', '.join(ids)}); verified against the manifest")
        return "existing", ids
    prior = [r for r in attempts_for(base, dstr) if r.get("start_ms")]
    if prior or any(i in manifest for i in ids):
        raise AttemptRefused(f"{dstr}: an earlier attempt recorded a window ({prior[-1]['state'] if prior else 'partial manifest'}); "
                             "not retried - a retry would move the window")
    age_h = (now - decision).total_seconds() / 3600
    if not 0 <= age_h <= MAX_DECISION_AGE_H:
        record(base, attempt, dstr, "skipped", run, clock(), reason=f"stale decision ({age_h:.2f}h > {MAX_DECISION_AGE_H}h)")
        raise StaleDecision(f"decision close {dstr} is {age_h:.2f}h from now; not forecasting a stale bar")
    try:
        fit_doc, fit_sha = load_fit(base, dt.datetime(decision.year, decision.month, 1, tzinfo=UTC))
        admit = C.admit_dvol(dvol_state, dvol, decision, dvol_report or {}, "live")
        prepared = C.from_ms(clock()).replace(microsecond=0)
        bundle, bsha, docs = build(bars, dvol, fit_doc, fit_sha, prepared,
                                   dict(sources or {}, dvol_admissibility=admit))
    except Exception as exc:
        record(base, attempt, dstr, "failed", run, clock(), reason=f"{type(exc).__name__}: {exc}"[:300])
        raise
    start_ms = min(_ms(R._t(d["start_utc"])) for d in docs)
    window = {"ids": ids, "start_ms": start_ms, "bundle": bsha}
    frozen_at = clock()
    if start_ms - frozen_at < C.MIN_MARGIN_S * 1000:
        record(base, attempt, dstr, "abandoned", run, frozen_at, reason="clock reached the freezing margin before the window start", **window)
        raise RuntimeError(f"{dstr}: freezing at {frozen_at} leaves < {C.MIN_MARGIN_S}s before the window start; abandoned")
    write_blob(base, f"{INPUTS}/{decision:%Y-%m}", bundle)
    record(base, attempt, dstr, "prepared", run, frozen_at, **window)
    items = [(f"registry/{d['id']}.json", _raw(d)) for d in docs]
    meta = {"attempt": attempt, "contract": C.contract_id(CONTRACT), "code_commit": run.get("code_commit"),
            "prepared": _ms(prepared), "publication": f"see {PUBLICATIONS}"}
    try:
        register_batch(base, items, frozen_at, meta, hooks=hooks)
    except Exception as exc:
        after = read_json(Path(base) / "state/forecast_manifest.json", {})
        if all(i in after and after[i].get("attempt") == attempt for i in ids):
            from registration import restore_sources
            restore_sources(base, ids)                  # commit point passed: roll forward
            print(f"forecast: registered despite a post-commit error ({exc}); sources restored")
        else:
            record(base, attempt, dstr, "failed", run, clock(), reason=f"registration: {type(exc).__name__}: {exc}"[:300], **window)
            raise
    record(base, attempt, dstr, "frozen", run, frozen_at, **window)
    return "frozen", ids


def _remote_manifest(branch="main"):
    subprocess.run(["git", "fetch", "--quiet", "origin", branch], check=True, timeout=60)
    commit = subprocess.run(["git", "rev-parse", f"origin/{branch}"], check=True, capture_output=True, text=True).stdout.strip()
    raw = subprocess.run(["git", "show", f"origin/{branch}:state/forecast_manifest.json"], check=True,
                         capture_output=True, text=True).stdout
    return commit, json.loads(raw)


def confirm(base=BASE, clock=None, remote=None, run=None):
    """Record remote confirmation for frozen attempts not yet confirmed. Returns the rows written."""
    from storage import read_json
    clock = clock or (lambda: int(time.time() * 1000))
    run = run or run_meta()
    remote = remote or _remote_manifest
    pubs = {r["attempt"] for r in _rows(base, PUBLICATIONS)}
    latest = {}
    for r in _rows(base, ATTEMPTS):
        latest[r["attempt"]] = r
    pending = [r for a, r in latest.items() if r["state"] == "frozen" and a not in pubs]
    if not pending:
        print("confirm: nothing pending")
        return []
    local = read_json(Path(base) / "state/forecast_manifest.json", {})
    commit, remote_manifest = remote()
    t = clock()
    out = []
    for r in pending:
        ok = all(i in remote_manifest and remote_manifest[i]["sha256"] == local[i]["sha256"] for i in r["ids"])
        if not ok:
            print(f"confirm: {r['attempt']} not on the remote yet")
            continue
        row = {"attempt": r["attempt"], "ids": r["ids"], "commit": commit, "confirmed": t, "start_ms": r["start_ms"],
               "eligible": t < r["start_ms"], "method": "git fetch origin; manifest entries and hashes match",
               "run": run}
        _append(base, PUBLICATIONS, row)
        record(base, r["attempt"], r["decision_utc"], "published" if row["eligible"] else "published-late", run, t,
               ids=r["ids"], start_ms=r["start_ms"], commit=commit)
        out.append(row)
    return out


# --------------------------------------------------------------------------------------------
# Replay (offline)
# --------------------------------------------------------------------------------------------
def replay(fid, base=BASE):
    """Rebuild a registered RC1D forecast from its retained bundle, fit and calendar; compare with frozen bytes."""
    from storage import read_json
    entry = read_json(Path(base) / "state/forecast_manifest.json", {})[fid]
    frozen = json.loads((Path(base) / entry["frozen"]).read_bytes())
    bsha = frozen["input_bundle"]
    decision = R._t(frozen["decision_utc"])
    path = Path(base) / INPUTS / f"{decision:%Y-%m}" / f"{bsha}.json.gz"
    if not path.exists():
        raise FileNotFoundError(f"input bundle {bsha[:12]} missing - forecast cannot be replayed")
    got, bundle = read_blob(path)
    if got != bsha:
        raise ValueError(f"input bundle altered: {got[:12]} != {bsha[:12]}")
    fit_doc, fit_sha = load_fit(base, dt.datetime(decision.year, decision.month, 1, tzinfo=UTC))
    if fit_sha != bundle["fit"]["sha256"]:
        raise ValueError("fit file changed since the forecast")
    if hashlib.sha256(CALENDAR.read_bytes()).hexdigest() != bundle["calendar_sha256"]:
        raise ValueError("calendar changed since the forecast")
    bars = [dict(b) for b in bundle["bars"]]
    _, sha2, docs = build(bars, bundle["dvol"], fit_doc, fit_sha, R._t(bundle["prepared_utc"]), bundle["sources"])
    if sha2 != bsha:
        raise ValueError("rebuilt bundle differs from the retained bundle")
    mine = next(d for d in docs if d["id"] == fid)
    if mine["events"] != frozen["events"] or mine["start_utc"] != frozen["start_utc"]:
        raise ValueError("replay does not reproduce the registered events")
    return mine


# --------------------------------------------------------------------------------------------
# Status surface
# --------------------------------------------------------------------------------------------
def status(base=BASE, now=None, out_json="reports/range_status.json", out_md="reports/range.md"):
    import range_reader as RR
    now = now or _now()
    st = RR.status(base, now)
    target = Path(base) / out_json
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(st, indent=1, sort_keys=True) + "\n")
    (Path(base) / out_md).write_text(RR.markdown(st))
    print(f"status: {st['outcomes']} -> {out_json}")
    return st


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "refit":
        refit()
    elif cmd == "forecast":
        try:
            forecast()
        except StaleDecision as exc:
            print(f"forecast skipped: {exc}")
            if os.environ.get("GITHUB_EVENT_NAME") == "schedule":
                raise SystemExit(1)
        except AttemptRefused as exc:
            print(f"forecast refused: {exc}")
    elif cmd == "confirm":
        confirm()
    elif cmd == "status":
        status()
    elif cmd == "replay":
        print(json.dumps(replay(sys.argv[2]), indent=1))
    else:
        raise SystemExit("usage: range_job.py refit|forecast|confirm|status|replay <id>")
