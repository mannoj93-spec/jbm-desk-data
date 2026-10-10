# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-10T16:16:22.729Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-10T12:25:00.000Z; last scored 2026-10-10T12:57:07.328Z. Stream start: 2026-10-01T00:00:00Z. Registered 153, confirmed 153, eligible 153. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 49 | 49 | 39 | 20 | 0 | 0 | 0 | 0 | -0.0051 | 0.01115 | 23/0/26 | 0.0107 | -0.1189 | unavailable (1) | -0.08695 | -0.08185 |
| 24h | 44 | 44 | 8 | 44 | 0 | 0 | 0 | 0 | -0.00832 | 0.01401 | 21/0/23 | 0.0241 | -0.1449 | unavailable (1) | -0.12367 | -0.11535 |
| 72h | 32 | 32 | 2 | 32 | 0 | 0 | 0 | 0 | 0.00351 | 0.03369 | 14/0/18 | -0.0196 | 0.0526 | unavailable (0) | -0.09216 | -0.09567 |

Overlap (from actual windows): 4h: 20 of 49 windows overlap another; the largest disjoint subset has 39; 24h: 44 of 44 windows overlap another; the largest disjoint subset has 8; 72h: 32 of 32 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
