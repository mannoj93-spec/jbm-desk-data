# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-25T16:19:14.235Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-25T12:25:00.000Z; last scored 2026-10-25T12:46:00.410Z. Stream start: 2026-10-01T00:00:00Z. Registered 402, confirmed 402, eligible 402. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 139 | 132 | 116 | 32 | 7 | 0 | 0 | 0 | -0.00528 | -0.00254 | 68/0/64 | 0.0122 | -0.1502 | unavailable (3) | -0.07859 | -0.07331 |
| 24h | 134 | 127 | 22 | 127 | 7 | 0 | 0 | 0 | -0.00451 | 0.00512 | 59/0/68 | 0.0147 | -0.0971 | unavailable (3) | -0.10229 | -0.09778 |
| 72h | 122 | 121 | 7 | 121 | 1 | 0 | 0 | 0 | -0.01627 | -0.02742 | 83/0/38 | 0.0911 | -0.3609 | unavailable (2) | -0.07764 | -0.06137 |

Overlap (from actual windows): 4h: 32 of 132 windows overlap another; the largest disjoint subset has 116; 24h: 127 of 127 windows overlap another; the largest disjoint subset has 22; 72h: 121 of 121 windows overlap another; the largest disjoint subset has 7.

Not registered, by reason: rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
