# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-10T09:01:09.559Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-10T08:25:00.000Z; last scored 2026-10-10T08:54:11.893Z. Stream start: 2026-10-01T00:00:00Z. Registered 147, confirmed 147, eligible 147. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 48 | 48 | 39 | 18 | 0 | 0 | 0 | 0 | -0.00401 | 0.01186 | 22/0/26 | 0.0085 | -0.094 | unavailable (1) | -0.0784 | -0.07439 |
| 24h | 43 | 43 | 8 | 43 | 0 | 0 | 0 | 0 | -0.00692 | 0.01681 | 20/0/23 | 0.0202 | -0.1207 | unavailable (1) | -0.12075 | -0.11383 |
| 72h | 31 | 31 | 2 | 31 | 0 | 0 | 0 | 0 | 0.00549 | 0.04264 | 13/0/18 | -0.0303 | 0.0821 | unavailable (0) | -0.09015 | -0.09564 |

Overlap (from actual windows): 4h: 18 of 48 windows overlap another; the largest disjoint subset has 39; 24h: 43 of 43 windows overlap another; the largest disjoint subset has 8; 72h: 31 of 31 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
