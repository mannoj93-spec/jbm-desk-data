# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-13T08:20:14.817Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-13T04:25:00.000Z; last scored 2026-10-13T05:00:19.327Z. Stream start: 2026-10-01T00:00:00Z. Registered 201, confirmed 201, eligible 201. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 65 | 65 | 52 | 26 | 0 | 0 | 0 | 0 | -0.00385 | 0.00525 | 30/0/35 | 0.0087 | -0.1011 | unavailable (1) | -0.12226 | -0.11841 |
| 24h | 60 | 60 | 10 | 60 | 0 | 0 | 0 | 0 | -0.01293 | -0.00702 | 33/0/27 | 0.0376 | -0.2442 | unavailable (1) | -0.16218 | -0.14925 |
| 72h | 48 | 48 | 3 | 48 | 0 | 0 | 0 | 0 | -0.00725 | -0.02459 | 27/0/21 | 0.0377 | -0.1236 | unavailable (1) | -0.11769 | -0.11044 |

Overlap (from actual windows): 4h: 26 of 65 windows overlap another; the largest disjoint subset has 52; 24h: 60 of 60 windows overlap another; the largest disjoint subset has 10; 72h: 48 of 48 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
