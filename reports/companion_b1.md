# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-07T00:23:16.518Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-06T20:25:00.000Z; last scored 2026-10-06T20:53:51.341Z. Stream start: 2026-10-01T00:00:00Z. Registered 87, confirmed 87, eligible 87. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 27 | 27 | 22 | 10 | 0 | 0 | 0 | 0 | -0.00123 | 0.02081 | 11/0/16 | 0.0027 | -0.0248 | unavailable (0) | -0.10349 | -0.10227 |
| 24h | 22 | 22 | 4 | 22 | 0 | 0 | 0 | 0 | -0.01497 | -0.01957 | 12/0/10 | 0.0386 | -0.2094 | unavailable (0) | -0.15998 | -0.14501 |
| 72h | 16 | 16 | 1 | 16 | 0 | 0 | 0 | 0 | -0.02841 | -0.05405 | 11/0/5 | 0.1639 | -0.3987 | unavailable (0) | -0.14254 | -0.11414 |

Overlap (from actual windows): 4h: 10 of 27 windows overlap another; the largest disjoint subset has 22; 24h: 22 of 22 windows overlap another; the largest disjoint subset has 4; 72h: 16 of 16 windows overlap another; the largest disjoint subset has 1.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
