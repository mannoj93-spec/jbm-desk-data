# Paper sizing experiment PS1

Generated 2026-10-07T04:24:02.590Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-07T04:20:39.453Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 108 physical; 108 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 4.18 days; 26 scheduled decisions; coverage 69.2%; execution delay after the 4H close: median 18.1 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 17 closed intervals over 100.0 h; extended intervals 3.

Outcomes: executed 18; missed: stale: processed after close + max_delay 8

Execution states: completed 18

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 17 | 100 | -0.23% | -19.9% | 10.4% | -1.91 | 0.34 | 29.7 | 37.45 / 37.45 | -0.94% | -0.60% | -0.60% |
| ordinary | VOL | 17 | 100 | -0.30% | -26.1% | 13.7% | -1.91 | 0.45 | 39.0 | 49.25 / 49.25 | -1.23% | -0.79% | -0.79% |
| ordinary | B2 | 17 | 100 | 0.22% | 19.1% | 16.2% | 1.18 | 0.67 | 170.0 | 215.83 / 236.87 | -1.54% | -0.96% | -0.96% |
| stressed | FIXED | 17 | 100 | -0.26% | -22.6% | 10.4% | -2.17 | 0.34 | 29.7 | 68.11 / 68.11 | -0.94% | -0.60% | -0.60% |
| stressed | VOL | 17 | 100 | -0.34% | -29.7% | 13.7% | -2.17 | 0.45 | 39.1 | 89.57 / 89.57 | -1.23% | -0.79% | -0.79% |
| stressed | B2 | 17 | 100 | 0.04% | 3.7% | 16.2% | 0.23 | 0.67 | 170.1 | 392.06 / 429.73 | -1.60% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 17 | 0 | 3.093 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 45.24% | 0.00030 | 0.187 | 0.00026 |
| stressed | 17 | 0 | 2.402 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 33.41% | 0.00022 | 0.140 | 0.00018 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-07T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 4.2 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
