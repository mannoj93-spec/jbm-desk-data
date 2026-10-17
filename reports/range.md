# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-17T14:03:06.503Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-17T16:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261017T1200Z | 2026-10-17T12:25:00Z → 2026-10-17T16:25:00Z | 2026-10-17T16:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261017T1200Z | 2026-10-17T12:25:00Z → 2026-10-18T12:25:00Z | 2026-10-17T17:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261017T1200Z | 2026-10-17T12:25:00Z → 2026-10-20T12:25:00Z | 2026-10-17T17:15:00Z | eligible and current |

Due production decisions: 129; outcomes: failed 1, missing 5, registered-pending 18, scored 101, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 118 | 0.42334 | 0.52964 | 20.1% | -0.1063 | -0.10625 | 77/0/41 | 74% / 74% | 1.2451 / 1.4442 | 2 | unavailable: 2 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 44 of 118 overlap another, largest disjoint subset 96 |
| 24h | 113 | 0.30001 | 0.43374 | 30.8% | -0.13372 | -0.12396 | 80/0/33 | 90% / 80% | 1.1138 / 1.304 | 2 | unavailable: 2 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 113 of 113 overlap another, largest disjoint subset 20 |
| 72h | 101 | 0.15814 | 0.26923 | 41.3% | -0.11109 | -0.10078 | 85/0/16 | 99% / 94% | 1.0387 / 1.1951 | 2 | unavailable: 2 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 101 of 101 overlap another, largest disjoint subset 7 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 0 | 118 | 0 |
| 24h | 6 | 0 | 0 | 0 | 113 | 0 |
| 72h | 18 | 0 | 0 | 0 | 101 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-14T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-14T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-15T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-15T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-15T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-15T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-15T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-15T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-16T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-16T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-16T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-16T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-16T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-16T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-17T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-17T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-17T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-17T12:00:00Z | registered-pending | eligible; 0/3 scored |
