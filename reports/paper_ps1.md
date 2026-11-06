# Paper sizing experiment PS1

Generated 2026-11-06T19:08:28.740Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-06T16:24:05.776Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 960 physical; 960 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 34.8 days; 209 scheduled decisions; coverage 76.6%; execution delay after the 4H close: median 19.3 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 159 closed intervals over 832.1 h; extended intervals 7.

Outcomes: executed 160; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 35

Execution states: completed 160

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 159 | 832 | -3.61% | -38.7% | 11.3% | -3.42 | 0.33 | 3.6 | 37.45 / 37.45 | -4.30% | -1.36% | -0.76% |
| ordinary | VOL | 159 | 832 | -4.96% | -53.5% | 15.9% | -3.37 | 0.45 | 8.1 | 82.98 / 90.69 | -5.84% | -2.00% | -1.07% |
| ordinary | B2 | 159 | 832 | -5.64% | -61.1% | 14.4% | -4.24 | 0.58 | 112.2 | 1185.93 / 1244.19 | -7.29% | -2.24% | -1.12% |
| stressed | FIXED | 159 | 832 | -3.64% | -39.1% | 11.3% | -3.45 | 0.33 | 3.6 | 68.11 / 68.11 | -4.30% | -1.36% | -0.76% |
| stressed | VOL | 159 | 832 | -5.02% | -54.3% | 15.9% | -3.41 | 0.45 | 8.1 | 150.85 / 164.86 | -5.87% | -2.00% | -1.07% |
| stressed | B2 | 159 | 832 | -6.54% | -71.2% | 14.4% | -4.95 | 0.58 | 112.3 | 2125.85 / 2230.75 | -8.07% | -2.25% | -1.12% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 159 | 3 | -0.872 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -7.55% | -0.00005 | -0.029 | -0.00013 |
| stressed | 159 | 3 | -1.540 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -16.91% | -0.00010 | -0.066 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-06T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 34.8 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
