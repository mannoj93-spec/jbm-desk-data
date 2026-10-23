# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-23T04:31:13.948Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-23T00:25:00.000Z; last scored 2026-10-23T00:30:59.571Z. Stream start: 2026-10-01T00:00:00Z. Registered 369, confirmed 369, eligible 369. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 124 | 122 | 106 | 32 | 2 | 0 | 0 | 0 | -0.00541 | -0.00254 | 63/0/59 | 0.0125 | -0.1563 | unavailable (2) | -0.07756 | -0.07214 |
| 24h | 119 | 118 | 20 | 118 | 1 | 0 | 0 | 0 | -0.00586 | 0.00562 | 54/0/64 | 0.02 | -0.1258 | unavailable (2) | -0.13036 | -0.1245 |
| 72h | 107 | 107 | 7 | 107 | 0 | 0 | 0 | 0 | -0.01827 | -0.02809 | 76/0/31 | 0.1001 | -0.4124 | unavailable (2) | -0.07759 | -0.05932 |

Overlap (from actual windows): 4h: 32 of 122 windows overlap another; the largest disjoint subset has 106; 24h: 118 of 118 windows overlap another; the largest disjoint subset has 20; 72h: 107 of 107 windows overlap another; the largest disjoint subset has 7.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
