# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-11-14T11:20:31.175Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-11-14T12:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261114T0800Z | 2026-11-14T08:25:00Z → 2026-11-14T12:25:00Z | 2026-11-14T12:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261114T0800Z | 2026-11-14T08:25:00Z → 2026-11-15T08:25:00Z | 2026-11-14T13:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261114T0800Z | 2026-11-14T08:25:00Z → 2026-11-17T08:25:00Z | 2026-11-14T13:15:00Z | eligible and current |

Due production decisions: 296; outcomes: failed 35, missing 5, registered-pending 18, scored 234, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 251 | 0.39875 | 0.49252 | 19.0% | -0.09377 | -0.05652 | 152/0/99 | 78% / 75% | 1.2449 / 1.4445 | 5 | unavailable: 5 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 60 of 251 overlap another, largest disjoint subset 221 |
| 24h | 246 | 0.33685 | 0.43444 | 22.5% | -0.09759 | -0.10661 | 152/0/94 | 82% / 76% | 1.1136 / 1.3041 | 5 | unavailable: 5 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 246 of 246 overlap another, largest disjoint subset 42 |
| 72h | 234 | 0.24424 | 0.29467 | 17.1% | -0.05044 | -0.05813 | 157/0/77 | 89% / 92% | 1.0382 / 1.1941 | 5 | unavailable: 5 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 234 of 234 overlap another, largest disjoint subset 14 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 0 | 251 | 0 |
| 24h | 6 | 0 | 0 | 0 | 246 | 0 |
| 72h | 18 | 0 | 0 | 0 | 234 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-11-11T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-11T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-11T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-12T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-12T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-12T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-12T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-12T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-12T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-13T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-13T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-13T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-13T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-13T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-13T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-14T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-14T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-14T08:00:00Z | registered-pending | eligible; 0/3 scored |
