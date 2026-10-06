# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-06T16:20:08.648Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-06T12:25:00.000Z; last scored 2026-10-06T13:00:15.833Z. Stream start: 2026-10-01T00:00:00Z. Registered 81, confirmed 81, eligible 81. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 25 | 25 | 20 | 10 | 0 | 0 | 0 | 0 | -0.00166 | 0.02081 | 10/0/15 | 0.0037 | -0.0327 | unavailable (0) | -0.11221 | -0.11055 |
| 24h | 21 | 21 | 4 | 21 | 0 | 0 | 0 | 0 | -0.01321 | -0.00903 | 11/0/10 | 0.0346 | -0.1815 | unavailable (0) | -0.18259 | -0.16937 |
| 72h | 15 | 15 | 1 | 15 | 0 | 0 | 0 | 0 | -0.02803 | -0.06015 | 10/0/5 | 0.1721 | -0.3802 | unavailable (0) | -0.13393 | -0.1059 |

Overlap (from actual windows): 4h: 10 of 25 windows overlap another; the largest disjoint subset has 20; 24h: 21 of 21 windows overlap another; the largest disjoint subset has 4; 72h: 15 of 15 windows overlap another; the largest disjoint subset has 1.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
