# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-11-20T21:47:15.897Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-11-21T01:15:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | stale | range-rc1d-4h-20261120T1600Z | 2026-11-20T16:25:00Z → 2026-11-20T20:25:00Z | 2026-11-20T20:25:00Z | window ended |
| 24h | stale | range-rc1d-24h-20261120T1600Z | 2026-11-20T16:25:00Z → 2026-11-21T16:25:00Z | 2026-11-20T21:15:00Z | expired at 2026-11-20T21:15:00Z (a newer decision was due; no newer forecast is current) |
| 72h | stale | range-rc1d-72h-20261120T1600Z | 2026-11-20T16:25:00Z → 2026-11-23T16:25:00Z | 2026-11-20T21:15:00Z | expired at 2026-11-20T21:15:00Z (a newer decision was due; no newer forecast is current) |

Due production decisions: 335; outcomes: failed 36, missing 5, registered-pending 17, scored 273, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 290 | 0.40201 | 0.48483 | 17.1% | -0.08282 | -0.04611 | 169/0/121 | 79% / 77% | 1.2448 / 1.4447 | 6 | unavailable: 6 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 64 of 290 overlap another, largest disjoint subset 258 |
| 24h | 285 | 0.35242 | 0.43104 | 18.2% | -0.07862 | -0.06062 | 172/0/113 | 80% / 76% | 1.1135 / 1.304 | 6 | unavailable: 6 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 285 of 285 overlap another, largest disjoint subset 48 |
| 72h | 273 | 0.29301 | 0.33237 | 11.8% | -0.03936 | -0.04135 | 173/0/100 | 83% / 87% | 1.0376 / 1.1936 | 6 | unavailable: 6 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 273 of 273 overlap another, largest disjoint subset 16 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 0 | 0 | 0 | 0 | 290 | 0 |
| 24h | 5 | 0 | 0 | 0 | 285 | 0 |
| 72h | 17 | 0 | 0 | 0 | 273 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-11-18T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-18T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-19T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-11-20T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-20T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-20T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-20T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-20T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-11-20T20:00:00Z | failed | ValueError: DVOL retrieval_error is not admissible (live) |
