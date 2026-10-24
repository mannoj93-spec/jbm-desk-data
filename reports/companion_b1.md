# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-24T08:49:07.773Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-24T04:25:00.000Z; last scored 2026-10-24T05:00:59.987Z. Stream start: 2026-10-01T00:00:00Z. Registered 378, confirmed 378, eligible 378. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 131 | 124 | 108 | 32 | 7 | 0 | 0 | 0 | -0.00563 | -0.00254 | 64/0/60 | 0.0131 | -0.1625 | unavailable (2) | -0.07795 | -0.07232 |
| 24h | 126 | 123 | 21 | 123 | 3 | 0 | 0 | 0 | -0.00654 | 0.00293 | 59/0/64 | 0.0216 | -0.1428 | unavailable (2) | -0.12116 | -0.11462 |
| 72h | 114 | 114 | 7 | 114 | 0 | 0 | 0 | 0 | -0.0186 | -0.02851 | 81/0/33 | 0.1054 | -0.4201 | unavailable (2) | -0.07966 | -0.06105 |

Overlap (from actual windows): 4h: 32 of 124 windows overlap another; the largest disjoint subset has 108; 24h: 123 of 123 windows overlap another; the largest disjoint subset has 21; 72h: 114 of 114 windows overlap another; the largest disjoint subset has 7.

Not registered, by reason: rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
