# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-16T08:15:01.864Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-16T04:25:00.000Z; last scored 2026-10-16T05:10:04.191Z. Stream start: 2026-10-01T00:00:00Z. Registered 255, confirmed 255, eligible 255. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 83 | 83 | 69 | 28 | 0 | 0 | 0 | 0 | -0.00607 | -0.00216 | 43/0/40 | 0.0142 | -0.1714 | unavailable (1) | -0.10416 | -0.09809 |
| 24h | 78 | 78 | 13 | 78 | 0 | 0 | 0 | 0 | -0.00919 | 0.00334 | 36/0/42 | 0.0264 | -0.1914 | unavailable (1) | -0.16166 | -0.15247 |
| 72h | 66 | 66 | 4 | 66 | 0 | 0 | 0 | 0 | -0.00691 | -0.01105 | 38/0/28 | 0.0441 | -0.1359 | unavailable (1) | -0.11693 | -0.11001 |

Overlap (from actual windows): 4h: 28 of 83 windows overlap another; the largest disjoint subset has 69; 24h: 78 of 78 windows overlap another; the largest disjoint subset has 13; 72h: 66 of 66 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
