# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-11-15T12:28:39.802Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-11-15T04:25:00.000Z; last scored 2026-11-15T05:16:40.777Z. Stream start: 2026-10-01T00:00:00Z. Registered 534, confirmed 534, eligible 534. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 230 | 177 | 157 | 40 | 53 | 0 | 0 | 0 | -0.00537 | -0.00297 | 94/0/83 | 0.0129 | -0.1602 | unavailable (4) | -0.09064 | -0.08528 |
| 24h | 225 | 175 | 33 | 174 | 50 | 0 | 0 | 0 | -0.00811 | -0.00362 | 93/0/82 | 0.0241 | -0.1873 | unavailable (4) | -0.10618 | -0.09808 |
| 72h | 213 | 175 | 12 | 175 | 38 | 0 | 0 | 0 | -0.01257 | -0.01679 | 115/0/60 | 0.0501 | -0.3026 | unavailable (4) | -0.0518 | -0.03923 |

Overlap (from actual windows): 4h: 40 of 177 windows overlap another; the largest disjoint subset has 157; 24h: 174 of 175 windows overlap another; the largest disjoint subset has 33; 72h: 175 of 175 windows overlap another; the largest disjoint subset has 12.

Not registered, by reason: late (126); rc1d-unavailable (144)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
