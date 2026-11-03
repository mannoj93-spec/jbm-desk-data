# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-11-03T08:21:55.665Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-11-03T04:25:00.000Z; last scored 2026-11-03T04:33:42.224Z. Stream start: 2026-10-01T00:00:00Z. Registered 495, confirmed 495, eligible 495. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 178 | 165 | 146 | 38 | 13 | 0 | 0 | 0 | -0.00585 | -0.00306 | 88/0/77 | 0.0139 | -0.1762 | unavailable (3) | -0.0797 | -0.07386 |
| 24h | 178 | 165 | 29 | 165 | 13 | 0 | 0 | 0 | -0.00637 | -0.00319 | 84/0/81 | 0.0198 | -0.1471 | unavailable (3) | -0.1025 | -0.09613 |
| 72h | 174 | 161 | 10 | 161 | 13 | 0 | 0 | 0 | -0.01228 | -0.01679 | 104/0/57 | 0.0486 | -0.2929 | unavailable (3) | -0.058 | -0.04572 |

Overlap (from actual windows): 4h: 38 of 165 windows overlap another; the largest disjoint subset has 146; 24h: 165 of 165 windows overlap another; the largest disjoint subset has 29; 72h: 161 of 161 windows overlap another; the largest disjoint subset has 10.

Not registered, by reason: late (18); rc1d-unavailable (72)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
