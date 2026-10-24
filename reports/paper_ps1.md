# Paper sizing experiment PS1

Generated 2026-10-24T16:19:42.967Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-24T16:19:39.470Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 696 physical; 696 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 21.68 days; 131 scheduled decisions; coverage 88.5%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 115 closed intervals over 520.0 h; extended intervals 6.

Outcomes: executed 116; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 116

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 115 | 520 | -1.99% | -33.8% | 10.4% | -3.24 | 0.34 | 5.8 | 37.45 / 37.45 | -2.68% | -0.84% | -0.61% |
| ordinary | VOL | 115 | 520 | -2.78% | -47.5% | 14.3% | -3.32 | 0.45 | 11.8 | 76.49 / 76.49 | -3.69% | -1.25% | -0.85% |
| ordinary | B2 | 115 | 520 | -2.57% | -43.8% | 14.3% | -3.06 | 0.55 | 137.3 | 918.11 / 944.38 | -4.28% | -0.99% | -0.85% |
| stressed | FIXED | 115 | 520 | -2.02% | -34.3% | 10.4% | -3.29 | 0.34 | 5.8 | 68.11 / 68.11 | -2.68% | -0.84% | -0.61% |
| stressed | VOL | 115 | 520 | -2.84% | -48.6% | 14.3% | -3.40 | 0.45 | 11.8 | 139.06 / 139.06 | -3.71% | -1.25% | -0.85% |
| stressed | B2 | 115 | 520 | -3.28% | -56.2% | 14.3% | -3.94 | 0.55 | 137.4 | 1643.04 / 1690.45 | -4.87% | -0.99% | -0.85% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 115 | 2 | 0.263 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 3.66% | 0.00002 | 0.016 | -0.00005 |
| stressed | 115 | 2 | -0.537 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | -7.63% | -0.00004 | -0.034 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-24T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 21.7 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
