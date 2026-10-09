# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-09T08:24:51.041Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-09T04:25:00.000Z; last scored 2026-10-09T04:55:50.939Z. Stream start: 2026-10-01T00:00:00Z. Registered 129, confirmed 129, eligible 129. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 41 | 41 | 33 | 16 | 0 | 0 | 0 | 0 | 0.00062 | 0.0171 | 16/0/25 | -0.0013 | 0.0145 | unavailable (0) | -0.07388 | -0.0745 |
| 24h | 36 | 36 | 7 | 36 | 0 | 0 | 0 | 0 | -0.00488 | 0.02172 | 16/0/20 | 0.0137 | -0.0802 | unavailable (0) | -0.13588 | -0.131 |
| 72h | 24 | 24 | 2 | 24 | 0 | 0 | 0 | 0 | -0.00302 | 0.00231 | 12/0/12 | 0.0182 | -0.0432 | unavailable (0) | -0.09898 | -0.09595 |

Overlap (from actual windows): 4h: 16 of 41 windows overlap another; the largest disjoint subset has 33; 24h: 36 of 36 windows overlap another; the largest disjoint subset has 7; 72h: 24 of 24 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
