# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-11-26T12:19:34.113Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-11-26T13:15:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | stale | range-rc1d-4h-20261126T0800Z | 2026-11-26T08:15:00Z → 2026-11-26T12:15:00Z | 2026-11-26T12:15:00Z | window ended |
| 24h | valid-current | range-rc1d-24h-20261126T0800Z | 2026-11-26T08:15:00Z → 2026-11-27T08:15:00Z | 2026-11-26T13:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261126T0800Z | 2026-11-26T08:15:00Z → 2026-11-29T08:15:00Z | 2026-11-26T13:15:00Z | eligible and current |

Current decision 2026-11-26T12:00:00Z: registered-pending (frozen; publication confirmation pending). Due production decisions: 368; outcomes: failed 36, missing 5, registered-pending 18, scored 305, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 322 | 0.40932 | 0.48264 | 15.2% | -0.07331 | -0.03764 | 185/0/137 | 78% / 77% | 1.2447 / 1.4448 | 7 | unavailable: 7 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 68 of 322 overlap another, largest disjoint subset 288 |
| 24h | 317 | 0.36995 | 0.42833 | 13.6% | -0.05838 | -0.03814 | 181/0/136 | 79% / 76% | 1.1134 / 1.304 | 7 | unavailable: 7 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 317 of 317 overlap another, largest disjoint subset 54 |
| 72h | 305 | 0.32964 | 0.36397 | 9.4% | -0.03433 | -0.03965 | 187/0/118 | 79% / 83% | 1.0372 / 1.1932 | 7 | unavailable: 7 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 305 of 305 overlap another, largest disjoint subset 18 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 0 | 322 | 0 |
| 24h | 7 | 0 | 0 | 0 | 317 | 0 |
| 72h | 19 | 0 | 0 | 0 | 305 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-11-23T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-23T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-23T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-24T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-24T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-24T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-24T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-24T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-24T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-25T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-25T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-25T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-25T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-25T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-25T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-26T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-26T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-26T08:00:00Z | registered-pending | eligible; 0/3 scored |
