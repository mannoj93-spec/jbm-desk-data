# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-11-27T08:28:37.018Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-11-27T00:15:00.000Z; last scored 2026-11-27T01:17:11.998Z. Stream start: 2026-10-01T00:00:00Z. Registered 552, confirmed 552, eligible 552. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 300 | 184 | 164 | 40 | 116 | 0 | 0 | 0 | -0.00507 | -0.00295 | 97/0/87 | 0.012 | -0.146 | unavailable (4) | -0.08815 | -0.08309 |
| 24h | 295 | 183 | 37 | 182 | 112 | 0 | 0 | 0 | -0.00649 | -0.00322 | 95/0/88 | 0.0191 | -0.1431 | unavailable (4) | -0.10121 | -0.09471 |
| 72h | 283 | 181 | 14 | 181 | 102 | 0 | 0 | 0 | -0.01146 | -0.01536 | 117/0/64 | 0.0456 | -0.2604 | unavailable (4) | -0.05148 | -0.04002 |

Overlap (from actual windows): 4h: 40 of 184 windows overlap another; the largest disjoint subset has 164; 24h: 182 of 183 windows overlap another; the largest disjoint subset has 37; 72h: 181 of 181 windows overlap another; the largest disjoint subset has 14.

Not registered, by reason: late (312); rc1d-unavailable (153)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
