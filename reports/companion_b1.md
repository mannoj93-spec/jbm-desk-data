# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-16T20:23:35.746Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-16T16:25:00.000Z; last scored 2026-10-16T17:10:06.088Z. Stream start: 2026-10-01T00:00:00Z. Registered 264, confirmed 264, eligible 264. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 86 | 86 | 71 | 30 | 0 | 0 | 0 | 0 | -0.00545 | -0.00123 | 44/0/42 | 0.0127 | -0.1533 | unavailable (2) | -0.10225 | -0.0968 |
| 24h | 81 | 81 | 14 | 81 | 0 | 0 | 0 | 0 | -0.00902 | 0.00375 | 37/0/44 | 0.0262 | -0.1904 | unavailable (1) | -0.16355 | -0.15453 |
| 72h | 69 | 69 | 4 | 69 | 0 | 0 | 0 | 0 | -0.009 | -0.01213 | 41/0/28 | 0.0586 | -0.1776 | unavailable (1) | -0.12216 | -0.11316 |

Overlap (from actual windows): 4h: 30 of 86 windows overlap another; the largest disjoint subset has 71; 24h: 81 of 81 windows overlap another; the largest disjoint subset has 14; 72h: 69 of 69 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
