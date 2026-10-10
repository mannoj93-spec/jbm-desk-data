# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-10T09:53:59.758Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-10T12:20:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261010T0800Z | 2026-10-10T08:20:00Z → 2026-10-10T12:20:00Z | 2026-10-10T12:20:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261010T0800Z | 2026-10-10T08:20:00Z → 2026-10-11T08:20:00Z | 2026-10-10T13:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261010T0800Z | 2026-10-10T08:20:00Z → 2026-10-13T08:20:00Z | 2026-10-10T13:15:00Z | eligible and current |

Due production decisions: 86; outcomes: failed 1, missing 5, registered-pending 18, scored 58, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 75 | 0.43631 | 0.51713 | 15.6% | -0.08082 | -0.07082 | 48/0/27 | 71% / 75% | 1.2452 / 1.4441 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 30 of 75 overlap another, largest disjoint subset 60 |
| 24h | 70 | 0.29491 | 0.39341 | 25.0% | -0.0985 | -0.10314 | 44/0/26 | 93% / 87% | 1.1138 / 1.3036 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 70 of 70 overlap another, largest disjoint subset 13 |
| 72h | 58 | 0.19808 | 0.27703 | 28.5% | -0.07895 | -0.06618 | 45/0/13 | 100% / 98% | 1.0385 / 1.1958 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 58 of 58 overlap another, largest disjoint subset 4 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 0 | 75 | 0 |
| 24h | 6 | 0 | 0 | 0 | 70 | 0 |
| 72h | 18 | 0 | 0 | 0 | 58 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-07T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-07T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-07T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-08T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-08T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-08T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-08T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-08T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-08T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-09T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-09T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-10T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-10T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-10T08:00:00Z | registered-pending | eligible; 0/3 scored |
