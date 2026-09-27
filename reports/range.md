# Range forecasts - status

Generated 2026-09-27T07:50:35Z by reader-12.2.0; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-09-27T08:20:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (hourly scoring).

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20260927T0400Z | 2026-09-27T04:20:00Z → 2026-09-27T08:20:00Z | 2026-09-27T08:20:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20260927T0400Z | 2026-09-27T04:20:00Z → 2026-09-28T04:20:00Z | 2026-09-27T09:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20260927T0400Z | 2026-09-27T04:20:00Z → 2026-09-30T04:20:00Z | 2026-09-27T09:15:00Z | eligible and current |

Due production decisions: 7; outcomes: missing 1, registered-pending 6.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Prospective scores (RC1D, losses on the registered point; windows overlap within a horizon, so independent n is far below the count; below ~100 independent windows nothing is eligible for forecast status):

| horizon | scored | MAE B2 | MAE B0 | skill | coverage B2 | coverage B0 |
|---|---|---|---|---|---|---|
| 4h | 5 | 0.46994 | 0.85825 | 45.2% | 60% | 20% |
| 24h | 1 | 0.3651 | 1.18779 | 69.3% | 100% | 0% |
| 72h | 0 | — | — | — | — | — |

Scoring pipeline (RC1D):

| horizon | waiting maturity | waiting observations | ready | scored | ineligible |
|---|---|---|---|---|---|
| 4h | 1 | 0 | 0 | 5 | 0 |
| 24h | 5 | 0 | 0 | 1 | 0 |
| 72h | 6 | 0 | 0 | 0 | 0 |

| decision | outcome | reason |
|---|---|---|
| 2026-09-26T04:00:00Z | registered-pending | eligible; 2/3 scored |
| 2026-09-26T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-26T12:00:00Z | missing | no production attempt or run record (run absent, or it failed before persisting) |
| 2026-09-26T16:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-26T20:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-27T00:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-27T04:00:00Z | registered-pending | eligible; 0/3 scored |
