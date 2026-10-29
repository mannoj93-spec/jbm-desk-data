# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-29T21:33:18.239Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-29T20:25:00.000Z; last scored 2026-10-29T21:16:28.468Z. Stream start: 2026-10-01T00:00:00Z. Registered 471, confirmed 471, eligible 471. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 165 | 156 | 138 | 36 | 9 | 0 | 0 | 0 | -0.00472 | -0.00254 | 81/0/75 | 0.0112 | -0.1438 | unavailable (3) | -0.06351 | -0.0588 |
| 24h | 160 | 151 | 26 | 151 | 9 | 0 | 0 | 0 | -0.00557 | -0.00194 | 76/0/75 | 0.0186 | -0.1286 | unavailable (3) | -0.0859 | -0.08033 |
| 72h | 148 | 140 | 9 | 140 | 8 | 0 | 0 | 0 | -0.01575 | -0.02217 | 100/0/40 | 0.0687 | -0.3749 | unavailable (3) | -0.05297 | -0.03722 |

Overlap (from actual windows): 4h: 36 of 156 windows overlap another; the largest disjoint subset has 138; 24h: 151 of 151 windows overlap another; the largest disjoint subset has 26; 72h: 140 of 140 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (6); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
