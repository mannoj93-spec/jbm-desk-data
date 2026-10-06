# Paper sizing experiment PS1

Generated 2026-10-06T05:02:34.927Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-06T04:19:37.231Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 72 physical; 72 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 3.21 days; 20 scheduled decisions; coverage 60.0%; execution delay after the 4H close: median 14.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 11 closed intervals over 76.0 h; extended intervals 3.

Outcomes: executed 12; missed: stale: processed after close + max_delay 8

Execution states: completed 12

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 11 | 76 | 0.39% | 44.7% | 8.7% | 5.15 | 0.34 | 39.1 | 37.45 / 37.45 | -0.50% | -0.39% | -0.39% |
| ordinary | VOL | 11 | 76 | 0.51% | 58.8% | 11.4% | 5.15 | 0.45 | 51.4 | 49.25 / 49.25 | -0.66% | -0.51% | -0.51% |
| ordinary | B2 | 11 | 76 | 1.23% | 140.7% | 13.3% | 10.58 | 0.73 | 203.5 | 196.13 / 203.18 | -0.67% | -0.51% | -0.51% |
| stressed | FIXED | 11 | 76 | 0.36% | 41.2% | 8.7% | 4.72 | 0.34 | 39.2 | 68.11 / 68.11 | -0.50% | -0.39% | -0.39% |
| stressed | VOL | 11 | 76 | 0.47% | 54.1% | 11.5% | 4.72 | 0.45 | 51.4 | 89.57 / 89.57 | -0.66% | -0.51% | -0.51% |
| stressed | B2 | 11 | 76 | 1.07% | 122.3% | 13.4% | 9.14 | 0.73 | 203.6 | 356.28 / 369.09 | -0.70% | -0.51% | -0.51% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 11 | 0 | 5.424 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 81.90% | 0.00065 | 0.340 | 0.00076 |
| stressed | 11 | 0 | 4.414 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 68.15% | 0.00054 | 0.284 | 0.00064 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-06T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 3.2 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
