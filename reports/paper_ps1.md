# Paper sizing experiment PS1

Generated 2026-11-17T12:28:18.345Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-17T12:28:12.940Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1320 physical; 1320 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 45.52 days; 274 scheduled decisions; coverage 80.3%; execution delay after the 4H close: median 20.7 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 219 closed intervals over 1092.1 h; extended intervals 12.

Outcomes: executed 220; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 220

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 219 | 1092 | -8.03% | -67.1% | 12.0% | -5.61 | 0.33 | 3.2 | 42.58 / 42.58 | -9.14% | -1.36% | -0.80% |
| ordinary | VOL | 219 | 1092 | -9.90% | -83.6% | 15.4% | -5.43 | 0.42 | 8.3 | 110.14 / 110.14 | -11.11% | -2.00% | -1.04% |
| ordinary | B2 | 219 | 1092 | -11.48% | -97.9% | 14.7% | -6.68 | 0.54 | 114.2 | 1560.41 / 1560.41 | -13.42% | -2.24% | -1.13% |
| stressed | FIXED | 219 | 1092 | -8.06% | -67.4% | 12.0% | -5.64 | 0.33 | 3.2 | 77.42 / 77.42 | -9.15% | -1.36% | -0.80% |
| stressed | VOL | 219 | 1092 | -9.99% | -84.4% | 15.4% | -5.47 | 0.42 | 8.3 | 200.14 / 200.14 | -11.15% | -2.00% | -1.04% |
| stressed | B2 | 219 | 1092 | -12.61% | -108.1% | 14.6% | -7.38 | 0.54 | 114.3 | 2785.41 / 2785.41 | -14.41% | -2.25% | -1.13% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 219 | 5 | -1.250 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -14.21% | -0.00008 | -0.058 | -0.00018 |
| stressed | 219 | 5 | -1.908 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -23.68% | -0.00013 | -0.097 | -0.00023 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-17T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 45.5 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
