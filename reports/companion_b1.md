# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-10T08:11:40.852Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-10T04:25:00.000Z; last scored 2026-10-10T04:55:51.586Z. Stream start: 2026-10-01T00:00:00Z. Registered 147, confirmed 147, eligible 147. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 47 | 47 | 38 | 18 | 0 | 0 | 0 | 0 | -0.00286 | 0.01258 | 21/0/26 | 0.006 | -0.0674 | unavailable (1) | -0.06851 | -0.06565 |
| 24h | 42 | 42 | 8 | 42 | 0 | 0 | 0 | 0 | -0.00574 | 0.01751 | 19/0/23 | 0.0167 | -0.0998 | unavailable (1) | -0.11896 | -0.11322 |
| 72h | 30 | 30 | 2 | 30 | 0 | 0 | 0 | 0 | 0.00392 | 0.03369 | 13/0/17 | -0.021 | 0.0582 | unavailable (0) | -0.09169 | -0.09562 |

Overlap (from actual windows): 4h: 18 of 47 windows overlap another; the largest disjoint subset has 38; 24h: 42 of 42 windows overlap another; the largest disjoint subset has 8; 72h: 30 of 30 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
