# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-03T08:16:04.339Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-03T04:25:00.000Z; last scored 2026-10-03T04:53:25.929Z. Stream start: 2026-10-01T00:00:00Z. Registered 45, confirmed 45, eligible 45. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 13 | 13 | 9 | 8 | 0 | 0 | 0 | 0 | -0.00084 | 0.03366 | 6/0/7 | 0.0016 | -0.0158 | unavailable (0) | -0.09689 | -0.09604 |
| 24h | 8 | 8 | 2 | 8 | 0 | 0 | 0 | 0 | 0.04306 | 0.04868 | 1/0/7 | -0.1421 | 1.8071 | unavailable (0) | -0.23893 | -0.28198 |
| 72h | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | —/—/— | — | — | unavailable (0) | — | — |

Overlap (from actual windows): 4h: 8 of 13 windows overlap another; the largest disjoint subset has 9; 24h: 8 of 8 windows overlap another; the largest disjoint subset has 2.

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
