# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-31T19:51:31.453Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-31T16:25:00.000Z; last scored 2026-10-31T17:16:13.557Z. Stream start: 2026-10-01T00:00:00Z. Registered 492, confirmed 492, eligible 492. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 176 | 163 | 145 | 36 | 13 | 0 | 0 | 0 | -0.0055 | -0.00297 | 86/0/77 | 0.0131 | -0.1655 | unavailable (3) | -0.0728 | -0.0673 |
| 24h | 171 | 159 | 28 | 159 | 12 | 0 | 0 | 0 | -0.00465 | 0.00132 | 78/0/81 | 0.0147 | -0.108 | unavailable (3) | -0.09436 | -0.08971 |
| 72h | 159 | 150 | 9 | 150 | 9 | 0 | 0 | 0 | -0.01357 | -0.01708 | 100/0/50 | 0.0571 | -0.3277 | unavailable (3) | -0.06267 | -0.0491 |

Overlap (from actual windows): 4h: 36 of 163 windows overlap another; the largest disjoint subset has 145; 24h: 159 of 159 windows overlap another; the largest disjoint subset has 28; 72h: 150 of 150 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (18); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
