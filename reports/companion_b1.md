# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-18T04:25:35.538Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-18T00:25:00.000Z; last scored 2026-10-18T01:14:19.849Z. Stream start: 2026-10-01T00:00:00Z. Registered 288, confirmed 288, eligible 288. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 94 | 94 | 78 | 32 | 0 | 0 | 0 | 0 | -0.00687 | -0.00254 | 49/0/45 | 0.0155 | -0.1859 | unavailable (2) | -0.10926 | -0.1024 |
| 24h | 89 | 89 | 15 | 89 | 0 | 0 | 0 | 0 | -0.01144 | 0.00148 | 44/0/45 | 0.0345 | -0.24 | unavailable (2) | -0.16579 | -0.15434 |
| 72h | 77 | 77 | 5 | 77 | 0 | 0 | 0 | 0 | -0.00914 | -0.01213 | 46/0/31 | 0.062 | -0.1879 | unavailable (1) | -0.11847 | -0.10932 |

Overlap (from actual windows): 4h: 32 of 94 windows overlap another; the largest disjoint subset has 78; 24h: 89 of 89 windows overlap another; the largest disjoint subset has 15; 72h: 77 of 77 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
