# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-30T06:33:39.966Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-30T04:25:00.000Z; last scored 2026-10-30T05:31:15.020Z. Stream start: 2026-10-01T00:00:00Z. Registered 471, confirmed 471, eligible 471. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 167 | 157 | 139 | 36 | 10 | 0 | 0 | 0 | -0.00448 | -0.00216 | 81/0/76 | 0.0105 | -0.1363 | unavailable (3) | -0.06498 | -0.06051 |
| 24h | 162 | 153 | 26 | 153 | 9 | 0 | 0 | 0 | -0.00524 | 0.00074 | 76/0/77 | 0.0171 | -0.1216 | unavailable (3) | -0.08794 | -0.0827 |
| 72h | 150 | 142 | 9 | 142 | 8 | 0 | 0 | 0 | -0.01522 | -0.0216 | 100/0/42 | 0.0663 | -0.3627 | unavailable (3) | -0.05594 | -0.04072 |

Overlap (from actual windows): 4h: 36 of 157 windows overlap another; the largest disjoint subset has 139; 24h: 153 of 153 windows overlap another; the largest disjoint subset has 26; 72h: 142 of 142 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (12); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
