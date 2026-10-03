# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-03T04:16:53.098Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-03T08:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261003T0400Z | 2026-10-03T04:25:00Z → 2026-10-03T08:25:00Z | 2026-10-03T08:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261003T0400Z | 2026-10-03T04:25:00Z → 2026-10-04T04:25:00Z | 2026-10-03T09:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261003T0400Z | 2026-10-03T04:25:00Z → 2026-10-06T04:25:00Z | 2026-10-03T09:15:00Z | eligible and current |

Current decision 2026-10-03T04:00:00Z: registered-pending (eligible; 0/3 scored). Due production decisions: 42; outcomes: failed 1, missing 1, registered-pending 18, scored 22.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 39 | 0.41761 | 0.49806 | 16.2% | -0.08046 | -0.0494 | 24/0/15 | 74% / 77% | 1.2454 / 1.4439 | 0 | unavailable: 0 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 20 of 39 overlap another, largest disjoint subset 29 |
| 24h | 34 | 0.25206 | 0.35304 | 28.6% | -0.10098 | -0.13474 | 20/0/14 | 97% / 85% | 1.1139 / 1.3028 | 0 | unavailable: 0 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 34 of 34 overlap another, largest disjoint subset 6 |
| 72h | 22 | 0.24116 | 0.31827 | 24.2% | -0.07712 | -0.05958 | 20/0/2 | 100% / 100% | 1.0381 / 1.1975 | 0 | unavailable: 0 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 22 of 22 overlap another, largest disjoint subset 2 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 0 | 39 | 0 |
| 24h | 7 | 0 | 0 | 0 | 34 | 0 |
| 72h | 19 | 0 | 0 | 0 | 22 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-09-30T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-30T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-30T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-30T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-30T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-01T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-01T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-01T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-01T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-01T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-01T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-02T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-02T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-02T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-02T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-02T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-02T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-03T00:00:00Z | registered-pending | eligible; 0/3 scored |
