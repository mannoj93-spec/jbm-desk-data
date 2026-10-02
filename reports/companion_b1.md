# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-02T08:16:21.515Z by companion-1.2.0; source cutoff 2026-10-02T04:54:22.763Z. Stream start: 2026-10-01T00:00:00Z. Registered 27, confirmed 27, eligible 27. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 7 | 7 | 5 | 4 | 0 | 0 | 0 | 0 | 0.01831 | 0.03428 | 2/0/5 | -0.0403 | 0.4354 | unavailable (0) | -0.02869 | -0.04699 |
| 24h | 2 | 2 | 1 | 2 | 0 | 0 | 0 | 0 | 0.02228 | 0.02228 | 1/0/1 | -0.1022 | 0.5031 | unavailable (0) | -0.17974 | -0.20203 |
| 72h | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | —/—/— | — | — | unavailable (0) | — | — |

Overlap (from actual windows): 4h: 4 of 7 windows overlap another; the largest disjoint subset has 5; 24h: 2 of 2 windows overlap another; the largest disjoint subset has 1.

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
