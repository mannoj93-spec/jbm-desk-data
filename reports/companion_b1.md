# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-13T20:27:42.646Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-13T16:25:00.000Z; last scored 2026-10-13T17:00:34.959Z. Stream start: 2026-10-01T00:00:00Z. Registered 210, confirmed 210, eligible 210. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 68 | 68 | 55 | 26 | 0 | 0 | 0 | 0 | -0.00472 | 0.0033 | 33/0/35 | 0.0109 | -0.1254 | unavailable (1) | -0.11804 | -0.11333 |
| 24h | 63 | 63 | 11 | 63 | 0 | 0 | 0 | 0 | -0.01212 | -0.00397 | 33/0/30 | 0.0349 | -0.2341 | unavailable (1) | -0.16517 | -0.15305 |
| 72h | 51 | 51 | 3 | 51 | 0 | 0 | 0 | 0 | -0.00627 | -0.01685 | 27/0/24 | 0.0341 | -0.1098 | unavailable (1) | -0.11443 | -0.10816 |

Overlap (from actual windows): 4h: 26 of 68 windows overlap another; the largest disjoint subset has 55; 24h: 63 of 63 windows overlap another; the largest disjoint subset has 11; 72h: 51 of 51 windows overlap another; the largest disjoint subset has 3.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
