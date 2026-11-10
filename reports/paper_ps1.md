# Paper sizing experiment PS1

Generated 2026-11-10T02:42:39.692Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-10T00:24:54.571Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1068 physical; 1068 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 38.11 days; 229 scheduled decisions; coverage 77.7%; execution delay after the 4H close: median 19.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 177 closed intervals over 912.1 h; extended intervals 9.

Outcomes: executed 178; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 37

Execution states: completed 178

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 177 | 912 | -3.81% | -37.3% | 10.9% | -3.43 | 0.33 | 3.3 | 37.45 / 37.45 | -4.87% | -1.36% | -0.72% |
| ordinary | VOL | 177 | 912 | -5.17% | -51.0% | 15.2% | -3.35 | 0.44 | 8.1 | 90.69 / 90.69 | -6.45% | -2.00% | -1.02% |
| ordinary | B2 | 177 | 912 | -6.38% | -63.3% | 14.0% | -4.53 | 0.59 | 121.7 | 1398.14 / 1403.78 | -8.43% | -2.24% | -1.08% |
| stressed | FIXED | 177 | 912 | -3.84% | -37.6% | 10.9% | -3.45 | 0.33 | 3.3 | 68.11 / 68.11 | -4.88% | -1.36% | -0.72% |
| stressed | VOL | 177 | 912 | -5.24% | -51.7% | 15.2% | -3.40 | 0.44 | 8.1 | 164.86 / 164.86 | -6.49% | -2.00% | -1.02% |
| stressed | B2 | 177 | 912 | -7.44% | -74.2% | 14.0% | -5.32 | 0.59 | 121.7 | 2507.49 / 2517.63 | -9.36% | -2.25% | -1.08% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 177 | 4 | -1.173 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -12.30% | -0.00007 | -0.048 | -0.00015 |
| stressed | 177 | 4 | -1.920 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -22.55% | -0.00013 | -0.088 | -0.00022 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-10T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 38.1 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
