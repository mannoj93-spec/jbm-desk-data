# Paper sizing experiment PS1

Generated 2026-11-08T12:22:26.909Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-08T12:22:22.968Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1020 physical; 1020 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 36.52 days; 220 scheduled decisions; coverage 77.3%; execution delay after the 4H close: median 19.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 169 closed intervals over 876.0 h; extended intervals 8.

Outcomes: executed 170; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 36

Execution states: completed 170

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 169 | 876 | -3.49% | -35.6% | 11.0% | -3.24 | 0.33 | 3.4 | 37.45 / 37.45 | -4.30% | -1.36% | -0.72% |
| ordinary | VOL | 169 | 876 | -4.84% | -49.6% | 15.4% | -3.21 | 0.44 | 8.4 | 90.69 / 90.69 | -5.84% | -2.00% | -1.02% |
| ordinary | B2 | 169 | 876 | -5.59% | -57.5% | 14.1% | -4.09 | 0.59 | 121.5 | 1344.41 / 1349.89 | -7.41% | -2.24% | -1.06% |
| stressed | FIXED | 169 | 876 | -3.52% | -35.9% | 11.0% | -3.26 | 0.33 | 3.4 | 68.11 / 68.11 | -4.30% | -1.36% | -0.72% |
| stressed | VOL | 169 | 876 | -4.91% | -50.4% | 15.4% | -3.26 | 0.44 | 8.4 | 164.86 / 164.86 | -5.87% | -2.00% | -1.02% |
| stressed | B2 | 169 | 876 | -6.62% | -68.4% | 14.0% | -4.88 | 0.59 | 121.5 | 2411.06 / 2420.88 | -8.27% | -2.25% | -1.06% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 169 | 4 | -0.877 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -7.86% | -0.00005 | -0.031 | -0.00013 |
| stressed | 169 | 4 | -1.621 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -18.06% | -0.00011 | -0.071 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-08T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 36.5 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
