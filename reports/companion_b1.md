# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-31T04:39:02.187Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-31T00:25:00.000Z; last scored 2026-10-31T00:31:25.418Z. Stream start: 2026-10-01T00:00:00Z. Registered 483, confirmed 483, eligible 483. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 172 | 160 | 142 | 36 | 12 | 0 | 0 | 0 | -0.00462 | -0.00254 | 83/0/77 | 0.0109 | -0.1404 | unavailable (3) | -0.06576 | -0.06114 |
| 24h | 167 | 157 | 27 | 157 | 10 | 0 | 0 | 0 | -0.00423 | 0.00132 | 76/0/81 | 0.0133 | -0.0983 | unavailable (3) | -0.09509 | -0.09086 |
| 72h | 155 | 147 | 9 | 147 | 8 | 0 | 0 | 0 | -0.01406 | -0.01937 | 100/0/47 | 0.0604 | -0.3371 | unavailable (3) | -0.06128 | -0.04722 |

Overlap (from actual windows): 4h: 36 of 160 windows overlap another; the largest disjoint subset has 142; 24h: 157 of 157 windows overlap another; the largest disjoint subset has 27; 72h: 147 of 147 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (18); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
