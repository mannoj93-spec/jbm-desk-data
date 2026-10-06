# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-06T00:23:28.512Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-05T20:55:00.000Z; last scored 2026-10-05T21:33:21.593Z. Stream start: 2026-10-01T00:00:00Z. Registered 69, confirmed 69, eligible 69. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 22 | 22 | 17 | 10 | 0 | 0 | 0 | 0 | -0.00639 | 0.01396 | 10/0/12 | 0.0128 | -0.1219 | unavailable (0) | -0.11315 | -0.10675 |
| 24h | 17 | 17 | 4 | 16 | 0 | 0 | 0 | 0 | -0.00785 | 0.03168 | 7/0/10 | 0.0188 | -0.0976 | unavailable (0) | -0.24819 | -0.24035 |
| 72h | 12 | 12 | 1 | 12 | 0 | 0 | 0 | 0 | -0.01308 | -0.04696 | 7/0/5 | 0.1203 | -0.1734 | unavailable (0) | -0.13581 | -0.12273 |

Overlap (from actual windows): 4h: 10 of 22 windows overlap another; the largest disjoint subset has 17; 24h: 16 of 17 windows overlap another; the largest disjoint subset has 4; 72h: 12 of 12 windows overlap another; the largest disjoint subset has 1.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
