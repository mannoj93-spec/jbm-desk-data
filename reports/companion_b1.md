# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-03T15:01:03.822Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-03T12:25:00.000Z; last scored 2026-10-03T14:48:56.450Z. Stream start: 2026-10-01T00:00:00Z. Registered 45, confirmed 45, eligible 45. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 15 | 15 | 11 | 8 | 0 | 0 | 0 | 0 | -0.01353 | -0.01181 | 8/0/7 | 0.025 | -0.2266 | unavailable (0) | -0.15788 | -0.14436 |
| 24h | 10 | 10 | 2 | 10 | 0 | 0 | 0 | 0 | 0.04995 | 0.0541 | 1/0/9 | -0.1418 | 1.9469 | unavailable (0) | -0.163 | -0.21295 |
| 72h | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | —/—/— | — | — | unavailable (0) | — | — |

Overlap (from actual windows): 4h: 8 of 15 windows overlap another; the largest disjoint subset has 11; 24h: 10 of 10 windows overlap another; the largest disjoint subset has 2.

Not registered, by reason: rc1d-unavailable (3)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
