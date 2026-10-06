# Paper sizing experiment PS1

Generated 2026-10-06T13:04:37.126Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-06T12:18:23.251Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 84 physical; 84 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 3.54 days; 22 scheduled decisions; coverage 63.6%; execution delay after the 4H close: median 16.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 13 closed intervals over 84.0 h; extended intervals 3.

Outcomes: executed 14; missed: stale: processed after close + max_delay 8

Execution states: completed 14

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 13 | 84 | 0.66% | 68.9% | 8.3% | 8.30 | 0.34 | 35.4 | 37.45 / 37.45 | -0.50% | -0.39% | -0.39% |
| ordinary | VOL | 13 | 84 | 0.87% | 90.5% | 10.9% | 8.31 | 0.45 | 46.5 | 49.25 / 49.25 | -0.66% | -0.51% | -0.51% |
| ordinary | B2 | 13 | 84 | 1.57% | 162.4% | 12.4% | 13.10 | 0.70 | 190.7 | 203.18 / 203.18 | -0.67% | -0.51% | -0.51% |
| stressed | FIXED | 13 | 84 | 0.63% | 65.7% | 8.3% | 7.88 | 0.34 | 35.4 | 68.11 / 68.11 | -0.50% | -0.39% | -0.39% |
| stressed | VOL | 13 | 84 | 0.83% | 86.3% | 10.9% | 7.88 | 0.45 | 46.5 | 89.57 / 89.57 | -0.66% | -0.51% | -0.51% |
| stressed | B2 | 13 | 84 | 1.40% | 145.2% | 12.5% | 11.63 | 0.70 | 190.8 | 369.09 / 369.09 | -0.70% | -0.51% | -0.51% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 13 | 0 | 4.796 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 71.91% | 0.00053 | 0.302 | 0.00069 |
| stressed | 13 | 0 | 3.741 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 58.86% | 0.00043 | 0.249 | 0.00059 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-06T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 3.5 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
