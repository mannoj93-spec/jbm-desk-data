# Paper sizing experiment PS1

Generated 2026-10-05T12:20:51.224Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-05T12:13:05.867Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 54 physical; 54 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 2.51 days; 16 scheduled decisions; coverage 56.2%; execution delay after the 4H close: median 13.1 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 8 closed intervals over 59.9 h; extended intervals 2.

Outcomes: executed 9; missed: stale: processed after close + max_delay 7

Execution states: completed 9

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 8 | 60 | 0.60% | 87.4% | 6.3% | 13.80 | 0.34 | 49.6 | 37.45 / 37.45 | -0.16% | -0.16% | -0.16% |
| ordinary | VOL | 8 | 60 | 0.79% | 114.9% | 8.3% | 13.81 | 0.45 | 65.2 | 49.25 / 49.25 | -0.21% | -0.21% | -0.21% |
| ordinary | B2 | 8 | 60 | 1.62% | 234.7% | 11.1% | 21.21 | 0.81 | 226.1 | 171.51 / 171.51 | -0.24% | -0.24% | -0.24% |
| stressed | FIXED | 8 | 60 | 0.57% | 83.0% | 6.4% | 12.89 | 0.34 | 49.7 | 68.11 / 68.11 | -0.16% | -0.16% | -0.16% |
| stressed | VOL | 8 | 60 | 0.75% | 109.0% | 8.5% | 12.90 | 0.45 | 65.3 | 89.57 / 89.57 | -0.21% | -0.21% | -0.21% |
| stressed | B2 | 8 | 60 | 1.48% | 214.4% | 11.3% | 18.95 | 0.81 | 226.2 | 311.56 / 311.56 | -0.26% | -0.26% | -0.26% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 8 | 0 | 7.401 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 119.86% | 0.00102 | 0.482 | 0.00126 |
| stressed | 8 | 0 | 6.055 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 105.33% | 0.00090 | 0.424 | 0.00112 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-05T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 2.5 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
