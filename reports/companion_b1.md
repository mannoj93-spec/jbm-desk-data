# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-22T01:23:43.848Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-22T00:25:00.000Z; last scored 2026-10-22T01:19:16.829Z. Stream start: 2026-10-01T00:00:00Z. Registered 354, confirmed 354, eligible 354. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 118 | 117 | 101 | 32 | 1 | 0 | 0 | 0 | -0.00558 | -0.00216 | 60/0/57 | 0.0128 | -0.1589 | unavailable (2) | -0.07967 | -0.07409 |
| 24h | 113 | 113 | 19 | 113 | 0 | 0 | 0 | 0 | -0.00741 | 0.00293 | 54/0/59 | 0.0254 | -0.1577 | unavailable (2) | -0.13399 | -0.12658 |
| 72h | 101 | 101 | 6 | 101 | 0 | 0 | 0 | 0 | -0.01615 | -0.02686 | 70/0/31 | 0.0883 | -0.3615 | unavailable (2) | -0.08301 | -0.06686 |

Overlap (from actual windows): 4h: 32 of 117 windows overlap another; the largest disjoint subset has 101; 24h: 113 of 113 windows overlap another; the largest disjoint subset has 19; 72h: 101 of 101 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
