# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-08T16:21:46.139Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-08T12:25:00.000Z; last scored 2026-10-08T13:02:25.476Z. Stream start: 2026-10-01T00:00:00Z. Registered 117, confirmed 117, eligible 117. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 37 | 37 | 30 | 14 | 0 | 0 | 0 | 0 | -0.00012 | 0.0171 | 15/0/22 | 0.0003 | -0.0027 | unavailable (0) | -0.07369 | -0.07357 |
| 24h | 32 | 32 | 6 | 32 | 0 | 0 | 0 | 0 | -0.00896 | 0.00459 | 16/0/16 | 0.0251 | -0.1413 | unavailable (0) | -0.13251 | -0.12356 |
| 72h | 21 | 21 | 2 | 21 | 0 | 0 | 0 | 0 | -0.01303 | -0.03399 | 12/0/9 | 0.0911 | -0.1884 | unavailable (0) | -0.09702 | -0.08399 |

Overlap (from actual windows): 4h: 14 of 37 windows overlap another; the largest disjoint subset has 30; 24h: 32 of 32 windows overlap another; the largest disjoint subset has 6; 72h: 21 of 21 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
