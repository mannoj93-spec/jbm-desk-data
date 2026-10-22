# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-22T05:21:29.581Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-22T04:25:00.000Z; last scored 2026-10-22T05:15:38.643Z. Stream start: 2026-10-01T00:00:00Z. Registered 357, confirmed 357, eligible 357. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 119 | 118 | 102 | 32 | 1 | 0 | 0 | 0 | -0.00536 | -0.00123 | 60/0/58 | 0.0122 | -0.1529 | unavailable (2) | -0.07952 | -0.07417 |
| 24h | 114 | 114 | 19 | 114 | 0 | 0 | 0 | 0 | -0.00708 | 0.00334 | 54/0/60 | 0.0244 | -0.1508 | unavailable (2) | -0.13263 | -0.12555 |
| 72h | 102 | 102 | 6 | 102 | 0 | 0 | 0 | 0 | -0.01643 | -0.0269 | 71/0/31 | 0.0898 | -0.3689 | unavailable (2) | -0.08139 | -0.06496 |

Overlap (from actual windows): 4h: 32 of 118 windows overlap another; the largest disjoint subset has 102; 24h: 114 of 114 windows overlap another; the largest disjoint subset has 19; 72h: 102 of 102 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
