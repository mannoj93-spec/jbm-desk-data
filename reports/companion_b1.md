# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-24T03:49:15.271Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-24T00:25:00.000Z; last scored 2026-10-24T01:07:52.366Z. Stream start: 2026-10-01T00:00:00Z. Registered 372, confirmed 372, eligible 372. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 130 | 123 | 107 | 32 | 7 | 0 | 0 | 0 | -0.00527 | -0.00216 | 63/0/60 | 0.0122 | -0.1525 | unavailable (2) | -0.07656 | -0.0713 |
| 24h | 125 | 123 | 21 | 123 | 2 | 0 | 0 | 0 | -0.00654 | 0.00293 | 59/0/64 | 0.0216 | -0.1428 | unavailable (2) | -0.12116 | -0.11462 |
| 72h | 113 | 113 | 7 | 113 | 0 | 0 | 0 | 0 | -0.01925 | -0.02893 | 81/0/32 | 0.1084 | -0.4381 | unavailable (2) | -0.0789 | -0.05965 |

Overlap (from actual windows): 4h: 32 of 123 windows overlap another; the largest disjoint subset has 107; 24h: 123 of 123 windows overlap another; the largest disjoint subset has 21; 72h: 113 of 113 windows overlap another; the largest disjoint subset has 7.

Not registered, by reason: rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
