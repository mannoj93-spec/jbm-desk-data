# Paper sizing experiment PS1

Generated 2026-11-19T08:25:41.308Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-19T08:25:37.597Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1380 physical; 1380 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 47.35 days; 285 scheduled decisions; coverage 80.7%; execution delay after the 4H close: median 20.8 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 229 closed intervals over 1136.1 h; extended intervals 13.

Outcomes: executed 230; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 41

Execution states: completed 230

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 229 | 1136 | -8.66% | -69.8% | 12.2% | -5.70 | 0.33 | 3.1 | 42.58 / 42.58 | -9.86% | -1.36% | -0.81% |
| ordinary | VOL | 229 | 1136 | -10.38% | -84.5% | 15.3% | -5.51 | 0.41 | 8.0 | 110.14 / 110.14 | -11.63% | -2.00% | -1.01% |
| ordinary | B2 | 229 | 1136 | -12.00% | -98.6% | 14.6% | -6.77 | 0.53 | 110.7 | 1567.12 / 1572.78 | -13.90% | -2.24% | -1.09% |
| stressed | FIXED | 229 | 1136 | -8.69% | -70.1% | 12.2% | -5.73 | 0.33 | 3.1 | 77.42 / 77.42 | -9.86% | -1.36% | -0.81% |
| stressed | VOL | 229 | 1136 | -10.46% | -85.2% | 15.3% | -5.56 | 0.41 | 8.0 | 200.14 / 200.14 | -11.68% | -2.00% | -1.01% |
| stressed | B2 | 229 | 1136 | -13.12% | -108.4% | 14.6% | -7.45 | 0.53 | 110.8 | 2797.26 / 2807.42 | -14.90% | -2.25% | -1.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 229 | 5 | -1.253 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -14.06% | -0.00008 | -0.059 | -0.00016 |
| stressed | 229 | 5 | -1.893 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -23.21% | -0.00013 | -0.096 | -0.00022 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-19T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 47.4 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
