# Paper sizing experiment PS1

Generated 2026-10-18T00:33:03.060Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-18T00:18:21.928Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 498 physical; 498 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 15.02 days; 91 scheduled decisions; coverage 91.2%; execution delay after the 4H close: median 18.5 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 82 closed intervals over 360.0 h; extended intervals 3.

Outcomes: executed 83; missed: stale: processed after close + max_delay 8

Execution states: completed 83

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 82 | 360 | -1.27% | -31.1% | 10.4% | -3.00 | 0.34 | 8.3 | 37.45 / 37.45 | -2.16% | -0.84% | -0.63% |
| ordinary | VOL | 82 | 360 | -1.79% | -44.0% | 14.6% | -3.01 | 0.47 | 13.5 | 60.71 / 60.71 | -2.96% | -1.25% | -0.89% |
| ordinary | B2 | 82 | 360 | -1.18% | -28.8% | 13.4% | -2.15 | 0.57 | 149.7 | 677.04 / 716.67 | -3.05% | -0.96% | -0.77% |
| stressed | FIXED | 82 | 360 | -1.30% | -31.9% | 10.4% | -3.07 | 0.34 | 8.3 | 68.11 / 68.11 | -2.16% | -0.84% | -0.63% |
| stressed | VOL | 82 | 360 | -1.84% | -45.3% | 14.7% | -3.09 | 0.47 | 13.5 | 110.37 / 110.37 | -2.97% | -1.25% | -0.89% |
| stressed | B2 | 82 | 360 | -1.72% | -42.3% | 13.4% | -3.17 | 0.57 | 149.8 | 1226.74 / 1298.38 | -3.47% | -0.96% | -0.77% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 82 | 1 | 0.852 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 15.21% | 0.00008 | 0.061 | 0.00001 |
| stressed | 82 | 1 | -0.078 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 2.95% | 0.00001 | 0.012 | -0.00005 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-18T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 15.0 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
