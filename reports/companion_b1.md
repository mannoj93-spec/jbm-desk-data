# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-06T08:18:24.232Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-06T04:25:00.000Z; last scored 2026-10-06T04:54:58.028Z. Stream start: 2026-10-01T00:00:00Z. Registered 75, confirmed 75, eligible 75. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 23 | 23 | 18 | 10 | 0 | 0 | 0 | 0 | -0.00457 | 0.0171 | 10/0/13 | 0.0094 | -0.0878 | unavailable (0) | -0.1098 | -0.10523 |
| 24h | 19 | 19 | 4 | 19 | 0 | 0 | 0 | 0 | -0.0103 | 0.0182 | 9/0/10 | 0.0263 | -0.1353 | unavailable (0) | -0.21162 | -0.20132 |
| 72h | 14 | 14 | 1 | 14 | 0 | 0 | 0 | 0 | -0.02434 | -0.05405 | 9/0/5 | 0.1649 | -0.3243 | unavailable (0) | -0.13721 | -0.11288 |

Overlap (from actual windows): 4h: 10 of 23 windows overlap another; the largest disjoint subset has 18; 24h: 19 of 19 windows overlap another; the largest disjoint subset has 4; 72h: 14 of 14 windows overlap another; the largest disjoint subset has 1.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
