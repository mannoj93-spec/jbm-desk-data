# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-09T04:24:24.230Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-09T00:25:00.000Z; last scored 2026-10-09T01:04:27.868Z. Stream start: 2026-10-01T00:00:00Z. Registered 126, confirmed 126, eligible 126. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 40 | 40 | 33 | 14 | 0 | 0 | 0 | 0 | -0.00014 | 0.01548 | 16/0/24 | 0.0003 | -0.0033 | unavailable (0) | -0.07396 | -0.07382 |
| 24h | 35 | 35 | 7 | 35 | 0 | 0 | 0 | 0 | -0.0056 | 0.02306 | 16/0/19 | 0.0157 | -0.091 | unavailable (0) | -0.13578 | -0.13018 |
| 72h | 23 | 23 | 2 | 23 | 0 | 0 | 0 | 0 | -0.00602 | -0.01045 | 12/0/11 | 0.0382 | -0.0862 | unavailable (0) | -0.09581 | -0.08979 |

Overlap (from actual windows): 4h: 14 of 40 windows overlap another; the largest disjoint subset has 33; 24h: 35 of 35 windows overlap another; the largest disjoint subset has 7; 72h: 23 of 23 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
