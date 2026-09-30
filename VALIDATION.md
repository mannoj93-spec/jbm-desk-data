# Validation record — maintenance, revision 2.19 (crypto-desk 12.4)

Validated 2026-09-30 17:00–17:30Z on branch `desk-maint-2-19` from `main` at `a1341401` (container; Python 3.11.15 and 3.12.11). Earlier blocks below are kept as recorded.

| Check (2.19) | Result |
|---|---|
| Baseline evidence (GitHub API, check-run annotations, git) | Since the 2.18 merge: 13 scheduled `range.yml` runs, one failure (36520641829, Sep 29 04:13Z, preflight `test_pinned_bytes_detect_revision`), 08:00Z recovered (36541614717). `range-score.yml` 52 runs, all succeeded. `range-monitor.yml` 13 runs: red 05:58Z–18:00Z Sep 29 on the failed decision, otherwise green. Registry: 78 RC1D forecasts, 54 scores |
| Reproductions | (1) The 2.18 archive test fails when the clock crosses a 2-second boundary between two builds of the same fixture; 2.19 passes. (2) The documented skill loop exits 0 after an early failing file (repro in `TestStartupRunner`); `check_package.py` exits nonzero. (3) `make_release._generation_identity` on the 2.18 `range_job.py` reports the typed package. (4) The audit's evidence figures at `12575d3` are reproduced exactly by `range_reader.evaluation` |
| Regression suite (`python -m unittest discover -s regression`, includes every desk suite) | 559 run, 0 failed, 1 skipped on 3.11.15 and 3.12.11. The skip is `TestStartupRunner`, which needs the skill's `check_package.py` and runs in the package |
| Desk suites directly | measure 40, archive 51, range model 18, contract 10, range job 26, hardening 18, release 7 (1 skip), as-of 21, ops 29, verify 7 — both Pythons |
| Focused | archive determinism test and the pin test, 40 consecutive runs, 0 failures |
| Fixtures, release, checksums | `test_fixtures.py` all pass; `make_release.py check` OK; `SHA256SUMS` verifies (166 files) |
| O21 verify gate | PASS on 3.11 (max difference 0.0) and 3.12 (rows 1.0e-12) |
| Production records | All 78 RC1D forecasts pass hash, strict validation and replay. All 54 scores re-verify from evidence, with no duplicate keys. No file under `registry/`, `state/` or `reports/` changed |
| Skill package 12.4 | `check_package.py` PASS: 7 files, executed 173, failed 0, errors 0, skipped 42 (repository-only classes) |
| Not observed | CI on the PR; any 2.19 run after merge. October rollover: the first October fit at the Oct 1 00:02Z run is pending |

# Validation record — maintenance, revision 2.18 (crypto-desk 12.3)

Validated 2026-09-28 ~13:00–14:00Z on branch `desk-maint-2-18` from `main` at `0215ee17` (container; Python 3.11.15
and 3.12.11). Earlier blocks below are kept as recorded.

| Check (2.18) | Result |
|---|---|
| Baseline evidence (GitHub API, git, ~13:10Z) | Range forecasts: every scheduled run from Sep 26 16:00Z to Sep 28 12:00Z succeeded (13 runs); 12:00Z Sep 26 (run 36241307098) the only failure, not back-filled. Hourly scoring: scheduled runs succeeding every hour. Monitor: runs 36260779081 … 36353516254 (8) failed; 36367972798 (Sep 28 01:57Z), 36384226557 (05:58Z), 36407004774 (10:00Z) succeeded, all scheduled, no manual run. Registry: 42 RC1D forecasts; scores 4h 13, 24h 8, 72h 0 |
| Reproduction: preflight time bomb | Real scorer run on a disposable copy of `main` at Sep 29 05:00Z (synthetic bars): the 2.17 `TestLiveRecords` fails; the 2.18 `TestLiveRecords` and `TestScoringStates` pass on the same state |
| Reproduction: status clock | 2.17 code on the fixture, clock fixed at 08:15:21.900Z (08:00Z batch confirmed 08:15:21.137Z): status `generated_utc` 08:15:21Z, current 4h = the 04:00Z batch. 2.18: `generated_utc` 08:15:21.900Z, current = the 08:00Z batch |
| Reproduction: monitor | monitor-12.2.1 with the latest 4h frozen file corrupted (status `integrity-failed`): no problems; with a fresh-stamped status carrying an expired current state: no current-state problem. monitor-12.3.0: both alert |
| Regression suite (`python -m unittest discover -s regression`, includes every desk suite) | 551 passed, 0 skipped, on 3.11.15 and 3.12.11 (536 before; +15: hardening 1, as-of 4, ops 10) |
| Desk suites run directly | measure 40, archive 50, range model 18, contract 10, range job 26, hardening 18, release 3, as-of 21, ops 26, verify 7 — all OK, 0 skipped, both Pythons |
| Fixtures / release / checksums | `test_fixtures.py` all pass (both); `make_release.py check` OK (release `9be41659…`); `SHA256SUMS` 166 files verify |
| O21 verify gate | PASS on 3.11.15 (max difference 0.0) and 3.12.11 (rows max 1.0e-12) |
| Production records | All 42 RC1D forecasts: hash, strict validation and replay OK; all 21 RC1D scores: evidence hash and forecast reference re-verified; no duplicate score keys. No file under `registry/`, `state/` or `reports/` changed |
| Unchanged | Contract ids (`RC1D/contract-12.0.0/175a4dd4c6c0`), model spec, September fit, calendars, frozen bytes, scores, evidence, lab evaluation ids (no lab or research code changed) |
| Not yet observed | This revision on GitHub: CI on the pull request, the first scheduled forecast, scoring and monitor runs after merge, and the 72h window's first production score (matures Sep 29 04:25Z) passing the next preflight |

# Validation record — monitor fix, revision 2.17.1

Validated 2026-09-28 ~00:30Z (Python 3.11, container). Earlier blocks below are kept as recorded.

| Check (2.17.1) | Result |
|---|---|
| Production evidence (verified) | Range stream monitor runs #1–#8 (Sep 26 17:56Z – Sep 27 21:56Z) all failed; run #8 (36353516254) annotation: "actions: range.yml run 36241307098 (2026-09-26T12:14:41Z) concluded failure with no record in the repository". Range forecasts: 8 scheduled runs Sep 26 16:00Z – Sep 27 20:00Z, all `published` in `state/range_runs.jsonl`, all confirmed eligible; no integrity failures |
| Reproduction | Monitor on the Sep 27 21:56Z repository with that run in the Actions list: the same single error. Without the Actions list: no problems (the repository checks were healthy) |
| Same on 2.17.1 | CI-like sparse checkout (with `desk/deployments.jsonl`): no problems at 21:56Z; `acknowledged_runs` = [36241307098]; a new unrecorded failed run still alarms; a due decision inside the lookback whose failure is in the deployment log is reported with that cause |
| Regression suite | 536 passed (desk 204), 0 skipped; fixtures 25; evaluation ids identical |

