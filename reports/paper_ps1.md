# Paper sizing experiment PS1

Generated 2026-10-08T01:06:57.589Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-08T00:18:51.905Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 138 physical; 138 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 5.05 days; 31 scheduled decisions; coverage 74.2%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 22 closed intervals over 120.0 h; extended intervals 3.

Outcomes: executed 23; missed: stale: processed after close + max_delay 8

Execution states: completed 23

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 22 | 120 | -0.52% | -38.2% | 9.3% | -4.12 | 0.34 | 24.8 | 37.45 / 37.45 | -1.23% | -0.60% | -0.60% |
| ordinary | VOL | 22 | 120 | -0.69% | -50.2% | 12.2% | -4.13 | 0.45 | 32.6 | 49.25 / 49.25 | -1.61% | -0.79% | -0.79% |
| ordinary | B2 | 22 | 120 | -0.25% | -18.5% | 14.5% | -1.28 | 0.63 | 173.9 | 264.81 / 264.81 | -2.00% | -0.96% | -0.96% |
| stressed | FIXED | 22 | 120 | -0.55% | -40.4% | 9.3% | -4.36 | 0.34 | 24.8 | 68.11 / 68.11 | -1.23% | -0.60% | -0.60% |
| stressed | VOL | 22 | 120 | -0.73% | -53.2% | 12.2% | -4.37 | 0.45 | 32.6 | 89.57 / 89.57 | -1.61% | -0.79% | -0.79% |
| stressed | B2 | 22 | 120 | -0.47% | -34.2% | 14.5% | -2.36 | 0.63 | 174.0 | 480.45 / 480.45 | -2.10% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 22 | 0 | 2.855 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 31.73% | 0.00020 | 0.138 | 0.00012 |
| stressed | 22 | 0 | 2.011 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 19.00% | 0.00012 | 0.083 | 0.00004 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-08T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 5.0 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
