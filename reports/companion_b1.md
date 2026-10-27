# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-27T04:10:42.459Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-27T00:25:00.000Z; last scored 2026-10-27T00:31:06.809Z. Stream start: 2026-10-01T00:00:00Z. Registered 426, confirmed 426, eligible 426. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 148 | 140 | 123 | 34 | 8 | 0 | 0 | 0 | -0.00538 | -0.00299 | 73/0/67 | 0.0126 | -0.1571 | unavailable (3) | -0.07302 | -0.06764 |
| 24h | 143 | 136 | 23 | 136 | 7 | 0 | 0 | 0 | -0.00583 | 0.00239 | 66/0/70 | 0.0191 | -0.128 | unavailable (3) | -0.10115 | -0.09532 |
| 72h | 131 | 124 | 8 | 124 | 7 | 0 | 0 | 0 | -0.01632 | -0.0269 | 86/0/38 | 0.0904 | -0.3663 | unavailable (2) | -0.07759 | -0.06127 |

Overlap (from actual windows): 4h: 34 of 140 windows overlap another; the largest disjoint subset has 123; 24h: 136 of 136 windows overlap another; the largest disjoint subset has 23; 72h: 124 of 124 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: late (3); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
