# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-15T08:33:05.683Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-15T04:25:00.000Z; last scored 2026-10-15T05:08:39.056Z. Stream start: 2026-10-01T00:00:00Z. Registered 237, confirmed 237, eligible 237. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 77 | 77 | 64 | 26 | 0 | 0 | 0 | 0 | -0.0053 | 0.00242 | 38/0/39 | 0.0123 | -0.1464 | unavailable (1) | -0.10556 | -0.10026 |
| 24h | 72 | 72 | 12 | 72 | 0 | 0 | 0 | 0 | -0.01105 | -0.00107 | 36/0/36 | 0.031 | -0.2236 | unavailable (1) | -0.14718 | -0.13613 |
| 72h | 60 | 60 | 4 | 60 | 0 | 0 | 0 | 0 | -0.00646 | -0.01105 | 34/0/26 | 0.0386 | -0.1226 | unavailable (1) | -0.10389 | -0.09744 |

Overlap (from actual windows): 4h: 26 of 77 windows overlap another; the largest disjoint subset has 64; 24h: 72 of 72 windows overlap another; the largest disjoint subset has 12; 72h: 60 of 60 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
