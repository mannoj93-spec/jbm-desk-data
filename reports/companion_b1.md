# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-11-26T08:58:23.650Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-11-26T04:15:00.000Z; last scored 2026-11-26T04:32:06.124Z. Stream start: 2026-10-01T00:00:00Z. Registered 552, confirmed 552, eligible 552. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 294 | 183 | 163 | 40 | 111 | 0 | 0 | 0 | -0.00476 | -0.00293 | 96/0/87 | 0.0113 | -0.1377 | unavailable (4) | -0.08785 | -0.08309 |
| 24h | 289 | 181 | 36 | 180 | 108 | 0 | 0 | 0 | -0.0064 | -0.00322 | 94/0/87 | 0.0189 | -0.1418 | unavailable (4) | -0.10174 | -0.09534 |
| 72h | 277 | 180 | 14 | 180 | 97 | 0 | 0 | 0 | -0.0121 | -0.01608 | 117/0/63 | 0.0483 | -0.2796 | unavailable (4) | -0.05206 | -0.03997 |

Overlap (from actual windows): 4h: 40 of 183 windows overlap another; the largest disjoint subset has 163; 24h: 180 of 181 windows overlap another; the largest disjoint subset has 36; 72h: 180 of 180 windows overlap another; the largest disjoint subset has 14.

Not registered, by reason: late (294); rc1d-unavailable (153)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
