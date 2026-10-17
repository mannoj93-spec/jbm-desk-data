# Paper sizing experiment PS1

Generated 2026-10-17T16:22:40.633Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-17T16:17:34.968Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 486 physical; 486 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 14.68 days; 89 scheduled decisions; coverage 91.0%; execution delay after the 4H close: median 18.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 80 closed intervals over 352.0 h; extended intervals 3.

Outcomes: executed 81; missed: stale: processed after close + max_delay 8

Execution states: completed 81

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 80 | 352 | -1.32% | -33.1% | 10.5% | -3.16 | 0.34 | 8.5 | 37.45 / 37.45 | -2.16% | -0.84% | -0.63% |
| ordinary | VOL | 80 | 352 | -1.86% | -46.7% | 14.8% | -3.16 | 0.47 | 13.8 | 60.71 / 60.71 | -2.96% | -1.25% | -0.89% |
| ordinary | B2 | 80 | 352 | -1.32% | -33.0% | 13.4% | -2.46 | 0.57 | 153.1 | 677.04 / 677.04 | -3.05% | -0.96% | -0.77% |
| stressed | FIXED | 80 | 352 | -1.35% | -33.9% | 10.5% | -3.23 | 0.34 | 8.5 | 68.11 / 68.11 | -2.16% | -0.84% | -0.63% |
| stressed | VOL | 80 | 352 | -1.91% | -48.0% | 14.8% | -3.24 | 0.47 | 13.8 | 110.37 / 110.37 | -2.97% | -1.25% | -0.89% |
| stressed | B2 | 80 | 352 | -1.86% | -46.8% | 13.4% | -3.49 | 0.57 | 153.1 | 1226.74 / 1226.74 | -3.47% | -0.96% | -0.77% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 80 | 1 | 0.701 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 13.74% | 0.00007 | 0.055 | 0.00000 |
| stressed | 80 | 1 | -0.248 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 1.21% | 0.00001 | 0.005 | -0.00006 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-17T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 14.7 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
