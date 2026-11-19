# Paper sizing experiment PS1

Generated 2026-11-19T23:20:14.707Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-19T20:27:18.903Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1398 physical; 1398 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 47.97 days; 288 scheduled decisions; coverage 80.9%; execution delay after the 4H close: median 20.9 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 232 closed intervals over 1148.1 h; extended intervals 13.

Outcomes: executed 233; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 41

Execution states: completed 233

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 232 | 1148 | -9.37% | -75.1% | 12.3% | -6.13 | 0.33 | 3.0 | 42.58 / 42.58 | -10.02% | -1.36% | -0.81% |
| ordinary | VOL | 232 | 1148 | -10.92% | -88.3% | 15.3% | -5.78 | 0.41 | 7.9 | 110.14 / 110.14 | -11.75% | -2.00% | -1.01% |
| ordinary | B2 | 232 | 1148 | -12.60% | -102.7% | 14.5% | -7.07 | 0.53 | 110.1 | 1572.78 / 1572.78 | -14.13% | -2.24% | -1.09% |
| stressed | FIXED | 232 | 1148 | -9.41% | -75.4% | 12.3% | -6.15 | 0.33 | 3.0 | 77.42 / 77.42 | -10.02% | -1.36% | -0.81% |
| stressed | VOL | 232 | 1148 | -11.01% | -89.0% | 15.3% | -5.82 | 0.41 | 7.9 | 200.14 / 200.14 | -11.80% | -2.00% | -1.01% |
| stressed | B2 | 232 | 1148 | -13.71% | -112.5% | 14.5% | -7.76 | 0.53 | 110.2 | 2807.42 / 2807.42 | -15.13% | -2.25% | -1.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 232 | 5 | -1.294 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -14.49% | -0.00008 | -0.061 | -0.00016 |
| stressed | 232 | 5 | -1.933 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -23.58% | -0.00013 | -0.098 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-19T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 48.0 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
