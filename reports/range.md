# Range forecasts - status

Generated 2026-09-30T04:15:18.215Z by reader-12.3.0; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-09-30T08:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (hourly scoring).

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20260930T0400Z | 2026-09-30T04:25:00Z → 2026-09-30T08:25:00Z | 2026-09-30T08:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20260930T0400Z | 2026-09-30T04:25:00Z → 2026-10-01T04:25:00Z | 2026-09-30T09:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20260930T0400Z | 2026-09-30T04:25:00Z → 2026-10-03T04:25:00Z | 2026-09-30T09:15:00Z | eligible and current |

Current decision 2026-09-30T04:00:00Z: registered-pending (eligible; 0/3 scored). Due production decisions: 24; outcomes: failed 1, missing 1, registered-pending 17, scored 5.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Prospective scores (RC1D, losses on the registered point; windows overlap within a horizon, so independent n is far below the count; below ~100 independent windows nothing is eligible for forecast status):

| horizon | scored | MAE B2 | MAE B0 | skill | coverage B2 | coverage B0 |
|---|---|---|---|---|---|---|
| 4h | 21 | 0.36501 | 0.46133 | 20.9% | 76% | 76% |
| 24h | 17 | 0.2257 | 0.29375 | 23.2% | 100% | 82% |
| 72h | 5 | 0.26071 | 0.45171 | 42.3% | 100% | 100% |

Scoring pipeline (RC1D):

| horizon | waiting maturity | waiting observations | ready | scored | ineligible |
|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 21 | 0 |
| 24h | 6 | 0 | 0 | 17 | 0 |
| 72h | 18 | 0 | 0 | 5 | 0 |

| decision | outcome | reason |
|---|---|---|
| 2026-09-27T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-27T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-27T12:00:00Z | registered-pending | eligible; 2/3 scored |
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
| 2026-09-29T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-29T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-29T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-29T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-30T00:00:00Z | registered-pending | eligible; 0/3 scored |
