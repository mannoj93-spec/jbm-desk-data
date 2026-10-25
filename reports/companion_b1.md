# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-25T22:26:04.128Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-25T20:25:00.000Z; last scored 2026-10-25T20:31:35.480Z. Stream start: 2026-10-01T00:00:00Z. Registered 405, confirmed 405, eligible 405. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 141 | 134 | 118 | 32 | 7 | 0 | 0 | 0 | -0.00555 | -0.00413 | 70/0/64 | 0.013 | -0.1591 | unavailable (3) | -0.07935 | -0.0738 |
| 24h | 136 | 129 | 22 | 129 | 7 | 0 | 0 | 0 | -0.00524 | 0.00375 | 61/0/68 | 0.017 | -0.1128 | unavailable (3) | -0.10382 | -0.09858 |
| 72h | 124 | 122 | 7 | 122 | 2 | 0 | 0 | 0 | -0.01633 | -0.02718 | 84/0/38 | 0.0915 | -0.3637 | unavailable (2) | -0.07748 | -0.06115 |

Overlap (from actual windows): 4h: 32 of 134 windows overlap another; the largest disjoint subset has 118; 24h: 129 of 129 windows overlap another; the largest disjoint subset has 22; 72h: 122 of 122 windows overlap another; the largest disjoint subset has 7.

Not registered, by reason: rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
