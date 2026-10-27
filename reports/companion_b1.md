# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-27T14:58:13.715Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-27T12:25:00.000Z; last scored 2026-10-27T13:16:14.799Z. Stream start: 2026-10-01T00:00:00Z. Registered 432, confirmed 432, eligible 432. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 151 | 143 | 125 | 36 | 8 | 0 | 0 | 0 | -0.00526 | -0.00293 | 74/0/69 | 0.0125 | -0.1551 | unavailable (3) | -0.07117 | -0.06591 |
| 24h | 146 | 139 | 24 | 139 | 7 | 0 | 0 | 0 | -0.00579 | 0.00148 | 69/0/70 | 0.0188 | -0.1284 | unavailable (3) | -0.09553 | -0.08974 |
| 72h | 134 | 127 | 8 | 127 | 7 | 0 | 0 | 0 | -0.01617 | -0.02628 | 89/0/38 | 0.0852 | -0.3674 | unavailable (3) | -0.0762 | -0.06003 |

Overlap (from actual windows): 4h: 36 of 143 windows overlap another; the largest disjoint subset has 125; 24h: 139 of 139 windows overlap another; the largest disjoint subset has 24; 72h: 127 of 127 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: late (3); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
