# Paper sizing experiment PS1

Generated 2026-11-20T12:25:57.076Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-20T12:25:52.323Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1422 physical; 1422 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 48.52 days; 292 scheduled decisions; coverage 81.2%; execution delay after the 4H close: median 21.1 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 236 closed intervals over 1164.1 h; extended intervals 13.

Outcomes: executed 237; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 41

Execution states: completed 237

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 236 | 1164 | -9.66% | -76.4% | 12.2% | -6.27 | 0.33 | 3.0 | 42.58 / 42.58 | -10.30% | -1.36% | -0.81% |
| ordinary | VOL | 236 | 1164 | -11.14% | -88.9% | 15.2% | -5.86 | 0.41 | 7.8 | 110.14 / 110.14 | -11.97% | -2.00% | -1.01% |
| ordinary | B2 | 236 | 1164 | -12.83% | -103.4% | 14.4% | -7.17 | 0.52 | 108.7 | 1572.78 / 1572.78 | -14.36% | -2.24% | -1.09% |
| stressed | FIXED | 236 | 1164 | -9.69% | -76.7% | 12.2% | -6.29 | 0.33 | 3.0 | 77.42 / 77.42 | -10.31% | -1.36% | -0.81% |
| stressed | VOL | 236 | 1164 | -11.22% | -89.6% | 15.2% | -5.91 | 0.41 | 7.8 | 200.14 / 200.14 | -12.01% | -2.00% | -1.01% |
| stressed | B2 | 236 | 1164 | -13.95% | -113.0% | 14.4% | -7.85 | 0.52 | 108.8 | 2807.42 / 2807.42 | -15.36% | -2.25% | -1.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 236 | 5 | -1.303 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -14.49% | -0.00008 | -0.061 | -0.00015 |
| stressed | 236 | 5 | -1.938 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -23.47% | -0.00013 | -0.098 | -0.00020 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-20T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 48.5 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
