# Paper sizing experiment PS1

Generated 2026-10-13T21:16:09.787Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-13T20:18:13.615Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 348 physical; 348 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 10.89 days; 66 scheduled decisions; coverage 87.9%; execution delay after the 4H close: median 18.7 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 57 closed intervals over 260.0 h; extended intervals 3.

Outcomes: executed 58; missed: stale: processed after close + max_delay 8

Execution states: completed 58

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 57 | 260 | -0.56% | -19.0% | 10.4% | -1.82 | 0.34 | 11.5 | 37.45 / 37.45 | -2.01% | -0.65% | -0.63% |
| ordinary | VOL | 57 | 260 | -0.72% | -24.5% | 14.6% | -1.67 | 0.47 | 17.0 | 55.22 / 55.22 | -2.69% | -0.97% | -0.88% |
| ordinary | B2 | 57 | 260 | -0.16% | -5.3% | 14.8% | -0.35 | 0.61 | 154.0 | 503.97 / 503.97 | -3.04% | -0.96% | -0.95% |
| stressed | FIXED | 57 | 260 | -0.59% | -20.0% | 10.4% | -1.92 | 0.34 | 11.5 | 68.11 / 68.11 | -2.01% | -0.65% | -0.63% |
| stressed | VOL | 57 | 260 | -0.77% | -26.0% | 14.6% | -1.78 | 0.47 | 17.0 | 100.40 / 100.40 | -2.70% | -0.97% | -0.88% |
| stressed | B2 | 57 | 260 | -0.57% | -19.1% | 14.8% | -1.29 | 0.61 | 154.1 | 913.95 / 913.95 | -3.13% | -0.96% | -0.95% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 57 | 1 | 1.321 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 19.22% | 0.00010 | 0.093 | 0.00007 |
| stressed | 57 | 1 | 0.485 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 6.89% | 0.00004 | 0.034 | 0.00000 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-13T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 10.9 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
