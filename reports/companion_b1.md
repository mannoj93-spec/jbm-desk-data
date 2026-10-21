# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-21T04:33:38.812Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-21T00:25:00.000Z; last scored 2026-10-21T01:19:16.993Z. Stream start: 2026-10-01T00:00:00Z. Registered 342, confirmed 342, eligible 342. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 112 | 112 | 96 | 32 | 0 | 0 | 0 | 0 | -0.00542 | -0.00123 | 57/0/55 | 0.0123 | -0.1527 | unavailable (2) | -0.08293 | -0.07751 |
| 24h | 107 | 107 | 18 | 107 | 0 | 0 | 0 | 0 | -0.0066 | 0.00375 | 50/0/57 | 0.0217 | -0.1378 | unavailable (2) | -0.13877 | -0.13217 |
| 72h | 95 | 95 | 6 | 95 | 0 | 0 | 0 | 0 | -0.015 | -0.02225 | 64/0/31 | 0.0832 | -0.3277 | unavailable (2) | -0.08889 | -0.07389 |

Overlap (from actual windows): 4h: 32 of 112 windows overlap another; the largest disjoint subset has 96; 24h: 107 of 107 windows overlap another; the largest disjoint subset has 18; 72h: 95 of 95 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
