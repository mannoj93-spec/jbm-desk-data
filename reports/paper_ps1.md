# Paper sizing experiment PS1

Generated 2026-10-25T05:24:49.665Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-25T04:19:02.808Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 714 physical; 714 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 22.23 days; 134 scheduled decisions; coverage 88.8%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 118 closed intervals over 532.0 h; extended intervals 6.

Outcomes: executed 119; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 119

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 118 | 532 | -1.53% | -25.3% | 10.4% | -2.42 | 0.34 | 5.6 | 37.45 / 37.45 | -2.68% | -0.84% | -0.61% |
| ordinary | VOL | 118 | 532 | -2.11% | -35.0% | 14.3% | -2.45 | 0.46 | 11.6 | 76.49 / 76.49 | -3.69% | -1.25% | -0.85% |
| ordinary | B2 | 118 | 532 | -1.84% | -30.6% | 14.4% | -2.13 | 0.55 | 138.2 | 944.38 / 953.23 | -4.28% | -0.99% | -0.85% |
| stressed | FIXED | 118 | 532 | -1.56% | -25.8% | 10.4% | -2.47 | 0.34 | 5.7 | 68.11 / 68.11 | -2.68% | -0.84% | -0.61% |
| stressed | VOL | 118 | 532 | -2.17% | -36.1% | 14.3% | -2.52 | 0.46 | 11.6 | 139.06 / 139.06 | -3.71% | -1.25% | -0.85% |
| stressed | B2 | 118 | 532 | -2.58% | -43.0% | 14.3% | -3.01 | 0.55 | 138.3 | 1690.45 / 1706.38 | -4.87% | -0.99% | -0.85% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 118 | 2 | 0.319 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 4.45% | 0.00002 | 0.020 | -0.00003 |
| stressed | 118 | 2 | -0.484 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | -6.94% | -0.00004 | -0.032 | -0.00009 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-25T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 22.2 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
