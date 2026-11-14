# Paper sizing experiment PS1

Generated 2026-11-14T04:24:24.072Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-14T04:24:18.570Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1200 physical; 1200 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 42.18 days; 254 scheduled decisions; coverage 78.7%; execution delay after the 4H close: median 20.3 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 199 closed intervals over 1012.1 h; extended intervals 12.

Outcomes: executed 200; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 200

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 199 | 1012 | -7.12% | -64.0% | 11.3% | -5.64 | 0.33 | 3.0 | 37.45 / 42.58 | -7.78% | -1.36% | -0.77% |
| ordinary | VOL | 199 | 1012 | -9.03% | -81.9% | 15.5% | -5.29 | 0.43 | 8.3 | 103.56 / 103.56 | -9.87% | -2.00% | -1.06% |
| ordinary | B2 | 199 | 1012 | -10.20% | -93.1% | 14.4% | -6.48 | 0.56 | 118.0 | 1492.69 / 1492.69 | -11.78% | -2.24% | -1.11% |
| stressed | FIXED | 199 | 1012 | -7.16% | -64.3% | 11.3% | -5.66 | 0.33 | 3.0 | 68.11 / 77.42 | -7.79% | -1.36% | -0.77% |
| stressed | VOL | 199 | 1012 | -9.11% | -82.6% | 15.5% | -5.34 | 0.43 | 8.3 | 188.25 / 188.25 | -9.92% | -2.00% | -1.06% |
| stressed | B2 | 199 | 1012 | -11.30% | -103.8% | 14.3% | -7.23 | 0.56 | 118.1 | 2677.38 / 2677.38 | -12.75% | -2.25% | -1.12% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 199 | 4 | -1.189 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -11.26% | -0.00007 | -0.046 | -0.00017 |
| stressed | 199 | 4 | -1.890 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -21.12% | -0.00012 | -0.086 | -0.00023 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-14T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 42.2 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
