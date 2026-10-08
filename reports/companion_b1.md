# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-08T17:04:20.937Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-08T16:25:00.000Z; last scored 2026-10-08T17:00:18.027Z. Stream start: 2026-10-01T00:00:00Z. Registered 117, confirmed 117, eligible 117. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 38 | 38 | 31 | 14 | 0 | 0 | 0 | 0 | 0.00018 | 0.01548 | 15/0/23 | -0.0004 | 0.004 | unavailable (0) | -0.07731 | -0.07748 |
| 24h | 33 | 33 | 6 | 33 | 0 | 0 | 0 | 0 | -0.00768 | 0.0182 | 16/0/17 | 0.0217 | -0.1222 | unavailable (0) | -0.13498 | -0.12731 |
| 72h | 22 | 22 | 2 | 22 | 0 | 0 | 0 | 0 | -0.00911 | -0.02222 | 12/0/10 | 0.0618 | -0.1302 | unavailable (0) | -0.09607 | -0.08696 |

Overlap (from actual windows): 4h: 14 of 38 windows overlap another; the largest disjoint subset has 31; 24h: 33 of 33 windows overlap another; the largest disjoint subset has 6; 72h: 22 of 22 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
