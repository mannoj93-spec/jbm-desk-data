"""Research lab entry point (lab-2.1; publication gate 2.12).

  python -m lab.run update                       as-of replay over the collector's stored data
  python -m lab.run update --reconstruct-days 60 also an exploratory historical reconstruction
                                                 (public Binance 1-minute history for BTC perp/spot,
                                                 ETH, SOL; cached under LAB_CACHE, never committed)
  python -m lab.run update --no-write            compute and print; write nothing
  python -m lab.run update --now MS              reproduce a run at a past data cutoff (read-only
                                                 unless --write-past is also given)

Writes (unless --no-write), all under the evaluation-version namespace so older versions and the
legacy lab-1.0 outputs are never touched:
  research/v2/<design>/<version>/events|outcomes/YYYY-MM.jsonl  frozen decisions and labels
  research/v2/<design>/<version>/checkpoints.jsonl              completed checkpoint records (append-only)
  research/v2/<design>/<version>/controls/YYYY-MM.jsonl         frozen hourly control selections (B, C, F)
  research/v2/experiments/YYYY-MM.jsonl, research/v2/ledger/YYYY-MM.jsonl
  research/evidence/v2/<design>@<version>.json, research/evidence/index.json
  reports/research.md, reports/skill_proposals.md
  state/lab_registrations.json (registration clocks, never rewritten), state/lab_run_state.json
Budget: LAB_BUDGET seconds (default 900); a design not reached is reported as not run. A module
that raises is reported as an error; the others still run and are written.
Summary (stdout, and --summary PATH): schema lab_summary/2 - per design the evaluation version, the
cutoff, status, research-integrity validation (required / status / reasons) and the publication
decision (evidence.publication). scripts/merge_research.py refuses to publish outputs that do not
match it. A design whose required input integrity fails is blocked: nothing of its evaluation is
persisted, its watermark (state/lab_run_state.json) is not advanced, and the run exits 1.
Never places trades, registers forecasts, or edits skill files.
"""
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

from lab import controls, evidence, experiments
from lab.common import LAB_VERSION, ROOT, append, atomic_json, code_hash, iso, read_dir, read_json
from lab.data import Store, fetch_history, history_window

MODULES = {"flow_absorption": "lab.modules.flow_absorption", "account_behavior": "lab.modules.accounts",
           "liq_exposure": "lab.modules.liq_exposure", "twap_lifecycle": "lab.modules.twap",
           "liquidity_recovery": "lab.modules.liquidity", "options_disagreement": "lab.modules.options_disagreement",
           "cross_asset": "lab.modules.cross_asset", "deleveraging": "lab.modules.deleveraging"}
RECON_SERIES = ("binance_klines_1m_BTCUSDT_perp", "binance_klines_1m_BTCUSDT_spot",
                "binance_klines_1m_ETHUSDT_perp", "binance_klines_1m_SOLUSDT_perp")
INPUT_DIRS = ("data/prices", "data/snap", "data/series/binance_funding_settled", "data/options", "data/hl_accounts",
              "data/hl_enrich", "data/okx_insurance", "data/liq/orders", "state/hl_cohort_fixed_v2.json")
RUN_STATE = "state/lab_run_state.json"


class Lab:
    def __init__(self, base, now, write=True):
        self.base, self.now, self.write = Path(base), now, write
        self.store = Store(base, cutoff=now)
        self.code = code_hash()
        self.history, self.history_sha = {}, {}
        self.control_context = None


def input_hashes(base, cutoff_note):
    out = {}
    for rel in INPUT_DIRS:
        p = Path(base) / rel
        files = [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file()) if p.exists() else []
        h = hashlib.sha256()
        for f in files:
            h.update(f.relative_to(base).as_posix().encode() + b"\0" + f.read_bytes() + b"\0")
        out[rel] = {"files": len(files), "sha256": h.hexdigest() if files else None}
    out["_note"] = cutoff_note
    return out


def git_commit(base):
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=base, capture_output=True, text=True,
                              timeout=10).stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def data_cutoff(base, now):
    """Latest collector run observed by `now` (what the lab could read)."""
    runs = [r for p in sorted((Path(base) / "data/runs").glob("*.jsonl"))[-2:] for r in
            (json.loads(l) for l in p.read_text().splitlines() if l.strip())
            if r.get("observed_at") is not None and r["observed_at"] <= now]
    return max((r["observed_at"] for r in runs), default=None)


