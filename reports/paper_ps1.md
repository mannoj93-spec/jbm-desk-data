# Paper sizing experiment PS1

Generated 2026-11-21T20:27:27.048Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-21T20:27:22.837Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1464 physical; 1464 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 49.85 days; 300 scheduled decisions; coverage 81.3%; execution delay after the 4H close: median 21.3 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 243 closed intervals over 1196.1 h; extended intervals 14.

Outcomes: executed 244; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 42

Execution states: completed 244

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 243 | 1196 | -10.21% | -78.8% | 14.2% | -5.54 | 0.33 | 2.9 | 42.58 / 42.58 | -13.01% | -1.73% | -0.95% |
| ordinary | VOL | 243 | 1196 | -11.55% | -89.9% | 16.0% | -5.61 | 0.41 | 7.6 | 110.14 / 110.14 | -14.01% | -2.00% | -1.06% |
| ordinary | B2 | 243 | 1196 | -13.64% | -107.4% | 15.8% | -6.82 | 0.52 | 107.9 | 1598.00 / 1598.00 | -16.76% | -2.24% | -1.17% |
| stressed | FIXED | 243 | 1196 | -10.24% | -79.1% | 14.2% | -5.56 | 0.33 | 2.9 | 77.42 / 77.42 | -13.02% | -1.73% | -0.95% |
| stressed | VOL | 243 | 1196 | -11.64% | -90.6% | 16.0% | -5.65 | 0.41 | 7.6 | 200.14 / 200.14 | -14.06% | -2.00% | -1.06% |
| stressed | B2 | 243 | 1196 | -14.77% | -117.0% | 15.8% | -7.43 | 0.52 | 108.0 | 2852.68 / 2852.68 | -17.75% | -2.25% | -1.18% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 243 | 5 | -1.209 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -17.53% | -0.00010 | -0.073 | -0.00016 |
| stressed | 243 | 5 | -1.781 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -26.43% | -0.00015 | -0.110 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-21T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 49.9 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
