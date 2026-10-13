# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-13T16:21:57.714Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-13T12:25:00.000Z; last scored 2026-10-13T13:08:06.552Z. Stream start: 2026-10-01T00:00:00Z. Registered 207, confirmed 207, eligible 207. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 67 | 67 | 54 | 26 | 0 | 0 | 0 | 0 | -0.00429 | 0.00418 | 32/0/35 | 0.0099 | -0.1138 | unavailable (1) | -0.1221 | -0.11781 |
| 24h | 62 | 62 | 11 | 62 | 0 | 0 | 0 | 0 | -0.01244 | -0.00449 | 33/0/29 | 0.0359 | -0.2386 | unavailable (1) | -0.166 | -0.15356 |
| 72h | 50 | 50 | 3 | 50 | 0 | 0 | 0 | 0 | -0.00641 | -0.01955 | 27/0/23 | 0.0343 | -0.1112 | unavailable (1) | -0.1154 | -0.10899 |

Overlap (from actual windows): 4h: 26 of 67 windows overlap another; the largest disjoint subset has 54; 24h: 62 of 62 windows overlap another; the largest disjoint subset has 11; 72h: 50 of 50 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
