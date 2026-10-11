# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-11T12:20:30.846Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-11T08:25:00.000Z; last scored 2026-10-11T08:54:58.979Z. Stream start: 2026-10-01T00:00:00Z. Registered 168, confirmed 168, eligible 168. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 54 | 54 | 43 | 22 | 0 | 0 | 0 | 0 | -0.00526 | 0.00751 | 26/0/28 | 0.0116 | -0.1267 | unavailable (1) | -0.13178 | -0.12652 |
| 24h | 49 | 49 | 9 | 49 | 0 | 0 | 0 | 0 | -0.0147 | -0.02285 | 26/0/23 | 0.0398 | -0.2548 | unavailable (1) | -0.16329 | -0.14859 |
| 72h | 37 | 37 | 3 | 37 | 0 | 0 | 0 | 0 | -0.00172 | -0.01045 | 19/0/18 | 0.0105 | -0.0271 | unavailable (0) | -0.11026 | -0.10854 |

Overlap (from actual windows): 4h: 22 of 54 windows overlap another; the largest disjoint subset has 43; 24h: 49 of 49 windows overlap another; the largest disjoint subset has 9; 72h: 37 of 37 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
