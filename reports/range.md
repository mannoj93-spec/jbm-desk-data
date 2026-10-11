# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-11T04:16:29.986Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-11T04:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261011T0000Z | 2026-10-11T00:25:00Z → 2026-10-11T04:25:00Z | 2026-10-11T04:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261011T0000Z | 2026-10-11T00:25:00Z → 2026-10-12T00:25:00Z | 2026-10-11T05:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261011T0000Z | 2026-10-11T00:25:00Z → 2026-10-14T00:25:00Z | 2026-10-11T05:15:00Z | eligible and current |

Current decision 2026-10-11T04:00:00Z: registered-pending (frozen; publication confirmation pending). Due production decisions: 90; outcomes: failed 1, missing 5, registered-pending 18, scored 62, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 79 | 0.43458 | 0.5434 | 20.0% | -0.10881 | -0.08652 | 52/0/27 | 71% / 72% | 1.2452 / 1.4441 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 34 of 79 overlap another, largest disjoint subset 62 |
| 24h | 74 | 0.30086 | 0.41786 | 28.0% | -0.117 | -0.11491 | 48/0/26 | 93% / 82% | 1.1138 / 1.3037 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 74 of 74 overlap another, largest disjoint subset 13 |
| 72h | 62 | 0.18749 | 0.27455 | 31.7% | -0.08706 | -0.07132 | 49/0/13 | 100% / 98% | 1.0385 / 1.1957 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 62 of 62 overlap another, largest disjoint subset 4 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 0 | 79 | 0 |
| 24h | 7 | 0 | 0 | 0 | 74 | 0 |
| 72h | 19 | 0 | 0 | 0 | 62 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-08T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-08T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-08T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-08T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-08T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-10T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-10T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-10T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-10T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-11T00:00:00Z | registered-pending | eligible; 0/3 scored |
