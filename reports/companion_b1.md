# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-20T09:21:44.538Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-20T08:25:00.000Z; last scored 2026-10-20T09:15:46.420Z. Stream start: 2026-10-01T00:00:00Z. Registered 327, confirmed 327, eligible 327. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 108 | 108 | 92 | 32 | 0 | 0 | 0 | 0 | -0.00503 | 0.00106 | 54/0/54 | 0.0117 | -0.1399 | unavailable (2) | -0.09089 | -0.08586 |
| 24h | 103 | 103 | 17 | 103 | 0 | 0 | 0 | 0 | -0.00651 | 0.00375 | 48/0/55 | 0.021 | -0.1344 | unavailable (2) | -0.14343 | -0.13692 |
| 72h | 91 | 91 | 6 | 91 | 0 | 0 | 0 | 0 | -0.01469 | -0.02225 | 60/0/31 | 0.0833 | -0.3141 | unavailable (2) | -0.0938 | -0.07912 |

Overlap (from actual windows): 4h: 32 of 108 windows overlap another; the largest disjoint subset has 92; 24h: 103 of 103 windows overlap another; the largest disjoint subset has 17; 72h: 91 of 91 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
