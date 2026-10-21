# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-21T08:19:51.977Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-21T12:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261021T0800Z | 2026-10-21T08:25:00Z → 2026-10-21T12:25:00Z | 2026-10-21T12:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261021T0800Z | 2026-10-21T08:25:00Z → 2026-10-22T08:25:00Z | 2026-10-21T13:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261021T0800Z | 2026-10-21T08:25:00Z → 2026-10-24T08:25:00Z | 2026-10-21T13:15:00Z | eligible and current |

Current decision 2026-10-21T08:00:00Z: registered-pending (eligible; 0/3 scored). Due production decisions: 151; outcomes: failed 1, missing 5, registered-pending 18, scored 123, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 140 | 0.42427 | 0.50663 | 16.3% | -0.08236 | -0.05735 | 85/0/55 | 74% / 75% | 1.2451 / 1.4442 | 3 | unavailable: 3 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 44 of 140 overlap another, largest disjoint subset 118 |
| 24h | 135 | 0.28233 | 0.40464 | 30.2% | -0.12231 | -0.11269 | 92/0/43 | 91% / 82% | 1.1138 / 1.304 | 3 | unavailable: 3 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 135 of 135 overlap another, largest disjoint subset 23 |
| 72h | 123 | 0.17682 | 0.25866 | 31.6% | -0.08184 | -0.07051 | 92/0/31 | 98% / 95% | 1.0387 / 1.1949 | 2 | unavailable: 2 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 123 of 123 overlap another, largest disjoint subset 8 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 0 | 140 | 0 |
| 24h | 7 | 0 | 0 | 0 | 135 | 0 |
| 72h | 19 | 0 | 0 | 0 | 123 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-18T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-18T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-18T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-18T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-19T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-19T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-19T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-19T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-19T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-19T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-20T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-20T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-20T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-20T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-20T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-20T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-21T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-21T04:00:00Z | registered-pending | eligible; 0/3 scored |
