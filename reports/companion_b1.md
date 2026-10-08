# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-08T12:18:06.455Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-08T08:25:00.000Z; last scored 2026-10-08T08:57:02.966Z. Stream start: 2026-10-01T00:00:00Z. Registered 114, confirmed 114, eligible 114. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 36 | 36 | 29 | 14 | 0 | 0 | 0 | 0 | -0.00047 | 0.01895 | 15/0/21 | 0.001 | -0.0106 | unavailable (0) | -0.06862 | -0.06815 |
| 24h | 31 | 31 | 6 | 31 | 0 | 0 | 0 | 0 | -0.00794 | 0.0182 | 15/0/16 | 0.0222 | -0.1237 | unavailable (0) | -0.13607 | -0.12813 |
| 72h | 20 | 20 | 2 | 20 | 0 | 0 | 0 | 0 | -0.01681 | -0.03997 | 12/0/8 | 0.113 | -0.2447 | unavailable (0) | -0.10345 | -0.08664 |

Overlap (from actual windows): 4h: 14 of 36 windows overlap another; the largest disjoint subset has 29; 24h: 31 of 31 windows overlap another; the largest disjoint subset has 6; 72h: 20 of 20 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
