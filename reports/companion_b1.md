# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-19T08:37:00.770Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-19T04:25:00.000Z; last scored 2026-10-19T05:16:08.220Z. Stream start: 2026-10-01T00:00:00Z. Registered 309, confirmed 309, eligible 309. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 101 | 101 | 85 | 32 | 0 | 0 | 0 | 0 | -0.006 | -0.00216 | 52/0/49 | 0.0137 | -0.1641 | unavailable (2) | -0.09816 | -0.09216 |
| 24h | 96 | 96 | 16 | 96 | 0 | 0 | 0 | 0 | -0.00747 | 0.00334 | 45/0/51 | 0.0236 | -0.1511 | unavailable (2) | -0.1573 | -0.14984 |
| 72h | 84 | 84 | 5 | 84 | 0 | 0 | 0 | 0 | -0.01195 | -0.01604 | 53/0/31 | 0.0725 | -0.2512 | unavailable (2) | -0.10004 | -0.08809 |

Overlap (from actual windows): 4h: 32 of 101 windows overlap another; the largest disjoint subset has 85; 24h: 96 of 96 windows overlap another; the largest disjoint subset has 16; 72h: 84 of 84 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
