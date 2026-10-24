# Paper sizing experiment PS1

Generated 2026-10-24T15:37:00.726Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-24T12:18:23.892Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 690 physical; 690 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 21.65 days; 130 scheduled decisions; coverage 88.5%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 114 closed intervals over 516.0 h; extended intervals 6.

Outcomes: executed 115; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 115

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 114 | 516 | -1.58% | -27.0% | 10.3% | -2.61 | 0.34 | 5.8 | 37.45 / 37.45 | -2.28% | -0.84% | -0.61% |
| ordinary | VOL | 114 | 516 | -2.19% | -37.5% | 14.1% | -2.66 | 0.45 | 11.9 | 76.49 / 76.49 | -3.10% | -1.25% | -0.84% |
| ordinary | B2 | 114 | 516 | -1.60% | -27.4% | 13.7% | -2.00 | 0.54 | 138.4 | 918.11 / 918.11 | -3.34% | -0.96% | -0.78% |
| stressed | FIXED | 114 | 516 | -1.61% | -27.6% | 10.3% | -2.67 | 0.34 | 5.8 | 68.11 / 68.11 | -2.28% | -0.84% | -0.61% |
| stressed | VOL | 114 | 516 | -2.25% | -38.6% | 14.1% | -2.73 | 0.45 | 11.9 | 139.06 / 139.06 | -3.12% | -1.25% | -0.84% |
| stressed | B2 | 114 | 516 | -2.32% | -39.8% | 13.7% | -2.91 | 0.54 | 138.4 | 1643.04 / 1643.04 | -3.92% | -0.96% | -0.78% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 114 | 2 | 0.663 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 10.12% | 0.00005 | 0.047 | -0.00000 |
| stressed | 114 | 2 | -0.175 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | -1.26% | -0.00001 | -0.006 | -0.00006 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-24T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 21.7 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
