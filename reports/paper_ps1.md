# Paper sizing experiment PS1

Generated 2026-10-25T22:51:42.721Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-25T20:19:21.060Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 738 physical; 738 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 22.95 days; 138 scheduled decisions; coverage 89.1%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 122 closed intervals over 548.0 h; extended intervals 6.

Outcomes: executed 123; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 123

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 122 | 548 | -1.63% | -26.3% | 10.3% | -2.56 | 0.34 | 5.5 | 37.45 / 37.45 | -2.68% | -0.84% | -0.58% |
| ordinary | VOL | 122 | 548 | -2.26% | -36.5% | 14.1% | -2.59 | 0.46 | 11.2 | 76.49 / 76.49 | -3.69% | -1.25% | -0.80% |
| ordinary | B2 | 122 | 548 | -2.06% | -33.2% | 14.2% | -2.35 | 0.55 | 137.1 | 963.84 / 973.90 | -4.28% | -0.99% | -0.81% |
| stressed | FIXED | 122 | 548 | -1.66% | -26.8% | 10.3% | -2.61 | 0.34 | 5.5 | 68.11 / 68.11 | -2.68% | -0.84% | -0.58% |
| stressed | VOL | 122 | 548 | -2.32% | -37.6% | 14.1% | -2.66 | 0.46 | 11.2 | 139.06 / 139.06 | -3.71% | -1.25% | -0.80% |
| stressed | B2 | 122 | 548 | -2.81% | -45.6% | 14.1% | -3.23 | 0.55 | 137.2 | 1725.53 / 1743.69 | -4.87% | -0.99% | -0.82% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 122 | 2 | 0.245 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 3.30% | 0.00002 | 0.015 | -0.00004 |
| stressed | 122 | 2 | -0.565 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | -8.02% | -0.00004 | -0.037 | -0.00010 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-25T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 23.0 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
