# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-11T04:22:28.136Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-11T00:25:00.000Z; last scored 2026-10-11T01:01:47.024Z. Stream start: 2026-10-01T00:00:00Z. Registered 162, confirmed 162, eligible 162. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 52 | 52 | 41 | 22 | 0 | 0 | 0 | 0 | -0.00542 | 0.01099 | 25/0/27 | 0.0116 | -0.1282 | unavailable (1) | -0.12112 | -0.1157 |
| 24h | 47 | 47 | 8 | 47 | 0 | 0 | 0 | 0 | -0.01271 | -0.00903 | 24/0/23 | 0.0359 | -0.2188 | unavailable (1) | -0.14799 | -0.13528 |
| 72h | 35 | 35 | 3 | 35 | 0 | 0 | 0 | 0 | -0.00041 | 0.01508 | 17/0/18 | 0.0024 | -0.0063 | unavailable (0) | -0.10323 | -0.10282 |

Overlap (from actual windows): 4h: 22 of 52 windows overlap another; the largest disjoint subset has 41; 24h: 47 of 47 windows overlap another; the largest disjoint subset has 8; 72h: 35 of 35 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
