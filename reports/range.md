# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-12T15:03:58.506Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-12T16:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261012T1200Z | 2026-10-12T12:25:00Z → 2026-10-12T16:25:00Z | 2026-10-12T16:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261012T1200Z | 2026-10-12T12:25:00Z → 2026-10-13T12:25:00Z | 2026-10-12T17:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261012T1200Z | 2026-10-12T12:25:00Z → 2026-10-15T12:25:00Z | 2026-10-12T17:15:00Z | eligible and current |

Due production decisions: 99; outcomes: failed 1, missing 5, registered-pending 18, scored 71, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 88 | 0.41337 | 0.52014 | 20.5% | -0.10678 | -0.07955 | 58/0/30 | 73% / 75% | 1.2451 / 1.4441 | 2 | unavailable: 2 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 38 of 88 overlap another, largest disjoint subset 69 |
| 24h | 83 | 0.29978 | 0.43414 | 30.9% | -0.13436 | -0.11799 | 57/0/26 | 90% / 81% | 1.1138 / 1.3038 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 83 of 83 overlap another, largest disjoint subset 15 |
| 72h | 71 | 0.19206 | 0.28997 | 33.8% | -0.09791 | -0.08645 | 58/0/13 | 99% / 94% | 1.0386 / 1.1955 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 71 of 71 overlap another, largest disjoint subset 5 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 0 | 88 | 0 |
| 24h | 6 | 0 | 0 | 0 | 83 | 0 |
| 72h | 18 | 0 | 0 | 0 | 71 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-09T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-09T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-11T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-12T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-12T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-12T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-12T12:00:00Z | registered-pending | eligible; 0/3 scored |
