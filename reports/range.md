# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-11-05T00:50:28.526Z by reader-12.4.6; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-11-05T05:15:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | stale | range-rc1d-4h-20261031T2000Z | 2026-10-31T20:25:00Z → 2026-11-01T00:25:00Z | 2026-11-01T00:25:00Z | window ended |
| 24h | stale | range-rc1d-24h-20261031T2000Z | 2026-10-31T20:25:00Z → 2026-11-01T20:25:00Z | 2026-11-01T01:15:00Z | window ended |
| 72h | stale | range-rc1d-72h-20261031T2000Z | 2026-10-31T20:25:00Z → 2026-11-03T20:25:00Z | 2026-11-01T01:15:00Z | window ended |

Current decision 2026-11-05T00:00:00Z: failed (run 41943739312: refit failure). Due production decisions: 239; outcomes: failed 25, missing 5, scored 205, skipped 4.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 205 | 0.40004 | 0.48175 | 17.0% | -0.08171 | -0.04282 | 124/0/81 | 77% / 77% | 1.245 / 1.4442 | 4 | unavailable: 4 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h windows, one per 4H decision; actual registered [start, end) windows: 54 of 205 overlap another, largest disjoint subset 178 |
| 24h | 205 | 0.30678 | 0.39978 | 23.3% | -0.093 | -0.10027 | 130/0/75 | 86% / 80% | 1.1138 / 1.3042 | 4 | unavailable: 4 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h windows, one per 4H decision; actual registered [start, end) windows: 205 of 205 overlap another, largest disjoint subset 35 |
| 72h | 205 | 0.24181 | 0.29449 | 17.9% | -0.05267 | -0.05844 | 137/0/68 | 90% / 95% | 1.0388 / 1.1947 | 4 | unavailable: 4 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h windows, one per 4H decision; actual registered [start, end) windows: 205 of 205 overlap another, largest disjoint subset 12 |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 0 | 0 | 0 | 0 | 205 | 0 |
| 24h | 0 | 0 | 0 | 0 | 205 | 0 |
| 72h | 0 | 0 | 0 | 0 | 205 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-11-02T00:00:00Z | failed | run 41367224718: refit failure |
| 2026-11-02T04:00:00Z | failed | run 41391094044: refit failure |
| 2026-11-02T08:00:00Z | failed | run 41413185470: refit failure |
| 2026-11-02T12:00:00Z | failed | run 41444905604: refit failure |
| 2026-11-02T16:00:00Z | failed | run 41495819863: refit failure |
| 2026-11-02T20:00:00Z | failed | run 41518281919: refit failure |
| 2026-11-03T00:00:00Z | failed | run 41563591284: refit failure |
| 2026-11-03T04:00:00Z | failed | run 41578215816: refit failure |
| 2026-11-03T08:00:00Z | failed | run 41629556748: refit failure |
| 2026-11-03T12:00:00Z | failed | run 41635838224: refit failure |
| 2026-11-03T16:00:00Z | failed | run 41701186104: refit failure |
| 2026-11-03T20:00:00Z | failed | run 41712763664: refit failure |
| 2026-11-04T00:00:00Z | failed | run 41748800588: refit failure |
| 2026-11-04T04:00:00Z | failed | run 41773299425: refit failure |
| 2026-11-04T08:00:00Z | failed | run 41824745295: refit failure |
| 2026-11-04T12:00:00Z | failed | run 41829415041: refit failure |
| 2026-11-04T16:00:00Z | failed | run 41897304618: refit failure |
| 2026-11-04T20:00:00Z | failed | run 41906761639: refit failure |
