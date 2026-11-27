# Paper sizing experiment PS1

Generated 2026-11-27T08:28:40.491Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-27T08:28:35.892Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1656 physical; 1656 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 55.35 days; 333 scheduled decisions; coverage 82.9%; execution delay after the 4H close: median 21.8 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 275 closed intervals over 1328.1 h; extended intervals 15.

Outcomes: executed 276; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 43

Execution states: completed 276

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 275 | 1328 | -9.51% | -65.9% | 14.3% | -4.62 | 0.33 | 2.7 | 42.58 / 42.58 | -13.01% | -1.73% | -0.93% |
| ordinary | VOL | 275 | 1328 | -11.03% | -77.1% | 15.6% | -4.95 | 0.39 | 6.9 | 110.14 / 110.14 | -14.01% | -2.00% | -1.03% |
| ordinary | B2 | 275 | 1328 | -12.99% | -91.8% | 15.3% | -6.00 | 0.49 | 101.5 | 1648.21 / 1648.21 | -16.76% | -2.24% | -1.13% |
| stressed | FIXED | 275 | 1328 | -9.54% | -66.2% | 14.3% | -4.64 | 0.33 | 2.7 | 77.42 / 77.42 | -13.02% | -1.73% | -0.93% |
| stressed | VOL | 275 | 1328 | -11.11% | -77.7% | 15.6% | -4.99 | 0.39 | 6.9 | 200.14 / 200.14 | -14.06% | -2.00% | -1.03% |
| stressed | B2 | 275 | 1328 | -14.16% | -100.7% | 15.3% | -6.58 | 0.49 | 101.6 | 2942.76 / 2942.76 | -17.75% | -2.25% | -1.14% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 275 | 6 | -1.042 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -14.71% | -0.00008 | -0.064 | -0.00014 |
| stressed | 275 | 6 | -1.590 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -23.05% | -0.00013 | -0.100 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-27T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 55.4 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
