# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-11-10T13:05:45.772Z by companion-1.3.0; observation cutoff (latest included outcome-window end) 2026-11-10T12:25:00.000Z; last scored 2026-11-10T13:01:32.880Z. Stream start: 2026-10-01T00:00:00Z. Registered 522, confirmed 522, eligible 522. Lifecycle active. Evidence class: **descriptive**. Integrity: ok (0 recorded failure rows).

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 201 | 174 | 154 | 40 | 27 | 0 | 0 | 0 | -0.0059 | -0.00301 | 93/0/81 | 0.0143 | -0.1786 | unavailable (4) | -0.09105 | -0.08515 |
| 24h | 196 | 173 | 32 | 173 | 23 | 0 | 0 | 0 | -0.00766 | -0.00335 | 91/0/82 | 0.0228 | -0.1767 | unavailable (4) | -0.10538 | -0.09772 |
| 72h | 184 | 168 | 11 | 168 | 16 | 0 | 0 | 0 | -0.01275 | -0.01708 | 110/0/58 | 0.0503 | -0.3088 | unavailable (4) | -0.05401 | -0.04126 |

Overlap (from actual windows): 4h: 40 of 174 windows overlap another; the largest disjoint subset has 154; 24h: 173 of 173 windows overlap another; the largest disjoint subset has 32; 72h: 168 of 168 windows overlap another; the largest disjoint subset has 11.

Not registered, by reason: late (57); rc1d-unavailable (135)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions (a resampling device for dependence, not a measured effective sample size), 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair or any integrity failure; 'retired' once terminated.
