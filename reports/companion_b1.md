# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-20T04:22:11.514Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-20T00:25:00.000Z; last scored 2026-10-20T01:19:18.635Z. Stream start: 2026-10-01T00:00:00Z. Registered 324, confirmed 324, eligible 324. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 106 | 106 | 90 | 32 | 0 | 0 | 0 | 0 | -0.00552 | -0.00123 | 54/0/52 | 0.0127 | -0.1528 | unavailable (2) | -0.09298 | -0.08745 |
| 24h | 101 | 101 | 17 | 101 | 0 | 0 | 0 | 0 | -0.00616 | 0.00512 | 46/0/55 | 0.0198 | -0.1261 | unavailable (2) | -0.14717 | -0.14101 |
| 72h | 89 | 89 | 6 | 89 | 0 | 0 | 0 | 0 | -0.01416 | -0.0221 | 58/0/31 | 0.0816 | -0.3004 | unavailable (2) | -0.09518 | -0.08102 |

Overlap (from actual windows): 4h: 32 of 106 windows overlap another; the largest disjoint subset has 90; 24h: 101 of 101 windows overlap another; the largest disjoint subset has 17; 72h: 89 of 89 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
