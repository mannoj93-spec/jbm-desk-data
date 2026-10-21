# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-21T09:21:26.624Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-21T08:25:00.000Z; last scored 2026-10-21T09:15:48.409Z. Stream start: 2026-10-01T00:00:00Z. Registered 345, confirmed 345, eligible 345. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 114 | 114 | 98 | 32 | 0 | 0 | 0 | 0 | -0.00585 | -0.00254 | 59/0/55 | 0.0134 | -0.1656 | unavailable (2) | -0.08122 | -0.07537 |
| 24h | 109 | 109 | 18 | 109 | 0 | 0 | 0 | 0 | -0.007 | 0.00293 | 52/0/57 | 0.0233 | -0.1473 | unavailable (2) | -0.13544 | -0.12844 |
| 72h | 97 | 97 | 6 | 97 | 0 | 0 | 0 | 0 | -0.01529 | -0.02396 | 66/0/31 | 0.0832 | -0.3371 | unavailable (2) | -0.0839 | -0.06861 |

Overlap (from actual windows): 4h: 32 of 114 windows overlap another; the largest disjoint subset has 98; 24h: 109 of 109 windows overlap another; the largest disjoint subset has 18; 72h: 97 of 97 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
