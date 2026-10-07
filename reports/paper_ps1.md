# Paper sizing experiment PS1

Generated 2026-10-07T00:12:21.021Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-07T00:12:20.386Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 102 physical; 102 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 4.01 days; 25 scheduled decisions; coverage 68.0%; execution delay after the 4H close: median 17.7 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 16 closed intervals over 95.9 h; extended intervals 3.

Outcomes: executed 17; missed: stale: processed after close + max_delay 8

Execution states: completed 17

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 16 | 96 | 0.38% | 34.3% | 8.0% | 4.31 | 0.34 | 31.0 | 37.45 / 37.45 | -0.50% | -0.39% | -0.39% |
| ordinary | VOL | 16 | 96 | 0.50% | 45.1% | 10.5% | 4.32 | 0.45 | 40.7 | 49.25 / 49.25 | -0.66% | -0.51% | -0.51% |
| ordinary | B2 | 16 | 96 | 1.19% | 107.8% | 11.9% | 9.07 | 0.67 | 177.3 | 215.83 / 215.83 | -0.67% | -0.51% | -0.51% |
| stressed | FIXED | 16 | 96 | 0.35% | 31.5% | 8.0% | 3.95 | 0.34 | 31.0 | 68.11 / 68.11 | -0.50% | -0.39% | -0.39% |
| stressed | VOL | 16 | 96 | 0.45% | 41.5% | 10.5% | 3.95 | 0.45 | 40.8 | 89.57 / 89.57 | -0.66% | -0.51% | -0.51% |
| stressed | B2 | 16 | 96 | 1.01% | 91.7% | 11.9% | 7.69 | 0.67 | 177.4 | 392.06 / 392.06 | -0.70% | -0.51% | -0.51% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 16 | 0 | 4.750 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 62.64% | 0.00043 | 0.270 | 0.00050 |
| stressed | 16 | 0 | 3.740 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 50.28% | 0.00034 | 0.218 | 0.00041 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-07T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 4.0 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
