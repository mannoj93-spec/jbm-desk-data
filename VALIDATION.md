# Validation record — maintenance, revision 2.21 (crypto-desk 12.4.4 on the 12.4 release family)

Validated 2026-10-01 00:30–02:00Z on branch `maint-2-21` from `main` at `8e8e3c14` (container; Python 3.11.15 and 3.12.11). Earlier blocks below are kept as recorded; test counts in them are restated in the last row.

| Check (2.21) | Result |
|---|---|
| Baseline | `main` 8e8e3c14; 2.20 deployed. Before any change: 84 RC1D forecasts replay, 57 of 57 scores reproduce from retained evidence; findings 1–8 reproduced on the deployed code (`CHANGELOG.md` 2.21) |
| Regression suite (`python -m unittest discover -s regression`) | 3.12.11: ran 656, executed 655, passed 655, failed 0, errors 0, skipped 1. 3.11.15: ran 656, executed 654, passed 654, failed 0, errors 0, skipped 2 (lab evaluation versions hash the 3.12 AST). Unavailable: none. One earlier full 3.11 run had 1 failure in `test_rev26.test_one_hung_venue_cannot_cost_every_venue_its_snapshot` (collector stage budget 243.6 s against a 241 s bound); collector code is untouched, the test passed 5 of 5 in isolation, 3 of 3 on unmodified `main`, and on the full rerun - recorded as a pre-existing timing-sensitive test, not fixed here |
| Stream tests (`desk/test_streams.py`) | ran 97 (41 earlier + 56 new: atomic execution 7, time accounting 8, quote validation 12, PS1 integrity 6, companion integrity 6, lifecycle 7, workflow stages 8, retired protocol 2); 3.12 executed 97, passed 97; 3.11 executed 96, passed 96, skipped 1 |
| Numerical fixtures | duration-weighted Sharpe on (0.02, −0.01, 0.03) over (4, 8, 4) h = 21.9/√1.14975; equal 4h spacing reduces to v1's √2190 formula to 1e-9 |
| Preserved | after the build: 84 RC1D forecasts replay, 57 of 57 scores reproduce; `registry/`, `state/`, `desk/fits/`, `streams/` and `reports/` unchanged by the build; PS1 v1 protocol byte-identical (`00acb5bc…`); calibration and script unchanged, `calibrate.py verify` PASS on both Pythons; lab code hash and 3.12 evaluation versions unchanged |
| Fixtures, release, checksums, O21 verify | `test_fixtures.py` all pass; `make_release.py check` OK (release 2.21 manifest); `SHA256SUMS` verifies; O21 `verify` PASS |
| Dry run on a copy of `main` | every stage through `stream_ops.py`; companion fit validates; PS1 `decide`/`execute` refused at lifecycle `proposed` (approval is recorded only by a production run on `main`); reports written with evidence class and lifecycle; verdict `completed` |
| Not executed | the workflow on GitHub with 2.21; any PS1 v2 decision or execution; the PS1 launch (not before 2026-10-03T00:00Z) |
| Restated counts (unittest "Ran" includes skipped) | 2.20 regression "600 run": executed 599 (3.12) and 598 (3.11). Package 12.4 `check_package.py` "executed 173 … skipped 42": ran 173, executed 131 |

# Validation record — research upgrade, revision 2.20 (crypto-desk 12.4.3 on the 12.4 release family)

Validated 2026-09-30 22:30–23:30Z on branch `research-ps1` from `main` at `89fde1a7` (container; Python 3.11.15 and 3.12.11). Earlier blocks below are kept as recorded.

| Check (2.20) | Result |
|---|---|
| Baseline | `main` 89fde1a7; repo 2.19 deployed (PR #23 merged 17:34:07Z; first 2.19 scoring and monitor runs in `desk/deployments.jsonl`). Registry at the base: RC1D batches through 2026-09-30T20:00Z |
| Regression suite (`python -m unittest discover -s regression`, every desk suite, now including `test_streams`) | 600 run, 0 failed; skipped 1 on 3.12.11, 2 on 3.11.15 (the extra 3.11 skip: lab evaluation versions hash the 3.12 AST) |
| New tests (`desk/test_streams.py`) | 41: look-ahead (4), late registration (6), hindsight fills (5), joint missing data (5), accounting (7), retries (3), identity preservation (6), RC1D compatibility (3), feasibility (2) |
| Identity preservation | range_model spec `ae6aa254…`, contract ids RC1D/RC1, range-job-12.4.0 and the O21 selection unchanged; lab `code_hash` equals every current evidence card's `code_sha256`; on 3.12 every design's evaluation version recomputes to the current id; a companion and PS1 run leave `registry/` and the manifest byte-identical |
| PS1 calibration | `calibrate.py verify` PASS on both Pythons (k_b2 0.798527, k_vol 1.010628, s_uncond 0.009417 over 4,380 decisions 2024-09-23 .. 2026-09-22, 25 monthly refits) |
| Fixtures, release, checksums, O21 verify | `test_fixtures.py` all pass; `make_release.py check` OK (release 2.20 manifest); `SHA256SUMS` 176 files verify; O21 `verify` PASS |
| Dry run on a copy of `main` | companion fit written for 2026-09 (n 14,430 / 14,425 / 14,413); the 20:00Z companions recorded missed (window already started - correct); PS1 `not launched`; reports written |
| Live quote probe (container) | Binance spot depth via www.binance.com returned a valid 20-level book in ~0.6 s; a GitHub-runner capture is unobserved until the workflow runs |
| Not executed | the workflow on GitHub; any companion or PS1 registration; the PS1 launch (not before 2026-10-03T00:00Z and only after merge); the October rollover |

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

