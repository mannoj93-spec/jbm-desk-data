# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-22T17:01:43.154Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-22T16:25:00.000Z; last scored 2026-10-22T16:33:25.241Z. Stream start: 2026-10-01T00:00:00Z. Registered 363, confirmed 363, eligible 363. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 122 | 121 | 105 | 32 | 1 | 0 | 0 | 0 | -0.00533 | -0.00216 | 62/0/59 | 0.0124 | -0.1534 | unavailable (2) | -0.07943 | -0.07409 |
| 24h | 117 | 116 | 20 | 116 | 1 | 0 | 0 | 0 | -0.00643 | 0.00443 | 54/0/62 | 0.0222 | -0.1374 | unavailable (2) | -0.1297 | -0.12327 |
| 72h | 105 | 105 | 6 | 105 | 0 | 0 | 0 | 0 | -0.0176 | -0.02742 | 74/0/31 | 0.0955 | -0.3959 | unavailable (2) | -0.07665 | -0.05905 |

Overlap (from actual windows): 4h: 32 of 121 windows overlap another; the largest disjoint subset has 105; 24h: 116 of 116 windows overlap another; the largest disjoint subset has 20; 72h: 105 of 105 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
