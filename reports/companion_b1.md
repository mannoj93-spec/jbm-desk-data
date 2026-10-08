# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-08T00:18:52.216Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-07T20:55:00.000Z; last scored 2026-10-07T21:55:04.689Z. Stream start: 2026-10-01T00:00:00Z. Registered 105, confirmed 105, eligible 105. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 33 | 33 | 27 | 12 | 0 | 0 | 0 | 0 | -0.00088 | 0.02081 | 14/0/19 | 0.0019 | -0.019 | unavailable (0) | -0.07162 | -0.07074 |
| 24h | 28 | 28 | 5 | 28 | 0 | 0 | 0 | 0 | -0.00642 | 0.0219 | 13/0/15 | 0.0171 | -0.0965 | unavailable (0) | -0.14645 | -0.14002 |
| 72h | 17 | 17 | 2 | 17 | 0 | 0 | 0 | 0 | -0.02528 | -0.04796 | 11/0/6 | 0.1476 | -0.3602 | unavailable (0) | -0.12579 | -0.10051 |

Overlap (from actual windows): 4h: 12 of 33 windows overlap another; the largest disjoint subset has 27; 24h: 28 of 28 windows overlap another; the largest disjoint subset has 5; 72h: 17 of 17 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
