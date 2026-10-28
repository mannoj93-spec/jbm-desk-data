# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-28T00:20:17.427Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-27T20:25:00.000Z; last scored 2026-10-27T21:31:20.558Z. Stream start: 2026-10-01T00:00:00Z. Registered 441, confirmed 441, eligible 441. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 153 | 145 | 127 | 36 | 8 | 0 | 0 | 0 | -0.00519 | -0.00293 | 75/0/70 | 0.0123 | -0.1543 | unavailable (3) | -0.06999 | -0.06479 |
| 24h | 148 | 140 | 24 | 140 | 8 | 0 | 0 | 0 | -0.00582 | -0.00023 | 70/0/70 | 0.0188 | -0.1296 | unavailable (3) | -0.09328 | -0.08746 |
| 72h | 136 | 129 | 8 | 129 | 7 | 0 | 0 | 0 | -0.01613 | -0.02615 | 91/0/38 | 0.0805 | -0.3692 | unavailable (3) | -0.07267 | -0.05654 |

Overlap (from actual windows): 4h: 36 of 145 windows overlap another; the largest disjoint subset has 127; 24h: 140 of 140 windows overlap another; the largest disjoint subset has 24; 72h: 129 of 129 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: late (3); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
