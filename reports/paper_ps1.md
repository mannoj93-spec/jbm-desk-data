# Paper sizing experiment PS1

Generated 2026-10-14T04:20:13.333Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-14T04:20:12.328Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 360 physical; 360 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 11.18 days; 68 scheduled decisions; coverage 88.2%; execution delay after the 4H close: median 18.7 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 59 closed intervals over 268.0 h; extended intervals 3.

Outcomes: executed 60; missed: stale: processed after close + max_delay 8

Execution states: completed 60

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 59 | 268 | -0.39% | -12.7% | 10.3% | -1.24 | 0.34 | 11.2 | 37.45 / 37.45 | -2.01% | -0.65% | -0.63% |
| ordinary | VOL | 59 | 268 | -0.47% | -15.3% | 14.4% | -1.06 | 0.47 | 16.5 | 55.22 / 55.22 | -2.69% | -0.97% | -0.88% |
| ordinary | B2 | 59 | 268 | 0.06% | 1.9% | 14.6% | 0.13 | 0.60 | 151.9 | 512.37 / 512.37 | -3.04% | -0.96% | -0.95% |
| stressed | FIXED | 59 | 268 | -0.42% | -13.7% | 10.3% | -1.34 | 0.34 | 11.2 | 68.11 / 68.11 | -2.01% | -0.65% | -0.63% |
| stressed | VOL | 59 | 268 | -0.51% | -16.8% | 14.4% | -1.17 | 0.47 | 16.5 | 100.40 / 100.40 | -2.70% | -0.97% | -0.88% |
| stressed | B2 | 59 | 268 | -0.36% | -11.8% | 14.6% | -0.81 | 0.60 | 151.9 | 929.16 / 929.16 | -3.13% | -0.96% | -0.95% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 59 | 1 | 1.193 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 17.22% | 0.00009 | 0.084 | 0.00008 |
| stressed | 59 | 1 | 0.357 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 5.03% | 0.00003 | 0.025 | 0.00001 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-14T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 11.2 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
