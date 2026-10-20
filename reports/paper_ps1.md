# Paper sizing experiment PS1

Generated 2026-10-20T20:26:45.844Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-20T20:18:46.645Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 600 physical; 600 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 17.85 days; 108 scheduled decisions; coverage 92.6%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 99 closed intervals over 428.0 h; extended intervals 3.

Outcomes: executed 100; missed: stale: processed after close + max_delay 8

Execution states: completed 100

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 99 | 428 | -0.82% | -16.8% | 10.5% | -1.61 | 0.34 | 7.0 | 37.45 / 37.45 | -2.23% | -0.84% | -0.63% |
| ordinary | VOL | 99 | 428 | -1.21% | -24.8% | 14.5% | -1.71 | 0.46 | 12.4 | 66.21 / 66.21 | -3.05% | -1.25% | -0.89% |
| ordinary | B2 | 99 | 428 | -0.58% | -11.8% | 13.9% | -0.85 | 0.56 | 153.3 | 846.28 / 858.07 | -3.34% | -0.96% | -0.80% |
| stressed | FIXED | 99 | 428 | -0.85% | -17.4% | 10.5% | -1.67 | 0.34 | 7.0 | 68.11 / 68.11 | -2.23% | -0.84% | -0.63% |
| stressed | VOL | 99 | 428 | -1.26% | -26.0% | 14.5% | -1.79 | 0.46 | 12.4 | 120.36 / 120.36 | -3.06% | -1.25% | -0.89% |
| stressed | B2 | 99 | 428 | -1.24% | -25.6% | 13.9% | -1.84 | 0.56 | 153.4 | 1513.37 / 1534.66 | -3.82% | -0.96% | -0.80% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 99 | 2 | 0.864 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 13.00% | 0.00006 | 0.055 | 0.00002 |
| stressed | 99 | 2 | -0.053 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 0.33% | 0.00000 | 0.001 | -0.00004 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-20T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 17.9 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
