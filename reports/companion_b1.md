# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-14T16:33:06.790Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-14T12:25:00.000Z; last scored 2026-10-14T13:16:40.340Z. Stream start: 2026-10-01T00:00:00Z. Registered 225, confirmed 225, eligible 225. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 73 | 73 | 60 | 26 | 0 | 0 | 0 | 0 | -0.00469 | 0.00418 | 35/0/38 | 0.0111 | -0.1276 | unavailable (1) | -0.10703 | -0.10234 |
| 24h | 68 | 68 | 12 | 68 | 0 | 0 | 0 | 0 | -0.0126 | -0.00449 | 36/0/32 | 0.0345 | -0.25 | unavailable (1) | -0.14276 | -0.13017 |
| 72h | 56 | 56 | 4 | 56 | 0 | 0 | 0 | 0 | -0.00667 | -0.01347 | 31/0/25 | 0.039 | -0.1224 | unavailable (1) | -0.11148 | -0.10482 |

Overlap (from actual windows): 4h: 26 of 73 windows overlap another; the largest disjoint subset has 60; 24h: 68 of 68 windows overlap another; the largest disjoint subset has 12; 72h: 56 of 56 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
