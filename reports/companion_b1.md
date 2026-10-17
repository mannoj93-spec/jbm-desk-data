# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-17T13:18:08.912Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-10-17T12:25:00.000Z; last scored 2026-10-17T13:12:41.457Z. Stream start: 2026-10-01T00:00:00Z. Registered 276, confirmed 276, eligible 276. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 91 | 91 | 75 | 32 | 0 | 0 | 0 | 0 | -0.00732 | -0.00293 | 48/0/43 | 0.0165 | -0.2006 | unavailable (2) | -0.11259 | -0.10526 |
| 24h | 86 | 86 | 15 | 86 | 0 | 0 | 0 | 0 | -0.00897 | 0.00239 | 41/0/45 | 0.0271 | -0.1925 | unavailable (2) | -0.15591 | -0.14694 |
| 72h | 74 | 74 | 5 | 74 | 0 | 0 | 0 | 0 | -0.00834 | -0.01105 | 43/0/31 | 0.0567 | -0.1686 | unavailable (1) | -0.12751 | -0.11917 |

Overlap (from actual windows): 4h: 32 of 91 windows overlap another; the largest disjoint subset has 75; 24h: 86 of 86 windows overlap another; the largest disjoint subset has 15; 72h: 74 of 74 windows overlap another; the largest disjoint subset has 5.

Not registered, by reason: rc1d-unavailable (24)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
