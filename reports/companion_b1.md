# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)

Generated 2026-10-01T09:03:04.502Z by companion-1.1.0. Stream start: 2026-10-01T00:00:00Z. Registered 9, confirmed 9, eligible 9. Lifecycle active. Evidence class: **descriptive**. Integrity failures recorded: 0.

> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.

| horizon | RC1D scored (eligible) | paired | non-overlapping | missing | late | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (blocks) | B2−B0 mean (same windows) | B1−B0 mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4h | 2 | 2 | 2 | 0 | 0 | 0 | -0.00158 | -0.00158 | 1/0/1 | 0.0045 | -0.0225 | unavailable (0) | -0.01806 | -0.01648 |
| 24h | 0 | 0 | 0 | 0 | 0 | 0 | — | — | —/—/— | — | — | unavailable (0) | — | — |
| 72h | 0 | 0 | 0 | 0 | 0 | 0 | — | — | —/—/— | — | — | unavailable (0) | — | — |

Overlap: 24h windows start every 4h and overlap 6-fold; consecutive pairs are dependent (about 0 non-overlapping windows) 72h windows start every 4h and overlap 18-fold; consecutive pairs are dependent (about 0 non-overlapping windows)

Method: companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows. Uncertainty: moving-block bootstrap of paired differences, blocks of 42 decisions, 2000 resamples, seed 20260930, 95% interval; reported only from 10 blocks. Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent.
Evidence class rule: no pre-registered success threshold exists for the companion, so its ceiling is 'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; 'unavailable' with no scored pair; 'retired' once terminated.
