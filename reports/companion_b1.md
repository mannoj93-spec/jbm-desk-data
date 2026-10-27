# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-27T08:22:50.067Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-27T04:25:00.000Z; last scored 2026-10-27T04:46:05.064Z. Stream start: 2026-10-01T00:00:00Z. Registered 429, confirmed 429, eligible 429. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 149 | 141 | 124 | 34 | 8 | 0 | 0 | 0 | -0.00527 | -0.00293 | 73/0/68 | 0.0124 | -0.1543 | unavailable (3) | -0.07246 | -0.06719 |
| 24h | 144 | 137 | 24 | 137 | 7 | 0 | 0 | 0 | -0.0058 | 0.00186 | 67/0/70 | 0.019 | -0.1278 | unavailable (3) | -0.09941 | -0.0936 |
| 72h | 132 | 125 | 8 | 125 | 7 | 0 | 0 | 0 | -0.01626 | -0.02686 | 87/0/38 | 0.0887 | -0.3665 | unavailable (2) | -0.07729 | -0.06103 |

Overlap (from actual windows): 4h: 34 of 141 windows overlap another; the largest disjoint subset has 124; 24h: 137 of 137 windows overlap another; the largest disjoint subset has 24; 72h: 125 of 125 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: late (3); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
