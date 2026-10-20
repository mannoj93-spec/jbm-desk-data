# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-20T17:24:33.788Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-20T16:25:00.000Z; last scored 2026-10-20T17:16:28.208Z. Stream start: 2026-10-01T00:00:00Z. Registered 333, confirmed 333, eligible 333. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 110 | 110 | 94 | 32 | 0 | 0 | 0 | 0 | -0.00501 | 0.00106 | 55/0/55 | 0.0114 | -0.1404 | unavailable (2) | -0.08732 | -0.08231 |
| 24h | 105 | 105 | 18 | 105 | 0 | 0 | 0 | 0 | -0.00712 | 0.00293 | 50/0/55 | 0.023 | -0.1477 | unavailable (2) | -0.13994 | -0.13282 |
| 72h | 93 | 93 | 6 | 93 | 0 | 0 | 0 | 0 | -0.0149 | -0.02225 | 62/0/31 | 0.0836 | -0.322 | unavailable (2) | -0.09263 | -0.07774 |

Overlap (from actual windows): 4h: 32 of 110 windows overlap another; the largest disjoint subset has 94; 24h: 105 of 105 windows overlap another; the largest disjoint subset has 18; 72h: 93 of 93 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
