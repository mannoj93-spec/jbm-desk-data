# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-13T12:18:27.728Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-13T08:25:00.000Z; last scored 2026-10-13T09:00:23.757Z. Stream start: 2026-10-01T00:00:00Z. Registered 204, confirmed 204, eligible 204. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 66 | 66 | 53 | 26 | 0 | 0 | 0 | 0 | -0.00432 | 0.00472 | 31/0/35 | 0.0098 | -0.1138 | unavailable (1) | -0.11949 | -0.11516 |
| 24h | 61 | 61 | 11 | 61 | 0 | 0 | 0 | 0 | -0.01269 | -0.00501 | 33/0/28 | 0.0368 | -0.2416 | unavailable (1) | -0.1639 | -0.1512 |
| 72h | 49 | 49 | 3 | 49 | 0 | 0 | 0 | 0 | -0.00668 | -0.02225 | 27/0/22 | 0.0353 | -0.1147 | unavailable (1) | -0.11684 | -0.11016 |

Overlap (from actual windows): 4h: 26 of 66 windows overlap another; the largest disjoint subset has 53; 24h: 61 of 61 windows overlap another; the largest disjoint subset has 11; 72h: 49 of 49 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
