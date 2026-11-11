#!/usr/bin/env python3
"""Component readiness records (readiness-1.0.0, repo 2.30; states updated after the merges in 2.30.1; brief section 17).

    python3 scripts/readiness.py write    # (re)write research/readiness/<id>.json and docs/READINESS.md
    python3 scripts/readiness.py check    # identities current, vocabulary and evidence rules hold

One small record per component: code identity (path, version, sha256 computed from the file), and per state -
implemented, tested, pushed, merged, installed, deployed, observed, registered, prepared, blocked, pending - a value and
the evidence for it. Rules the checker enforces:
  - a test is evidence only for 'tested'; installed, deployed and observed need operational evidence (a workflow run,
    a scheduler record, an installation, an observation) and merged needs a merge commit;
  - 'registered' needs effective evidence (a first-main record or a registry receipt);
  - a record's code sha256 must match the file now (a stale record fails the check).
The dashboard (scripts/build_dashboard.py developments.readiness) displays these records as recorded; it never infers
a state. The closure table for a release is generated from them (docs/READINESS.md).
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/readiness"
STATES = ("implemented", "tested", "pushed", "merged", "installed", "deployed", "observed", "registered", "prepared",
          "blocked", "pending")
OPERATIONAL = ("workflow-run", "scheduler", "installation", "observation")
KINDS = {"implemented": ("commit",), "tested": ("test",), "pushed": ("branch", "pull-request"),
         "merged": ("merge-commit",), "installed": ("installation",), "deployed": OPERATIONAL,
         "observed": ("observation", "workflow-run"), "registered": ("first-main", "registry-receipt"),
         "prepared": ("file",), "blocked": ("decision", "dependency"), "pending": ("decision", "dependency", "file")}
AS_OF = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
BRANCH = {"kind": "branch", "ref": "repo-2.30-integration-hardening"}
MERGED = [{"kind": "merge-commit", "ref": "d26ab329 PR #48 merged 2026-10-20T12:14:00Z"}]


def _t(ref):
    return {"kind": "test", "ref": ref}


def _f(ref):
    return {"kind": "file", "ref": ref}


# id: (title, code path, version string, states {state: (value, [evidence])}, blockers)
COMPONENTS = {
    "persistence-retry": ("Collector persistence retry (20A; shallow fetch 2.30.5)", "scripts/commit_push.sh", "repo 2.30.5",
                          {"implemented": True, "tested": [_t("regression/test_rev230_persistence.py"), _t("regression/test_rev2305_persistence.py")],
                           "pushed": [{"kind": "pull-request", "ref": "#59"}],
                           "merged": [{"kind": "merge-commit", "ref": "cc299cec PR #59 merged 2026-10-28T23:29:09Z"}],
                           "deployed": [{"kind": "workflow-run", "ref": "every writer since cc299cec runs this script from main"}],
                           "observed": [{"kind": "workflow-run", "ref": "43053116320 (range, 2026-11-11T15:55Z): push rejected after the PR #64 merge moved main; bounded fetch ok tip=122aee25; rebase ok; push attempt 2 confirmed after 8 s"},
                                        {"kind": "workflow-run", "ref": "43070718492 (collector, 2026-11-11T17:42Z): push rejected after the PR #66 merge moved main; bounded fetch ok tip=6b84c10e; rebase ok; push attempt 2 confirmed after 14 s"}]},
                          []),
    "range-source-readiness": ("Daily range-source readiness and registry-driven repairs", "range_source_repair.py", "repo 2.30.8",
                               {"implemented": True, "tested": [_t("regression/test_research_repairs.py")],
                                "pushed": [{"kind": "pull-request", "ref": "#64"}],
                                "merged": [{"kind": "merge-commit", "ref": "122aee25 PR #64 merged 2026-11-11T15:55:43Z"}],
                                "deployed": [{"kind": "workflow-run", "ref": "43055968133 (range, 2026-11-11T16:12Z, main 6e9e3ba0): refit entry point returned fit-valid; forecast confirmed 16:20:51Z"}],
                                "observed": [{"kind": "workflow-run", "ref": "43051257211 (readiness, manual on the PR branch, 2026-11-11T15:44Z): ready, Nov 1-10, 10 daily files ok"}]},
                               ["first scheduled readiness run on main (22:37 UTC daily) not yet read when this record was written",
                                "range-repair-capture.yml has never captured a real gap (none exists); against the live archive it refused the October gap, which the provider has since filled",
                                "a repair cannot be captured before the provider publishes the gap month's monthly archive (about 33.5 h after month end for October 2026)"]),
    "health-monitors": ("Health monitors: native schedule as secondary trigger, timer token, malformed lines", "health.py", "health-1.5.0 (repo 2.30.9)",
                        {"implemented": True, "tested": [_t("regression/test_health.py"), _t("regression/test_recovery.py"), _t("regression/test_rev227.py")],
                         "pushed": [{"kind": "pull-request", "ref": "#65"}],
                         "merged": [{"kind": "merge-commit", "ref": "6e9e3ba0 PR #65 merged 2026-11-11T16:09:16Z"}],
                         "deployed": [{"kind": "workflow-run", "ref": "43055963854 (collector, 2026-11-11T16:12Z): Record operational health succeeded on health-1.5.0"}],
                         "observed": [{"kind": "observation", "ref": "state/incidents.jsonl: native_schedule_day rows for 2026-11-08, -09 and -10 recorded 2026-11-11T16:15:12Z; reports/health.md carries the token and integrity lines"},
                                      {"kind": "workflow-run", "ref": "43080336496 (watchdog, schedule, 2026-11-11T18:42Z): external timer arriving, 12 of 12 opportunities on time in 3 h; one line for 4 recovered native silences"}]},
                        ["the watchdog starts on the native schedule: one start between 10:59Z and 18:42Z on 2026-11-11 (463 minutes), so a silent external timer is reported only when it next starts; the operator declined an independent alert",
                         "token.expires_utc in docs/acceptance/timer.json is unrecorded until the operator fills it"]),
    "lab-parking": ("Parked lab designs and research identity guards", "scripts/lab_designs.py", "repo 2.30.10",
                    {"implemented": True, "tested": [_t("regression/test_lab_parking.py"), _t("regression/test_identity_guard.py")],
                     "pushed": [{"kind": "pull-request", "ref": "#66"}],
                     "merged": [{"kind": "merge-commit", "ref": "6b84c10e PR #66 merged 2026-11-11T17:43:58Z"}],
                     "deployed": [{"kind": "workflow-run", "ref": "43090780786 (research lab, schedule, 2026-11-11T19:49Z): five active designs, compute job 4 m 47 s, persist success"}],
                     "observed": [{"kind": "workflow-run", "ref": "43090780786: run 6.2 minutes end to end against 33-53 minutes for the previous five runs"}]},
                    ["how a parked design's hourly control selection treats the parked interval if it is unparked: not established",
                     "the weekly report's issue-closing step has not run (next report Monday 00:30 UTC)"]),
    "recovery-39333253907": ("Failed-run recovery (20B)", "scripts/restore_failed_run.py",
                             "restore-1.0.0 (recovery branch recovery-39333253907)", {"implemented": True, "pushed": [{"kind": "pull-request", "ref": "#47"}],
                                               "merged": [{"kind": "merge-commit", "ref": "ad3f3d81 PR #47 merged 2026-10-20T12:13:44Z"}]},
                             []),
    "panel": ("Continuous feature panel (F2)", "research_tools/panel.py", "panel-1.1.0",
              {"implemented": True, "tested": [_t("regression/test_rev230.py::F2PanelFreshnessTests")], "pushed": [BRANCH],
               "merged": MERGED}, []),
    "research-api": ("Research interface (F3, 16)", "research_tools/research_api.py", "research-api-1.1.0",
                     {"implemented": True, "tested": [_t("regression/test_rev230.py::F3ResearchAPITests")],
                      "pushed": [BRANCH], "merged": MERGED}, []),
    "search-ledger": ("Search ledger (F6)", "research_tools/search_ledger.py", "search-ledger-1.1.0",
                      {"implemented": True, "tested": [_t("regression/test_rev230.py::F6LedgerTests")], "pushed": [BRANCH],
                       "merged": MERGED}, []),
    "evaluator-service": ("Evaluator boundary (F6)", "research_tools/evaluator_service.py", "evaluator-service-1.0.0",
                          {"implemented": True, "tested": [_t("regression/test_rev230.py::F6LedgerTests (OS-user case runs only as root)")],
                           "pushed": [BRANCH], "merged": MERGED, "deployed": False},
                          ["no host runs the service as a separate OS user; in CI and single-user checkouts the boundary is a convention"]),
    "dir1": ("DIR1 guarded runner (F4, F5, 15)", "research_tools/dir1_runner.py", "dir1-runner-1.0.0",
             {"implemented": True, "tested": [_t("regression/test_rev230.py::F4RunnerTests"),
                                              _t("regression/test_rev230.py::F5ComparisonTests")],
              "pushed": [BRANCH], "merged": MERGED, "prepared": [_f("research/registrations/dir1-prepared/protocol.json")],
              "registered": False, "deployed": False},
             ["frontier arm uncommissioned (no model account, identity or transport)",
              "statistical artifact not trained/frozen; no publication workflow; 4-hour horizon awaits measured latency"]),
    "pilot-acceptance": ("E1 pilot acceptance (F7)", "stream/pilot_acceptance.py", "pilot-acceptance-1.1.0",
                         {"implemented": True, "tested": [_t("regression/test_rev230.py::F7PilotAcceptanceTests")],
                          "pushed": [BRANCH], "merged": MERGED, "prepared": [_f("stream/pilot_e1.json")], "deployed": False},
                         ["E1 recorder uncommissioned: standing no-host decision"]),
    "archive-store": ("Raw archive (F9)", "research_tools/archive_store.py", "archive-store-1.1.0",
                      {"implemented": True, "tested": [_t("regression/test_rev230.py::F9ArchiveTests")], "pushed": [BRANCH],
                       "merged": MERGED, "deployed": False},
                      ["not wired into the collector; needs a storage budget and an operator-provided bucket"]),
    "o33-v3.1": ("O33 v3.1 effective record (F8)", "research/registrations/o33-v3.1/effective.json", "o33-effective/1",
                 {"implemented": True, "registered": [{"kind": "first-main", "ref": "1864d3d9 pr_merge 2026-10-19T19:51:07Z"}],
                  "pushed": [BRANCH], "merged": MERGED}, []),
    "o33-correction-1": ("O33 v3.1 correction 1 (F8)", "research/registrations/o33-v3.1-correction-1/enforcement/desk_register.py",
                         "register-2.4.0", {"implemented": True, "tested": [_t("regression/test_rev230.py::F8O33Tests")],
                                            "pushed": [BRANCH], "merged": MERGED,
                                            "registered": [{"kind": "first-main", "ref": "d26ab329 pr_merge 2026-10-20T12:14:00Z (effective.json)"}]},
                         []),
    "calibration": ("DIR1 evaluator calibration (13)", "research_tools/calibration_harness.py", "calibration-harness-1.0.0",
                    {"implemented": True, "tested": [_t("research/calibration/dir1-primary-v1/attempts.jsonl (seed 33, pass)")],
                     "pushed": [BRANCH], "merged": MERGED},
                    ["one simulated world; a pass is necessary, not sufficient, for promotion"]),
    "options-skew": ("Options skew feasibility (14)", "research_tools/options_skew.py", "options-skew-0.1.0",
                     {"implemented": True, "tested": [_t("regression/test_rev230.py::Section14Tests")], "pushed": [BRANCH],
                      "merged": MERGED, "registered": False},
                     ["filters not registered; panel keeps options_disagreement gated"]),
    "replenishment": ("Replenishment contract (14)", "research_tools/replenishment.py", "replenishment-0.1.0",
                      {"implemented": True, "tested": [_t("regression/test_rev230.py::Section14Tests")], "pushed": [BRANCH],
                       "merged": MERGED}, ["needs sequence-valid books from the uncommissioned E1 recorder"]),
    "a2": ("A2 synchronized flow (15)", "research_tools/a2_sync.py", "a2-sync-0.1.0",
           {"implemented": True, "tested": [_t("regression/test_rev230.py::Section15Tests")], "pushed": [BRANCH],
            "merged": MERGED, "prepared": [_f("research/registrations/a2-synchronized-prepared/protocol.json")],
            "registered": False}, ["no registration decision"]),
    "ps1-t1": ("PS1-T1 turnover control (15)", "research_tools/ps1_t1_runner.py", "ps1-t1-runner-1.0.0",
               {"implemented": True, "tested": [_t("regression/test_rev230.py::Section15Tests")], "pushed": [BRANCH],
                "merged": MERGED, "prepared": [_f("research/registrations/ps1-t1-prepared/protocol.json")],
                "registered": False, "blocked": [{"kind": "decision", "ref": "primary band (design_issue)"}]},
               ["operator decision on the primary band: band 0.05 is PS1 v3's own configuration"]),
}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def _head():
    import subprocess
    try:
        return subprocess.check_output(["git", "rev-parse", "--short=12", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


HEAD = _head()


def record(cid):
    title, path, version, states, blockers = COMPONENTS[cid]
    st = {}
    for s in STATES:
        v = states.get(s)
        if isinstance(v, list):
            st[s] = {"value": True, "evidence": v}
        elif v is True:
            st[s] = {"value": True, "evidence": [{"kind": "commit", "ref": f"at or before {HEAD}"}] if s == "implemented" else []}
        elif v is False:
            st[s] = {"value": False, "evidence": []}
    return {"schema": "component-readiness/1", "id": cid, "title": title, "as_of_utc": AS_OF,
            "code": {"path": path, "version": version, "sha256": sha(path)}, "states": st, "blockers": blockers,
            "generator": "scripts/readiness.py readiness-1.0.0"}


def problems(rec):
    out = []
    for s, v in rec["states"].items():
        if s not in STATES:
            out.append(f"{rec['id']}: unknown state {s}")
            continue
        if v["value"]:
            if not v["evidence"]:
                out.append(f"{rec['id']}: {s} true without evidence")
            for e in v["evidence"]:
                if e["kind"] not in KINDS[s]:
                    out.append(f"{rec['id']}: {e['kind']} evidence cannot establish {s}")
    if (ROOT / rec["code"]["path"]).exists() and sha(rec["code"]["path"]) != rec["code"]["sha256"]:
        out.append(f"{rec['id']}: code identity stale ({rec['code']['path']} changed)")
    return out


def markdown(recs):
    cols = ("implemented", "tested", "pushed", "merged", "deployed", "observed", "registered")
    lines = ["# Component readiness (generated by scripts/readiness.py; do not edit)", "",
             f"As of {AS_OF}. A state is shown only with its evidence; a unit test establishes 'tested', nothing more.", "",
             "| component | version | " + " | ".join(cols) + " | blockers |", "|---|---|" + "---|" * len(cols) + "---|"]
    for r in recs:
        cells = []
        for c in cols:
            v = r["states"].get(c)
            cells.append("yes" if v and v["value"] else ("no" if v else "-"))
        lines.append(f"| {r['title']} | {r['code']['version']} | " + " | ".join(cells) + f" | {'; '.join(r['blockers']) or '-'} |")
    return "\n".join(lines) + "\n"


def main(argv):
    if argv[1:] == ["write"]:
        DIR.mkdir(parents=True, exist_ok=True)
        recs = [record(c) for c in COMPONENTS]
        for r in recs:
            (DIR / f"{r['id']}.json").write_text(json.dumps(r, indent=1, sort_keys=True) + "\n")
        (ROOT / "docs/READINESS.md").write_text(markdown(recs))
        print(f"written {len(recs)} records")
        return 0
    probs = []
    for p in sorted(DIR.glob("*.json")):
        probs += problems(json.loads(p.read_text()))
    print("OK" if not probs else "\n".join(probs))
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
