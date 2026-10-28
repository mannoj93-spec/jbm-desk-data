# Paper sizing experiment PS1

Generated 2026-10-28T08:22:01.985Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-28T08:21:57.871Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 828 physical; 828 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 25.35 days; 153 scheduled decisions; coverage 90.2%; execution delay after the 4H close: median 19.1 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 137 closed intervals over 608.0 h; extended intervals 6.

Outcomes: executed 138; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 138

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 137 | 608 | -1.38% | -20.0% | 9.9% | -2.03 | 0.34 | 4.9 | 37.45 / 37.45 | -2.68% | -0.84% | -0.58% |
| ordinary | VOL | 137 | 608 | -1.89% | -27.5% | 13.6% | -2.03 | 0.46 | 10.1 | 76.49 / 76.49 | -3.69% | -1.25% | -0.80% |
| ordinary | B2 | 137 | 608 | -1.85% | -26.9% | 13.6% | -1.97 | 0.54 | 132.3 | 1028.16 / 1040.68 | -4.34% | -0.99% | -0.81% |
| stressed | FIXED | 137 | 608 | -1.41% | -20.5% | 9.9% | -2.07 | 0.34 | 5.0 | 68.11 / 68.11 | -2.68% | -0.84% | -0.58% |
| stressed | VOL | 137 | 608 | -1.95% | -28.4% | 13.6% | -2.10 | 0.46 | 10.1 | 139.06 / 139.06 | -3.71% | -1.25% | -0.80% |
| stressed | B2 | 137 | 608 | -2.65% | -38.7% | 13.6% | -2.85 | 0.54 | 132.4 | 1841.55 / 1864.14 | -5.00% | -0.99% | -0.82% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 137 | 3 | 0.060 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 0.67% | 0.00000 | 0.003 | -0.00003 |
| stressed | 137 | 3 | -0.753 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -10.31% | -0.00005 | -0.049 | -0.00009 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-28T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 25.3 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
