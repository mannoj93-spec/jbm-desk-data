# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-13T08:19:12.975Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-13T12:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261013T0800Z | 2026-10-13T08:25:00Z → 2026-10-13T12:25:00Z | 2026-10-13T12:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261013T0800Z | 2026-10-13T08:25:00Z → 2026-10-14T08:25:00Z | 2026-10-13T13:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261013T0800Z | 2026-10-13T08:25:00Z → 2026-10-16T08:25:00Z | 2026-10-13T13:15:00Z | eligible and current |

Current decision 2026-10-13T08:00:00Z: registered-pending (eligible; 0/3 scored). Due production decisions: 103; outcomes: failed 1, missing 5, registered-pending 18, scored 75, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 92 | 0.42218 | 0.53354 | 20.9% | -0.11136 | -0.10464 | 62/0/30 | 72% / 74% | 1.2451 / 1.4441 | 2 | unavailable: 2 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 38 of 92 overlap another, largest disjoint subset 73 |
| 24h | 87 | 0.29996 | 0.43138 | 30.5% | -0.13142 | -0.11713 | 60/0/27 | 91% / 80% | 1.1138 / 1.3038 | 2 | unavailable: 2 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 87 of 87 overlap another, largest disjoint subset 15 |
| 72h | 75 | 0.19449 | 0.29361 | 33.8% | -0.09912 | -0.08799 | 62/0/13 | 99% / 92% | 1.0386 / 1.1954 | 1 | unavailable: 1 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 75 of 75 overlap another, largest disjoint subset 5 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 0 | 92 | 0 |
| 24h | 7 | 0 | 0 | 0 | 87 | 0 |
| 72h | 19 | 0 | 0 | 0 | 75 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-10T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-10T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-11T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-12T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-12T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-12T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-12T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-12T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-12T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-13T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-13T04:00:00Z | registered-pending | eligible; 0/3 scored |
