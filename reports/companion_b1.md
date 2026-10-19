# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-19T12:35:24.668Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-19T08:25:00.000Z; last scored 2026-10-19T09:16:43.457Z. Stream start: 2026-10-01T00:00:00Z. Registered 312, confirmed 312, eligible 312. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 102 | 102 | 86 | 32 | 0 | 0 | 0 | 0 | -0.0061 | -0.00254 | 53/0/49 | 0.014 | -0.1676 | unavailable (2) | -0.09676 | -0.09066 |
| 24h | 97 | 97 | 16 | 97 | 0 | 0 | 0 | 0 | -0.00702 | 0.00375 | 45/0/52 | 0.0222 | -0.1421 | unavailable (2) | -0.15374 | -0.14673 |
| 72h | 85 | 85 | 5 | 85 | 0 | 0 | 0 | 0 | -0.01238 | -0.01685 | 54/0/31 | 0.0744 | -0.2609 | unavailable (2) | -0.09942 | -0.08703 |

Overlap (from actual windows): 4h: 32 of 102 windows overlap another; the largest disjoint subset has 86; 24h: 97 of 97 windows overlap another; the largest disjoint subset has 16; 72h: 85 of 85 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
