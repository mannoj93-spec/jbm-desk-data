# Paper sizing experiment PS1

Generated 2026-10-16T04:27:28.821Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-16T04:20:50.394Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 432 physical; 432 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 13.19 days; 80 scheduled decisions; coverage 90.0%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 71 closed intervals over 316.0 h; extended intervals 3.

Outcomes: executed 72; missed: stale: processed after close + max_delay 8

Execution states: completed 72

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 71 | 316 | -1.04% | -29.0% | 11.0% | -2.63 | 0.34 | 9.5 | 37.45 / 37.45 | -2.16% | -0.84% | -0.70% |
| ordinary | VOL | 71 | 316 | -1.49% | -41.6% | 15.6% | -2.67 | 0.47 | 15.4 | 60.71 / 60.71 | -2.96% | -1.25% | -1.00% |
| ordinary | B2 | 71 | 316 | -0.73% | -20.4% | 14.0% | -1.45 | 0.56 | 151.6 | 602.24 / 602.24 | -3.04% | -0.96% | -0.84% |
| stressed | FIXED | 71 | 316 | -1.07% | -29.9% | 11.0% | -2.71 | 0.34 | 9.5 | 68.11 / 68.11 | -2.16% | -0.84% | -0.70% |
| stressed | VOL | 71 | 316 | -1.54% | -43.0% | 15.6% | -2.75 | 0.47 | 15.4 | 110.37 / 110.37 | -2.97% | -1.25% | -1.00% |
| stressed | B2 | 71 | 316 | -1.22% | -34.0% | 14.0% | -2.43 | 0.56 | 151.6 | 1091.83 / 1091.83 | -3.13% | -0.96% | -0.84% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 71 | 1 | 1.215 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 21.21% | 0.00011 | 0.082 | 0.00004 |
| stressed | 71 | 1 | 0.325 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 8.95% | 0.00005 | 0.035 | -0.00002 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-16T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 13.2 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
