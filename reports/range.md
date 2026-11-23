# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-11-23T23:17:03.588Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-11-24T00:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261123T2000Z | 2026-11-23T20:25:00Z → 2026-11-24T00:25:00Z | 2026-11-24T00:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261123T2000Z | 2026-11-23T20:25:00Z → 2026-11-24T20:25:00Z | 2026-11-24T01:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261123T2000Z | 2026-11-23T20:25:00Z → 2026-11-26T20:25:00Z | 2026-11-24T01:15:00Z | eligible and current |

Due production decisions: 353; outcomes: failed 36, missing 5, registered-pending 18, scored 290, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 307 | 0.41033 | 0.4879 | 15.9% | -0.07757 | -0.03904 | 177/0/130 | 78% / 76% | 1.2447 / 1.4447 | 7 | unavailable: 7 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 66 of 307 overlap another, largest disjoint subset 274 |
| 24h | 302 | 0.37025 | 0.43312 | 14.5% | -0.06287 | -0.04621 | 174/0/128 | 79% / 76% | 1.1134 / 1.304 | 7 | unavailable: 7 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 302 of 302 overlap another, largest disjoint subset 51 |
| 72h | 290 | 0.32805 | 0.3596 | 8.8% | -0.03155 | -0.03947 | 178/0/112 | 79% / 83% | 1.0374 / 1.1934 | 6 | unavailable: 6 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 290 of 290 overlap another, largest disjoint subset 17 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 0 | 307 | 0 |
| 24h | 6 | 0 | 0 | 0 | 302 | 0 |
| 72h | 18 | 0 | 0 | 0 | 290 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-11-21T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-21T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-21T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-21T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-21T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-21T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-22T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-22T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-22T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-22T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-22T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-22T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-23T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-23T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-23T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-23T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-23T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-23T20:00:00Z | registered-pending | eligible; 0/3 scored |
