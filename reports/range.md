# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-24T00:17:43.777Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-24T00:20:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261023T2000Z | 2026-10-23T20:20:00Z → 2026-10-24T00:20:00Z | 2026-10-24T00:20:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261023T2000Z | 2026-10-23T20:20:00Z → 2026-10-24T20:20:00Z | 2026-10-24T01:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261023T2000Z | 2026-10-23T20:20:00Z → 2026-10-26T20:20:00Z | 2026-10-24T01:15:00Z | eligible and current |

Current decision 2026-10-24T00:00:00Z: registered-pending (frozen; publication confirmation pending). Due production decisions: 167; outcomes: failed 1, missing 5, registered-pending 18, scored 139, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 156 | 0.4134 | 0.48646 | 15.0% | -0.07306 | -0.04028 | 93/0/63 | 74% / 76% | 1.2451 / 1.4442 | 3 | unavailable: 3 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 44 of 156 overlap another, largest disjoint subset 134 |
| 24h | 151 | 0.28799 | 0.39899 | 27.8% | -0.111 | -0.10027 | 98/0/53 | 89% / 82% | 1.1138 / 1.3041 | 3 | unavailable: 3 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 151 of 151 overlap another, largest disjoint subset 26 |
| 72h | 139 | 0.16943 | 0.24487 | 30.8% | -0.07544 | -0.06748 | 100/0/39 | 99% / 96% | 1.0387 / 1.1949 | 3 | unavailable: 3 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 139 of 139 overlap another, largest disjoint subset 9 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 0 | 156 | 0 |
| 24h | 7 | 0 | 0 | 0 | 151 | 0 |
| 72h | 19 | 0 | 0 | 0 | 139 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-21T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-21T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-21T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-21T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-21T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-21T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-22T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-22T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-22T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-22T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-22T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-22T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-23T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-23T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-23T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-23T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-23T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-23T20:00:00Z | registered-pending | eligible; 0/3 scored |
