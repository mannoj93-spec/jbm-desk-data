# Paper sizing experiment PS1

Generated 2026-10-26T05:32:36.718Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-26T04:21:51.904Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 750 physical; 750 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 23.23 days; 140 scheduled decisions; coverage 89.3%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 124 closed intervals over 556.0 h; extended intervals 6.

Outcomes: executed 125; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 125

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 124 | 556 | -1.89% | -30.0% | 10.2% | -2.93 | 0.34 | 5.4 | 37.45 / 37.45 | -2.68% | -0.84% | -0.58% |
| ordinary | VOL | 124 | 556 | -2.63% | -42.0% | 14.0% | -3.00 | 0.46 | 11.1 | 76.49 / 76.49 | -3.69% | -1.25% | -0.80% |
| ordinary | B2 | 124 | 556 | -2.53% | -40.3% | 14.1% | -2.86 | 0.55 | 138.8 | 989.52 / 989.52 | -4.28% | -0.99% | -0.81% |
| stressed | FIXED | 124 | 556 | -1.92% | -30.5% | 10.2% | -2.98 | 0.34 | 5.4 | 68.11 / 68.11 | -2.68% | -0.84% | -0.58% |
| stressed | VOL | 124 | 556 | -2.70% | -43.0% | 14.0% | -3.07 | 0.46 | 11.1 | 139.06 / 139.06 | -3.71% | -1.25% | -0.80% |
| stressed | B2 | 124 | 556 | -3.30% | -52.8% | 14.1% | -3.75 | 0.55 | 138.9 | 1771.86 / 1771.86 | -4.89% | -0.99% | -0.82% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 124 | 2 | 0.143 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 1.71% | 0.00001 | 0.008 | -0.00005 |
| stressed | 124 | 2 | -0.683 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | -9.78% | -0.00005 | -0.045 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-26T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 23.2 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
