# Validation record — maintenance, revision 2.27 (crypto-desk 12.4.10 on the 12.4 release family)

Implemented 2026-10-05 20:15–21:30Z on branch `maint-2-27` from `main` at `b2298393`. Container; Python 3.13.

| Check | Result |
|---|---|
| Regression suite (`regression/test_*.py`, 24 files) | all OK; new/rewritten: `test_acceptance` 41 (was 11; includes 7 tests from an independent adversarial review run before release - its 6 false passes and crashes now fail or report insufficient), `test_rev227` 15; `test_acceptance` also OK on 3.12 and 3.11; updated expectations: `test_recovery` (2 dispatches per slot, run-name), `test_rev22` (watchdog on persisted success), `test_host_keys`/`test_push_credential` (10 persistence steps) |
| Desk tests, fixtures | `desk/test_*.py` 11 files OK (2 skipped as before); `test_fixtures.py` pass |
| Dashboard | `node --test dashboard/model.test.mjs` 18 pass; `test_dashboard` OK |
| Release and checksums | `make_release.py check` OK (repo 2.27; no desk module changed); `check_checksums.py check` OK |
| Production-data replay (copy of `main` `b2298393`) | 147 of 147 RC1D forecasts replay; 129 of 129 RC1D scores reproduced from retained evidence; PS1 `verify_chain` ok, 10 executions, 60 of 60 ledger rows, 0 unaccounted; companion report integrity ok, 66 registered |
| Reviewer counterexamples | launch removed, corrupt actions without executions, fills after the window: each now fails; owner-actor streams 37339803624 resolves to native range 37339238832 (verified); recovery streams 37339631785 timer-corroborated (not strict); external-to-untitled title change changes the evidence hash and the verdict |
| Acceptance on production (diagnostic) | window 2026-10-04T18:00–10-05T18:00Z, cutoff 20:00Z, commit `b2298393`, Actions evidence sha256 `fd88049f…` (569 runs, complete): **fail** (pre-2.26 gaps, 2 host-key persistence losses, a human streams dispatch, pre-2.26 untitled lineage incl. five range decisions published by recovery runs without lineage titles); identical on offline replay |
| Artifact 11366790310 | downloaded 20:14Z, sha256 equal to GitHub's digest; gate dry run exit 0; preserved, not published |
| Not executed here | any workflow change on GitHub (runners unavailable since ~18:55Z); live yield receipts; a timer-provider receipt export; the prospective 24 h window after 2.27 |

# Validation record — maintenance, revision 2.26 (crypto-desk 12.4.9 on the 12.4 release family)

Implemented 2026-10-05 13:10–14:00Z on branch `maint-2-26-1` from `main` at `ad9df852`. Container; Python 3.12.3, 3.11.17.

| Check | Result |
|---|---|
| Regression suite | 3.12: ran 837, failures 0, errors 0, skipped 1. 3.11: ran 837, failures 0, errors 0, skipped 2. New: `test_host_keys` 14, `test_acceptance` 11, `test_restore` 3, `test_monitor_aging` 6, recovery lineage/branch 6, heartbeat 1 |
| Fixtures, desk tests | `test_fixtures.py` pass (3.12, 3.11); `desk/test_*.py` (11 files) OK; PS1 `calibrate.py verify` PASS; O21 `verify` PASS |
| Dashboard | `node --test dashboard/model.test.mjs` 17 pass; `test_dashboard` (Playwright) OK |
| Release and checksums | `make_release.py check` OK (repo 2.26; no desk module changed); `check_checksums.py check` OK, 212 entries |
| Production-data replay (copy of `main` `ad9df852`) | 144 of 144 RC1D forecasts replay; PS1 `verify_chain` ok, 54 of 54 ledger rows verified; companion report integrity ok, 63 registered |
| Artifacts | 11322590457 and 11326693263 downloaded; SHA-256 equal to GitHub's digests (d1bd305d…, e1772c6a…) |
| Scheduling evidence | 1,098 runs (Oct 1 – Oct 5 14:00Z, complete pagination), 101 collector job timings |
| Acceptance on production | window 2026-10-04T21:00Z–10-05T21:00Z evaluated 13:20Z: pending (partial values in the closure record); runs before 2.26 carry no lineage in their titles, so their chain lineage is unknown |
| Not executed here | GitHub-side scheduler cause; Actions settings/billing (not served); a live authenticated host-key lookup (the session cannot call /meta); the prospective 24 h window after 2.26 |

# Validation record — maintenance, revision 2.25 (crypto-desk 12.4.8 on the 12.4 release family)

Implemented 2026-10-04 18:40–19:50Z on branch `maint-2-26` from `main` at `af9b0868` (still the tip at 19:44Z). Container;
Python 3.12.3, 3.11.17 and 3.13.16 available.

