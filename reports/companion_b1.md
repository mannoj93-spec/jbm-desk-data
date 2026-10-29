# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-29T08:21:10.160Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-29T04:25:00.000Z; last scored 2026-10-29T05:01:07.441Z. Stream start: 2026-10-01T00:00:00Z. Registered 462, confirmed 462, eligible 462. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 161 | 152 | 134 | 36 | 9 | 0 | 0 | 0 | -0.00493 | -0.00254 | 79/0/73 | 0.0117 | -0.1497 | unavailable (3) | -0.06464 | -0.05971 |
| 24h | 156 | 148 | 25 | 148 | 8 | 0 | 0 | 0 | -0.0057 | -0.00256 | 75/0/73 | 0.0187 | -0.1305 | unavailable (3) | -0.08343 | -0.07772 |
| 72h | 144 | 137 | 9 | 137 | 7 | 0 | 0 | 0 | -0.01567 | -0.02225 | 97/0/40 | 0.0706 | -0.3689 | unavailable (3) | -0.05899 | -0.04333 |

Overlap (from actual windows): 4h: 36 of 152 windows overlap another; the largest disjoint subset has 134; 24h: 148 of 148 windows overlap another; the largest disjoint subset has 25; 72h: 137 of 137 windows overlap another; the largest disjoint subset has 9.

Not registered, by reason: late (6); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