def family_variants(base, designs):
    """Variants ever tried per family: (version or legacy design hash, variant) pairs from both ledgers
    plus the current designs."""
    fam = {}
    for r in read_dir(base, "research/ledger"):                        # legacy lab-1.0
        fam.setdefault(r.get("family"), set()).add((r.get("design_sha256"), r.get("variant")))
    for r in read_dir(base, "research/v2/ledger"):
        fam.setdefault(r.get("family"), set()).add((r.get("version"), r.get("variant")))
    for d in designs:
        for v in d["variants"]:
            fam.setdefault(d["family"], set()).add((d["_version"], v["name"]))
    return {k: len(v) for k, v in fam.items()}


def family_variants_at(base, designs, registrations=None):
    """{family: f(t)} - the variant count of a family as of time t: (version or legacy design hash,
    variant) pairs recorded in either ledger at or before t, plus the variants of current design
    versions registered at or before t (a design's own current version is always registered before
    its checkpoint cutoffs). Ledgers and registrations are append-only, so the count at a past cutoff
    is reproducible."""
    rows = {}
    for r in read_dir(base, "research/ledger"):
        rows.setdefault(r.get("family"), []).append((r.get("t") or 0, (r.get("design_sha256"), r.get("variant"))))
    for r in read_dir(base, "research/v2/ledger"):
        rows.setdefault(r.get("family"), []).append((r.get("t") or 0, (r.get("version"), r.get("variant"))))
    for d in designs:
        reg = ((registrations or {}).get(d["id"]) or {}).get("registered") or 0
        rows.setdefault(d["family"], []).extend((reg, (d["_version"], v["name"])) for v in d["variants"])

    def at(fam):
        return lambda t: len({k for tt, k in rows.get(fam, []) if tt <= t})
    fams = set(rows)
    return {f: at(f) for f in fams}


