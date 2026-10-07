# Paper sizing experiment PS1

Generated 2026-10-07T16:22:06.008Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-07T16:21:03.058Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 126 physical; 126 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 4.68 days; 29 scheduled decisions; coverage 72.4%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 20 closed intervals over 112.0 h; extended intervals 3.

Outcomes: executed 21; missed: stale: processed after close + max_delay 8

Execution states: completed 21

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 20 | 112 | -0.41% | -32.0% | 9.7% | -3.30 | 0.34 | 26.5 | 37.45 / 37.45 | -1.14% | -0.60% | -0.60% |
| ordinary | VOL | 20 | 112 | -0.54% | -42.1% | 12.7% | -3.31 | 0.45 | 34.9 | 49.25 / 49.25 | -1.50% | -0.79% | -0.79% |
| ordinary | B2 | 20 | 112 | -0.10% | -8.0% | 15.2% | -0.53 | 0.64 | 186.0 | 264.81 / 264.81 | -1.88% | -0.96% | -0.96% |
| stressed | FIXED | 20 | 112 | -0.44% | -34.4% | 9.7% | -3.55 | 0.34 | 26.6 | 68.11 / 68.11 | -1.14% | -0.60% | -0.60% |
| stressed | VOL | 20 | 112 | -0.58% | -45.3% | 12.8% | -3.55 | 0.45 | 34.9 | 89.57 / 89.57 | -1.50% | -0.79% | -0.79% |
| stressed | B2 | 20 | 112 | -0.32% | -24.8% | 15.2% | -1.63 | 0.64 | 186.1 | 480.45 / 480.45 | -1.98% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 20 | 0 | 2.779 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 34.14% | 0.00022 | 0.145 | 0.00015 |
| stressed | 20 | 0 | 1.918 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 20.49% | 0.00013 | 0.088 | 0.00006 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-07T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 4.7 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
