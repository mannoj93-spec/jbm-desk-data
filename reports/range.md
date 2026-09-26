# Range forecasts — prospective scores

Generated 2026-09-26T02:17:09Z by range-job-11.2.0 from `registry/scores.jsonl` (scored weekly by `report.py`). Model range-11.1.0, frozen spec `ae6aa254c786`, status before these scores: exploratory, holdout-consistent (O21, Sep 26 2026).

Skill = 1 − MAE(B2) ÷ MAE(B0) on |ln q50 − ln realized ln(high/low)|, the same windows for both. Coverage is the share of realized ranges inside q10–q90 (nominal 80%). Windows overlap within a horizon (a 72h window every 4h), so independent n is far below the count; nothing here is eligible for forecast status below ~100 independent windows.

| horizon | scored | late / unscorable | MAE B2 | MAE B0 | skill | coverage B2 | coverage B0 |
|---|---|---|---|---|---|---|---|
| 4h | 0 | 0 / 0 | — | — | — | — | — |
| 24h | 0 | 0 / 0 | — | — | — | — | — |
| 72h | 0 | 0 / 0 | — | — | — | — | — |
