# Paper sizing experiment PS1

Generated 2026-11-18T12:25:34.841Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-18T12:25:30.132Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1350 physical; 1350 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 46.52 days; 280 scheduled decisions; coverage 80.4%; execution delay after the 4H close: median 20.7 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 224 closed intervals over 1116.1 h; extended intervals 13.

Outcomes: executed 225; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 41

Execution states: completed 225

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 224 | 1116 | -8.37% | -68.6% | 12.0% | -5.72 | 0.33 | 3.1 | 42.58 / 42.58 | -9.16% | -1.36% | -0.78% |
| ordinary | VOL | 224 | 1116 | -10.16% | -84.1% | 15.3% | -5.49 | 0.42 | 8.1 | 110.14 / 110.14 | -11.11% | -2.00% | -1.01% |
| ordinary | B2 | 224 | 1116 | -11.81% | -98.7% | 14.6% | -6.76 | 0.53 | 112.4 | 1567.12 / 1567.12 | -13.45% | -2.24% | -1.09% |
| stressed | FIXED | 224 | 1116 | -8.41% | -68.9% | 12.0% | -5.74 | 0.33 | 3.1 | 77.42 / 77.42 | -9.17% | -1.36% | -0.78% |
| stressed | VOL | 224 | 1116 | -10.25% | -84.9% | 15.3% | -5.54 | 0.42 | 8.1 | 200.14 / 200.14 | -11.15% | -2.00% | -1.01% |
| stressed | B2 | 224 | 1116 | -12.93% | -108.7% | 14.6% | -7.46 | 0.53 | 112.5 | 2797.26 / 2797.26 | -14.45% | -2.25% | -1.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 224 | 5 | -1.274 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -14.54% | -0.00008 | -0.060 | -0.00017 |
| stressed | 224 | 5 | -1.924 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -23.85% | -0.00014 | -0.098 | -0.00023 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-18T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 46.5 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
