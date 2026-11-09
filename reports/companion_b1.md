# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-11-09T18:35:25.126Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-11-09T16:25:00.000Z; last scored 2026-11-09T17:31:25.468Z. Stream start: 2026-10-01T00:00:00Z. Registered 519, confirmed 519, eligible 519. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 196 | 173 | 153 | 40 | 23 | 0 | 0 | 0 | -0.0057 | -0.00297 | 92/0/81 | 0.0138 | -0.1727 | unavailable (4) | -0.09275 | -0.08704 |
| 24h | 191 | 172 | 31 | 172 | 19 | 0 | 0 | 0 | -0.00752 | -0.00329 | 90/0/82 | 0.0223 | -0.1733 | unavailable (4) | -0.1061 | -0.09858 |
| 72h | 179 | 165 | 10 | 165 | 14 | 0 | 0 | 0 | -0.01223 | -0.01679 | 107/0/58 | 0.0479 | -0.2951 | unavailable (3) | -0.05436 | -0.04212 |

Overlap (from actual windows): 4h: 40 of 173 windows overlap another; the largest disjoint subset has 153; 24h: 172 of 172 windows overlap another; the largest disjoint subset has 31; 72h: 165 of 165 windows overlap another; the largest disjoint subset has 10.

Not registered, by reason: late (45); rc1d-unavailable (135)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
