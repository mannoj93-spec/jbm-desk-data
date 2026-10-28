# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-28T20:20:46.803Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-28T16:25:00.000Z; last scored 2026-10-28T17:31:18.214Z. Stream start: 2026-10-01T00:00:00Z. Registered 453, confirmed 453, eligible 453. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 158 | 150 | 132 | 36 | 8 | 0 | 0 | 0 | -0.00502 | -0.00254 | 78/0/72 | 0.012 | -0.1516 | unavailable (3) | -0.0661 | -0.06107 |
| 24h | 153 | 145 | 25 | 145 | 8 | 0 | 0 | 0 | -0.00586 | -0.00321 | 75/0/70 | 0.0192 | -0.1328 | unavailable (3) | -0.08634 | -0.08048 |
| 72h | 141 | 134 | 8 | 134 | 7 | 0 | 0 | 0 | -0.01599 | -0.02358 | 96/0/38 | 0.0741 | -0.3729 | unavailable (3) | -0.06414 | -0.04815 |

Overlap (from actual windows): 4h: 36 of 150 windows overlap another; the largest disjoint subset has 132; 24h: 145 of 145 windows overlap another; the largest disjoint subset has 25; 72h: 134 of 134 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: late (6); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
