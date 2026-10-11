# Paper sizing experiment PS1

Generated 2026-10-11T04:21:37.073Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-11T04:21:35.734Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 252 physical; 252 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 8.18 days; 50 scheduled decisions; coverage 84.0%; execution delay after the 4H close: median 18.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 41 closed intervals over 196.0 h; extended intervals 3.

Outcomes: executed 42; missed: stale: processed after close + max_delay 8

Execution states: completed 42

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 41 | 196 | -0.71% | -31.7% | 8.8% | -3.58 | 0.34 | 15.3 | 37.45 / 37.45 | -2.01% | -0.60% | -0.51% |
| ordinary | VOL | 41 | 196 | -0.94% | -42.0% | 11.7% | -3.59 | 0.46 | 22.5 | 55.22 / 55.22 | -2.64% | -0.79% | -0.67% |
| ordinary | B2 | 41 | 196 | -0.40% | -18.0% | 13.1% | -1.37 | 0.63 | 160.9 | 397.54 / 413.92 | -3.04% | -0.96% | -0.76% |
| stressed | FIXED | 41 | 196 | -0.74% | -33.0% | 8.8% | -3.73 | 0.34 | 15.3 | 68.11 / 68.11 | -2.01% | -0.60% | -0.51% |
| stressed | VOL | 41 | 196 | -0.98% | -44.1% | 11.7% | -3.76 | 0.46 | 22.5 | 100.40 / 100.40 | -2.64% | -0.79% | -0.67% |
| stressed | B2 | 41 | 196 | -0.72% | -32.5% | 13.0% | -2.49 | 0.63 | 161.0 | 721.13 / 750.80 | -3.13% | -0.96% | -0.76% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 41 | 0 | 2.214 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 24.04% | 0.00013 | 0.122 | 0.00007 |
| stressed | 41 | 0 | 1.265 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 11.58% | 0.00006 | 0.059 | 0.00000 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-11T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 8.2 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
