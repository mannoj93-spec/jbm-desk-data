# Paper sizing experiment PS1

Generated 2026-11-11T23:09:39.249Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-11T21:00:34.136Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1128 physical; 1128 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 39.97 days; 240 scheduled decisions; coverage 78.3%; execution delay after the 4H close: median 19.9 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 187 closed intervals over 956.7 h; extended intervals 10.

Outcomes: executed 188; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 38

Execution states: completed 188

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 187 | 957 | -4.00% | -37.4% | 10.8% | -3.47 | 0.33 | 3.2 | 37.45 / 37.45 | -5.25% | -1.36% | -0.69% |
| ordinary | VOL | 187 | 957 | -5.37% | -50.6% | 14.9% | -3.38 | 0.44 | 7.7 | 90.69 / 90.69 | -6.84% | -2.00% | -0.97% |
| ordinary | B2 | 187 | 957 | -6.52% | -61.7% | 13.7% | -4.50 | 0.58 | 120.2 | 1443.72 / 1443.72 | -8.71% | -2.24% | -1.03% |
| stressed | FIXED | 187 | 957 | -4.03% | -37.7% | 10.8% | -3.49 | 0.33 | 3.2 | 68.11 / 68.11 | -5.25% | -1.36% | -0.69% |
| stressed | VOL | 187 | 957 | -5.44% | -51.3% | 14.9% | -3.43 | 0.44 | 7.7 | 164.86 / 164.86 | -6.87% | -2.00% | -0.97% |
| stressed | B2 | 187 | 957 | -7.62% | -72.6% | 13.7% | -5.29 | 0.58 | 120.3 | 2589.39 / 2589.39 | -9.67% | -2.25% | -1.03% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 187 | 4 | -1.113 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -11.17% | -0.00007 | -0.045 | -0.00014 |
| stressed | 187 | 4 | -1.862 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -21.31% | -0.00012 | -0.085 | -0.00020 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-11T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 40.0 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
