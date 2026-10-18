# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-18T08:17:39.970Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-18T04:25:00.000Z; last scored 2026-10-18T05:07:01.434Z. Stream start: 2026-10-01T00:00:00Z. Registered 291, confirmed 291, eligible 291. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 95 | 95 | 79 | 32 | 0 | 0 | 0 | 0 | -0.00653 | -0.00216 | 49/0/46 | 0.0149 | -0.177 | unavailable (2) | -0.10829 | -0.10176 |
| 24h | 90 | 90 | 15 | 90 | 0 | 0 | 0 | 0 | -0.0105 | 0.00167 | 44/0/46 | 0.0319 | -0.2176 | unavailable (2) | -0.16561 | -0.15511 |
| 72h | 78 | 78 | 5 | 78 | 0 | 0 | 0 | 0 | -0.0096 | -0.01265 | 47/0/31 | 0.0649 | -0.1978 | unavailable (1) | -0.11536 | -0.10576 |

Overlap (from actual windows): 4h: 32 of 95 windows overlap another; the largest disjoint subset has 79; 24h: 90 of 90 windows overlap another; the largest disjoint subset has 15; 72h: 78 of 78 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
