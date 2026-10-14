# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-14T05:18:29.742Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-14T04:25:00.000Z; last scored 2026-10-14T05:09:43.669Z. Stream start: 2026-10-01T00:00:00Z. Registered 216, confirmed 216, eligible 216. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 71 | 71 | 58 | 26 | 0 | 0 | 0 | 0 | -0.00508 | 0.00242 | 35/0/36 | 0.0118 | -0.1367 | unavailable (1) | -0.10711 | -0.10202 |
| 24h | 66 | 66 | 11 | 66 | 0 | 0 | 0 | 0 | -0.0119 | -0.00379 | 34/0/32 | 0.0335 | -0.2333 | unavailable (1) | -0.15708 | -0.14518 |
| 72h | 54 | 54 | 4 | 54 | 0 | 0 | 0 | 0 | -0.00683 | -0.01532 | 30/0/24 | 0.0386 | -0.123 | unavailable (1) | -0.11165 | -0.10483 |

Overlap (from actual windows): 4h: 26 of 71 windows overlap another; the largest disjoint subset has 58; 24h: 66 of 66 windows overlap another; the largest disjoint subset has 11; 72h: 54 of 54 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
