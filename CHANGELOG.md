# Desk production fixes, revision 2.17 (crypto-desk 12.2) — 2026-09-26

Response to the assessment of package 12.1 / repo 2.16 (overnight snapshot `03ab599`), built on `365ff99`.
Collection cadence, API budgets, research designs and skills are unchanged. **No evaluation version changes**
(all eight lab evaluation ids identical, `lab/versioning.py`). Semantic contract ids unchanged
(`contract-12.0.0`): no calculation changed. Frozen model, monthly fits, research outputs, registered forecasts,
publication rows and research clocks untouched; nothing back-filled. Implementation versions: reader-12.2.0,
contract-12.2.0, range-job-12.2.0, scoring-2.5, ops-12.2.0 and monitor-12.2.0 (new).

| # | Finding (reproduced on 2.16) | Fix | Tests |
|---|---|---|---|
| 1 | Run 36241307098 (12:00Z) failed preflight: `read_current(now=04:30Z)` returned the 08:00Z batch (also at 03:50Z, before either decision); the test read the growing production registry | As-of reader: only records whose decision, preparation, registration and publication confirmation are at or before `now`; newest governs; a pending record is skipped, an integrity failure never is; windows may start after `now`; `revalidate` lower bound (`unavailable`). Tests on an immutable fixture of the 04:00Z/08:00Z batches (`desk/fixtures/rc1d_20260926`); ID-specific hash/replay checks on production records | `test_asof.TestAsOf` (before/after each publication, grace, expiry, future start, cached lower bound, third batch, integrity), `TestProductionCompatibility` |
| 2 | Registration at the window start read `valid-current` but scored "late"; 00:04 preparation with a 01:00 start passed; `attempt: []` and `contract: []` raised `TypeError` | `range_contract.eligibility` shared by reader and scorer; exact window via `range_contract.window` (70-min limit kept); chronology prepared <= registered <= confirmed; type checks before lookups; `registration.forecasts(errors=...)` reports malformed records instead of aborting scoring | `test_asof.TestEligibilityAndValidation` |
| 3 | The failed run left no attempt row; status said "in progress", later "missing"; the watchdog covers the collector only | `state/range_runs.jsonl` (`desk/range_ops.py`, stdlib): start, per-stage outcome with the failing test line, terminal outcome; status outcomes not-started / running / failed / skipped / published / scored; `range-monitor.yml` (`desk/range_monitor.py`, stdlib, read-only): failed or absent runs, last eligible publication, status freshness, scoring backlog, Actions run list | `test_ops.TestLifecycleLog`, `TestStatusOutcomes`, `TestMonitor` |
| 4 | The 04:20–08:20Z 4h target matured unscored: scoring ran only with the weekly report | `range-score.yml` hourly: `range_job.py score` (existing scorer, `only_prefix="range-rc1d-"`, 5-min maturity buffer, evidence retained, idempotent by id and hash); attempts in `state/range_scoring.jsonl`; per-horizon states in the status | `test_ops.TestHourlyScoring` (boundary, incomplete coverage then recovery, repeat, scoring while forecasting fails) |
| 5 | `verify` on 3.12 printed OUT OF TOLERANCE (the rows-file hash compared as data) and exited 0; rows not compared | Two gates: exact integrity of stored artifacts; per-value numerical equivalence of summary and all 275,016 row values, categorical exact; rerun hashes reported only; exit 1/2; CI runs it | `test_verify` (tolerated rounding, material change, missing row, changed conclusion, altered bytes, exit codes) |
| 6 | `make_release._version` recorded the contract module's inline comment | ast-parsed literal; release, deployment log (2.16 merge, first scheduled publication, the 12:00Z failure), status expiry, research-family wording | `test_ops.TestVersionParser`, `test_release` |

**Tests.** 535 regression tests (332 + desk 203: measure 40, archive 50, range model 18, contract 10, range job 26,
hardening 17, release 3, as-of 17, ops 15, verify 7), no skips, Python 3.11; 25 numerical fixtures unchanged;
`o21_reanalysis.py verify` PASS on 3.11 (max row difference 0.0) and 3.12.3 (1.0e-12; rerun bytes differ, reported).

