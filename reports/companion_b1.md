# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-11-24T04:32:09.117Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-11-23T16:25:00.000Z; last scored 2026-11-23T17:02:46.176Z. Stream start: 2026-10-01T00:00:00Z. Registered 543, confirmed 543, eligible 543. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 281 | 181 | 161 | 40 | 100 | 0 | 0 | 0 | -0.00524 | -0.00297 | 96/0/85 | 0.0124 | -0.1523 | unavailable (4) | -0.08936 | -0.08413 |
| 24h | 276 | 180 | 35 | 179 | 96 | 0 | 0 | 0 | -0.00676 | -0.00329 | 94/0/86 | 0.02 | -0.1503 | unavailable (4) | -0.10215 | -0.09539 |
| 72h | 264 | 178 | 13 | 178 | 86 | 0 | 0 | 0 | -0.01309 | -0.01682 | 117/0/61 | 0.0521 | -0.3082 | unavailable (4) | -0.05133 | -0.03824 |

Overlap (from actual windows): 4h: 40 of 181 windows overlap another; the largest disjoint subset has 161; 24h: 179 of 180 windows overlap another; the largest disjoint subset has 35; 72h: 178 of 178 windows overlap another; the largest disjoint subset has 13.

Not registered, by reason: late (264); rc1d-unavailable (153)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
