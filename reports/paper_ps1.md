# Paper sizing experiment PS1

Generated 2026-11-26T08:58:27.782Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-26T08:09:25.601Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1620 physical; 1620 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 54.37 days; 327 scheduled decisions; coverage 82.6%; execution delay after the 4H close: median 21.6 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 269 closed intervals over 1303.8 h; extended intervals 15.

Outcomes: executed 270; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 43

Execution states: completed 270

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 269 | 1304 | -10.07% | -71.3% | 14.3% | -4.98 | 0.33 | 2.7 | 42.58 / 42.58 | -13.01% | -1.73% | -0.93% |
| ordinary | VOL | 269 | 1304 | -11.45% | -81.7% | 15.7% | -5.21 | 0.39 | 7.0 | 110.14 / 110.14 | -14.01% | -2.00% | -1.03% |
| ordinary | B2 | 269 | 1304 | -13.45% | -97.0% | 15.4% | -6.30 | 0.49 | 102.5 | 1637.33 / 1637.33 | -16.76% | -2.24% | -1.13% |
| stressed | FIXED | 269 | 1304 | -10.11% | -71.6% | 14.3% | -5.00 | 0.33 | 2.7 | 77.42 / 77.42 | -13.02% | -1.73% | -0.93% |
| stressed | VOL | 269 | 1304 | -11.53% | -82.3% | 15.7% | -5.25 | 0.39 | 7.0 | 200.14 / 200.14 | -14.06% | -2.00% | -1.03% |
| stressed | B2 | 269 | 1304 | -14.60% | -106.1% | 15.4% | -6.89 | 0.49 | 102.6 | 2923.25 / 2923.25 | -17.75% | -2.25% | -1.14% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 269 | 6 | -1.084 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -15.30% | -0.00008 | -0.066 | -0.00014 |
| stressed | 269 | 6 | -1.635 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -23.72% | -0.00013 | -0.102 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-26T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 54.4 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
