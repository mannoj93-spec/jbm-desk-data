# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-11-17T09:01:48.528Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-11-17T12:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261117T0800Z | 2026-11-17T08:25:00Z → 2026-11-17T12:25:00Z | 2026-11-17T12:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261117T0800Z | 2026-11-17T08:25:00Z → 2026-11-18T08:25:00Z | 2026-11-17T13:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261117T0800Z | 2026-11-17T08:25:00Z → 2026-11-20T08:25:00Z | 2026-11-17T13:15:00Z | eligible and current |

Current decision 2026-11-17T08:00:00Z: registered-pending (eligible; 0/3 scored). Due production decisions: 313; outcomes: failed 35, missing 5, registered-pending 17, scored 252, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 269 | 0.40124 | 0.4921 | 18.5% | -0.09086 | -0.05365 | 162/0/107 | 78% / 76% | 1.2448 / 1.4446 | 6 | unavailable: 6 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 62 of 269 overlap another, largest disjoint subset 238 |
| 24h | 264 | 0.36505 | 0.44829 | 18.6% | -0.08324 | -0.08436 | 159/0/105 | 80% / 75% | 1.1135 / 1.304 | 6 | unavailable: 6 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 264 of 264 overlap another, largest disjoint subset 45 |
| 72h | 252 | 0.29805 | 0.34343 | 13.2% | -0.04539 | -0.05041 | 165/0/87 | 83% / 86% | 1.0379 / 1.1939 | 6 | unavailable: 6 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 252 of 252 overlap another, largest disjoint subset 15 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 0 | 269 | 0 |
| 24h | 6 | 0 | 0 | 0 | 264 | 0 |
| 72h | 18 | 0 | 0 | 0 | 252 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-11-14T08:00:00Z | scored | all horizons scored |
| 2026-11-14T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-14T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-14T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-15T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-15T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-15T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-15T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-15T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-15T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-16T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-16T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-16T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-16T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-16T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-16T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-17T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-17T04:00:00Z | registered-pending | eligible; 1/3 scored |
