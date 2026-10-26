# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-26T09:55:57.865Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-26T08:25:00.000Z; last scored 2026-10-26T09:30:59.313Z. Stream start: 2026-10-01T00:00:00Z. Registered 414, confirmed 414, eligible 414. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 144 | 137 | 120 | 34 | 7 | 0 | 0 | 0 | -0.00541 | -0.00293 | 71/0/66 | 0.0127 | -0.1564 | unavailable (3) | -0.07491 | -0.0695 |
| 24h | 139 | 132 | 23 | 132 | 7 | 0 | 0 | 0 | -0.00594 | 0.00239 | 64/0/68 | 0.0193 | -0.1286 | unavailable (3) | -0.10387 | -0.09792 |
| 72h | 127 | 123 | 8 | 123 | 4 | 0 | 0 | 0 | -0.01631 | -0.02693 | 85/0/38 | 0.0918 | -0.3647 | unavailable (2) | -0.07768 | -0.06137 |

Overlap (from actual windows): 4h: 34 of 137 windows overlap another; the largest disjoint subset has 120; 24h: 132 of 132 windows overlap another; the largest disjoint subset has 23; 72h: 123 of 123 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
