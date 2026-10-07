# Paper sizing experiment PS1

Generated 2026-10-07T21:02:42.511Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-07T20:11:36.451Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 132 physical; 132 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 4.88 days; 30 scheduled decisions; coverage 73.3%; execution delay after the 4H close: median 18.1 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 21 closed intervals over 115.9 h; extended intervals 3.

Outcomes: executed 22; missed: stale: processed after close + max_delay 8

Execution states: completed 22

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 21 | 116 | -0.43% | -32.9% | 9.5% | -3.48 | 0.34 | 25.7 | 37.45 / 37.45 | -1.14% | -0.60% | -0.60% |
| ordinary | VOL | 21 | 116 | -0.57% | -43.4% | 12.4% | -3.49 | 0.45 | 33.7 | 49.25 / 49.25 | -1.50% | -0.79% | -0.79% |
| ordinary | B2 | 21 | 116 | -0.14% | -10.4% | 14.8% | -0.70 | 0.64 | 180.0 | 264.81 / 264.81 | -1.89% | -0.96% | -0.96% |
| stressed | FIXED | 21 | 116 | -0.47% | -35.3% | 9.5% | -3.73 | 0.34 | 25.7 | 68.11 / 68.11 | -1.14% | -0.60% | -0.60% |
| stressed | VOL | 21 | 116 | -0.61% | -46.4% | 12.4% | -3.73 | 0.45 | 33.8 | 89.57 / 89.57 | -1.50% | -0.79% | -0.79% |
| stressed | B2 | 21 | 116 | -0.35% | -26.6% | 14.8% | -1.80 | 0.64 | 180.0 | 480.45 / 480.45 | -1.99% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 21 | 0 | 2.788 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 32.97% | 0.00021 | 0.141 | 0.00014 |
| stressed | 21 | 0 | 1.934 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 19.78% | 0.00012 | 0.086 | 0.00005 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-07T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 4.9 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
