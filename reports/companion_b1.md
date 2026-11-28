# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-11-28T00:27:55.046Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-11-27T20:30:00.000Z; last scored 2026-11-27T20:47:04.521Z. Stream start: 2026-10-01T00:00:00Z. Registered 558, confirmed 558, eligible 558. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 304 | 185 | 165 | 40 | 119 | 0 | 0 | 0 | -0.00535 | -0.00297 | 98/0/87 | 0.0127 | -0.1536 | unavailable (4) | -0.08691 | -0.08157 |
| 24h | 299 | 184 | 37 | 183 | 115 | 0 | 0 | 0 | -0.00693 | -0.00329 | 96/0/88 | 0.0204 | -0.1518 | unavailable (4) | -0.10214 | -0.09521 |
| 72h | 287 | 181 | 14 | 181 | 106 | 0 | 0 | 0 | -0.01146 | -0.01536 | 117/0/64 | 0.0456 | -0.2604 | unavailable (4) | -0.05148 | -0.04002 |

Overlap (from actual windows): 4h: 40 of 185 windows overlap another; the largest disjoint subset has 165; 24h: 183 of 184 windows overlap another; the largest disjoint subset has 37; 72h: 181 of 181 windows overlap another; the largest disjoint subset has 14.

Not registered, by reason: late (315); rc1d-unavailable (156)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
