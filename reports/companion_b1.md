# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-28T21:24:21.974Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-28T20:25:00.000Z; last scored 2026-10-28T21:16:37.170Z. Stream start: 2026-10-01T00:00:00Z. Registered 453, confirmed 453, eligible 453. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 159 | 150 | 132 | 36 | 9 | 0 | 0 | 0 | -0.00502 | -0.00254 | 78/0/72 | 0.012 | -0.1516 | unavailable (3) | -0.0661 | -0.06107 |
| 24h | 154 | 146 | 25 | 146 | 8 | 0 | 0 | 0 | -0.0058 | -0.0032 | 75/0/71 | 0.0189 | -0.1317 | unavailable (3) | -0.08444 | -0.07864 |
| 72h | 142 | 135 | 8 | 135 | 7 | 0 | 0 | 0 | -0.01585 | -0.02336 | 96/0/39 | 0.0729 | -0.3709 | unavailable (3) | -0.06273 | -0.04687 |

Overlap (from actual windows): 4h: 36 of 150 windows overlap another; the largest disjoint subset has 132; 24h: 146 of 146 windows overlap another; the largest disjoint subset has 25; 72h: 135 of 135 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: late (6); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
