# Paper sizing experiment PS1

Generated 2026-10-31T16:17:59.623Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-31T16:17:54.906Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 948 physical; 948 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 28.68 days; 173 scheduled decisions; coverage 91.3%; execution delay after the 4H close: median 19.3 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 157 closed intervals over 688.0 h; extended intervals 6.

Outcomes: executed 158; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 158

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 157 | 688 | -2.83% | -36.5% | 11.4% | -3.21 | 0.33 | 4.4 | 37.45 / 37.45 | -3.76% | -1.36% | -0.71% |
| ordinary | VOL | 157 | 688 | -3.96% | -51.4% | 16.0% | -3.21 | 0.46 | 9.7 | 82.98 / 82.98 | -5.23% | -2.00% | -1.01% |
| ordinary | B2 | 157 | 688 | -3.48% | -45.1% | 14.5% | -3.12 | 0.52 | 132.9 | 1162.05 / 1170.25 | -5.47% | -1.31% | -0.89% |
| stressed | FIXED | 157 | 688 | -2.86% | -36.9% | 11.4% | -3.24 | 0.33 | 4.4 | 68.11 / 68.11 | -3.76% | -1.36% | -0.71% |
| stressed | VOL | 157 | 688 | -4.02% | -52.3% | 16.0% | -3.27 | 0.46 | 9.8 | 150.85 / 150.85 | -5.25% | -2.00% | -1.01% |
| stressed | B2 | 157 | 688 | -4.38% | -57.1% | 14.4% | -3.95 | 0.52 | 133.0 | 2082.84 / 2097.61 | -6.22% | -1.31% | -0.89% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 157 | 3 | 0.094 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 6.27% | 0.00003 | 0.026 | -0.00004 |
| stressed | 157 | 3 | -0.685 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -4.80% | -0.00002 | -0.020 | -0.00010 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-31T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 28.7 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
