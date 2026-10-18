# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-18T00:33:02.111Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-17T20:25:00.000Z; last scored 2026-10-17T21:03:26.126Z. Stream start: 2026-10-01T00:00:00Z. Registered 285, confirmed 285, eligible 285. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 93 | 93 | 77 | 32 | 0 | 0 | 0 | 0 | -0.00728 | -0.00293 | 49/0/44 | 0.0166 | -0.1973 | unavailable (2) | -0.11728 | -0.11 |
| 24h | 88 | 88 | 15 | 88 | 0 | 0 | 0 | 0 | -0.01068 | 0.00167 | 43/0/45 | 0.032 | -0.2252 | unavailable (2) | -0.15996 | -0.14929 |
| 72h | 76 | 76 | 5 | 76 | 0 | 0 | 0 | 0 | -0.00899 | -0.01189 | 45/0/31 | 0.0607 | -0.1836 | unavailable (1) | -0.12097 | -0.11198 |

Overlap (from actual windows): 4h: 32 of 93 windows overlap another; the largest disjoint subset has 77; 24h: 88 of 88 windows overlap another; the largest disjoint subset has 15; 72h: 76 of 76 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
