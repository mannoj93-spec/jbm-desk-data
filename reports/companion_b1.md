# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-31T12:22:30.270Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-31T08:25:00.000Z; last scored 2026-10-31T09:01:24.179Z. Stream start: 2026-10-01T00:00:00Z. Registered 489, confirmed 489, eligible 489. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 174 | 161 | 143 | 36 | 13 | 0 | 0 | 0 | -0.00493 | -0.00293 | 84/0/77 | 0.0117 | -0.1493 | unavailable (3) | -0.06777 | -0.06283 |
| 24h | 169 | 158 | 28 | 158 | 11 | 0 | 0 | 0 | -0.00465 | 0.00132 | 77/0/81 | 0.0146 | -0.1076 | unavailable (3) | -0.09463 | -0.08998 |
| 72h | 157 | 149 | 9 | 149 | 8 | 0 | 0 | 0 | -0.01373 | -0.01732 | 100/0/49 | 0.0582 | -0.3308 | unavailable (3) | -0.06235 | -0.04862 |

Overlap (from actual windows): 4h: 36 of 161 windows overlap another; the largest disjoint subset has 143; 24h: 158 of 158 windows overlap another; the largest disjoint subset has 28; 72h: 149 of 149 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (18); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
