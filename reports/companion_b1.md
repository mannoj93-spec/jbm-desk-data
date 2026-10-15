# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-15T20:25:48.991Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-15T16:25:00.000Z; last scored 2026-10-15T17:15:34.963Z. Stream start: 2026-10-01T00:00:00Z. Registered 246, confirmed 246, eligible 246. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 80 | 80 | 67 | 26 | 0 | 0 | 0 | 0 | -0.00549 | 0.00106 | 40/0/40 | 0.0126 | -0.153 | unavailable (1) | -0.11262 | -0.10713 |
| 24h | 75 | 75 | 13 | 75 | 0 | 0 | 0 | 0 | -0.01007 | 0.00186 | 36/0/39 | 0.0283 | -0.2068 | unavailable (1) | -0.15726 | -0.14718 |
| 72h | 63 | 63 | 4 | 63 | 0 | 0 | 0 | 0 | -0.00623 | -0.01045 | 36/0/27 | 0.0387 | -0.1212 | unavailable (1) | -0.10954 | -0.1033 |

Overlap (from actual windows): 4h: 26 of 80 windows overlap another; the largest disjoint subset has 67; 24h: 75 of 75 windows overlap another; the largest disjoint subset has 13; 72h: 63 of 63 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
