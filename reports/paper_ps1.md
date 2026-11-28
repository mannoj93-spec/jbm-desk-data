# Paper sizing experiment PS1

Generated 2026-11-28T16:52:13.854Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-28T16:26:58.263Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1698 physical; 1698 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 56.7 days; 341 scheduled decisions; coverage 83.0%; execution delay after the 4H close: median 21.8 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 282 closed intervals over 1360.1 h; extended intervals 16.

Outcomes: executed 283; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 44

Execution states: completed 283

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 282 | 1360 | -10.69% | -72.8% | 14.3% | -5.10 | 0.33 | 2.6 | 42.58 / 42.58 | -13.01% | -1.73% | -0.92% |
| ordinary | VOL | 282 | 1360 | -11.92% | -81.7% | 15.5% | -5.29 | 0.39 | 6.8 | 110.14 / 110.14 | -14.01% | -2.00% | -1.01% |
| ordinary | B2 | 282 | 1360 | -13.99% | -97.1% | 15.2% | -6.37 | 0.48 | 101.4 | 1682.75 / 1690.85 | -16.76% | -2.24% | -1.10% |
| stressed | FIXED | 282 | 1360 | -10.72% | -73.0% | 14.3% | -5.11 | 0.33 | 2.6 | 77.42 / 77.42 | -13.02% | -1.73% | -0.92% |
| stressed | VOL | 282 | 1360 | -12.00% | -82.3% | 15.5% | -5.32 | 0.39 | 6.8 | 200.14 / 200.14 | -14.06% | -2.00% | -1.01% |
| stressed | B2 | 282 | 1360 | -15.18% | -106.0% | 15.2% | -6.96 | 0.48 | 101.6 | 3004.73 / 3019.25 | -17.75% | -2.25% | -1.11% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 282 | 6 | -1.089 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -15.34% | -0.00008 | -0.067 | -0.00013 |
| stressed | 282 | 6 | -1.640 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -23.69% | -0.00013 | -0.103 | -0.00018 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-28T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 56.7 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
