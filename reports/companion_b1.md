# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-13T00:25:47.121Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-12T20:25:00.000Z; last scored 2026-10-12T20:58:13.982Z. Stream start: 2026-10-01T00:00:00Z. Registered 195, confirmed 195, eligible 195. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 63 | 63 | 50 | 26 | 0 | 0 | 0 | 0 | -0.00436 | 0.00418 | 30/0/33 | 0.0103 | -0.1131 | unavailable (1) | -0.11843 | -0.11407 |
| 24h | 58 | 58 | 10 | 58 | 0 | 0 | 0 | 0 | -0.01323 | -0.01391 | 31/0/27 | 0.0391 | -0.2457 | unavailable (1) | -0.16316 | -0.14994 |
| 72h | 46 | 46 | 3 | 46 | 0 | 0 | 0 | 0 | -0.00845 | -0.03046 | 27/0/19 | 0.0425 | -0.1415 | unavailable (1) | -0.11943 | -0.11098 |

Overlap (from actual windows): 4h: 26 of 63 windows overlap another; the largest disjoint subset has 50; 24h: 58 of 58 windows overlap another; the largest disjoint subset has 10; 72h: 46 of 46 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
