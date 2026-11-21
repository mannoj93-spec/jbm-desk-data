# Paper sizing experiment PS1

Generated 2026-11-21T04:26:42.544Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-21T04:26:37.325Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1440 physical; 1440 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 49.19 days; 296 scheduled decisions; coverage 81.1%; execution delay after the 4H close: median 21.1 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 239 closed intervals over 1180.1 h; extended intervals 14.

Outcomes: executed 240; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 42

Execution states: completed 240

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 239 | 1180 | -12.39% | -98.2% | 13.7% | -7.19 | 0.33 | 3.0 | 42.58 / 42.58 | -13.01% | -1.73% | -0.98% |
| ordinary | VOL | 239 | 1180 | -13.21% | -105.1% | 15.8% | -6.65 | 0.41 | 7.7 | 110.14 / 110.14 | -14.01% | -2.00% | -1.09% |
| ordinary | B2 | 239 | 1180 | -15.27% | -123.0% | 15.5% | -7.94 | 0.52 | 108.7 | 1592.26 / 1598.00 | -16.76% | -2.24% | -1.21% |
| stressed | FIXED | 239 | 1180 | -12.42% | -98.5% | 13.7% | -7.21 | 0.33 | 3.0 | 77.42 / 77.42 | -13.02% | -1.73% | -0.98% |
| stressed | VOL | 239 | 1180 | -13.29% | -105.8% | 15.8% | -6.70 | 0.41 | 7.7 | 200.14 / 200.14 | -14.06% | -2.00% | -1.09% |
| stressed | B2 | 239 | 1180 | -16.37% | -132.7% | 15.5% | -8.57 | 0.52 | 108.9 | 2842.38 / 2852.68 | -17.75% | -2.25% | -1.22% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 239 | 5 | -1.284 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -17.91% | -0.00010 | -0.074 | -0.00014 |
| stressed | 239 | 5 | -1.872 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -26.90% | -0.00015 | -0.111 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-21T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 49.2 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
