# Paper sizing experiment PS1

Generated 2026-11-14T11:22:27.825Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-14T08:24:07.543Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1206 physical; 1206 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 42.47 days; 255 scheduled decisions; coverage 78.8%; execution delay after the 4H close: median 20.3 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 200 closed intervals over 1016.1 h; extended intervals 12.

Outcomes: executed 201; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 201

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 200 | 1016 | -6.98% | -62.4% | 11.3% | -5.51 | 0.33 | 3.4 | 42.58 / 42.58 | -7.78% | -1.36% | -0.74% |
| ordinary | VOL | 200 | 1016 | -8.88% | -80.2% | 15.4% | -5.19 | 0.43 | 8.3 | 103.56 / 103.56 | -9.87% | -2.00% | -1.02% |
| ordinary | B2 | 200 | 1016 | -10.04% | -91.2% | 14.3% | -6.36 | 0.56 | 117.6 | 1492.69 / 1492.69 | -11.78% | -2.24% | -1.07% |
| stressed | FIXED | 200 | 1016 | -7.01% | -62.7% | 11.3% | -5.53 | 0.33 | 3.4 | 77.42 / 77.42 | -7.79% | -1.36% | -0.74% |
| stressed | VOL | 200 | 1016 | -8.96% | -81.0% | 15.4% | -5.24 | 0.43 | 8.3 | 188.25 / 188.25 | -9.92% | -2.00% | -1.02% |
| stressed | B2 | 200 | 1016 | -11.13% | -101.8% | 14.3% | -7.10 | 0.56 | 117.7 | 2677.38 / 2677.38 | -12.75% | -2.25% | -1.07% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 200 | 4 | -1.161 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -10.99% | -0.00006 | -0.045 | -0.00017 |
| stressed | 200 | 4 | -1.860 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -20.81% | -0.00012 | -0.085 | -0.00023 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-14T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 42.5 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
