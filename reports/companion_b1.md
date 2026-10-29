# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-29T04:54:53.577Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-29T00:25:00.000Z; last scored 2026-10-29T01:16:27.116Z. Stream start: 2026-10-01T00:00:00Z. Registered 459, confirmed 459, eligible 459. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 160 | 151 | 133 | 36 | 9 | 0 | 0 | 0 | -0.00503 | -0.00293 | 79/0/72 | 0.0121 | -0.1525 | unavailable (3) | -0.06467 | -0.05964 |
| 24h | 155 | 147 | 25 | 147 | 8 | 0 | 0 | 0 | -0.00575 | -0.00319 | 75/0/72 | 0.0187 | -0.1312 | unavailable (3) | -0.08278 | -0.07703 |
| 72h | 143 | 136 | 8 | 136 | 7 | 0 | 0 | 0 | -0.0157 | -0.0228 | 96/0/40 | 0.0716 | -0.3685 | unavailable (3) | -0.06098 | -0.04527 |

Overlap (from actual windows): 4h: 36 of 151 windows overlap another; the largest disjoint subset has 133; 24h: 147 of 147 windows overlap another; the largest disjoint subset has 25; 72h: 136 of 136 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: late (6); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
