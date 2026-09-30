# Range forecasts - status

Generated 2026-09-30T14:57:56.942Z by reader-12.3.0; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-09-30T16:30:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (hourly scoring).

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20260930T1200Z | 2026-09-30T12:30:00Z → 2026-09-30T16:30:00Z | 2026-09-30T16:30:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20260930T1200Z | 2026-09-30T12:30:00Z → 2026-10-01T12:30:00Z | 2026-09-30T17:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20260930T1200Z | 2026-09-30T12:30:00Z → 2026-10-03T12:30:00Z | 2026-09-30T17:15:00Z | eligible and current |

Due production decisions: 27; outcomes: failed 1, missing 1, registered-pending 17, scored 8.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Prospective scores (RC1D, losses on the registered point; windows overlap within a horizon, so independent n is far below the count; below ~100 independent windows nothing is eligible for forecast status):

| horizon | scored | MAE B2 | MAE B0 | skill | coverage B2 | coverage B0 |
|---|---|---|---|---|---|---|
| 4h | 24 | 0.35925 | 0.44488 | 19.2% | 79% | 79% |
| 24h | 19 | 0.23502 | 0.27673 | 15.1% | 100% | 84% |
| 72h | 8 | 0.28762 | 0.41338 | 30.4% | 100% | 100% |

Scoring pipeline (RC1D):

| horizon | waiting maturity | waiting observations | ready | scored | ineligible |
|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 24 | 0 |
| 24h | 6 | 0 | 0 | 19 | 0 |
| 72h | 17 | 0 | 0 | 8 | 0 |

| decision | outcome | reason |
|---|---|---|
| 2026-09-27T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-27T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-28T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-28T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-28T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-28T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-28T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-28T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-29T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-29T04:00:00Z | failed | run 36520641829: preflight failure: release check: OK; FAIL: test_pinned_bytes_detect_revision (__main__.TestProvenanceAndAvailability.test_pinned_bytes_detect_revision) |
| 2026-09-29T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-29T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-29T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-29T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-30T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-30T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-30T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-30T12:00:00Z | registered-pending | eligible; 0/3 scored |
