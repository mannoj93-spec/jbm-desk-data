# Paper sizing experiment PS1

Generated 2026-11-27T04:27:11.239Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-27T04:27:05.513Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1650 physical; 1650 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 55.19 days; 332 scheduled decisions; coverage 82.8%; execution delay after the 4H close: median 21.7 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 274 closed intervals over 1324.1 h; extended intervals 15.

Outcomes: executed 275; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 43

Execution states: completed 275

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 274 | 1324 | -9.71% | -67.6% | 14.3% | -4.74 | 0.33 | 2.7 | 42.58 / 42.58 | -13.01% | -1.73% | -0.93% |
| ordinary | VOL | 274 | 1324 | -11.18% | -78.4% | 15.6% | -5.04 | 0.39 | 6.9 | 110.14 / 110.14 | -14.01% | -2.00% | -1.03% |
| ordinary | B2 | 274 | 1324 | -13.13% | -93.1% | 15.3% | -6.08 | 0.49 | 101.4 | 1642.77 / 1648.21 | -16.76% | -2.24% | -1.13% |
| stressed | FIXED | 274 | 1324 | -9.74% | -67.8% | 14.3% | -4.75 | 0.33 | 2.7 | 77.42 / 77.42 | -13.02% | -1.73% | -0.93% |
| stressed | VOL | 274 | 1324 | -11.26% | -79.0% | 15.6% | -5.07 | 0.39 | 6.9 | 200.14 / 200.14 | -14.06% | -2.00% | -1.03% |
| stressed | B2 | 274 | 1324 | -14.29% | -102.0% | 15.3% | -6.66 | 0.49 | 101.6 | 2933.00 / 2942.76 | -17.75% | -2.25% | -1.14% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 274 | 6 | -1.040 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -14.68% | -0.00008 | -0.064 | -0.00014 |
| stressed | 274 | 6 | -1.586 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -23.01% | -0.00013 | -0.099 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-27T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 55.2 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