| Check | Result |
|---|---|
| Diagnosis | 483 run records since Oct 2 (Actions API): 0 queued, in progress or cancelled; every scheduled run started at creation; onset Oct 3 10–11Z; no workflow-file change at onset (`docs/incidents/2026-10-03-native-schedule.md`). Not verifiable from here: Actions permissions/billing endpoints, GitHub status, other repositories |
| Regression suite | 3.12: ran 796, failures 0, errors 0, skipped 1. 3.11: ran 796, failures 0, errors 0, skipped 2. New: `test_recovery` 23, `test_push_guard` 12 |
| Fixtures, desk tests | `test_fixtures.py` pass (3.12, 3.11); `desk/test_*.py` (11 files) OK; PS1 `calibrate.py verify` PASS; O21 `verify` PASS |
| Dashboard | `node --test dashboard/model.test.mjs` 16 pass; `test_dashboard` (Playwright) OK |
| Release and checksums | `make_release.py check` OK (repo 2.25; no desk module changed); `check_checksums.py check` OK, 205 entries |
| Defect reproduction | 2.24.1 `commit_push.sh data` with a staged `collector.py` pushed both files; 2.25 refuses and pushes nothing |
| Production-data copy (`main` af9b0868, read-only) | records byte-identical before and after `health.py` and `watchdog.py`; last 24 h to 19:44Z: 96 expected slots, 5 automated runs (all native), 5 of 95 intervals, longest automated gap 413 min; range 00:00/04:00/12:00 missed (late skip), 08:00/16:00 absent; watchdog exit 1 (service silent 103 min) |
| Not executed here | a real dispatch (needs merge); `github-actions[bot]` as the triggering actor of a token dispatch (verified only in production); the external cron (operator activation); 24 h unattended observation |

# Validation record — revision 2.24.1 (push credential for the release gate)

Validated 2026-10-03 16:15–16:35Z on branch `maint-2-25` from `main` at `e55bbd1e` (2.24 merged 15:33:40Z). Container; Python 3.12.11.

| Check | Result |
|---|---|
| Regression suite | 3.12.11: ran 761, executed 760, passed 760, failed 0, errors 0, skipped 1 (new: `test_push_credential` 4) |
| Push credential | with the key: pushes to the SSH remote, refreshes `origin/main`, leaves no key file, never prints it; failure path still removes it; without the key: workflow-token path unchanged; exactly the nine persistence steps receive the secret |
| Release and checksums | `make_release.py check` OK (release identity unchanged, repo 2.24); `check_checksums.py check` OK |
| Not executed | an SSH push with a real deploy key (needs the secret); the ruleset (operator import); `fixtures.yml` path filters under deploy-key pushes |

# Validation record — maintenance, revision 2.24 (crypto-desk 12.4.7 on the 12.4 release family)

Implemented 2026-10-03 14:15–14:45Z on branch `maint-2-24` from `main` at `24e6dcaf` (the assessed commit); re-verified 15:00–15:25Z after merging `main` at `8abd9c2f`. Container; Python 3.12.11 and 3.11.15; Node 22; Chromium via Playwright. Earlier blocks below are kept as recorded.

