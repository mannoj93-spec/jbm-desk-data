# Paper sizing experiment PS1

Generated 2026-10-18T04:25:37.341Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-18T04:17:07.152Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 504 physical; 504 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 15.18 days; 92 scheduled decisions; coverage 91.3%; execution delay after the 4H close: median 18.5 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 83 closed intervals over 363.9 h; extended intervals 3.

Outcomes: executed 84; missed: stale: processed after close + max_delay 8

Execution states: completed 84

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 83 | 364 | -1.10% | -26.7% | 10.3% | -2.58 | 0.34 | 8.2 | 37.45 / 37.45 | -2.16% | -0.84% | -0.63% |
| ordinary | VOL | 83 | 364 | -1.57% | -38.1% | 14.6% | -2.61 | 0.47 | 13.4 | 60.71 / 60.71 | -2.96% | -1.25% | -0.89% |
| ordinary | B2 | 83 | 364 | -0.94% | -22.8% | 13.4% | -1.71 | 0.57 | 156.8 | 716.67 / 716.67 | -3.05% | -0.96% | -0.77% |
| stressed | FIXED | 83 | 364 | -1.14% | -27.5% | 10.4% | -2.65 | 0.34 | 8.2 | 68.11 / 68.11 | -2.16% | -0.84% | -0.63% |
| stressed | VOL | 83 | 364 | -1.62% | -39.3% | 14.6% | -2.69 | 0.47 | 13.4 | 110.37 / 110.37 | -2.97% | -1.25% | -0.89% |
| stressed | B2 | 83 | 364 | -1.52% | -36.9% | 13.3% | -2.77 | 0.57 | 156.8 | 1298.38 / 1298.38 | -3.47% | -0.96% | -0.77% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 83 | 1 | 0.905 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 15.35% | 0.00008 | 0.062 | 0.00002 |
| stressed | 83 | 1 | -0.077 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 2.45% | 0.00001 | 0.010 | -0.00005 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-18T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 15.2 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