def compact(result):
    rows = []
    for v in result.get("variants", []):
        rows.append({"name": v["name"], "passes": [
            {"basis": p["basis"], "state": p["state"], "firings": p["firings"], "episodes": p["episodes"],
             "freeze_audit": p.get("freeze_audit")} for p in v["passes"]]})
    return {"t": result["t"], "design": result["design"], "version": result.get("version"),
            "design_sha256": result.get("design_sha256"), "status": result["status"],
            "status_reason": result["status_reason"], "variants": rows, "lab_version": LAB_VERSION,
            "code_sha256": result.get("code_sha256"), "error": result.get("error"), "seconds": result.get("seconds")}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["update"])
    ap.add_argument("--base", default=str(ROOT))
    ap.add_argument("--reconstruct-days", type=int, default=0)
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--designs", default="", help="comma-separated design ids (default: all)")
    ap.add_argument("--now", type=int, default=None, help="data cutoff in ms (default: now)")
    ap.add_argument("--write-past", action="store_true", help="allow writing with --now (tests only)")
    ap.add_argument("--summary", default=None, help="also write the machine-readable summary to this path")
    a = ap.parse_args(argv)
    t0 = time.monotonic()
    budget = float(os.environ.get("LAB_BUDGET", 900))
    now = a.now or int(time.time() * 1000)
    write = not a.no_write and (a.now is None or a.write_past)
    lab = Lab(a.base, now, write=write)
    if a.reconstruct_days:
        start, end = history_window(a.reconstruct_days, now)
        for name in RECON_SERIES:
            try:
                lab.history[name], lab.history_sha[name] = fetch_history(name, start, end)
            except Exception as exc:
                print(f"history {name}: {type(exc).__name__}: {exc}", file=sys.stderr)
    designs = [experiments.attach_version(a.base, experiments.load_design(p)) for p in experiments.design_files(a.base)]
    if a.designs:
        designs = [d for d in designs if d["id"] in a.designs.split(",")]
    registrations = experiments.register(a.base, designs, now, write=write)
    run_state = read_json(Path(a.base) / RUN_STATE, {})
    commit = git_commit(a.base)
    cutoff = data_cutoff(a.base, now) or now
    hashes = input_hashes(a.base, f"cutoff {iso(now)}; records with observed_at after the cutoff are ignored")
    n_fam = family_variants(a.base, designs)
    n_fam_at = family_variants_at(a.base, designs, registrations)
    results, ledger, accounting = [], [], {}
    for d in designs:
        key = f"{d['id']}@{d['_version']}"
        if time.monotonic() - t0 > budget:
            results.append({"t": now, "design": d["id"], "version": d["_version"], "status": "not run",
                            "status_reason": f"lab budget {budget:.0f} s exhausted", "variants": [],
                            "code_sha256": lab.code})
            continue
        s0 = time.monotonic()
        try:
            mod = importlib.import_module(MODULES[d["module"]])
            # hourly control policy (lab/controls.py): frozen selections of this version, the previous
            # run's cutoff, and a list the module fills with this run's new selections
            lab.control_context = {"frozen": controls.load_selections(a.base, d), "design": d,
                                   "last_cutoff": (run_state.get(key) or {}).get("last_cutoff"), "new": []}
            captured, idx = [], None             # read-only view of the labels run_design computes
            orig_label_all = experiments.label_all

            def recording(*args, **kw):
                out = orig_label_all(*args, **kw)
                captured.append(out[0])
                return out
            experiments.label_all = recording
            try:
                res, led = experiments.run_design(lab, d, mod, registrations.get(d["id"]), n_fam.get(d["family"], 1),
                                                  run_state=run_state.get(key), variants_at=n_fam_at.get(d["family"]))
            finally:
                experiments.label_all = orig_label_all
                lab.control_context = None
            try:                                  # diagnostics only: a failure here never fails the design
                flat = [(v["name"], p["basis"]) for v in res["variants"] for p in v["passes"]]
                idx = flat.index((d["primary_variant"], "prospective"))
                accounting[key] = evidence.control_accounting(d, registrations.get(d["id"]), captured[idx], now)
            except Exception as exc:
                accounting[key] = {"by_horizon": None, "decision_timing": None,
                                   "error": f"{type(exc).__name__}: {exc}"}
            # research integrity (2.12): checked inside run_design before anything was persisted
            # (experiments.input_integrity); a blocked evaluation must not advance the watermark, so a
            # later valid run treats the same decisions as new rather than as late replays
            if (res.get("integrity") or {}).get("required"):
                accounting[key] = dict(accounting.get(key) or {}, integrity=res["integrity"])
            if write:
                nxt = experiments.next_run_state(run_state.get(key), now, res)
                if nxt is not None:
                    run_state[key] = nxt
        except Exception as exc:
            res, led = {"t": now, "design": d["id"], "version": d.get("_version"), "status": "error",
                        "status_reason": f"{type(exc).__name__}: {exc}", "variants": [], "code_sha256": lab.code,
                        "error": traceback.format_exc()[-1500:]}, []
        res["seconds"] = round(time.monotonic() - s0, 1)
        results.append(res)
        ledger.extend(led)
    cards = []
    for d, res in zip(designs, results):
        sup = experiments.superseded_versions(a.base, d["id"], d["_version"])
        if not res.get("variants"):
            c = dict(evidence.error_card(d, res, now), superseded_versions=sup)
        else:
            c = evidence.card(d, res, commit, hashes, registrations.get(d["id"]), sup,
                              accounting.get(f"{d['id']}@{d['_version']}"))
        # the one publication decision (evidence.publication) and the last valid result, so a
        # failed attempt is never presented as the current passing evaluation
        cards.append(evidence.with_attempt(c, evidence.previous_card(a.base, c)))
    meta = {"code_sha256": lab.code, "commit": commit, "cutoff": cutoff, "seconds": round(time.monotonic() - t0, 1)}
    if write:
        append(a.base, "research/v2/experiments", [dict(compact(r), t_event=r["t"]) for r in results],
               key=lambda r: (r["t"], r["design"], r.get("version")))
        append(a.base, "research/v2/ledger", [dict(r, t_event=r["t"]) for r in ledger],
               key=lambda r: (r["t"], r["design"], r["version"], r["variant"], r["basis"]))
        evidence.write_cards(a.base, cards, now)
        (Path(a.base) / "reports").mkdir(exist_ok=True)
        (Path(a.base) / "reports/research.md").write_text(evidence.report(cards, now, meta))
        (Path(a.base) / "reports/skill_proposals.md").write_text(evidence.skill_proposals(cards, now))
        atomic_json(Path(a.base) / RUN_STATE, run_state)
    summary = evidence.run_summary(results, cards, now, commit, write, meta)
    text = json.dumps(summary, indent=1)
    print(text)
    if a.summary:                       # the persist job's publication metadata (scripts/merge_research.py)
        Path(a.summary).write_text(text + "\n")
    failed = [r["design"] for r in results if r.get("integrity") is not None
              and not experiments.evaluation_allowed(r["integrity"])]
    if failed:
        print(f"RESEARCH INTEGRITY FAILURE: {', '.join(failed)} - evaluation blocked, nothing published as "
              "current evidence for it (see reports/research.md)", file=sys.stderr)
    return 1 if failed or any(r["status"] == "error" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
