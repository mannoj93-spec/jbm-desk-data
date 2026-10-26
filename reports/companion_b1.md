# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-26T05:32:34.454Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-26T04:25:00.000Z; last scored 2026-10-26T05:30:58.040Z. Stream start: 2026-10-01T00:00:00Z. Registered 411, confirmed 411, eligible 411. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 143 | 136 | 119 | 34 | 7 | 0 | 0 | 0 | -0.00546 | -0.00413 | 71/0/65 | 0.0127 | -0.1573 | unavailable (3) | -0.07614 | -0.07068 |
| 24h | 138 | 131 | 23 | 131 | 7 | 0 | 0 | 0 | -0.00577 | 0.00293 | 63/0/68 | 0.0187 | -0.1244 | unavailable (3) | -0.10436 | -0.09859 |
| 72h | 126 | 123 | 8 | 123 | 3 | 0 | 0 | 0 | -0.01631 | -0.02693 | 85/0/38 | 0.0918 | -0.3647 | unavailable (2) | -0.07768 | -0.06137 |

Overlap (from actual windows): 4h: 34 of 136 windows overlap another; the largest disjoint subset has 119; 24h: 131 of 131 windows overlap another; the largest disjoint subset has 23; 72h: 123 of 123 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
