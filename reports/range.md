# Range forecasts - status

Generated 2026-09-29T20:16:02.019Z by reader-12.3.0; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-09-30T00:25:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (hourly scoring).

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20260929T2000Z | 2026-09-29T20:25:00Z → 2026-09-30T00:25:00Z | 2026-09-30T00:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20260929T2000Z | 2026-09-29T20:25:00Z → 2026-09-30T20:25:00Z | 2026-09-30T01:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20260929T2000Z | 2026-09-29T20:25:00Z → 2026-10-02T20:25:00Z | 2026-09-30T01:15:00Z | eligible and current |

Current decision 2026-09-29T20:00:00Z: registered-pending (eligible; 0/3 scored). Due production decisions: 22; outcomes: failed 1, missing 1, registered-pending 17, scored 3.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Prospective scores (RC1D, losses on the registered point; windows overlap within a horizon, so independent n is far below the count; below ~100 independent windows nothing is eligible for forecast status):

| horizon | scored | MAE B2 | MAE B0 | skill | coverage B2 | coverage B0 |
|---|---|---|---|---|---|---|
| 4h | 19 | 0.36857 | 0.48167 | 23.5% | 74% | 74% |
| 24h | 15 | 0.22292 | 0.32722 | 31.9% | 100% | 80% |
| 72h | 3 | 0.23716 | 0.46992 | 49.5% | 100% | 100% |

Scoring pipeline (RC1D):

| horizon | waiting maturity | waiting observations | ready | scored | ineligible |
|---|---|---|---|---|---|
| 4h | 2 | 0 | 0 | 19 | 0 |
| 24h | 6 | 0 | 0 | 15 | 0 |
| 72h | 18 | 0 | 0 | 3 | 0 |

| decision | outcome | reason |
|---|---|---|
| 2026-09-26T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-27T00:00:00Z | registered-pending | eligible; 2/3 scored |
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
| 2026-09-28T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-29T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-29T04:00:00Z | failed | run 36520641829: preflight failure: release check: OK; FAIL: test_pinned_bytes_detect_revision (__main__.TestProvenanceAndAvailability.test_pinned_bytes_detect_revision) |
| 2026-09-29T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-29T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-29T16:00:00Z | registered-pending | eligible; 0/3 scored |
