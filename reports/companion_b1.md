# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-21T21:16:42.585Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-21T20:25:00.000Z; last scored 2026-10-21T21:10:27.710Z. Stream start: 2026-10-01T00:00:00Z. Registered 351, confirmed 351, eligible 351. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 117 | 116 | 100 | 32 | 1 | 0 | 0 | 0 | -0.00579 | -0.00254 | 60/0/56 | 0.0132 | -0.1646 | unavailable (2) | -0.08002 | -0.07423 |
| 24h | 112 | 112 | 19 | 112 | 0 | 0 | 0 | 0 | -0.00711 | 0.00334 | 53/0/59 | 0.0241 | -0.151 | unavailable (2) | -0.13388 | -0.12677 |
| 72h | 100 | 100 | 6 | 100 | 0 | 0 | 0 | 0 | -0.01582 | -0.02651 | 69/0/31 | 0.0868 | -0.3535 | unavailable (2) | -0.08432 | -0.0685 |

Overlap (from actual windows): 4h: 32 of 116 windows overlap another; the largest disjoint subset has 100; 24h: 112 of 112 windows overlap another; the largest disjoint subset has 19; 72h: 100 of 100 windows overlap another; the largest disjoint subset has 6.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
