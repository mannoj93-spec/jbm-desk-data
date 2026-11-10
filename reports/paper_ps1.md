# Paper sizing experiment PS1

Generated 2026-11-10T12:30:30.694Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-10T12:26:23.119Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1086 physical; 1086 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 38.52 days; 232 scheduled decisions; coverage 78.0%; execution delay after the 4H close: median 19.7 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 180 closed intervals over 924.1 h; extended intervals 9.

Outcomes: executed 181; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 37

Execution states: completed 181

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 180 | 924 | -4.14% | -40.1% | 10.8% | -3.71 | 0.33 | 3.3 | 37.45 / 37.45 | -4.87% | -1.36% | -0.69% |
| ordinary | VOL | 180 | 924 | -5.52% | -53.8% | 15.1% | -3.56 | 0.44 | 8.0 | 90.69 / 90.69 | -6.45% | -2.00% | -0.97% |
| ordinary | B2 | 180 | 924 | -6.78% | -66.6% | 13.9% | -4.79 | 0.58 | 121.2 | 1409.48 / 1430.34 | -8.43% | -2.24% | -1.03% |
| stressed | FIXED | 180 | 924 | -4.17% | -40.4% | 10.8% | -3.73 | 0.33 | 3.3 | 68.11 / 68.11 | -4.88% | -1.36% | -0.69% |
| stressed | VOL | 180 | 924 | -5.59% | -54.5% | 15.1% | -3.61 | 0.44 | 8.0 | 164.86 / 164.86 | -6.49% | -2.00% | -0.97% |
| stressed | B2 | 180 | 924 | -7.85% | -77.5% | 13.9% | -5.59 | 0.58 | 121.2 | 2527.88 / 2565.36 | -9.37% | -2.25% | -1.03% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 180 | 4 | -1.228 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -12.80% | -0.00007 | -0.051 | -0.00016 |
| stressed | 180 | 4 | -1.978 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -23.01% | -0.00013 | -0.091 | -0.00022 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-10T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 38.5 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
