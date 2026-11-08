# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-11-08T20:49:14.582Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-11-08T16:25:00.000Z; last scored 2026-11-08T17:01:26.245Z. Stream start: 2026-10-01T00:00:00Z. Registered 516, confirmed 516, eligible 516. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 190 | 171 | 151 | 40 | 19 | 0 | 0 | 0 | -0.00589 | -0.00306 | 92/0/79 | 0.0142 | -0.1774 | unavailable (4) | -0.08981 | -0.08393 |
| 24h | 185 | 168 | 30 | 168 | 17 | 0 | 0 | 0 | -0.00757 | -0.00328 | 87/0/81 | 0.023 | -0.1726 | unavailable (4) | -0.1103 | -0.10273 |
| 72h | 178 | 165 | 10 | 165 | 13 | 0 | 0 | 0 | -0.01223 | -0.01679 | 107/0/58 | 0.0479 | -0.2951 | unavailable (3) | -0.05436 | -0.04212 |

Overlap (from actual windows): 4h: 40 of 171 windows overlap another; the largest disjoint subset has 151; 24h: 168 of 168 windows overlap another; the largest disjoint subset has 30; 72h: 165 of 165 windows overlap another; the largest disjoint subset has 10.

Not registered, by reason: late (36); rc1d-unavailable (132)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
