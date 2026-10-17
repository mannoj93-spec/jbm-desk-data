# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-17T20:21:46.614Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-17T16:25:00.000Z; last scored 2026-10-17T17:03:25.304Z. Stream start: 2026-10-01T00:00:00Z. Registered 282, confirmed 282, eligible 282. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 92 | 92 | 76 | 32 | 0 | 0 | 0 | 0 | -0.00786 | -0.00413 | 49/0/43 | 0.0179 | -0.2144 | unavailable (2) | -0.11818 | -0.11032 |
| 24h | 87 | 87 | 15 | 87 | 0 | 0 | 0 | 0 | -0.00985 | 0.00186 | 42/0/45 | 0.0299 | -0.2093 | unavailable (2) | -0.15698 | -0.14714 |
| 72h | 75 | 75 | 5 | 75 | 0 | 0 | 0 | 0 | -0.00879 | -0.01165 | 44/0/31 | 0.0593 | -0.1784 | unavailable (1) | -0.12394 | -0.11515 |

Overlap (from actual windows): 4h: 32 of 92 windows overlap another; the largest disjoint subset has 76; 24h: 87 of 87 windows overlap another; the largest disjoint subset has 15; 72h: 75 of 75 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
