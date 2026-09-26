#!/usr/bin/env python3
"""Write or check desk/release.json - the one place release identity lives (package 12.2, repo 2.17).

Identity only: package, commits, contract, module and artifact hashes, calendar, routing, stream start. Verified
deployment events live in desk/deployments.jsonl (append-only); live operational health in reports/range_status.json.
Every hash here is computed, never typed. `check` (run by test_release.py, the skill's check_package.py and
the workflow's test step) fails on any drift between the manifest and the modules beside it.
  python3 desk/make_release.py write [--deployment-json FILE]
  python3 desk/make_release.py check [DIR]      # DIR defaults to desk/; the skill passes its own folder
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARED = ("jbm_archive.py", "jbm_measure.py", "range_model.py", "range_contract.py", "range_reader.py", "range_ops.py")
REPO_ONLY = ("range_job.py", "retained.py", "range_monitor.py")
CALENDAR = "releases_2020_2026.csv"
FIELDS = ("package", "repo_revision", "base_commit", "audited_snapshot", "contract", "evaluated_contract", "model",
          "modules", "calendar", "artifacts", "registry_routing", "range_stream_start_utc", "deployment_log")
ARTIFACTS = ("research/o21/MANIFEST.json", "research/o21/reanalysis_12.0.json", "research/o21/reanalysis_12.0_rows.json.gz",
             "research/o21/holm_addendum_12.1.json")


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _version(path):
    """The string literal assigned to VERSION (or JOB_VERSION) at module level, parsed with ast: comments,
    spacing and quoting cannot leak into the recorded version (12.1 recorded an inline comment)."""
    import ast
    tree = ast.parse(Path(path).read_text())
    for key in ("VERSION", "JOB_VERSION"):
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == key for t in node.targets) \
                    and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                return node.value.value
    return None


def body(desk=HERE, previous=None):
    sys.path.insert(0, str(desk))
    import range_contract as C
    prev = previous or {}
    mods = {n: {"version": _version(desk / n), "sha256": _sha(desk / n), "shared_with_skill": True} for n in SHARED}
    mods.update({n: {"version": _version(desk / n), "sha256": _sha(desk / n), "shared_with_skill": False}
                 for n in REPO_ONLY if (desk / n).exists()})
    cal = desk / CALENDAR
    last = [x for x in cal.read_text().splitlines() if x and not x.startswith("#")][-1].split(",")[0]
    return {
        "package": "crypto-desk 12.2", "repo_revision": "2.17",
        "base_commit": "365ff99239733d26fb2609db79a5884c774dd5ef",
        "audited_snapshot": "03ab59957933e34c1f97dadbf56498fbe393d6c0 (package 12.1, repo 2.16; overnight production evidence)",
        "contract": C.contract_id("RC1D"), "evaluated_contract": C.contract_id("RC1"),
        "model": {"range_model": "range-11.1.0", "spec_sha256": _sha(desk / "range_model.py")},
        "modules": mods,
        "calendar": {"file": CALENDAR, "sha256": _sha(cal), "last_event_utc": last,
                     "versions": "every version a forecast used is retained as calendars/<sha256>.csv (replay resolves by hash)",
                     "vintages": "announcement times of schedule changes are not retained (see research/o21/reanalysis_12.0.json)"},
        "artifacts": {a: _sha(desk / a) for a in ARTIFACTS if (desk / a).exists()},
        "registry_routing": {
            "range stream (automatic)": "GitHub registry/, ids range-rc1d-{4h,24h,72h}-<decision>, desk/range_job.py; "
                                        "read through desk/range_reader.py or reports/range_status.json",
            "in-thread forecasts": "artifact registry https://claude.ai/artifact/8QyreLBMA2aT3BCkT6atkR",
            "legacy": "range-b2-* (repo 2.14, q50 contract, pre-12.0): scored as registered, never cited as current"},
        "range_stream_start_utc": "2026-09-26T04:00:00Z",
        "deployment_log": "desk/deployments.jsonl (append-only, verified events); operational health (changes every run, not release identity): reports/range_status.json, state/range_runs.jsonl, state/range_scoring.jsonl, range-monitor.yml",
    }


def write(extra=None):
    path = HERE / "release.json"
    prev = json.loads(path.read_text()) if path.exists() else {}
    if extra:
        prev.update(json.loads(Path(extra).read_text()))
    doc = body(previous=prev)
    doc["release_sha256"] = hashlib.sha256(json.dumps({k: doc[k] for k in FIELDS}, sort_keys=True).encode()).hexdigest()
    path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n")
    print(f"release.json written: {doc['release_sha256'][:12]}")


def check(folder=HERE) -> list:
    """Drift between release.json and the modules in `folder`. Empty list = consistent."""
    folder = Path(folder)
    doc = json.loads((folder / "release.json").read_text())
    problems = []
    for name, m in doc["modules"].items():
        if not m.get("shared_with_skill") and not (folder / name).exists():
            continue                                        # repo-only module, absent from the skill
        if not (folder / name).exists():
            problems.append(f"{name}: missing")
        elif _sha(folder / name) != m["sha256"]:
            problems.append(f"{name}: sha256 differs from release.json")
        elif _version(folder / name) != m["version"]:
            problems.append(f"{name}: version differs from release.json")
    cal = folder / CALENDAR if (folder / CALENDAR).exists() else folder / "data" / CALENDAR
    if not cal.exists():
        problems.append(f"{CALENDAR}: missing")
    elif _sha(cal) != doc["calendar"]["sha256"]:
        problems.append(f"{CALENDAR}: sha256 differs from release.json")
    if _sha(folder / "range_model.py") != doc["model"]["spec_sha256"]:
        problems.append("range_model.py is not the frozen specification")
    for rel, sha in (doc.get("artifacts") or {}).items():         # repository-only artifacts
        if (folder / "research").exists():
            if not (folder / rel).exists():
                problems.append(f"{rel}: missing")
            elif _sha(folder / rel) != sha:
                problems.append(f"{rel}: sha256 differs from release.json")
    for kept in sorted((folder / "calendars").glob("*.csv")) if (folder / "calendars").exists() else []:
        if _sha(kept) != kept.stem:
            problems.append(f"calendars/{kept.name}: content does not hash to its name")
    log = folder / "deployments.jsonl"
    if log.exists():
        for i, line in enumerate(log.read_text().splitlines(), 1):
            try:
                row = json.loads(line)
                assert isinstance(row, dict) and row.get("revision") and row.get("event")
            except (ValueError, AssertionError):
                problems.append(f"deployments.jsonl line {i}: not a revision/event object")
    want = hashlib.sha256(json.dumps({k: doc.get(k) for k in FIELDS}, sort_keys=True).encode()).hexdigest()
    if doc.get("release_sha256") != want:
        problems.append("release_sha256 does not match the manifest body")
    return problems


if __name__ == "__main__":
    if sys.argv[1] == "write":
        write(sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--deployment-json" else None)
    else:
        found = check(Path(sys.argv[2]) if len(sys.argv) > 2 else HERE)
        print("release check:", "OK" if not found else found)
        raise SystemExit(1 if found else 0)
