# Paper sizing experiment PS1

Generated 2026-10-10T08:11:41.619Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-10T08:11:40.390Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 222 physical; 222 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 7.34 days; 45 scheduled decisions; coverage 82.2%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 36 closed intervals over 175.9 h; extended intervals 3.

Outcomes: executed 37; missed: stale: processed after close + max_delay 8

Execution states: completed 37

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 36 | 176 | -0.73% | -36.4% | 9.4% | -3.87 | 0.34 | 17.0 | 37.45 / 37.45 | -2.01% | -0.60% | -0.60% |
| ordinary | VOL | 36 | 176 | -0.97% | -48.5% | 12.5% | -3.89 | 0.45 | 25.1 | 55.22 / 55.22 | -2.64% | -0.79% | -0.79% |
| ordinary | B2 | 36 | 176 | -0.45% | -22.4% | 13.9% | -1.61 | 0.59 | 172.1 | 381.54 / 387.12 | -3.04% | -0.96% | -0.96% |
| stressed | FIXED | 36 | 176 | -0.76% | -38.0% | 9.4% | -4.03 | 0.34 | 17.0 | 68.11 / 68.11 | -2.01% | -0.60% | -0.60% |
| stressed | VOL | 36 | 176 | -1.01% | -50.8% | 12.5% | -4.07 | 0.45 | 25.1 | 100.40 / 100.40 | -2.64% | -0.79% | -0.79% |
| stressed | B2 | 36 | 176 | -0.76% | -37.9% | 13.8% | -2.75 | 0.59 | 172.1 | 692.13 / 702.26 | -3.13% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 36 | 0 | 2.274 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 26.13% | 0.00015 | 0.129 | 0.00008 |
| stressed | 36 | 0 | 1.320 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 12.90% | 0.00007 | 0.064 | 0.00000 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-10T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 7.3 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
