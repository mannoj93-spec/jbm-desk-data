# Paper sizing experiment PS1

Generated 2026-11-28T04:28:19.397Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-28T04:28:14.565Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1680 physical; 1680 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 56.19 days; 338 scheduled decisions; coverage 82.8%; execution delay after the 4H close: median 21.8 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 279 closed intervals over 1348.1 h; extended intervals 16.

Outcomes: executed 280; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 44

Execution states: completed 280

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 279 | 1348 | -10.40% | -71.3% | 14.3% | -4.98 | 0.33 | 2.6 | 42.58 / 42.58 | -13.01% | -1.73% | -0.95% |
| ordinary | VOL | 279 | 1348 | -11.70% | -80.8% | 15.5% | -5.20 | 0.39 | 6.8 | 110.14 / 110.14 | -14.01% | -2.00% | -1.03% |
| ordinary | B2 | 279 | 1348 | -13.61% | -95.1% | 15.3% | -6.22 | 0.48 | 100.7 | 1658.34 / 1676.88 | -16.76% | -2.24% | -1.13% |
| stressed | FIXED | 279 | 1348 | -10.43% | -71.6% | 14.3% | -4.99 | 0.33 | 2.6 | 77.42 / 77.42 | -13.02% | -1.73% | -0.95% |
| stressed | VOL | 279 | 1348 | -11.78% | -81.4% | 15.5% | -5.24 | 0.39 | 6.8 | 200.14 / 200.14 | -14.06% | -2.00% | -1.03% |
| stressed | B2 | 279 | 1348 | -14.78% | -104.0% | 15.3% | -6.80 | 0.48 | 100.9 | 2960.93 / 2994.20 | -17.75% | -2.25% | -1.14% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 279 | 6 | -1.018 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -14.24% | -0.00008 | -0.062 | -0.00013 |
| stressed | 279 | 6 | -1.563 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -22.51% | -0.00012 | -0.098 | -0.00018 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-28T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 56.2 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
