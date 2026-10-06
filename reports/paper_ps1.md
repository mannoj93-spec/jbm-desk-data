# Paper sizing experiment PS1

Generated 2026-10-06T08:19:18.566Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-06T08:18:23.878Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 78 physical; 78 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 3.35 days; 21 scheduled decisions; coverage 61.9%; execution delay after the 4H close: median 16.1 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 12 closed intervals over 80.0 h; extended intervals 3.

Outcomes: executed 13; missed: stale: processed after close + max_delay 8

Execution states: completed 13

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 12 | 80 | 0.46% | 50.4% | 8.3% | 6.06 | 0.34 | 37.2 | 37.45 / 37.45 | -0.50% | -0.39% | -0.39% |
| ordinary | VOL | 12 | 80 | 0.61% | 66.2% | 10.9% | 6.07 | 0.45 | 48.8 | 49.25 / 49.25 | -0.66% | -0.51% | -0.51% |
| ordinary | B2 | 12 | 80 | 1.31% | 142.9% | 12.7% | 11.26 | 0.71 | 200.3 | 203.18 / 203.18 | -0.67% | -0.51% | -0.51% |
| stressed | FIXED | 12 | 80 | 0.43% | 47.0% | 8.3% | 5.63 | 0.34 | 37.2 | 68.11 / 68.11 | -0.50% | -0.39% | -0.39% |
| stressed | VOL | 12 | 80 | 0.57% | 61.8% | 11.0% | 5.64 | 0.45 | 48.9 | 89.57 / 89.57 | -0.66% | -0.51% | -0.51% |
| stressed | B2 | 12 | 80 | 1.15% | 124.8% | 12.8% | 9.78 | 0.71 | 200.4 | 369.09 / 369.09 | -0.70% | -0.51% | -0.51% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 12 | 0 | 5.197 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 76.65% | 0.00058 | 0.319 | 0.00070 |
| stressed | 12 | 0 | 4.140 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 62.96% | 0.00048 | 0.264 | 0.00059 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-06T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 3.3 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
