# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-11T00:17:38.554Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-10T20:20:00.000Z; last scored 2026-10-10T20:53:44.227Z. Stream start: 2026-10-01T00:00:00Z. Registered 159, confirmed 159, eligible 159. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 51 | 51 | 40 | 22 | 0 | 0 | 0 | 0 | -0.00503 | 0.01115 | 24/0/27 | 0.0108 | -0.1181 | unavailable (1) | -0.10801 | -0.10298 |
| 24h | 46 | 46 | 8 | 46 | 0 | 0 | 0 | 0 | -0.01133 | 0.00109 | 23/0/23 | 0.0322 | -0.1955 | unavailable (1) | -0.1368 | -0.12547 |
| 72h | 34 | 34 | 2 | 34 | 0 | 0 | 0 | 0 | 0.00062 | 0.01991 | 16/0/18 | -0.0036 | 0.0094 | unavailable (0) | -0.09884 | -0.09946 |

Overlap (from actual windows): 4h: 22 of 51 windows overlap another; the largest disjoint subset has 40; 24h: 46 of 46 windows overlap another; the largest disjoint subset has 8; 72h: 34 of 34 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
