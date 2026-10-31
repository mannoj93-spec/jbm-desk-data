# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-31T21:46:40.790Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-11-01T00:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261031T2000Z | 2026-10-31T20:25:00Z → 2026-11-01T00:25:00Z | 2026-11-01T00:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261031T2000Z | 2026-10-31T20:25:00Z → 2026-11-01T20:25:00Z | 2026-11-01T01:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261031T2000Z | 2026-10-31T20:25:00Z → 2026-11-03T20:25:00Z | 2026-11-01T01:15:00Z | eligible and current |

Due production decisions: 215; outcomes: failed 1, missing 5, registered-pending 18, scored 187, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 204 | 0.40161 | 0.4802 | 16.4% | -0.0786 | -0.0421 | 123/0/81 | 77% / 78% | 1.245 / 1.4442 | 4 | unavailable: 4 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 54 of 204 overlap another, largest disjoint subset 177 |
| 24h | 199 | 0.30132 | 0.38617 | 22.0% | -0.08485 | -0.09692 | 124/0/75 | 87% / 82% | 1.1138 / 1.3042 | 4 | unavailable: 4 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 199 of 199 overlap another, largest disjoint subset 34 |
| 72h | 187 | 0.22508 | 0.28858 | 22.0% | -0.0635 | -0.06596 | 131/0/56 | 91% / 94% | 1.0388 / 1.1947 | 4 | unavailable: 4 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 187 of 187 overlap another, largest disjoint subset 11 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 0 | 204 | 0 |
| 24h | 6 | 0 | 0 | 0 | 199 | 0 |
| 72h | 18 | 0 | 0 | 0 | 187 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-10-29T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-29T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-29T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-29T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-29T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-29T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-30T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-30T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-30T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-30T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-30T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-30T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-10-31T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-31T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-31T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-31T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-31T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-31T20:00:00Z | registered-pending | eligible; 0/3 scored |
