# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-16T16:31:26.654Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-16T12:25:00.000Z; last scored 2026-10-16T13:20:22.693Z. Stream start: 2026-10-01T00:00:00Z. Registered 261, confirmed 261, eligible 261. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 85 | 85 | 70 | 30 | 0 | 0 | 0 | 0 | -0.00596 | -0.00216 | 44/0/41 | 0.0138 | -0.1683 | unavailable (2) | -0.09988 | -0.09392 |
| 24h | 80 | 80 | 14 | 80 | 0 | 0 | 0 | 0 | -0.00859 | 0.00443 | 36/0/44 | 0.0251 | -0.1806 | unavailable (1) | -0.16963 | -0.16104 |
| 72h | 68 | 68 | 4 | 68 | 0 | 0 | 0 | 0 | -0.00836 | -0.01189 | 40/0/28 | 0.0541 | -0.1646 | unavailable (1) | -0.12024 | -0.11188 |

Overlap (from actual windows): 4h: 30 of 85 windows overlap another; the largest disjoint subset has 70; 24h: 80 of 80 windows overlap another; the largest disjoint subset has 14; 72h: 68 of 68 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
