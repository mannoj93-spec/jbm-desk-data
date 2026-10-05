# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-05T04:18:15.115Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-05T00:55:00.000Z; last scored 2026-10-05T01:00:30.182Z. Stream start: 2026-10-01T00:00:00Z. Registered 57, confirmed 57, eligible 57. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 17 | 17 | 13 | 8 | 0 | 0 | 0 | 0 | -0.00801 | 0.02081 | 8/0/9 | 0.0151 | -0.1378 | unavailable (0) | -0.14097 | -0.13296 |
| 24h | 16 | 16 | 3 | 16 | 0 | 0 | 0 | 0 | -0.00947 | 0.03725 | 7/0/9 | 0.0218 | -0.1146 | unavailable (0) | -0.26719 | -0.25771 |
| 72h | 7 | 7 | 1 | 7 | 0 | 0 | 0 | 0 | 0.03323 | 0.07655 | 2/0/5 | -0.4837 | 0.52 | unavailable (0) | -0.08537 | -0.1186 |

Overlap (from actual windows): 4h: 8 of 17 windows overlap another; the largest disjoint subset has 13; 24h: 16 of 16 windows overlap another; the largest disjoint subset has 3; 72h: 7 of 7 windows overlap another; the largest disjoint subset has 1.

Not registered, by reason: rc1d-unavailable (21)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
