# Paper sizing experiment PS1

Generated 2026-11-26T04:19:42.206Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-26T04:19:35.626Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1614 physical; 1614 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 54.18 days; 326 scheduled decisions; coverage 82.5%; execution delay after the 4H close: median 21.6 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 268 closed intervals over 1300.0 h; extended intervals 15.

Outcomes: executed 269; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 43

Execution states: completed 269

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 268 | 1300 | -9.96% | -70.7% | 14.4% | -4.93 | 0.33 | 2.7 | 42.58 / 42.58 | -13.01% | -1.73% | -0.93% |
| ordinary | VOL | 268 | 1300 | -11.37% | -81.3% | 15.7% | -5.18 | 0.39 | 7.1 | 110.14 / 110.14 | -14.01% | -2.00% | -1.03% |
| ordinary | B2 | 268 | 1300 | -13.36% | -96.7% | 15.4% | -6.26 | 0.49 | 102.7 | 1637.33 / 1637.33 | -16.76% | -2.24% | -1.13% |
| stressed | FIXED | 268 | 1300 | -9.99% | -70.9% | 14.4% | -4.94 | 0.33 | 2.7 | 77.42 / 77.42 | -13.02% | -1.73% | -0.93% |
| stressed | VOL | 268 | 1300 | -11.45% | -81.9% | 15.7% | -5.22 | 0.39 | 7.1 | 200.14 / 200.14 | -14.06% | -2.00% | -1.03% |
| stressed | B2 | 268 | 1300 | -14.52% | -105.7% | 15.4% | -6.85 | 0.49 | 102.9 | 2923.25 / 2923.25 | -17.75% | -2.25% | -1.14% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 268 | 6 | -1.086 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -15.37% | -0.00009 | -0.066 | -0.00014 |
| stressed | 268 | 6 | -1.637 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -23.81% | -0.00013 | -0.102 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-26T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 54.2 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
