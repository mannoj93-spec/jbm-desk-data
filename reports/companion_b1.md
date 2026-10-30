# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-30T16:26:39.277Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-30T12:25:00.000Z; last scored 2026-10-30T12:46:16.249Z. Stream start: 2026-10-01T00:00:00Z. Registered 477, confirmed 477, eligible 477. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 169 | 158 | 140 | 36 | 11 | 0 | 0 | 0 | -0.00474 | -0.00254 | 82/0/76 | 0.0111 | -0.1442 | unavailable (3) | -0.06593 | -0.06119 |
| 24h | 164 | 155 | 27 | 155 | 9 | 0 | 0 | 0 | -0.00484 | 0.00132 | 76/0/79 | 0.0153 | -0.1126 | unavailable (3) | -0.09017 | -0.08533 |
| 72h | 152 | 144 | 9 | 144 | 8 | 0 | 0 | 0 | -0.01474 | -0.02091 | 100/0/44 | 0.064 | -0.352 | unavailable (3) | -0.05863 | -0.04389 |

Overlap (from actual windows): 4h: 36 of 158 windows overlap another; the largest disjoint subset has 140; 24h: 155 of 155 windows overlap another; the largest disjoint subset has 27; 72h: 144 of 144 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (15); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
