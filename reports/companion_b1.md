# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-12T12:27:57.264Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-12T08:25:00.000Z; last scored 2026-10-12T08:59:44.925Z. Stream start: 2026-10-01T00:00:00Z. Registered 186, confirmed 186, eligible 186. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 60 | 60 | 47 | 26 | 0 | 0 | 0 | 0 | -0.00477 | 0.0033 | 29/0/31 | 0.0109 | -0.1206 | unavailable (1) | -0.11857 | -0.1138 |
| 24h | 55 | 55 | 10 | 55 | 0 | 0 | 0 | 0 | -0.01429 | -0.01972 | 30/0/25 | 0.0406 | -0.2594 | unavailable (1) | -0.17019 | -0.1559 |
| 72h | 43 | 43 | 3 | 43 | 0 | 0 | 0 | 0 | -0.00588 | -0.02225 | 24/0/19 | 0.0328 | -0.0965 | unavailable (1) | -0.11739 | -0.11151 |

Overlap (from actual windows): 4h: 26 of 60 windows overlap another; the largest disjoint subset has 47; 24h: 55 of 55 windows overlap another; the largest disjoint subset has 10; 72h: 43 of 43 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
