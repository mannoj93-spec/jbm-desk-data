# Paper sizing experiment PS1

Generated 2026-10-07T08:19:40.360Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-07T08:19:39.513Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 114 physical; 114 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 4.35 days; 27 scheduled decisions; coverage 70.4%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 18 closed intervals over 104.0 h; extended intervals 3.

Outcomes: executed 19; missed: stale: processed after close + max_delay 8

Execution states: completed 19

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 18 | 104 | -0.27% | -22.7% | 10.1% | -2.24 | 0.34 | 28.6 | 37.45 / 37.45 | -0.98% | -0.60% | -0.60% |
| ordinary | VOL | 18 | 104 | -0.35% | -29.8% | 13.3% | -2.25 | 0.45 | 37.5 | 49.25 / 49.25 | -1.28% | -0.79% | -0.79% |
| ordinary | B2 | 18 | 104 | 0.15% | 12.9% | 15.7% | 0.82 | 0.66 | 179.0 | 236.87 / 256.08 | -1.61% | -0.96% | -0.96% |
| stressed | FIXED | 18 | 104 | -0.30% | -25.2% | 10.1% | -2.50 | 0.34 | 28.6 | 68.11 / 68.11 | -0.98% | -0.60% | -0.60% |
| stressed | VOL | 18 | 104 | -0.39% | -33.2% | 13.3% | -2.50 | 0.45 | 37.6 | 89.57 / 89.57 | -1.28% | -0.79% | -0.79% |
| stressed | B2 | 18 | 104 | -0.04% | -3.3% | 15.7% | -0.21 | 0.66 | 179.1 | 429.73 / 464.61 | -1.68% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 18 | 0 | 3.066 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 42.67% | 0.00028 | 0.179 | 0.00023 |
| stressed | 18 | 0 | 2.291 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 29.89% | 0.00020 | 0.126 | 0.00014 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-07T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 4.3 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
