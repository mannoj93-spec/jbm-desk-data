# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-14T04:20:12.663Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-14T00:25:00.000Z; last scored 2026-10-14T01:16:00.324Z. Stream start: 2026-10-01T00:00:00Z. Registered 216, confirmed 216, eligible 216. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 70 | 70 | 57 | 26 | 0 | 0 | 0 | 0 | -0.00549 | 0.00106 | 35/0/35 | 0.0126 | -0.147 | unavailable (1) | -0.1071 | -0.10161 |
| 24h | 65 | 65 | 11 | 65 | 0 | 0 | 0 | 0 | -0.01131 | -0.00362 | 33/0/32 | 0.0325 | -0.2211 | unavailable (1) | -0.16529 | -0.15397 |
| 72h | 53 | 53 | 4 | 53 | 0 | 0 | 0 | 0 | -0.0067 | -0.01685 | 29/0/24 | 0.0373 | -0.1195 | unavailable (1) | -0.11212 | -0.10542 |

Overlap (from actual windows): 4h: 26 of 70 windows overlap another; the largest disjoint subset has 57; 24h: 65 of 65 windows overlap another; the largest disjoint subset has 11; 72h: 53 of 53 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
