# Range forecasts - status

[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml) [![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml) [![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)

Badges show the latest workflow run (recent operation), not what is current: current availability is the table below, on your own clock.

Generated 2026-10-01T16:15:09.387Z by reader-12.4.0; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-10-01T16:30:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (scored hourly by `range-score.yml`; the weekly report only summarises).

## Current availability

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20261001T1200Z | 2026-10-01T12:30:00Z → 2026-10-01T16:30:00Z | 2026-10-01T16:30:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20261001T1200Z | 2026-10-01T12:30:00Z → 2026-10-02T12:30:00Z | 2026-10-01T17:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20261001T1200Z | 2026-10-01T12:30:00Z → 2026-10-04T12:30:00Z | 2026-10-01T17:15:00Z | eligible and current |

Current decision 2026-10-01T16:00:00Z: registered-pending (frozen; publication confirmation pending). Due production decisions: 33; outcomes: failed 1, missing 1, registered-pending 17, scored 14.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Provenance correction (2.19): `package` recorded as "crypto-desk 12.2" should read "crypto-desk 12.3" for every RC1D forecast whose code_version ends with 'range-job-12.3.0' (the 2.18 job); the rule, not the list, defines the set, so forecasts the 2.18 job writes after this row are covered until 2.19 is deployed. Frozen records are unchanged; see `desk/provenance_corrections.jsonl`.

## Evidence (descriptive)

Mean absolute error of the ln-range forecast, B2 against B0 persistence, on scored eligible windows (not price error, direction or return). Method `rc1d-eval-1 (2026-09-30)`: paired differences d = B2 − B0 (negative favours B2); uncertainty only with ≥10 complete blocks of 42 decisions. Descriptive. Overlapping windows are dependent; the count of non-overlapping windows is not an effective sample size. No support claim; promotion criteria unchanged (queue.md section 0).

| horizon | n | MAE B2 | MAE B0 | reduction | mean d | median d | B2 better/tie/worse | coverage B2 / B0 | mean 10–90 width B2 / B0 (log) | blocks | 95% interval of mean d | overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 30 | 0.36926 | 0.45302 | 18.5% | -0.08376 | -0.04539 | 19/0/11 | 77% / 80% | 1.2455 / 1.4437 | 0 | unavailable: 0 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 4h, one per 4H decision; each overlaps up to 0 earlier and 0 later windows |
| 24h | 25 | 0.21914 | 0.29801 | 26.5% | -0.07886 | 0.03787 | 12/0/13 | 100% / 88% | 1.1139 / 1.3024 | 0 | unavailable: 0 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 24h, one per 4H decision; each overlaps up to 5 earlier and 5 later windows |
| 72h | 14 | 0.28059 | 0.37171 | 24.5% | -0.09113 | -0.05958 | 12/0/2 | 100% / 100% | 1.0381 / 1.1975 | 0 | unavailable: 0 complete block(s) of 42 decisions; rc1d-eval-1 (2026-09-30) needs 10 | 72h, one per 4H decision; each overlaps up to 17 earlier and 17 later windows |

## Scoring pipeline (RC1D)

Waiting maturity and ready (the next hourly scorer takes it) are normal; overdue and scoring failed are operational problems.

| horizon | waiting maturity | ready | overdue | scoring failed | scored | ineligible |
|---|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 0 | 30 | 0 |
| 24h | 7 | 0 | 0 | 0 | 25 | 0 |
| 72h | 18 | 0 | 0 | 0 | 14 | 0 |

## Recent decisions (history)

| decision | outcome | reason |
|---|---|---|
| 2026-09-28T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-28T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-29T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-29T04:00:00Z | failed | run 36520641829: preflight failure: release check: OK; FAIL: test_pinned_bytes_detect_revision (__main__.TestProvenanceAndAvailability.test_pinned_bytes_detect_revision) |
| 2026-09-29T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-29T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-29T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-29T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-30T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-30T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-30T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-30T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-30T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-30T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-01T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-01T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-01T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-10-01T12:00:00Z | registered-pending | eligible; 0/3 scored |
