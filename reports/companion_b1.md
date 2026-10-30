# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-30T21:09:59.816Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-30T16:25:00.000Z; last scored 2026-10-30T17:31:23.881Z. Stream start: 2026-10-01T00:00:00Z. Registered 480, confirmed 480, eligible 480. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 170 | 159 | 141 | 36 | 11 | 0 | 0 | 0 | -0.00447 | -0.00216 | 82/0/77 | 0.0105 | -0.1357 | unavailable (3) | -0.06731 | -0.06283 |
| 24h | 165 | 156 | 27 | 156 | 9 | 0 | 0 | 0 | -0.00452 | 0.00132 | 76/0/80 | 0.0142 | -0.1051 | unavailable (3) | -0.09242 | -0.0879 |
| 72h | 153 | 145 | 9 | 145 | 8 | 0 | 0 | 0 | -0.01446 | -0.02073 | 100/0/45 | 0.0627 | -0.3457 | unavailable (3) | -0.05973 | -0.04527 |

Overlap (from actual windows): 4h: 36 of 159 windows overlap another; the largest disjoint subset has 141; 24h: 156 of 156 windows overlap another; the largest disjoint subset has 27; 72h: 145 of 145 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (15); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
