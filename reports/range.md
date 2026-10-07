# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-07T04:16:43.941Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-07T04:20:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261007T0000Z | 2026-10-07T00:20:00Z → 2026-10-07T04:20:00Z | 2026-10-07T04:20:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261007T0000Z | 2026-10-07T00:20:00Z → 2026-10-08T00:20:00Z | 2026-10-07T05:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261007T0000Z | 2026-10-07T00:20:00Z → 2026-10-10T00:20:00Z | 2026-10-07T05:15:00Z | eligible and current |

Current decision 2026-10-07T04:00:00Z: registered-pending (frozen; publication confirmation pending). Due production decisions: 66; outcomes: failed 1, missing 5, registered-pending 13, scored 43, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 55 | 0.41742 | 0.51031 | 18.2% | -0.09289 | -0.06794 | 36/0/19 | 73% / 76% | 1.2453 / 1.444 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 22 of 55 overlap another, largest disjoint subset 44 |
| 24h | 50 | 0.29468 | 0.397 | 25.8% | -0.10232 | -0.10314 | 27/0/23 | 90% / 82% | 1.1139 / 1.3033 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 50 of 50 overlap another, largest disjoint subset 10 |
| 72h | 43 | 0.18665 | 0.28119 | 33.6% | -0.09454 | -0.07515 | 36/0/7 | 100% / 98% | 1.0384 / 1.1963 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 43 of 43 overlap another, largest disjoint subset 3 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 0 | 55 | 0 |
| 24h | 7 | 0 | 0 | 0 | 50 | 0 |
| 72h | 14 | 0 | 0 | 0 | 43 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-04T04:00:00Z | skipped | stale decision (1.75h > 1.0h) |
| 2026-10-04T08:00:00Z | missing | no production attempt or run record (run absent, or it failed before persisting) |
| 2026-10-04T12:00:00Z | skipped | stale decision (3.48h > 1.0h) |
| 2026-10-04T16:00:00Z | missing | no production attempt or run record (run absent, or it failed before persisting) |
| 2026-10-04T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-05T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-05T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-05T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-05T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-05T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-05T20:00:00Z | missing | no production attempt or run record (run absent, or it failed before persisting) |
| 2026-10-06T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-06T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-06T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-06T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-06T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-06T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-07T00:00:00Z | registered-pending | eligible; 0/3 scored |
