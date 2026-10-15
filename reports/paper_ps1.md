# Paper sizing experiment PS1

Generated 2026-10-15T08:21:47.657Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-15T08:21:45.965Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 402 physical; 402 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 12.35 days; 75 scheduled decisions; coverage 89.3%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 66 closed intervals over 296.0 h; extended intervals 3.

Outcomes: executed 67; missed: stale: processed after close + max_delay 8

Execution states: completed 67

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 66 | 296 | -1.38% | -41.1% | 11.0% | -3.75 | 0.34 | 10.1 | 37.45 / 37.45 | -2.11% | -0.84% | -0.70% |
| ordinary | VOL | 66 | 296 | -1.93% | -57.6% | 15.6% | -3.70 | 0.47 | 14.9 | 55.22 / 60.71 | -2.89% | -1.25% | -1.00% |
| ordinary | B2 | 66 | 296 | -0.84% | -25.1% | 14.4% | -1.74 | 0.58 | 153.7 | 572.41 / 572.41 | -3.04% | -0.96% | -0.84% |
| stressed | FIXED | 66 | 296 | -1.41% | -42.0% | 11.0% | -3.83 | 0.34 | 10.1 | 68.11 / 68.11 | -2.11% | -0.84% | -0.70% |
| stressed | VOL | 66 | 296 | -1.97% | -59.0% | 15.6% | -3.78 | 0.47 | 14.9 | 100.40 / 110.37 | -2.89% | -1.25% | -1.00% |
| stressed | B2 | 66 | 296 | -1.31% | -39.0% | 14.4% | -2.71 | 0.58 | 153.8 | 1037.85 / 1037.85 | -3.13% | -0.96% | -0.84% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 66 | 1 | 1.956 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 32.53% | 0.00017 | 0.131 | 0.00008 |
| stressed | 66 | 1 | 1.074 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 20.04% | 0.00010 | 0.082 | 0.00002 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-15T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 12.3 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
