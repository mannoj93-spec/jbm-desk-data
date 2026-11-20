# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-11-20T16:19:17.580Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-11-20T20:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261120T1600Z | 2026-11-20T16:25:00Z → 2026-11-20T20:25:00Z | 2026-11-20T20:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261120T1600Z | 2026-11-20T16:25:00Z → 2026-11-21T16:25:00Z | 2026-11-20T21:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261120T1600Z | 2026-11-20T16:25:00Z → 2026-11-23T16:25:00Z | 2026-11-20T21:15:00Z | eligible and current |

Current decision 2026-11-20T16:00:00Z: registered-pending (eligible; 0/3 scored). Due production decisions: 333; outcomes: failed 35, missing 5, registered-pending 18, scored 271, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 288 | 0.39873 | 0.48189 | 17.3% | -0.08315 | -0.04611 | 168/0/120 | 79% / 77% | 1.2448 / 1.4446 | 6 | unavailable: 6 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 64 of 288 overlap another, largest disjoint subset 256 |
| 24h | 283 | 0.35053 | 0.42995 | 18.5% | -0.07942 | -0.07102 | 172/0/111 | 81% / 76% | 1.1135 / 1.304 | 6 | unavailable: 6 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 283 of 283 overlap another, largest disjoint subset 48 |
| 72h | 271 | 0.2915 | 0.32949 | 11.5% | -0.03799 | -0.04055 | 171/0/100 | 83% / 87% | 1.0376 / 1.1936 | 6 | unavailable: 6 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 271 of 271 overlap another, largest disjoint subset 16 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 0 | 288 | 0 |
| 24h | 7 | 0 | 0 | 0 | 283 | 0 |
| 72h | 19 | 0 | 0 | 0 | 271 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-11-17T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-17T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-19T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-20T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-20T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-20T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-20T12:00:00Z | registered-pending | eligible; 0/3 scored |
