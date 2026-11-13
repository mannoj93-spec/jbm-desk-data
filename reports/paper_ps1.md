# Paper sizing experiment PS1

Generated 2026-11-13T01:05:29.488Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-13T00:25:53.945Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1170 physical; 1170 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 41.05 days; 247 scheduled decisions; coverage 79.0%; execution delay after the 4H close: median 20.2 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 194 closed intervals over 984.1 h; extended intervals 10.

Outcomes: executed 195; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 38

Execution states: completed 195

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 194 | 984 | -5.38% | -49.2% | 10.8% | -4.56 | 0.33 | 3.1 | 37.45 / 37.45 | -6.05% | -1.36% | -0.69% |
| ordinary | VOL | 194 | 984 | -6.87% | -63.4% | 14.8% | -4.27 | 0.43 | 8.1 | 98.40 / 98.40 | -7.74% | -2.00% | -0.97% |
| ordinary | B2 | 194 | 984 | -8.14% | -75.6% | 13.7% | -5.52 | 0.57 | 119.0 | 1466.70 / 1466.70 | -9.76% | -2.24% | -1.03% |
| stressed | FIXED | 194 | 984 | -5.41% | -49.5% | 10.8% | -4.59 | 0.33 | 3.1 | 68.11 / 68.11 | -6.05% | -1.36% | -0.69% |
| stressed | VOL | 194 | 984 | -6.95% | -64.1% | 14.8% | -4.32 | 0.43 | 8.1 | 178.87 / 178.87 | -7.78% | -2.00% | -0.97% |
| stressed | B2 | 194 | 984 | -9.24% | -86.3% | 13.7% | -6.31 | 0.57 | 119.0 | 2630.68 / 2630.68 | -10.73% | -2.25% | -1.03% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 194 | 4 | -1.246 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -12.26% | -0.00007 | -0.049 | -0.00015 |
| stressed | 194 | 4 | -1.989 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -22.24% | -0.00013 | -0.089 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-13T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 41.0 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
