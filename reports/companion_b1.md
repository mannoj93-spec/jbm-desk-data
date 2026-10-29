# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-29T21:03:49.629Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-29T16:25:00.000Z; last scored 2026-10-29T17:16:54.911Z. Stream start: 2026-10-01T00:00:00Z. Registered 471, confirmed 471, eligible 471. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 164 | 155 | 137 | 36 | 9 | 0 | 0 | 0 | -0.00495 | -0.00293 | 81/0/74 | 0.0117 | -0.1512 | unavailable (3) | -0.06151 | -0.05655 |
| 24h | 159 | 150 | 26 | 150 | 9 | 0 | 0 | 0 | -0.00569 | -0.00256 | 76/0/74 | 0.0189 | -0.1311 | unavailable (3) | -0.0842 | -0.07851 |
| 72h | 147 | 139 | 9 | 139 | 8 | 0 | 0 | 0 | -0.01567 | -0.0221 | 99/0/40 | 0.0691 | -0.3718 | unavailable (3) | -0.05532 | -0.03965 |

Overlap (from actual windows): 4h: 36 of 155 windows overlap another; the largest disjoint subset has 137; 24h: 150 of 150 windows overlap another; the largest disjoint subset has 26; 72h: 139 of 139 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (6); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
