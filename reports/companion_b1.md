# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-09T17:06:00.508Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-09T16:25:00.000Z; last scored 2026-10-09T16:57:18.122Z. Stream start: 2026-10-01T00:00:00Z. Registered 135, confirmed 135, eligible 135. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 44 | 44 | 36 | 16 | 0 | 0 | 0 | 0 | -0.00024 | 0.01548 | 18/0/26 | 0.0005 | -0.0057 | unavailable (1) | -0.07196 | -0.07172 |
| 24h | 39 | 39 | 7 | 39 | 0 | 0 | 0 | 0 | -0.00308 | 0.02038 | 16/0/23 | 0.0089 | -0.0525 | unavailable (0) | -0.13609 | -0.13301 |
| 72h | 27 | 27 | 2 | 27 | 0 | 0 | 0 | 0 | 0.00383 | 0.02474 | 12/0/15 | -0.0208 | 0.0558 | unavailable (0) | -0.10203 | -0.10586 |

Overlap (from actual windows): 4h: 16 of 44 windows overlap another; the largest disjoint subset has 36; 24h: 39 of 39 windows overlap another; the largest disjoint subset has 7; 72h: 27 of 27 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
