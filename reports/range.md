# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-28T00:31:12.086Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-28T04:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261028T0000Z | 2026-10-28T00:25:00Z → 2026-10-28T04:25:00Z | 2026-10-28T04:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261028T0000Z | 2026-10-28T00:25:00Z → 2026-10-29T00:25:00Z | 2026-10-28T05:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261028T0000Z | 2026-10-28T00:25:00Z → 2026-10-31T00:25:00Z | 2026-10-28T05:15:00Z | eligible and current |

Current decision 2026-10-28T00:00:00Z: registered-pending (eligible; 0/3 scored). Due production decisions: 191; outcomes: failed 1, missing 5, registered-pending 17, scored 164, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 181 | 0.40391 | 0.46999 | 14.1% | -0.06608 | -0.03822 | 106/0/75 | 76% / 78% | 1.245 / 1.4442 | 4 | unavailable: 4 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 50 of 181 overlap another, largest disjoint subset 156 |
| 24h | 176 | 0.29886 | 0.37727 | 20.8% | -0.07841 | -0.08637 | 107/0/69 | 88% / 84% | 1.1138 / 1.3041 | 4 | unavailable: 4 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 176 of 176 overlap another, largest disjoint subset 30 |
| 72h | 164 | 0.19097 | 0.26283 | 27.3% | -0.07186 | -0.06655 | 119/0/45 | 95% / 93% | 1.0388 / 1.1948 | 3 | unavailable: 3 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 164 of 164 overlap another, largest disjoint subset 10 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 0 | 181 | 0 |
| 24h | 6 | 0 | 0 | 0 | 176 | 0 |
| 72h | 18 | 0 | 0 | 0 | 164 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-25T00:00:00Z | scored | all horizons scored |
| 2026-10-25T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-25T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-25T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-25T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-25T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-26T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-26T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-26T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-26T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-26T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-26T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-27T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-27T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-27T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-27T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-27T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-27T20:00:00Z | registered-pending | eligible; 1/3 scored |
