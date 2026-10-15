# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-15T12:34:16.254Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-15T08:25:00.000Z; last scored 2026-10-15T09:12:29.658Z. Stream start: 2026-10-01T00:00:00Z. Registered 240, confirmed 240, eligible 240. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 78 | 78 | 65 | 26 | 0 | 0 | 0 | 0 | -0.00491 | 0.0033 | 38/0/40 | 0.0114 | -0.1357 | unavailable (1) | -0.10975 | -0.10485 |
| 24h | 73 | 73 | 13 | 73 | 0 | 0 | 0 | 0 | -0.01087 | 0.00148 | 36/0/37 | 0.0303 | -0.2215 | unavailable (1) | -0.15033 | -0.13946 |
| 72h | 61 | 61 | 4 | 61 | 0 | 0 | 0 | 0 | -0.00648 | -0.01045 | 35/0/26 | 0.0393 | -0.1241 | unavailable (1) | -0.10483 | -0.09835 |

Overlap (from actual windows): 4h: 26 of 78 windows overlap another; the largest disjoint subset has 65; 24h: 73 of 73 windows overlap another; the largest disjoint subset has 13; 72h: 61 of 61 windows overlap another; the largest disjoint subset has 4.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
