# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-18T12:18:41.191Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-18T08:25:00.000Z; last scored 2026-10-18T09:04:53.950Z. Stream start: 2026-10-01T00:00:00Z. Registered 294, confirmed 294, eligible 294. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 96 | 96 | 80 | 32 | 0 | 0 | 0 | 0 | -0.00678 | -0.00254 | 50/0/46 | 0.0154 | -0.1843 | unavailable (2) | -0.10944 | -0.10266 |
| 24h | 91 | 91 | 15 | 91 | 0 | 0 | 0 | 0 | -0.00961 | 0.00186 | 44/0/47 | 0.0295 | -0.1971 | unavailable (2) | -0.16582 | -0.15621 |
| 72h | 79 | 79 | 5 | 79 | 0 | 0 | 0 | 0 | -0.00993 | -0.01316 | 48/0/31 | 0.067 | -0.2057 | unavailable (1) | -0.11227 | -0.10233 |

Overlap (from actual windows): 4h: 32 of 96 windows overlap another; the largest disjoint subset has 80; 24h: 91 of 91 windows overlap another; the largest disjoint subset has 15; 72h: 79 of 79 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
