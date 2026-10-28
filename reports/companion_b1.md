# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-28T04:39:10.086Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-28T00:25:00.000Z; last scored 2026-10-28T00:31:12.086Z. Stream start: 2026-10-01T00:00:00Z. Registered 444, confirmed 444, eligible 444. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 154 | 146 | 128 | 36 | 8 | 0 | 0 | 0 | -0.00512 | -0.00254 | 75/0/71 | 0.0122 | -0.1526 | unavailable (3) | -0.06867 | -0.06355 |
| 24h | 149 | 141 | 24 | 141 | 8 | 0 | 0 | 0 | -0.0058 | -0.00194 | 71/0/70 | 0.0188 | -0.1297 | unavailable (3) | -0.09184 | -0.08604 |
| 72h | 137 | 130 | 8 | 130 | 7 | 0 | 0 | 0 | -0.01619 | -0.02506 | 92/0/38 | 0.0792 | -0.372 | unavailable (3) | -0.07086 | -0.05467 |

Overlap (from actual windows): 4h: 36 of 146 windows overlap another; the largest disjoint subset has 128; 24h: 141 of 141 windows overlap another; the largest disjoint subset has 24; 72h: 130 of 130 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: late (3); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
