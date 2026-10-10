# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-10T17:03:04.940Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-10T16:25:00.000Z; last scored 2026-10-10T16:54:38.896Z. Stream start: 2026-10-01T00:00:00Z. Registered 153, confirmed 153, eligible 153. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 50 | 50 | 40 | 20 | 0 | 0 | 0 | 0 | -0.00439 | 0.01186 | 23/0/27 | 0.0094 | -0.1026 | unavailable (1) | -0.09719 | -0.09281 |
| 24h | 45 | 45 | 8 | 45 | 0 | 0 | 0 | 0 | -0.00977 | 0.01121 | 22/0/23 | 0.0278 | -0.1696 | unavailable (1) | -0.12985 | -0.12008 |
| 72h | 33 | 33 | 2 | 33 | 0 | 0 | 0 | 0 | 0.00203 | 0.02474 | 15/0/18 | -0.0115 | 0.0306 | unavailable (0) | -0.09488 | -0.09691 |

Overlap (from actual windows): 4h: 20 of 50 windows overlap another; the largest disjoint subset has 40; 24h: 45 of 45 windows overlap another; the largest disjoint subset has 8; 72h: 33 of 33 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
