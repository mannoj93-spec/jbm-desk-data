# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-11T20:22:56.988Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-11T16:25:00.000Z; last scored 2026-10-11T16:55:06.087Z. Stream start: 2026-10-01T00:00:00Z. Registered 174, confirmed 174, eligible 174. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 56 | 56 | 45 | 22 | 0 | 0 | 0 | 0 | -0.00507 | 0.00698 | 27/0/29 | 0.011 | -0.1243 | unavailable (1) | -0.12526 | -0.12019 |
| 24h | 51 | 51 | 9 | 51 | 0 | 0 | 0 | 0 | -0.01554 | -0.02546 | 28/0/23 | 0.0418 | -0.274 | unavailable (1) | -0.17447 | -0.15893 |
| 72h | 39 | 39 | 3 | 39 | 0 | 0 | 0 | 0 | -0.00122 | -0.01045 | 20/0/19 | 0.0078 | -0.0196 | unavailable (0) | -0.11203 | -0.11082 |

Overlap (from actual windows): 4h: 22 of 56 windows overlap another; the largest disjoint subset has 45; 24h: 51 of 51 windows overlap another; the largest disjoint subset has 9; 72h: 39 of 39 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
