#!/usr/bin/env python3
"""Write or check desk/release.json - the one place release identity lives (package 12.0, repo 2.15).

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
SHARED = ("jbm_archive.py", "jbm_measure.py", "range_model.py", "range_contract.py", "range_reader.py")
REPO_ONLY = ("range_job.py",)
CALENDAR = "releases_2020_2026.csv"
FIELDS = ("package", "repo_revision", "base_commit", "audited_snapshot", "contract", "evaluated_contract", "model",
          "modules", "calendar", "registry_routing", "range_stream_start_utc", "deployment")


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _version(path):
    for line in Path(path).read_text().splitlines():
        s = line.strip()
        for key in ("VERSION = ", "JOB_VERSION = "):
            if s.startswith(key):
                return s.split("=", 1)[1].strip().strip('"')
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
        "package": "crypto-desk 12.0", "repo_revision": "2.15",
        "base_commit": "09549f89fee2158dae9516b64520529f23025085",
        "audited_snapshot": "0a9ba0e2eabbda73c6113723d05e447528650e74 (package 11.2, repo 2.14)",
        "contract": C.contract_id("RC1D"), "evaluated_contract": C.contract_id("RC1"),
        "model": {"range_model": "range-11.1.0", "spec_sha256": _sha(desk / "range_model.py")},
        "modules": mods,
        "calendar": {"file": CALENDAR, "sha256": _sha(cal), "last_event_utc": last,
                     "vintages": "not retained (actual release times; see research/o21/reanalysis_12.0.json)"},
        "registry_routing": {
            "range stream (automatic)": "GitHub registry/, ids range-rc1d-{4h,24h,72h}-<decision>, desk/range_job.py; "
                                        "read through desk/range_reader.py or reports/range_status.json",
            "in-thread forecasts": "artifact registry https://claude.ai/artifact/8QyreLBMA2aT3BCkT6atkR",
            "legacy": "range-b2-* (repo 2.14, q50 contract, pre-12.0): scored as registered, never cited as current"},
        "range_stream_start_utc": prev.get("range_stream_start_utc"),
        "deployment": prev.get("deployment") or {"state": "built and tested; not merged", "evidence": []},
    }


def write(extra=None):
    path = HERE / "release.json"
    prev = json.loads(path.read_text()) if path.exists() else {}
    if extra:
        prev.update(json.loads(Path(extra).read_text()))
    doc = body(previous=prev)
    doc["release_sha256"] = hashlib.sha256(json.dumps({k: doc[k] for k in FIELDS if k not in ("deployment", "range_stream_start_utc")},
                                                      sort_keys=True).encode()).hexdigest()
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
    if cal.exists() and _sha(cal) != doc["calendar"]["sha256"]:
        problems.append(f"{CALENDAR}: sha256 differs from release.json")
    if _sha(folder / "range_model.py") != doc["model"]["spec_sha256"]:
        problems.append("range_model.py is not the frozen specification")
    want = hashlib.sha256(json.dumps({k: doc[k] for k in FIELDS if k not in ("deployment", "range_stream_start_utc")},
                                     sort_keys=True).encode()).hexdigest()
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
