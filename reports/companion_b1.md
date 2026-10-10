# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-10T01:07:43.496Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-10T00:20:00.000Z; last scored 2026-10-10T01:02:38.223Z. Stream start: 2026-10-01T00:00:00Z. Registered 141, confirmed 141, eligible 141. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 46 | 46 | 37 | 18 | 0 | 0 | 0 | 0 | -0.00149 | 0.01322 | 20/0/26 | 0.0032 | -0.0357 | unavailable (1) | -0.06126 | -0.05977 |
| 24h | 41 | 41 | 7 | 41 | 0 | 0 | 0 | 0 | -0.00444 | 0.0182 | 18/0/23 | 0.013 | -0.0771 | unavailable (0) | -0.12259 | -0.11815 |
| 72h | 29 | 29 | 2 | 29 | 0 | 0 | 0 | 0 | 0.00658 | 0.04264 | 12/0/17 | -0.0345 | 0.0982 | unavailable (0) | -0.09474 | -0.10132 |

Overlap (from actual windows): 4h: 18 of 46 windows overlap another; the largest disjoint subset has 37; 24h: 41 of 41 windows overlap another; the largest disjoint subset has 7; 72h: 29 of 29 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
