# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-15T16:31:23.760Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-15T12:25:00.000Z; last scored 2026-10-15T13:21:56.808Z. Stream start: 2026-10-01T00:00:00Z. Registered 243, confirmed 243, eligible 243. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 79 | 79 | 66 | 26 | 0 | 0 | 0 | 0 | -0.00515 | 0.00242 | 39/0/40 | 0.0119 | -0.143 | unavailable (1) | -0.10331 | -0.09817 |
| 24h | 74 | 74 | 13 | 74 | 0 | 0 | 0 | 0 | -0.0106 | 0.00167 | 36/0/38 | 0.0294 | -0.2171 | unavailable (1) | -0.15514 | -0.14454 |
| 72h | 62 | 62 | 4 | 62 | 0 | 0 | 0 | 0 | -0.00657 | -0.01105 | 36/0/26 | 0.0403 | -0.1269 | unavailable (1) | -0.10661 | -0.10004 |

Overlap (from actual windows): 4h: 26 of 79 windows overlap another; the largest disjoint subset has 66; 24h: 74 of 74 windows overlap another; the largest disjoint subset has 13; 72h: 62 of 62 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
