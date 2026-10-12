# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-12T20:22:52.325Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-12T16:25:00.000Z; last scored 2026-10-12T16:56:08.586Z. Stream start: 2026-10-01T00:00:00Z. Registered 192, confirmed 192, eligible 192. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 62 | 62 | 49 | 26 | 0 | 0 | 0 | 0 | -0.00453 | 0.0033 | 30/0/32 | 0.0106 | -0.1165 | unavailable (1) | -0.11671 | -0.11218 |
| 24h | 57 | 57 | 10 | 57 | 0 | 0 | 0 | 0 | -0.01357 | -0.0188 | 31/0/26 | 0.0397 | -0.25 | unavailable (1) | -0.16554 | -0.15198 |
| 72h | 45 | 45 | 3 | 45 | 0 | 0 | 0 | 0 | -0.0077 | -0.02693 | 26/0/19 | 0.0398 | -0.1281 | unavailable (1) | -0.11789 | -0.11018 |

Overlap (from actual windows): 4h: 26 of 62 windows overlap another; the largest disjoint subset has 49; 24h: 57 of 57 windows overlap another; the largest disjoint subset has 10; 72h: 45 of 45 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
