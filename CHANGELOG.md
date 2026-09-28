# Maintenance, revision 2.18 (crypto-desk 12.3) — 2026-09-28

Base: `main` at `0215ee17` (after PR #19, repo 2.17.1). Shared modules changed (`range_contract.py`, `range_reader.py`),
so the package moves to 12.3; `range_job.py` and `range_monitor.py` are repository-only. Contract ids, evaluation ids,
the model, the September fit, calendars, frozen records, scores and evidence are unchanged.

| Finding | Change | Tests |
|---|---|---|
| **Preflight time bomb.** `test_hardening.TestLiveRecords` scored a copy of production at a synthetic Sep 29 time and required new `scored` rows for the three 04:00Z records. Once the real scorer scores the 72h window (matures Sep 29 04:25Z; hourly scoring at :41), no new rows exist and the forecast preflight fails from the 08:00Z run on. Reproduced by running the real scorer on a disposable copy past 04:25Z: the 2.17 test fails, the 2.18 tests pass | Production records keep their hash, validation and replay checks. Existing production scores of those records are validated as they stand (complete record, frozen hash, window, publication, loss basis, evidence hash, uniqueness) with no new rows required. Scoring behaviour moves to `test_ops.TestScoringStates` on the immutable fixture with explicit initial states | `TestLiveRecords` (2); `TestScoringStates` (5): unscored→full, partial→remaining (history byte-prefix kept), fully scored adds nothing across repeats, repeated at one instant, additional batch after full scoring |
| **Status clock precision.** `range_job._now()` dropped microseconds; the status step after a confirmation in the same second read "before" it (00:00Z Sep 28: confirmed 00:21:15.778Z, status evaluated 00:21:15.000Z, reported the 20:00Z batch) | `_now()` keeps full precision; report clocks (`now_utc`, `generated_utc`) are written with milliseconds (`range_contract.iso_ms`); `parse_utc`, the reader's and the monitor's parsers accept both forms. Stored forecast timestamps, windows and as-of filtering unchanged | `test_asof.TestSubSecondAvailability` (4): 1 ms before / at / after / later in the same second; JSON and Markdown agree; post-confirmation status shows the confirmed batch; job clock keeps microseconds; serialization round trip and 2.17 files still parse |
| **Monitor: current availability was informational.** A corrupted latest 4h frozen file made status `integrity-failed` and `check()` returned no problems; a fresh-stamped report carrying a stale current state also passed | monitor-12.3.0 `current` check on the monitor's clock: `integrity-failed` always alerts; `valid-current` alerts once its `valid_until_utc` has passed; any other state is a transition (info) only inside the run window of the interval the status was generated in, else persistent (alert); a status past `status_expires_utc` alerts | `test_integrity_failed_current_alerts_despite_publications`, `test_expired_cached_status_cannot_imply_health`, `test_transition_is_info_persistent_is_a_problem` |
| **Monitor: incident lifetime undefined.** Unrecorded failed runs stayed alarms while among the last 20 | Active while inside `LOOKBACK_H` (12 h, the runs check's window) or while no later scheduled run succeeded; otherwise historical (`info.historical_failures`). A failed latest scheduled run alarms even when recorded or acknowledged | `test_incident_lifetime` (resolved/out-of-window, never recovered, recent with later success, acknowledged-but-latest, the legacy Sep 26 incident); `test_sparse_checkout_covers_every_input` (`INPUTS` vs `range-monitor.yml`, no forecasting imports); existing subprocess test with broken forecasting code |
| Deployment log gaps | Appended, marked retrospective: PR #18 merge; first hourly production scoring (run 36249850242); first scheduled 2.17 publication (run 36254628462); PR #19 merge; first successful monitor execution (run 36367972798, scheduled). This deployment's rows are appended after it merges and is observed | `make_release check` (row shape) |

Separate (CI runtime only, its own PR): GitHub Actions Node.js 20 deprecation — `actions/checkout@v5`,
`actions/setup-python@v6`, `actions/upload-artifact@v6`, `actions/download-artifact@v7` (first majors whose
`action.yml` runs on `node24`; no input used here changed).

# Monitor fix, revision 2.17.1 (crypto-desk 12.2, package unchanged) — 2026-09-28

All eight scheduled runs of the range monitor (Sep 26 17:56Z – Sep 27 21:56Z) failed on one line: "actions: range.yml
run 36241307098 ... concluded failure with no record in the repository". That run (the 12:00Z preflight failure)
predates the run log; its verified cause is in `desk/deployments.jsonl`, which the monitor did not read, so it would
have alarmed on every run until the run left GitHub's 20-run list. The range stream itself was healthy: eight
scheduled runs published and were confirmed eligible (Sep 26 16:00Z – Sep 27 20:00Z); hourly scoring ran.

| Change | Tests |
|---|---|
| `desk/range_monitor.py` (monitor-12.2.1): runs recorded in the deployment log are acknowledged in the Actions check (listed under `acknowledged_runs`); a new unrecorded failure still alarms; a due decision whose failure is in the deployment log is reported with that cause instead of "no record". `range-monitor.yml` checks out `desk/deployments.jsonl` | `test_ops.TestMonitor.test_failure_recorded_in_the_deployment_log_is_acknowledged` |

No other module changed; shared skill modules are identical to package 12.2. Evaluation ids unchanged.

