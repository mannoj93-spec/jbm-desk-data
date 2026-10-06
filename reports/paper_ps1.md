# Paper sizing experiment PS1

Generated 2026-10-06T00:23:28.904Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-06T00:13:13.621Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 66 physical; 66 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 3.02 days; 19 scheduled decisions; coverage 57.9%; execution delay after the 4H close: median 13.2 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 10 closed intervals over 71.9 h; extended intervals 3.

Outcomes: executed 11; missed: stale: processed after close + max_delay 8

Execution states: completed 11

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 10 | 72 | 0.49% | 59.9% | 8.9% | 6.70 | 0.34 | 41.3 | 37.45 / 37.45 | -0.50% | -0.39% | -0.39% |
| ordinary | VOL | 10 | 72 | 0.65% | 78.7% | 11.7% | 6.70 | 0.45 | 54.3 | 49.25 / 49.25 | -0.66% | -0.51% | -0.51% |
| ordinary | B2 | 10 | 72 | 1.39% | 168.7% | 13.5% | 12.46 | 0.74 | 198.7 | 181.13 / 196.13 | -0.67% | -0.51% | -0.51% |
| stressed | FIXED | 10 | 72 | 0.46% | 56.1% | 9.0% | 6.25 | 0.34 | 41.4 | 68.11 / 68.11 | -0.50% | -0.39% | -0.39% |
| stressed | VOL | 10 | 72 | 0.61% | 73.8% | 11.8% | 6.25 | 0.45 | 54.4 | 89.57 / 89.57 | -0.66% | -0.51% | -0.51% |
| stressed | B2 | 10 | 72 | 1.24% | 150.8% | 13.6% | 11.08 | 0.74 | 198.8 | 329.05 / 356.28 | -0.70% | -0.51% | -0.51% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 10 | 0 | 5.762 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 90.05% | 0.00074 | 0.374 | 0.00089 |
| stressed | 10 | 0 | 4.826 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 76.98% | 0.00063 | 0.321 | 0.00078 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-06T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 3.0 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
