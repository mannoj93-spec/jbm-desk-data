# Paper sizing experiment PS1

Generated 2026-11-07T16:23:38.343Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-07T16:23:35.497Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 996 physical; 996 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 35.68 days; 215 scheduled decisions; coverage 77.2%; execution delay after the 4H close: median 19.3 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 165 closed intervals over 856.1 h; extended intervals 7.

Outcomes: executed 166; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 35

Execution states: completed 166

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 165 | 856 | -3.56% | -37.1% | 11.1% | -3.34 | 0.33 | 3.5 | 37.45 / 37.45 | -4.30% | -1.36% | -0.72% |
| ordinary | VOL | 165 | 856 | -4.91% | -51.5% | 15.6% | -3.30 | 0.45 | 8.6 | 90.69 / 90.69 | -5.84% | -2.00% | -1.02% |
| ordinary | B2 | 165 | 856 | -5.73% | -60.3% | 14.2% | -4.25 | 0.58 | 118.7 | 1286.33 / 1294.63 | -7.38% | -2.24% | -1.06% |
| stressed | FIXED | 165 | 856 | -3.59% | -37.4% | 11.1% | -3.36 | 0.33 | 3.5 | 68.11 / 68.11 | -4.30% | -1.36% | -0.72% |
| stressed | VOL | 165 | 856 | -4.98% | -52.3% | 15.6% | -3.35 | 0.45 | 8.6 | 164.86 / 164.86 | -5.87% | -2.00% | -1.02% |
| stressed | B2 | 165 | 856 | -6.71% | -71.0% | 14.2% | -5.01 | 0.58 | 118.8 | 2306.56 / 2321.49 | -8.24% | -2.25% | -1.06% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 165 | 3 | -0.950 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -8.81% | -0.00005 | -0.034 | -0.00014 |
| stressed | 165 | 3 | -1.668 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -18.73% | -0.00011 | -0.073 | -0.00020 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-07T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 35.7 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
