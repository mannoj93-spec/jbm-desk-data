# Paper sizing experiment PS1

Generated 2026-11-18T16:33:29.865Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-18T16:33:26.448Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1356 physical; 1356 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 46.69 days; 281 scheduled decisions; coverage 80.4%; execution delay after the 4H close: median 20.8 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 225 closed intervals over 1120.2 h; extended intervals 13.

Outcomes: executed 226; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 41

Execution states: completed 226

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 225 | 1120 | -9.20% | -75.5% | 12.3% | -6.15 | 0.33 | 3.1 | 42.58 / 42.58 | -9.84% | -1.36% | -0.81% |
| ordinary | VOL | 225 | 1120 | -10.79% | -89.3% | 15.4% | -5.79 | 0.42 | 8.1 | 110.14 / 110.14 | -11.62% | -2.00% | -1.01% |
| ordinary | B2 | 225 | 1120 | -12.35% | -103.1% | 14.7% | -7.03 | 0.53 | 112.1 | 1567.12 / 1567.12 | -13.89% | -2.24% | -1.09% |
| stressed | FIXED | 225 | 1120 | -9.23% | -75.7% | 12.3% | -6.17 | 0.33 | 3.1 | 77.42 / 77.42 | -9.85% | -1.36% | -0.81% |
| stressed | VOL | 225 | 1120 | -10.87% | -90.0% | 15.4% | -5.83 | 0.42 | 8.1 | 200.14 / 200.14 | -11.67% | -2.00% | -1.01% |
| stressed | B2 | 225 | 1120 | -13.47% | -113.1% | 14.6% | -7.73 | 0.53 | 112.2 | 2797.26 / 2797.26 | -14.89% | -2.25% | -1.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 225 | 5 | -1.245 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -13.84% | -0.00008 | -0.057 | -0.00016 |
| stressed | 225 | 5 | -1.892 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -23.12% | -0.00013 | -0.095 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-18T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 46.7 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
