# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-27T12:21:28.045Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-27T08:25:00.000Z; last scored 2026-10-27T09:31:08.299Z. Stream start: 2026-10-01T00:00:00Z. Registered 432, confirmed 432, eligible 432. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 150 | 142 | 124 | 36 | 8 | 0 | 0 | 0 | -0.0053 | -0.00299 | 74/0/68 | 0.0125 | -0.1559 | unavailable (3) | -0.07144 | -0.06614 |
| 24h | 145 | 138 | 24 | 138 | 7 | 0 | 0 | 0 | -0.00578 | 0.00167 | 68/0/70 | 0.0188 | -0.1279 | unavailable (3) | -0.09759 | -0.09181 |
| 72h | 133 | 126 | 8 | 126 | 7 | 0 | 0 | 0 | -0.01623 | -0.02657 | 88/0/38 | 0.087 | -0.3673 | unavailable (3) | -0.07684 | -0.06061 |

Overlap (from actual windows): 4h: 36 of 142 windows overlap another; the largest disjoint subset has 124; 24h: 138 of 138 windows overlap another; the largest disjoint subset has 24; 72h: 126 of 126 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: late (3); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
