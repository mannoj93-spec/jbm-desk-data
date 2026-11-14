# Paper sizing experiment PS1

Generated 2026-11-14T18:36:00.332Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-14T16:22:39.000Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1218 physical; 1218 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 42.78 days; 257 scheduled decisions; coverage 79.0%; execution delay after the 4H close: median 20.4 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 202 closed intervals over 1024.0 h; extended intervals 12.

Outcomes: executed 203; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 203

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 202 | 1024 | -7.83% | -69.8% | 11.6% | -6.01 | 0.33 | 3.4 | 42.58 / 42.58 | -8.49% | -1.36% | -0.78% |
| ordinary | VOL | 202 | 1024 | -9.69% | -87.2% | 15.6% | -5.59 | 0.43 | 8.3 | 103.56 / 103.56 | -10.54% | -2.00% | -1.04% |
| ordinary | B2 | 202 | 1024 | -11.21% | -101.7% | 14.8% | -6.86 | 0.56 | 117.6 | 1502.65 / 1516.36 | -12.77% | -2.24% | -1.13% |
| stressed | FIXED | 202 | 1024 | -7.87% | -70.1% | 11.6% | -6.04 | 0.33 | 3.4 | 77.42 / 77.42 | -8.49% | -1.36% | -0.78% |
| stressed | VOL | 202 | 1024 | -9.77% | -88.0% | 15.6% | -5.64 | 0.43 | 8.3 | 188.25 / 188.25 | -10.58% | -2.00% | -1.04% |
| stressed | B2 | 202 | 1024 | -12.30% | -112.3% | 14.8% | -7.58 | 0.56 | 117.6 | 2695.25 / 2719.87 | -13.74% | -2.25% | -1.13% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 202 | 4 | -1.264 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -14.47% | -0.00008 | -0.058 | -0.00018 |
| stressed | 202 | 4 | -1.938 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -24.30% | -0.00014 | -0.097 | -0.00024 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-14T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 42.8 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
