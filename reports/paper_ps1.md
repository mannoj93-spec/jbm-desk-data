# Paper sizing experiment PS1

Generated 2026-10-09T09:03:41.840Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-09T08:21:23.197Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 186 physical; 186 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 6.38 days; 39 scheduled decisions; coverage 79.5%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 30 closed intervals over 152.0 h; extended intervals 3.

Outcomes: executed 31; missed: stale: processed after close + max_delay 8

Execution states: completed 31

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 30 | 152 | -0.80% | -46.0% | 9.8% | -4.68 | 0.34 | 19.6 | 37.45 / 37.45 | -2.01% | -0.60% | -0.60% |
| ordinary | VOL | 30 | 152 | -1.05% | -60.6% | 12.9% | -4.69 | 0.45 | 25.8 | 49.25 / 49.25 | -2.64% | -0.79% | -0.79% |
| ordinary | B2 | 30 | 152 | -0.67% | -39.0% | 14.6% | -2.67 | 0.59 | 156.2 | 300.07 / 308.30 | -3.04% | -0.96% | -0.96% |
| stressed | FIXED | 30 | 152 | -0.83% | -47.8% | 9.8% | -4.86 | 0.34 | 19.7 | 68.11 / 68.11 | -2.01% | -0.60% | -0.60% |
| stressed | VOL | 30 | 152 | -1.09% | -63.0% | 12.9% | -4.87 | 0.45 | 25.9 | 89.57 / 89.57 | -2.64% | -0.79% | -0.79% |
| stressed | B2 | 30 | 152 | -0.92% | -53.1% | 14.5% | -3.65 | 0.59 | 156.3 | 544.42 / 559.35 | -3.13% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 30 | 0 | 2.015 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 21.61% | 0.00012 | 0.101 | 0.00004 |
| stressed | 30 | 0 | 1.215 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 9.88% | 0.00006 | 0.047 | -0.00003 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-09T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 6.4 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
