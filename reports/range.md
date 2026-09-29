# Range forecasts - status

Generated 2026-09-29T05:53:50.210Z by reader-12.3.0; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-09-29T09:15:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (hourly scoring).

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | stale | range-rc1d-4h-20260929T0000Z | 2026-09-29T00:25:00Z → 2026-09-29T04:25:00Z | 2026-09-29T04:25:00Z | window ended |
| 24h | stale | range-rc1d-24h-20260929T0000Z | 2026-09-29T00:25:00Z → 2026-09-30T00:25:00Z | 2026-09-29T05:15:00Z | expired at 2026-09-29T05:15:00Z (a newer decision was due; no newer forecast is current) |
| 72h | stale | range-rc1d-72h-20260929T0000Z | 2026-09-29T00:25:00Z → 2026-10-02T00:25:00Z | 2026-09-29T05:15:00Z | expired at 2026-09-29T05:15:00Z (a newer decision was due; no newer forecast is current) |

Due production decisions: 19; outcomes: failed 1, missing 1, registered-pending 16, scored 1.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Prospective scores (RC1D, losses on the registered point; windows overlap within a horizon, so independent n is far below the count; below ~100 independent windows nothing is eligible for forecast status):

| horizon | scored | MAE B2 | MAE B0 | skill | coverage B2 | coverage B0 |
|---|---|---|---|---|---|---|
| 4h | 17 | 0.35691 | 0.48932 | 27.1% | 76% | 76% |
| 24h | 12 | 0.2268 | 0.38862 | 41.6% | 100% | 75% |
| 72h | 1 | 0.21847 | 0.50018 | 56.3% | 100% | 100% |

Scoring pipeline (RC1D):

| horizon | waiting maturity | waiting observations | ready | scored | ineligible |
|---|---|---|---|---|---|
| 4h | 0 | 0 | 0 | 17 | 0 |
| 24h | 5 | 0 | 0 | 12 | 0 |
| 72h | 16 | 0 | 0 | 1 | 0 |

| decision | outcome | reason |
|---|---|---|
| 2026-09-26T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-26T12:00:00Z | missing | no production attempt or run record (run absent, or it failed before persisting) |
| 2026-09-26T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-26T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-27T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-27T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-27T08:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-27T12:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-27T16:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-27T20:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-28T00:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-28T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-28T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-28T12:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-28T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-28T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-29T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-29T04:00:00Z | failed | run 36520641829: preflight failure: release check: OK; FAIL: test_pinned_bytes_detect_revision (__main__.TestProvenanceAndAvailability.test_pinned_bytes_detect_revision) |
