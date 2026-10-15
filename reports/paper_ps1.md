# Paper sizing experiment PS1

Generated 2026-10-15T13:28:21.583Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-15T12:20:53.220Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 408 physical; 408 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 12.56 days; 76 scheduled decisions; coverage 89.5%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 67 closed intervals over 300.0 h; extended intervals 3.

Outcomes: executed 68; missed: stale: processed after close + max_delay 8

Execution states: completed 68

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 67 | 300 | -1.46% | -43.0% | 10.9% | -3.95 | 0.34 | 10.0 | 37.45 / 37.45 | -2.16% | -0.84% | -0.70% |
| ordinary | VOL | 67 | 300 | -2.04% | -60.3% | 15.5% | -3.90 | 0.47 | 16.2 | 60.71 / 60.71 | -2.96% | -1.25% | -1.00% |
| ordinary | B2 | 67 | 300 | -0.93% | -27.2% | 14.3% | -1.90 | 0.58 | 151.7 | 572.41 / 584.54 | -3.04% | -0.96% | -0.84% |
| stressed | FIXED | 67 | 300 | -1.49% | -43.9% | 10.9% | -4.03 | 0.34 | 10.0 | 68.11 / 68.11 | -2.16% | -0.84% | -0.70% |
| stressed | VOL | 67 | 300 | -2.09% | -61.8% | 15.5% | -3.99 | 0.47 | 16.2 | 110.37 / 110.37 | -2.97% | -1.25% | -1.00% |
| stressed | B2 | 67 | 300 | -1.39% | -40.9% | 14.3% | -2.87 | 0.58 | 151.7 | 1037.85 / 1059.79 | -3.13% | -0.96% | -0.84% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 67 | 1 | 1.996 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 33.10% | 0.00017 | 0.134 | 0.00008 |
| stressed | 67 | 1 | 1.127 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 20.91% | 0.00011 | 0.086 | 0.00002 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-15T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 12.6 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
