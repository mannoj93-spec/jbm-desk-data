# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-14T00:01:43.758Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-14T00:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261013T2000Z | 2026-10-13T20:25:00Z → 2026-10-14T00:25:00Z | 2026-10-14T00:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261013T2000Z | 2026-10-13T20:25:00Z → 2026-10-14T20:25:00Z | 2026-10-14T01:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261013T2000Z | 2026-10-13T20:25:00Z → 2026-10-16T20:25:00Z | 2026-10-14T01:15:00Z | eligible and current |

Current decision 2026-10-14T00:00:00Z: not-started (no run has recorded anything for this decision yet). Due production decisions: 107; outcomes: failed 1, missing 5, registered-pending 18, scored 79, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 96 | 0.41389 | 0.51849 | 20.2% | -0.1046 | -0.09549 | 63/0/33 | 73% / 75% | 1.2451 / 1.4441 | 2 | unavailable: 2 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 38 of 96 overlap another, largest disjoint subset 77 |
| 24h | 91 | 0.30543 | 0.43957 | 30.5% | -0.13414 | -0.11713 | 64/0/27 | 91% / 79% | 1.1138 / 1.3038 | 2 | unavailable: 2 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 91 of 91 overlap another, largest disjoint subset 16 |
| 72h | 79 | 0.18769 | 0.28477 | 34.1% | -0.09708 | -0.0799 | 66/0/13 | 99% / 92% | 1.0386 / 1.1954 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 79 of 79 overlap another, largest disjoint subset 5 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 0 | 96 | 0 |
| 24h | 6 | 0 | 0 | 0 | 91 | 0 |
| 72h | 18 | 0 | 0 | 0 | 79 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-11T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-12T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-12T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-12T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-12T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-12T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-12T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-13T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-13T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-13T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-13T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-13T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-13T20:00:00Z | registered-pending | eligible; 0/3 scored |
