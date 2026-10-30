# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-30T12:21:47.709Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-30T08:25:00.000Z; last scored 2026-10-30T08:54:27.492Z. Stream start: 2026-10-01T00:00:00Z. Registered 477, confirmed 477, eligible 477. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 168 | 157 | 139 | 36 | 11 | 0 | 0 | 0 | -0.00448 | -0.00216 | 81/0/76 | 0.0105 | -0.1363 | unavailable (3) | -0.06498 | -0.06051 |
| 24h | 163 | 154 | 27 | 154 | 9 | 0 | 0 | 0 | -0.00502 | 0.00103 | 76/0/78 | 0.0161 | -0.1167 | unavailable (3) | -0.08918 | -0.08416 |
| 72h | 151 | 143 | 9 | 143 | 8 | 0 | 0 | 0 | -0.01498 | -0.0211 | 100/0/43 | 0.0651 | -0.3573 | unavailable (3) | -0.0573 | -0.04232 |

Overlap (from actual windows): 4h: 36 of 157 windows overlap another; the largest disjoint subset has 139; 24h: 154 of 154 windows overlap another; the largest disjoint subset has 27; 72h: 143 of 143 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (12); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
