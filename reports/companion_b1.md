# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-28T15:33:27.466Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-28T12:25:00.000Z; last scored 2026-10-28T12:46:16.536Z. Stream start: 2026-10-01T00:00:00Z. Registered 450, confirmed 450, eligible 450. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 157 | 149 | 131 | 36 | 8 | 0 | 0 | 0 | -0.00505 | -0.00293 | 77/0/72 | 0.0121 | -0.1519 | unavailable (3) | -0.06637 | -0.06132 |
| 24h | 152 | 144 | 25 | 144 | 8 | 0 | 0 | 0 | -0.00581 | -0.0032 | 74/0/70 | 0.019 | -0.1313 | unavailable (3) | -0.08785 | -0.08204 |
| 72h | 140 | 133 | 8 | 133 | 7 | 0 | 0 | 0 | -0.01609 | -0.0238 | 95/0/38 | 0.0751 | -0.3739 | unavailable (3) | -0.0657 | -0.04961 |

Overlap (from actual windows): 4h: 36 of 149 windows overlap another; the largest disjoint subset has 131; 24h: 144 of 144 windows overlap another; the largest disjoint subset has 25; 72h: 133 of 133 windows overlap another; the largest disjoint subset has 8.

Not registered, by reason: late (3); rc1d-unavailable (27)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
