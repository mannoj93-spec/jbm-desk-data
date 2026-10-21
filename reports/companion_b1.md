# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-21T00:19:16.289Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-20T20:25:00.000Z; last scored 2026-10-20T21:11:13.441Z. Stream start: 2026-10-01T00:00:00Z. Registered 339, confirmed 339, eligible 339. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 111 | 111 | 95 | 32 | 0 | 0 | 0 | 0 | -0.00521 | -0.00031 | 56/0/55 | 0.0118 | -0.1463 | unavailable (2) | -0.08386 | -0.07865 |
| 24h | 106 | 106 | 18 | 106 | 0 | 0 | 0 | 0 | -0.00691 | 0.00334 | 50/0/56 | 0.0225 | -0.1439 | unavailable (2) | -0.13957 | -0.13266 |
| 72h | 94 | 94 | 6 | 94 | 0 | 0 | 0 | 0 | -0.01487 | -0.02217 | 63/0/31 | 0.0832 | -0.3232 | unavailable (2) | -0.09137 | -0.0765 |

Overlap (from actual windows): 4h: 32 of 111 windows overlap another; the largest disjoint subset has 95; 24h: 106 of 106 windows overlap another; the largest disjoint subset has 18; 72h: 94 of 94 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
