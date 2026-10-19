# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-19T01:24:26.567Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-19T00:25:00.000Z; last scored 2026-10-19T01:08:50.596Z. Stream start: 2026-10-01T00:00:00Z. Registered 303, confirmed 303, eligible 303. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 100 | 100 | 84 | 32 | 0 | 0 | 0 | 0 | -0.00591 | -0.00123 | 51/0/49 | 0.0134 | -0.1608 | unavailable (2) | -0.10109 | -0.09518 |
| 24h | 95 | 95 | 16 | 95 | 0 | 0 | 0 | 0 | -0.0081 | 0.00293 | 45/0/50 | 0.0255 | -0.1643 | unavailable (2) | -0.16065 | -0.15255 |
| 72h | 83 | 83 | 5 | 83 | 0 | 0 | 0 | 0 | -0.01144 | -0.01522 | 52/0/31 | 0.0709 | -0.2402 | unavailable (1) | -0.10143 | -0.08999 |

Overlap (from actual windows): 4h: 32 of 100 windows overlap another; the largest disjoint subset has 84; 24h: 95 of 95 windows overlap another; the largest disjoint subset has 16; 72h: 83 of 83 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
