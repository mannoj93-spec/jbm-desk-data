# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-14T00:32:56.066Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-13T20:25:00.000Z; last scored 2026-10-13T21:08:34.307Z. Stream start: 2026-10-01T00:00:00Z. Registered 213, confirmed 213, eligible 213. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 69 | 69 | 56 | 26 | 0 | 0 | 0 | 0 | -0.00513 | 0.00242 | 34/0/35 | 0.0119 | -0.1368 | unavailable (1) | -0.11222 | -0.1071 |
| 24h | 64 | 64 | 11 | 64 | 0 | 0 | 0 | 0 | -0.01181 | -0.00379 | 33/0/31 | 0.0338 | -0.2296 | unavailable (1) | -0.16413 | -0.15233 |
| 72h | 52 | 52 | 3 | 52 | 0 | 0 | 0 | 0 | -0.0064 | -0.015 | 28/0/24 | 0.0352 | -0.1132 | unavailable (1) | -0.11316 | -0.10677 |

Overlap (from actual windows): 4h: 26 of 69 windows overlap another; the largest disjoint subset has 56; 24h: 64 of 64 windows overlap another; the largest disjoint subset has 11; 72h: 52 of 52 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
