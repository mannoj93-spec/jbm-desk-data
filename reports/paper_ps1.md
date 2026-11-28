# Paper sizing experiment PS1

Generated 2026-11-28T00:27:59.358Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-27T20:25:59.684Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1674 physical; 1674 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 56.02 days; 337 scheduled decisions; coverage 82.8%; execution delay after the 4H close: median 21.8 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 278 closed intervals over 1340.1 h; extended intervals 15.

Outcomes: executed 279; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 44

Execution states: completed 279

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 278 | 1340 | -10.52% | -72.7% | 14.4% | -5.06 | 0.33 | 2.6 | 42.58 / 42.58 | -13.01% | -1.73% | -0.95% |
| ordinary | VOL | 278 | 1340 | -11.79% | -82.0% | 15.6% | -5.27 | 0.39 | 6.9 | 110.14 / 110.14 | -14.01% | -2.00% | -1.03% |
| ordinary | B2 | 278 | 1340 | -13.69% | -96.3% | 15.3% | -6.29 | 0.49 | 101.0 | 1653.22 / 1658.34 | -16.76% | -2.24% | -1.13% |
| stressed | FIXED | 278 | 1340 | -10.55% | -72.9% | 14.4% | -5.08 | 0.33 | 2.6 | 77.42 / 77.42 | -13.02% | -1.73% | -0.95% |
| stressed | VOL | 278 | 1340 | -11.87% | -82.6% | 15.6% | -5.31 | 0.39 | 6.9 | 200.14 / 200.14 | -14.06% | -2.00% | -1.03% |
| stressed | B2 | 278 | 1340 | -14.86% | -105.2% | 15.3% | -6.87 | 0.49 | 101.1 | 2951.74 / 2960.93 | -17.75% | -2.25% | -1.14% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 278 | 6 | -1.020 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -14.26% | -0.00008 | -0.062 | -0.00013 |
| stressed | 278 | 6 | -1.566 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -22.56% | -0.00012 | -0.098 | -0.00018 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-27T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 56.0 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
