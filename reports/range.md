# Range forecasts - status

Generated 2026-09-26T08:15:21Z by reader-12.1.0; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (weekly report).

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | valid-current | range-rc1d-4h-20260926T0800Z | 2026-09-26T08:25:00Z → 2026-09-26T12:25:00Z | 2026-09-26T12:25:00Z | eligible and current |
| 24h | valid-current | range-rc1d-24h-20260926T0800Z | 2026-09-26T08:25:00Z → 2026-09-27T08:25:00Z | 2026-09-26T13:15:00Z | eligible and current |
| 72h | valid-current | range-rc1d-72h-20260926T0800Z | 2026-09-26T08:25:00Z → 2026-09-29T08:25:00Z | 2026-09-26T13:15:00Z | eligible and current |

Current decision 2026-09-26T08:00:00Z: registered-pending (eligible; 0/3 scored). Due production decisions: 1; outcomes: registered-pending 1.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Prospective scores (RC1D, losses on the registered point; windows overlap within a horizon, so independent n is far below the count; below ~100 independent windows nothing is eligible for forecast status):

| horizon | scored | MAE B2 | MAE B0 | skill | coverage B2 | coverage B0 |
|---|---|---|---|---|---|---|
| 4h | 0 | — | — | — | — | — |
| 24h | 0 | — | — | — | — | — |
| 72h | 0 | — | — | — | — | — |

| decision | outcome | reason |
|---|---|---|
| 2026-09-26T04:00:00Z | registered-pending | eligible; 0/3 scored |
