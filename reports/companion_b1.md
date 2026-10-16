# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-16T00:32:35.609Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-15T20:25:00.000Z; last scored 2026-10-15T21:10:03.800Z. Stream start: 2026-10-01T00:00:00Z. Registered 249, confirmed 249, eligible 249. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 81 | 81 | 68 | 26 | 0 | 0 | 0 | 0 | -0.00579 | -0.00031 | 41/0/40 | 0.0133 | -0.1618 | unavailable (1) | -0.10665 | -0.10086 |
| 24h | 76 | 76 | 13 | 76 | 0 | 0 | 0 | 0 | -0.00986 | 0.00239 | 36/0/40 | 0.0279 | -0.2036 | unavailable (1) | -0.15754 | -0.14768 |
| 72h | 64 | 64 | 4 | 64 | 0 | 0 | 0 | 0 | -0.00586 | -0.0092 | 36/0/28 | 0.0368 | -0.1147 | unavailable (1) | -0.11211 | -0.10624 |

Overlap (from actual windows): 4h: 26 of 81 windows overlap another; the largest disjoint subset has 68; 24h: 76 of 76 windows overlap another; the largest disjoint subset has 13; 72h: 64 of 64 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
