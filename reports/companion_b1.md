# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-04T05:45:43.387Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-04T04:25:00.000Z; last scored 2026-10-04T05:34:36.152Z. Stream start: 2026-10-01T00:00:00Z. Registered 48, confirmed 48, eligible 48. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 16 | 16 | 12 | 8 | 0 | 0 | 0 | 0 | -0.00981 | 0.01092 | 8/0/8 | 0.019 | -0.1648 | unavailable (0) | -0.17057 | -0.16075 |
| 24h | 14 | 14 | 3 | 14 | 0 | 0 | 0 | 0 | 0.00136 | 0.04329 | 5/0/9 | -0.0031 | 0.0164 | unavailable (0) | -0.22951 | -0.23087 |
| 72h | 2 | 2 | 1 | 2 | 0 | 0 | 0 | 0 | 0.07931 | 0.07931 | 0/0/2 | -0.6237 | 25.2351 | unavailable (0) | 0.12983 | 0.05052 |

Overlap (from actual windows): 4h: 8 of 16 windows overlap another; the largest disjoint subset has 12; 24h: 14 of 14 windows overlap another; the largest disjoint subset has 3; 72h: 2 of 2 windows overlap another; the largest disjoint subset has 1.

Not registered, by reason: rc1d-unavailable (12)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
