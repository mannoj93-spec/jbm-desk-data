# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-19T17:19:20.576Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-19T16:25:00.000Z; last scored 2026-10-19T17:11:10.577Z. Stream start: 2026-10-01T00:00:00Z. Registered 315, confirmed 315, eligible 315. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 104 | 104 | 88 | 32 | 0 | 0 | 0 | 0 | -0.00559 | -0.00123 | 53/0/51 | 0.0129 | -0.1541 | unavailable (2) | -0.09652 | -0.09093 |
| 24h | 99 | 99 | 17 | 99 | 0 | 0 | 0 | 0 | -0.00617 | 0.00512 | 45/0/54 | 0.0197 | -0.1253 | unavailable (2) | -0.1509 | -0.14474 |
| 72h | 87 | 87 | 5 | 87 | 0 | 0 | 0 | 0 | -0.0135 | -0.02073 | 56/0/31 | 0.0792 | -0.2844 | unavailable (2) | -0.0972 | -0.0837 |

Overlap (from actual windows): 4h: 32 of 104 windows overlap another; the largest disjoint subset has 88; 24h: 99 of 99 windows overlap another; the largest disjoint subset has 17; 72h: 87 of 87 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
