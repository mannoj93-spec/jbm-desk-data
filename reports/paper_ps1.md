# Paper sizing experiment PS1

Generated 2026-11-19T12:42:41.966Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-19T12:25:51.911Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1386 physical; 1386 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 47.53 days; 286 scheduled decisions; coverage 80.8%; execution delay after the 4H close: median 20.8 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 230 closed intervals over 1140.1 h; extended intervals 13.

Outcomes: executed 231; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 41

Execution states: completed 231

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 230 | 1140 | -8.70% | -70.0% | 12.2% | -5.73 | 0.33 | 3.1 | 42.58 / 42.58 | -9.86% | -1.36% | -0.81% |
| ordinary | VOL | 230 | 1140 | -10.41% | -84.5% | 15.3% | -5.52 | 0.41 | 8.0 | 110.14 / 110.14 | -11.63% | -2.00% | -1.01% |
| ordinary | B2 | 230 | 1140 | -12.04% | -98.6% | 14.5% | -6.78 | 0.53 | 110.7 | 1572.78 / 1572.78 | -13.90% | -2.24% | -1.09% |
| stressed | FIXED | 230 | 1140 | -8.74% | -70.2% | 12.2% | -5.75 | 0.33 | 3.1 | 77.42 / 77.42 | -9.86% | -1.36% | -0.81% |
| stressed | VOL | 230 | 1140 | -10.50% | -85.2% | 15.3% | -5.57 | 0.41 | 8.0 | 200.14 / 200.14 | -11.68% | -2.00% | -1.01% |
| stressed | B2 | 230 | 1140 | -13.17% | -108.5% | 14.5% | -7.47 | 0.53 | 110.8 | 2807.42 / 2807.42 | -14.90% | -2.25% | -1.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 230 | 5 | -1.258 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -14.09% | -0.00008 | -0.059 | -0.00016 |
| stressed | 230 | 5 | -1.900 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -23.26% | -0.00013 | -0.096 | -0.00022 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-19T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 47.5 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
