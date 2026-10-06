# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-06T04:18:42.179Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-06T08:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261006T0400Z | 2026-10-06T04:25:00Z → 2026-10-06T08:25:00Z | 2026-10-06T08:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261006T0400Z | 2026-10-06T04:25:00Z → 2026-10-07T04:25:00Z | 2026-10-06T09:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261006T0400Z | 2026-10-06T04:25:00Z → 2026-10-09T04:25:00Z | 2026-10-06T09:15:00Z | eligible and current |

Current decision 2026-10-06T04:00:00Z: registered-pending (eligible; 0/3 scored). Due production decisions: 60; outcomes: failed 1, missing 5, registered-pending 10, scored 40, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 49 | 0.43164 | 0.52935 | 18.5% | -0.0977 | -0.06794 | 31/0/18 | 71% / 74% | 1.2453 / 1.4439 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 22 of 49 overlap another, largest disjoint subset 38 |
| 24h | 45 | 0.29462 | 0.42528 | 30.7% | -0.13066 | -0.1571 | 27/0/18 | 89% / 80% | 1.1139 / 1.3032 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 45 of 45 overlap another, largest disjoint subset 9 |
| 72h | 40 | 0.17839 | 0.26823 | 33.5% | -0.08985 | -0.06731 | 33/0/7 | 100% / 100% | 1.0384 / 1.1965 | 0 | unavailable: 0 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 40 of 40 overlap another, largest disjoint subset 3 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 0 | 49 | 0 |
| 24h | 6 | 0 | 0 | 0 | 45 | 0 |
| 72h | 11 | 0 | 0 | 0 | 40 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-03T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-03T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-03T12:00:00Z | skipped | stale decision (2.99h > 1.0h) |
| 2026-10-03T16:00:00Z | missing | no production attempt or run record (run absent, or it failed before persisting) |
| 2026-10-03T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-04T00:00:00Z | skipped | stale decision (3.19h > 1.0h) |
| 2026-10-04T04:00:00Z | skipped | stale decision (1.75h > 1.0h) |
| 2026-10-04T08:00:00Z | missing | no production attempt or run record (run absent, or it failed before persisting) |
| 2026-10-04T12:00:00Z | skipped | stale decision (3.48h > 1.0h) |
| 2026-10-04T16:00:00Z | missing | no production attempt or run record (run absent, or it failed before persisting) |
| 2026-10-04T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-05T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-05T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-05T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-05T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-05T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-05T20:00:00Z | missing | no production attempt or run record (run absent, or it failed before persisting) |
| 2026-10-06T00:00:00Z | registered-pending | eligible; 0/3 scored |
