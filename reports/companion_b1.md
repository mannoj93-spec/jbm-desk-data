# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-17T05:12:47.664Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-17T04:25:00.000Z; last scored 2026-10-17T05:06:01.741Z. Stream start: 2026-10-01T00:00:00Z. Registered 270, confirmed 270, eligible 270. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 89 | 89 | 74 | 30 | 0 | 0 | 0 | 0 | -0.00601 | -0.00216 | 46/0/43 | 0.0137 | -0.1678 | unavailable (2) | -0.10368 | -0.09766 |
| 24h | 84 | 84 | 14 | 84 | 0 | 0 | 0 | 0 | -0.00943 | 0.00239 | 40/0/44 | 0.0281 | -0.2023 | unavailable (2) | -0.15907 | -0.14964 |
| 72h | 72 | 72 | 5 | 72 | 0 | 0 | 0 | 0 | -0.0091 | -0.01189 | 43/0/29 | 0.061 | -0.1822 | unavailable (1) | -0.12733 | -0.11823 |

Overlap (from actual windows): 4h: 30 of 89 windows overlap another; the largest disjoint subset has 74; 24h: 84 of 84 windows overlap another; the largest disjoint subset has 14; 72h: 72 of 72 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
