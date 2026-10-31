# Paper sizing experiment PS1

Generated 2026-10-31T14:26:19.687Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-31T12:22:29.139Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 942 physical; 942 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 28.6 days; 172 scheduled decisions; coverage 91.3%; execution delay after the 4H close: median 19.3 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 156 closed intervals over 684.0 h; extended intervals 6.

Outcomes: executed 157; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 157

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 156 | 684 | -2.83% | -36.8% | 11.4% | -3.23 | 0.33 | 4.4 | 37.45 / 37.45 | -3.76% | -1.36% | -0.71% |
| ordinary | VOL | 156 | 684 | -3.97% | -51.9% | 16.1% | -3.23 | 0.46 | 9.8 | 82.98 / 82.98 | -5.23% | -2.00% | -1.01% |
| ordinary | B2 | 156 | 684 | -3.49% | -45.5% | 14.5% | -3.14 | 0.52 | 132.9 | 1155.80 / 1162.05 | -5.47% | -1.31% | -0.89% |
| stressed | FIXED | 156 | 684 | -2.86% | -37.2% | 11.4% | -3.26 | 0.33 | 4.4 | 68.11 / 68.11 | -3.76% | -1.36% | -0.71% |
| stressed | VOL | 156 | 684 | -4.03% | -52.7% | 16.1% | -3.28 | 0.46 | 9.8 | 150.85 / 150.85 | -5.25% | -2.00% | -1.01% |
| stressed | B2 | 156 | 684 | -4.39% | -57.5% | 14.5% | -3.97 | 0.52 | 133.0 | 2071.59 / 2082.84 | -6.22% | -1.31% | -0.89% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 156 | 3 | 0.094 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 6.31% | 0.00003 | 0.026 | -0.00004 |
| stressed | 156 | 3 | -0.683 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -4.76% | -0.00002 | -0.020 | -0.00010 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-31T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 28.6 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
