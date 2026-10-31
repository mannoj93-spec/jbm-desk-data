# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-31T23:14:12.785Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-31T20:25:00.000Z; last scored 2026-10-31T21:46:40.790Z. Stream start: 2026-10-01T00:00:00Z. Registered 495, confirmed 495, eligible 495. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 177 | 164 | 145 | 38 | 13 | 0 | 0 | 0 | -0.00572 | -0.00301 | 87/0/77 | 0.0136 | -0.1719 | unavailable (3) | -0.07582 | -0.0701 |
| 24h | 172 | 160 | 28 | 160 | 12 | 0 | 0 | 0 | -0.00509 | 0.00103 | 79/0/81 | 0.0161 | -0.1175 | unavailable (3) | -0.09489 | -0.0898 |
| 72h | 160 | 151 | 9 | 151 | 9 | 0 | 0 | 0 | -0.01336 | -0.01685 | 100/0/51 | 0.0558 | -0.323 | unavailable (3) | -0.06261 | -0.04925 |

Overlap (from actual windows): 4h: 38 of 164 windows overlap another; the largest disjoint subset has 145; 24h: 160 of 160 windows overlap another; the largest disjoint subset has 28; 72h: 151 of 151 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (18); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
