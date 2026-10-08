# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-08T21:05:17.934Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-08T20:25:00.000Z; last scored 2026-10-08T20:56:32.167Z. Stream start: 2026-10-01T00:00:00Z. Registered 120, confirmed 120, eligible 120. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 39 | 39 | 32 | 14 | 0 | 0 | 0 | 0 | 0.00063 | 0.0171 | 15/0/24 | -0.0014 | 0.0146 | unavailable (0) | -0.0861 | -0.08673 |
| 24h | 34 | 34 | 6 | 34 | 0 | 0 | 0 | 0 | -0.00652 | 0.02063 | 16/0/18 | 0.0183 | -0.1047 | unavailable (0) | -0.13626 | -0.12974 |
| 72h | 22 | 22 | 2 | 22 | 0 | 0 | 0 | 0 | -0.00911 | -0.02222 | 12/0/10 | 0.0618 | -0.1302 | unavailable (0) | -0.09607 | -0.08696 |

Overlap (from actual windows): 4h: 14 of 39 windows overlap another; the largest disjoint subset has 32; 24h: 34 of 34 windows overlap another; the largest disjoint subset has 6; 72h: 22 of 22 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
