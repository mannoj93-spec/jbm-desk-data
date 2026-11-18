# Paper sizing experiment PS1

Generated 2026-11-18T00:26:13.240Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-18T00:26:09.263Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1338 physical; 1338 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 46.02 days; 277 scheduled decisions; coverage 80.5%; execution delay after the 4H close: median 20.7 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 222 closed intervals over 1104.1 h; extended intervals 12.

Outcomes: executed 223; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 223

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 222 | 1104 | -8.15% | -67.4% | 12.1% | -5.59 | 0.33 | 3.1 | 42.58 / 42.58 | -9.16% | -1.36% | -0.78% |
| ordinary | VOL | 222 | 1104 | -9.99% | -83.5% | 15.4% | -5.43 | 0.42 | 8.2 | 110.14 / 110.14 | -11.11% | -2.00% | -1.01% |
| ordinary | B2 | 222 | 1104 | -11.67% | -98.4% | 14.7% | -6.72 | 0.54 | 113.6 | 1567.12 / 1567.12 | -13.45% | -2.24% | -1.09% |
| stressed | FIXED | 222 | 1104 | -8.18% | -67.7% | 12.1% | -5.62 | 0.33 | 3.1 | 77.42 / 77.42 | -9.17% | -1.36% | -0.78% |
| stressed | VOL | 222 | 1104 | -10.08% | -84.3% | 15.4% | -5.47 | 0.42 | 8.2 | 200.14 / 200.14 | -11.15% | -2.00% | -1.01% |
| stressed | B2 | 222 | 1104 | -12.79% | -108.6% | 14.6% | -7.42 | 0.54 | 113.6 | 2797.26 / 2797.26 | -14.45% | -2.25% | -1.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 222 | 5 | -1.289 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -14.87% | -0.00008 | -0.061 | -0.00018 |
| stressed | 222 | 5 | -1.943 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -24.29% | -0.00014 | -0.099 | -0.00023 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-18T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 46.0 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
