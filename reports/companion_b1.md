# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-16T12:34:16.946Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-16T08:25:00.000Z; last scored 2026-10-16T09:12:25.685Z. Stream start: 2026-10-01T00:00:00Z. Registered 258, confirmed 258, eligible 258. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 84 | 84 | 70 | 28 | 0 | 0 | 0 | 0 | -0.00642 | -0.00254 | 44/0/40 | 0.0148 | -0.1815 | unavailable (2) | -0.09966 | -0.09324 |
| 24h | 79 | 79 | 14 | 79 | 0 | 0 | 0 | 0 | -0.00882 | 0.00375 | 36/0/43 | 0.0257 | -0.1845 | unavailable (1) | -0.16602 | -0.1572 |
| 72h | 67 | 67 | 4 | 67 | 0 | 0 | 0 | 0 | -0.00768 | -0.01165 | 39/0/28 | 0.0493 | -0.151 | unavailable (1) | -0.11863 | -0.11095 |

Overlap (from actual windows): 4h: 28 of 84 windows overlap another; the largest disjoint subset has 70; 24h: 79 of 79 windows overlap another; the largest disjoint subset has 14; 72h: 67 of 67 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
