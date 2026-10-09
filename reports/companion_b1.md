# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-09T16:20:24.250Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-09T12:25:00.000Z; last scored 2026-10-09T13:00:58.002Z. Stream start: 2026-10-01T00:00:00Z. Registered 135, confirmed 135, eligible 135. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 43 | 43 | 35 | 16 | 0 | 0 | 0 | 0 | 0.00049 | 0.0171 | 17/0/26 | -0.001 | 0.0115 | unavailable (1) | -0.06711 | -0.0676 |
| 24h | 38 | 38 | 7 | 38 | 0 | 0 | 0 | 0 | -0.00389 | 0.01929 | 16/0/22 | 0.0111 | -0.0655 | unavailable (0) | -0.1336 | -0.12971 |
| 72h | 26 | 26 | 2 | 26 | 0 | 0 | 0 | 0 | 0.00201 | 0.01991 | 12/0/14 | -0.011 | 0.0289 | unavailable (0) | -0.10347 | -0.10548 |

Overlap (from actual windows): 4h: 16 of 43 windows overlap another; the largest disjoint subset has 35; 24h: 38 of 38 windows overlap another; the largest disjoint subset has 7; 72h: 26 of 26 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
