# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-20T13:31:18.756Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-20T12:25:00.000Z; last scored 2026-10-20T13:22:32.855Z. Stream start: 2026-10-01T00:00:00Z. Registered 330, confirmed 330, eligible 330. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 109 | 109 | 93 | 32 | 0 | 0 | 0 | 0 | -0.00515 | -0.00031 | 55/0/54 | 0.0119 | -0.1436 | unavailable (2) | -0.08955 | -0.08441 |
| 24h | 104 | 104 | 18 | 104 | 0 | 0 | 0 | 0 | -0.00675 | 0.00334 | 49/0/55 | 0.0217 | -0.1397 | unavailable (2) | -0.14128 | -0.13454 |
| 72h | 92 | 92 | 6 | 92 | 0 | 0 | 0 | 0 | -0.01483 | -0.0231 | 61/0/31 | 0.0835 | -0.3189 | unavailable (2) | -0.09321 | -0.07838 |

Overlap (from actual windows): 4h: 32 of 109 windows overlap another; the largest disjoint subset has 93; 24h: 104 of 104 windows overlap another; the largest disjoint subset has 18; 72h: 92 of 92 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
