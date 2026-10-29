# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-29T12:20:47.109Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-29T08:25:00.000Z; last scored 2026-10-29T09:01:04.153Z. Stream start: 2026-10-01T00:00:00Z. Registered 465, confirmed 465, eligible 465. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 162 | 153 | 135 | 36 | 9 | 0 | 0 | 0 | -0.00501 | -0.00293 | 80/0/73 | 0.012 | -0.1526 | unavailable (3) | -0.06285 | -0.05784 |
| 24h | 157 | 149 | 26 | 149 | 8 | 0 | 0 | 0 | -0.00574 | -0.00319 | 76/0/73 | 0.0189 | -0.1318 | unavailable (3) | -0.08379 | -0.07805 |
| 72h | 145 | 138 | 9 | 138 | 7 | 0 | 0 | 0 | -0.01566 | -0.02217 | 98/0/40 | 0.0698 | -0.3701 | unavailable (3) | -0.05723 | -0.04157 |

Overlap (from actual windows): 4h: 36 of 153 windows overlap another; the largest disjoint subset has 135; 24h: 149 of 149 windows overlap another; the largest disjoint subset has 26; 72h: 138 of 138 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (6); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
