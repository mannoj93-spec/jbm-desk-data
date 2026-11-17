# Paper sizing experiment PS1

Generated 2026-11-17T16:28:12.844Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-17T16:28:09.189Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1326 physical; 1326 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 45.69 days; 275 scheduled decisions; coverage 80.4%; execution delay after the 4H close: median 20.7 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 220 closed intervals over 1096.1 h; extended intervals 12.

Outcomes: executed 221; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 221

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 220 | 1096 | -8.51% | -71.1% | 12.0% | -5.91 | 0.33 | 3.2 | 42.58 / 42.58 | -9.16% | -1.36% | -0.78% |
| ordinary | VOL | 220 | 1096 | -10.27% | -86.6% | 15.4% | -5.62 | 0.42 | 8.2 | 110.14 / 110.14 | -11.11% | -2.00% | -1.01% |
| ordinary | B2 | 220 | 1096 | -11.90% | -101.2% | 14.7% | -6.89 | 0.54 | 113.8 | 1560.41 / 1567.12 | -13.44% | -2.24% | -1.09% |
| stressed | FIXED | 220 | 1096 | -8.55% | -71.4% | 12.0% | -5.93 | 0.33 | 3.2 | 77.42 / 77.42 | -9.17% | -1.36% | -0.78% |
| stressed | VOL | 220 | 1096 | -10.35% | -87.3% | 15.4% | -5.66 | 0.42 | 8.3 | 200.14 / 200.14 | -11.15% | -2.00% | -1.01% |
| stressed | B2 | 220 | 1096 | -13.01% | -111.4% | 14.7% | -7.60 | 0.54 | 113.9 | 2785.41 / 2797.26 | -14.44% | -2.25% | -1.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 220 | 5 | -1.278 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -14.63% | -0.00008 | -0.060 | -0.00017 |
| stressed | 220 | 5 | -1.934 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -24.07% | -0.00014 | -0.098 | -0.00023 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-17T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 45.7 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
