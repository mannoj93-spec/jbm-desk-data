# Range forecasts - status

Generated 2026-09-26T14:50:12Z by reader-12.2.0; contract `RC1D/contract-12.0.0/175a4dd4c6c0`. **Expires 2026-09-26T17:15:00Z**: after that this page cannot say what is current; before then re-check each row's valid-until on your own clock. Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (hourly scoring).

| horizon | state | id | window | valid until | reason |
|---|---|---|---|---|---|
| 4h | stale | range-rc1d-4h-20260926T0800Z | 2026-09-26T08:25:00Z → 2026-09-26T12:25:00Z | 2026-09-26T12:25:00Z | window ended |
| 24h | stale | range-rc1d-24h-20260926T0800Z | 2026-09-26T08:25:00Z → 2026-09-27T08:25:00Z | 2026-09-26T13:15:00Z | expired at 2026-09-26T13:15:00Z (a newer decision was due; no newer forecast is current) |
| 72h | stale | range-rc1d-72h-20260926T0800Z | 2026-09-26T08:25:00Z → 2026-09-29T08:25:00Z | 2026-09-26T13:15:00Z | expired at 2026-09-26T13:15:00Z (a newer decision was due; no newer forecast is current) |

Due production decisions: 3; outcomes: missing 1, registered-pending 2.
Non-production attempts (tests, local runs): 0. Orphan source files: 0. Integrity failures: 0. Legacy 2.14 registrations (q50-scored, pre-contract): 0.
Valid-current rows are current only until their valid_until_utc (see the JSON twin).

Prospective scores (RC1D, losses on the registered point; windows overlap within a horizon, so independent n is far below the count; below ~100 independent windows nothing is eligible for forecast status):

| horizon | scored | MAE B2 | MAE B0 | skill | coverage B2 | coverage B0 |
|---|---|---|---|---|---|---|
| 4h | 2 | 0.24817 | 0.91895 | 73.0% | 100% | 0% |
| 24h | 0 | — | — | — | — | — |
| 72h | 0 | — | — | — | — | — |

Scoring pipeline (RC1D):

| horizon | waiting maturity | waiting observations | ready | scored | ineligible |
|---|---|---|---|---|---|
| 4h | 0 | 0 | 0 | 2 | 0 |
| 24h | 2 | 0 | 0 | 0 | 0 |
| 72h | 2 | 0 | 0 | 0 | 0 |

| decision | outcome | reason |
|---|---|---|
| 2026-09-26T04:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-26T08:00:00Z | registered-pending | eligible; 1/3 scored |
| 2026-09-26T12:00:00Z | missing | no production attempt or run record (run absent, or it failed before persisting) |
