# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-09T12:20:43.722Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-09T08:25:00.000Z; last scored 2026-10-09T08:57:07.424Z. Stream start: 2026-10-01T00:00:00Z. Registered 132, confirmed 132, eligible 132. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 42 | 42 | 34 | 16 | 0 | 0 | 0 | 0 | -0.00039 | 0.01548 | 17/0/25 | 0.0008 | -0.0091 | unavailable (1) | -0.06604 | -0.06565 |
| 24h | 37 | 37 | 7 | 37 | 0 | 0 | 0 | 0 | -0.00429 | 0.02038 | 16/0/21 | 0.0122 | -0.0715 | unavailable (0) | -0.13525 | -0.13096 |
| 72h | 25 | 25 | 2 | 25 | 0 | 0 | 0 | 0 | -0.00044 | 0.01508 | 12/0/13 | 0.0025 | -0.0064 | unavailable (0) | -0.10176 | -0.10131 |

Overlap (from actual windows): 4h: 16 of 42 windows overlap another; the largest disjoint subset has 34; 24h: 37 of 37 windows overlap another; the largest disjoint subset has 7; 72h: 25 of 25 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
