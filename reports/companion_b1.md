# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-13T04:20:31.504Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-13T00:25:00.000Z; last scored 2026-10-13T01:06:05.084Z. Stream start: 2026-10-01T00:00:00Z. Registered 198, confirmed 198, eligible 198. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 64 | 64 | 51 | 26 | 0 | 0 | 0 | 0 | -0.00414 | 0.00472 | 30/0/34 | 0.0096 | -0.1081 | unavailable (1) | -0.11878 | -0.11464 |
| 24h | 59 | 59 | 10 | 59 | 0 | 0 | 0 | 0 | -0.01306 | -0.00903 | 32/0/27 | 0.0384 | -0.2447 | unavailable (1) | -0.16189 | -0.14883 |
| 72h | 47 | 47 | 3 | 47 | 0 | 0 | 0 | 0 | -0.00779 | -0.02693 | 27/0/20 | 0.0401 | -0.1316 | unavailable (1) | -0.12002 | -0.11223 |

Overlap (from actual windows): 4h: 26 of 64 windows overlap another; the largest disjoint subset has 51; 24h: 59 of 59 windows overlap another; the largest disjoint subset has 10; 72h: 47 of 47 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