| Check (2.24) | Result |
|---|---|
| Baseline | `main` 24e6dcaf → 8abd9c2f (2.23, PR #28 merged Oct 3 01:06Z). Production PS1: four decisions — 00:00Z executed under ps1-job-3.0.0; 04:00Z and 08:00Z under 3.1.0; 12:00Z missed (stale, recorded 15:01Z); 18 rows. Actions API: no scheduled run of any workflow 11:17:56Z–13:26:49Z; then no scheduled collector run from 13:26:49Z through at least 15:15Z while only six scheduled runs of other workflows arrived; the 12:00Z Range forecasts schedule arrived 14:57:50Z and recorded `skipped (stale decision 2.99h > 1.0h)`. Cause not established. Findings reproduced on `main`'s code before the change: unknown journal state (`ok=true`, 6 unaccounted rows, third decision executed, 12→18 rows); dashboard `market.bars=[null]` (uncaught error, Refresh disabled, chart lost) |
| Regression suite | 3.12.11: ran 757, executed 756, passed 756, failed 0, errors 0, skipped 1. 3.11.15: ran 757, executed 755, passed 755, failed 0, errors 0, skipped 2 (new: `test_health` 9, dashboard Python 5) |
| Stream tests (`desk/test_streams.py`) | ran 179 (169 earlier + 10 journal-validation tests); 3.12: executed 179, passed 179; 3.11: executed 178, passed 178, skipped 1 |
| Other desk test files | `test_asof`, `test_hardening`, `test_jbm_archive`, `test_jbm_measure`, `test_ops`, `test_range_contract`, `test_range_job`, `test_range_model`, `test_release` (1 skipped), `test_verify`: all OK |
| Dashboard | node 15 pass, 0 fail; `node --check` OK. Chromium at 1440×900 and 390×844 on a snapshot with a recorded health report: 34/34 general checks (initial failure, retry with the real chart drawn, `[null]`/non-finite/truncated bars and HTTP 500 keep the last good data, chart and provenance with Refresh re-enabled, six-view navigation, period redraws, health panel, no horizontal scroll, no uncaught errors); coverage separation 2/2 on the 09:03Z report state (100% as of its cutoff, 12:00Z listed as due since); 3/3 rollback checks (staged render exception, injected post-commit draw failure rolls back, retry succeeds). Without a health report the view says unknown |
| Release and checksums | `make_release.py check` OK (repo 2.24); `scripts/check_checksums.py check` OK |
| O21 and calibration | `o21_reanalysis.py verify` PASS; `calibrate.py verify` PASS; `test_fixtures.py` all pass |
| Replay (merged records) | 126 of 126 RC1D forecasts; 104 RC1D scores from retained evidence; 45 of 45 B1 forecasts; 25 of 25 B1 scores match verified inputs; no evidence file differs from `main` |
| Production PS1 under 3.2.0 (copy of `main` at 8abd9c2f) | 18 physical = 18 verified, 0 unaccounted (snapshot jobs 3.0.0 and 3.1.0); launch (00:00Z decision, first fill 1790986825236) unchanged; arm and paired figures and outcomes identical to the committed 15:01Z report; `streams/ps1/` byte-identical after verification and report |
| Health, read-only on the merged checkout at 15:01Z | source stale (last scheduled collector 13:27:02Z); gaps 11:04:10Z–13:27:02Z (142.86 min, resolved) and from 13:27:02Z (ongoing); 12:00Z range decision `missed: skipped`, PS1 12:00Z missed; no files written. `--record` on a disposable copy: 4 incidents (resolved gap marked `recorded_after_end`, ongoing gap, both 12:00Z decisions), a repeat check added 0 |
| Release gate | not enforced: `main` has no protection and no ruleset (API, 15:15Z). Creating one from this session is refused by its GitHub proxy (HTTP 403). Probe baseline: a workflow-token push to `ruleset-probe` succeeded (run 37132667779, commit 8d6383ec); enforcement itself untested |
| Not executed | any GitHub run of 2.24 on `main`; `health.py --record` in production; a ruleset; fresh-thread Claude scenarios |

# Validation record — maintenance, revision 2.23 (crypto-desk 12.4.6 on the 12.4 release family)

Validated 2026-10-02 23:50Z – 2026-10-03 00:45Z on branch `maint-2-23` from `main` at `dd5ca024`, merged with `main` at `7444d65c` and again after the PS1 launch (`1c8fcf14`) before finalizing (container; Python 3.13 for development, 3.12.11 and 3.11.15 for the suites; Node 22; Chromium via Playwright). Earlier blocks below are kept as recorded.

| Check (2.23) | Result |
|---|---|
| Baseline | `main` dd5ca024 → 7444d65c. 2.22 merged Oct 2 02:37Z (PR #26); ten production research-streams runs through Oct 2 21:01Z, every stage completed. PS1 v3 launched at the Oct 3 00:00Z decision under ps1-job-3.0.0 (first fill 00:20:25.236Z; run `1c8fcf14`). Findings 1–9 reproduced in disposable fixtures or on a pristine `main` archive before any change (`CHANGELOG.md` 2.23) |
| Regression suite (`python -m unittest discover -s regression`) | 3.12.11: ran 738, executed 737, passed 737, failed 0, errors 0, skipped 1. 3.11.15: ran 738, executed 736, passed 736, failed 0, errors 0, skipped 2 |
| Stream tests (`desk/test_streams.py`) | ran 169 (138 earlier + 31 new: ledger reconciliation 11, recovery lifecycle 8, historical exclusions 3, companion binding downgrade 5, overlap and clocks 4); two 2.21–2.22 tests that expected legacy acceptance of a stripped modern binding replaced. 3.12: executed 169, passed 169. 3.11: executed 168, passed 168, skipped 1 |
| Other desk test files | `test_asof`, `test_hardening`, `test_jbm_archive`, `test_jbm_measure`, `test_ops` (evidence-block assertion moved to actual-window overlap), `test_range_contract`, `test_range_job`, `test_range_model`, `test_release`, `test_verify`: all OK |
| Dashboard | `regression.test_dashboard` 5 OK; `node --test dashboard/model.test.mjs` 11 pass, 0 fail; `node --check dashboard/app.js` OK; Chromium acceptance 16/16 (initial HTTP failure, retry, failed refresh on malformed nested field / bad JSON / HTTP 500 keeps the previous snapshot and flags it across all six views, successful refresh clears the flag, PS1 and B1 panels show integrity and clocks). Original `main` reproduced the refresh defect (`research.filter is not a function`) |
| Release and checksums | `make_release.py check` OK (repo 2.23); `scripts/check_checksums.py check` OK (hashes verify; listed set equals the documented scope); `regression/test_checksums.py`: a changed covered file fails, the refreshed release passes, data excluded |
| O21 and calibration | `o21_reanalysis.py verify` PASS; `desk/research/ps1/calibrate.py verify` PASS |
| Replay on merged records | 117 of 117 RC1D forecasts replay; 92 scores reproduce from retained evidence; 36 of 36 B1 forecasts reproduce from fit and frozen features; 17 of 17 B1 scores match their verified inputs; companion pairs 11 / 6 / 0 (4h / 24h / 72h); RC1D and companion evaluation figures identical to the committed reports except the overlap description and named clocks |
| Preserved | no file under `registry/`, `state/`, `streams/`, `reports/`, `research/`, `desk/fits/`, `desk/inputs/`, `desk/calendars/`, `desk/research/` differs from `main`; PS1 protocol v3, v2, v1 and calibration byte-identical |
| Live PS1 launch under 3.1.0 (copy of merged `main`) | `verify_chain` ok: 1 execution, 6 physical = 6 verified, 0 unaccounted; snapshot job 3.0.0 rebuilt and matched; report `verified`, launch 00:00Z / 1790986825236 unchanged, arm and paired figures identical to the committed 3.0.0 report; `streams/ps1/` byte-identical after verification and report |
| Real CLIs through `stream_ops --semantic` on a copy of `main` | companion score, companion report, PS1 decide, execute, report: all stages completed |
| Not executed | any GitHub run of 2.23; any production PS1 execution under 3.1.0; fresh-thread Claude scenarios (skill `evals.md` 133–140 ready, unexecuted) |

# Validation record — maintenance, revision 2.22 (crypto-desk 12.4.5 on the 12.4 release family)

Validated 2026-10-02 01:45–02:45Z on branch `maint-2-22` from `main` at `dea47603` (container; Python 3.11.15 and 3.12.11). Earlier blocks below are kept as recorded.

| Check (2.22) | Result |
|---|---|
| Baseline | `main` dea47603 (2.21). 102 RC1D forecasts replay; 78 of 78 scores reproduce; 21 companions registered, 7 scored; 12 production research-streams runs on 2.21, every stage completed; PS1 approved under v2, not launched. Findings 1–7 reproduced offline on 2.21 (`CHANGELOG.md` 2.22) |
| Regression suite (`python -m unittest discover -s regression`) | 3.12.11: ran 697, executed 696, passed 696, failed 0, errors 0, skipped 1. 3.11.15: ran 697, executed 695, passed 695, failed 0, errors 0, skipped 2. Unavailable: none |
| Stream tests (`desk/test_streams.py`) | ran 138 (97 earlier, 41 new: PS1 verified consumption 8, launch reconciliation 7, auto-pause cadence 4, unequal-duration statistics 6, companion verified consumption 6, actual-window overlap 2, CLI semantics through the wrapper 6, checkpoints 2); 3.12 executed 138, passed 138; 3.11 executed 137, passed 137, skipped 1 |
| Statistics | exact four-outcome fixture: E[σ̂²] = 1 for (4, 4), (4, 24) and (4, 8, 72) h (v2: 0.4897959184 for (4, 24)); simulation with drift and a 72 h gap within 3% |
| Preserved | after the build: 102 forecasts replay, 78 of 78 scores reproduce; `registry/`, `state/`, `desk/fits/`, `streams/` and `reports/` unchanged by the build; PS1 v1 and v2 byte-identical; calibration and script unchanged, `calibrate.py verify` PASS on both Pythons |
| Fixtures, release, checksums, O21 verify | `test_fixtures.py` all pass; `make_release.py check` OK (release 2.22); `SHA256SUMS` verifies; O21 `verify` PASS on both Pythons |
| Dry run on a copy of `main` (real CLIs through `stream_ops --semantic`) | companion fit done; forecast/score expected (nothing new; 14 unscored); PS1 decide/execute expected (lifecycle proposed outside production); companion report done, integrity ok, 6 verified 4h pairs (largest disjoint subset 4); PS1 report "not launched"; verdict completed |
| Not executed | any GitHub run on 2.22; any PS1 v3 decision or execution; fresh-thread Claude behaviour checks |

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

