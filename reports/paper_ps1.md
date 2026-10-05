# Paper sizing experiment PS1

Generated 2026-10-05T05:18:50.603Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-05T04:13:04.567Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 42 physical; 42 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 2.22 days; 14 scheduled decisions; coverage 50.0%; execution delay after the 4H close: median 16.1 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 6 closed intervals over 51.9 h; extended intervals 2.

Outcomes: executed 7; missed: stale: processed after close + max_delay 7

Execution states: completed 7

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 6 | 52 | 0.54% | 91.6% | 6.2% | 14.82 | 0.34 | 57.4 | 37.45 / 37.45 | -0.16% | -0.16% | -0.16% |
| ordinary | VOL | 6 | 52 | 0.72% | 120.4% | 8.1% | 14.83 | 0.45 | 75.4 | 49.25 / 49.25 | -0.21% | -0.21% | -0.21% |
| ordinary | B2 | 6 | 52 | 1.54% | 258.8% | 11.7% | 22.20 | 0.87 | 261.7 | 171.51 / 171.51 | -0.24% | -0.24% | -0.24% |
| stressed | FIXED | 6 | 52 | 0.51% | 86.5% | 6.3% | 13.66 | 0.34 | 57.4 | 68.11 / 68.11 | -0.16% | -0.16% | -0.16% |
| stressed | VOL | 6 | 52 | 0.68% | 113.6% | 8.3% | 13.67 | 0.45 | 75.5 | 89.57 / 89.57 | -0.21% | -0.21% | -0.21% |
| stressed | B2 | 6 | 52 | 1.40% | 235.3% | 12.0% | 19.55 | 0.87 | 261.8 | 311.56 / 311.56 | -0.26% | -0.26% | -0.26% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 6 | 0 | 7.363 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 138.41% | 0.00137 | 0.570 | 0.00165 |
| stressed | 6 | 0 | 5.882 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 121.64% | 0.00120 | 0.496 | 0.00147 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-05T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 2.2 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
