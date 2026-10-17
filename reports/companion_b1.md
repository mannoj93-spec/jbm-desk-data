# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-17T04:25:27.886Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-17T00:25:00.000Z; last scored 2026-10-17T01:14:23.720Z. Stream start: 2026-10-01T00:00:00Z. Registered 270, confirmed 270, eligible 270. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 88 | 88 | 73 | 30 | 0 | 0 | 0 | 0 | -0.0053 | -0.00123 | 45/0/43 | 0.0121 | -0.1496 | unavailable (2) | -0.10002 | -0.09472 |
| 24h | 83 | 83 | 14 | 83 | 0 | 0 | 0 | 0 | -0.00945 | 0.00293 | 39/0/44 | 0.0278 | -0.2015 | unavailable (1) | -0.15884 | -0.14939 |
| 72h | 71 | 71 | 5 | 71 | 0 | 0 | 0 | 0 | -0.00951 | -0.01213 | 43/0/28 | 0.0632 | -0.1896 | unavailable (1) | -0.12606 | -0.11655 |

Overlap (from actual windows): 4h: 30 of 88 windows overlap another; the largest disjoint subset has 73; 24h: 83 of 83 windows overlap another; the largest disjoint subset has 14; 72h: 71 of 71 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
