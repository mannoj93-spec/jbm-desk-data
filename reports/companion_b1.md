# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-11-11T23:09:35.282Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-11-11T16:25:00.000Z; last scored 2026-11-11T17:01:38.077Z. Stream start: 2026-10-01T00:00:00Z. Registered 525, confirmed 525, eligible 525. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 209 | 175 | 155 | 40 | 34 | 0 | 0 | 0 | -0.00608 | -0.00306 | 94/0/81 | 0.0147 | -0.1841 | unavailable (4) | -0.08963 | -0.08355 |
| 24h | 204 | 174 | 32 | 174 | 30 | 0 | 0 | 0 | -0.00786 | -0.00349 | 92/0/82 | 0.0235 | -0.1816 | unavailable (4) | -0.10708 | -0.09922 |
| 72h | 192 | 172 | 11 | 172 | 20 | 0 | 0 | 0 | -0.01249 | -0.01608 | 113/0/59 | 0.0503 | -0.3058 | unavailable (4) | -0.05249 | -0.04 |

Overlap (from actual windows): 4h: 40 of 175 windows overlap another; the largest disjoint subset has 155; 24h: 174 of 174 windows overlap another; the largest disjoint subset has 32; 72h: 172 of 172 windows overlap another; the largest disjoint subset has 11.

Not registered, by reason: late (75); rc1d-unavailable (138)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
