# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-14T20:27:11.009Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-14T16:25:00.000Z; last scored 2026-10-14T17:12:22.871Z. Stream start: 2026-10-01T00:00:00Z. Registered 228, confirmed 228, eligible 228. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 74 | 74 | 61 | 26 | 0 | 0 | 0 | 0 | -0.00523 | 0.0033 | 36/0/38 | 0.0123 | -0.1422 | unavailable (1) | -0.11643 | -0.1112 |
| 24h | 69 | 69 | 12 | 69 | 0 | 0 | 0 | 0 | -0.01203 | -0.00397 | 36/0/33 | 0.0334 | -0.2395 | unavailable (1) | -0.14328 | -0.13124 |
| 72h | 57 | 57 | 4 | 57 | 0 | 0 | 0 | 0 | -0.00665 | -0.01316 | 32/0/25 | 0.0391 | -0.123 | unavailable (1) | -0.10941 | -0.10276 |

Overlap (from actual windows): 4h: 26 of 74 windows overlap another; the largest disjoint subset has 61; 24h: 69 of 69 windows overlap another; the largest disjoint subset has 12; 72h: 57 of 57 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
