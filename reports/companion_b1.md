# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-19T00:33:35.444Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-18T20:25:00.000Z; last scored 2026-10-18T21:02:53.502Z. Stream start: 2026-10-01T00:00:00Z. Registered 303, confirmed 303, eligible 303. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 99 | 99 | 83 | 32 | 0 | 0 | 0 | 0 | -0.00631 | -0.00216 | 51/0/48 | 0.0144 | -0.1718 | unavailable (2) | -0.10387 | -0.09757 |
| 24h | 94 | 94 | 16 | 94 | 0 | 0 | 0 | 0 | -0.00755 | 0.00334 | 44/0/50 | 0.0236 | -0.1533 | unavailable (2) | -0.16031 | -0.15276 |
| 72h | 82 | 82 | 5 | 82 | 0 | 0 | 0 | 0 | -0.01107 | -0.01451 | 51/0/31 | 0.0702 | -0.2315 | unavailable (1) | -0.10377 | -0.0927 |

Overlap (from actual windows): 4h: 32 of 99 windows overlap another; the largest disjoint subset has 83; 24h: 94 of 94 windows overlap another; the largest disjoint subset has 16; 72h: 82 of 82 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
