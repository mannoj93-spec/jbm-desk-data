# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-25T12:18:35.180Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-25T08:25:00.000Z; last scored 2026-10-25T09:15:47.674Z. Stream start: 2026-10-01T00:00:00Z. Registered 399, confirmed 399, eligible 399. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 138 | 131 | 115 | 32 | 7 | 0 | 0 | 0 | -0.00508 | -0.00216 | 67/0/64 | 0.0117 | -0.1445 | unavailable (3) | -0.07814 | -0.07306 |
| 24h | 133 | 126 | 22 | 126 | 7 | 0 | 0 | 0 | -0.00494 | 0.00443 | 59/0/67 | 0.0161 | -0.1063 | unavailable (3) | -0.10606 | -0.10112 |
| 72h | 121 | 120 | 7 | 120 | 1 | 0 | 0 | 0 | -0.01611 | -0.02718 | 82/0/38 | 0.0902 | -0.3562 | unavailable (2) | -0.07802 | -0.06191 |

Overlap (from actual windows): 4h: 32 of 131 windows overlap another; the largest disjoint subset has 115; 24h: 126 of 126 windows overlap another; the largest disjoint subset has 22; 72h: 120 of 120 windows overlap another; the largest disjoint subset has 7.

Not registered, by reason: rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
