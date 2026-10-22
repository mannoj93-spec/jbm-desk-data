# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-22T12:35:40.289Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-22T08:25:00.000Z; last scored 2026-10-22T09:16:22.677Z. Stream start: 2026-10-01T00:00:00Z. Registered 363, confirmed 363, eligible 363. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 120 | 119 | 103 | 32 | 1 | 0 | 0 | 0 | -0.0051 | -0.00031 | 60/0/59 | 0.0117 | -0.1457 | unavailable (2) | -0.08133 | -0.07623 |
| 24h | 115 | 115 | 19 | 115 | 0 | 0 | 0 | 0 | -0.00671 | 0.00375 | 54/0/61 | 0.0232 | -0.1432 | unavailable (2) | -0.13112 | -0.1244 |
| 72h | 103 | 103 | 6 | 103 | 0 | 0 | 0 | 0 | -0.01673 | -0.02693 | 72/0/31 | 0.0913 | -0.3766 | unavailable (2) | -0.07972 | -0.06299 |

Overlap (from actual windows): 4h: 32 of 119 windows overlap another; the largest disjoint subset has 103; 24h: 115 of 115 windows overlap another; the largest disjoint subset has 19; 72h: 103 of 103 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
