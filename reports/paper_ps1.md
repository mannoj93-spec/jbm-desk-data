# Paper sizing experiment PS1

Generated 2026-11-25T16:20:21.221Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-25T16:20:17.546Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1596 physical; 1596 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 53.68 days; 323 scheduled decisions; coverage 82.3%; execution delay after the 4H close: median 21.6 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 265 closed intervals over 1288.0 h; extended intervals 15.

Outcomes: executed 266; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 43

Execution states: completed 266

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 265 | 1288 | -11.09% | -79.9% | 14.2% | -5.63 | 0.33 | 2.7 | 42.58 / 42.58 | -13.01% | -1.73% | -0.93% |
| ordinary | VOL | 265 | 1288 | -12.22% | -88.6% | 15.7% | -5.66 | 0.39 | 7.1 | 110.14 / 110.14 | -14.01% | -2.00% | -1.03% |
| ordinary | B2 | 265 | 1288 | -14.13% | -103.6% | 15.4% | -6.73 | 0.50 | 102.9 | 1626.70 / 1626.70 | -16.76% | -2.24% | -1.13% |
| stressed | FIXED | 265 | 1288 | -11.12% | -80.2% | 14.2% | -5.64 | 0.33 | 2.7 | 77.42 / 77.42 | -13.02% | -1.73% | -0.93% |
| stressed | VOL | 265 | 1288 | -12.30% | -89.3% | 15.7% | -5.70 | 0.39 | 7.1 | 200.14 / 200.14 | -14.06% | -2.00% | -1.03% |
| stressed | B2 | 265 | 1288 | -15.27% | -112.7% | 15.4% | -7.32 | 0.50 | 103.0 | 2904.18 / 2904.18 | -17.75% | -2.25% | -1.14% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 265 | 6 | -1.071 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -14.98% | -0.00008 | -0.064 | -0.00013 |
| stressed | 265 | 6 | -1.625 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -23.44% | -0.00013 | -0.100 | -0.00018 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-25T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 53.7 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
