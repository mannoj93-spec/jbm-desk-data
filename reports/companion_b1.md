# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-17T12:25:41.071Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-17T08:25:00.000Z; last scored 2026-10-17T09:04:54.417Z. Stream start: 2026-10-01T00:00:00Z. Registered 276, confirmed 276, eligible 276. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 90 | 90 | 74 | 32 | 0 | 0 | 0 | 0 | -0.00668 | -0.00254 | 47/0/43 | 0.0152 | -0.1845 | unavailable (2) | -0.10803 | -0.10135 |
| 24h | 85 | 85 | 14 | 85 | 0 | 0 | 0 | 0 | -0.00872 | 0.00293 | 40/0/45 | 0.0261 | -0.1863 | unavailable (2) | -0.1576 | -0.14888 |
| 72h | 73 | 73 | 5 | 73 | 0 | 0 | 0 | 0 | -0.00874 | -0.01165 | 43/0/30 | 0.059 | -0.1759 | unavailable (1) | -0.1273 | -0.11856 |

Overlap (from actual windows): 4h: 32 of 90 windows overlap another; the largest disjoint subset has 74; 24h: 85 of 85 windows overlap another; the largest disjoint subset has 14; 72h: 73 of 73 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
