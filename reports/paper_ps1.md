# Paper sizing experiment PS1

Generated 2026-10-08T16:21:46.741Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-08T16:21:45.725Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 162 physical; 162 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 5.68 days; 35 scheduled decisions; coverage 77.1%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 26 closed intervals over 136.0 h; extended intervals 3.

Outcomes: executed 27; missed: stale: processed after close + max_delay 8

Execution states: completed 27

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 26 | 136 | -1.31% | -84.7% | 9.9% | -8.55 | 0.34 | 21.9 | 37.45 / 37.45 | -2.01% | -0.60% | -0.60% |
| ordinary | VOL | 26 | 136 | -1.72% | -111.7% | 13.0% | -8.57 | 0.45 | 28.8 | 49.25 / 49.25 | -2.64% | -0.79% | -0.79% |
| ordinary | B2 | 26 | 136 | -1.30% | -84.5% | 15.0% | -5.63 | 0.61 | 153.7 | 264.81 / 275.56 | -3.04% | -0.96% | -0.96% |
| stressed | FIXED | 26 | 136 | -1.34% | -86.7% | 9.9% | -8.75 | 0.34 | 21.9 | 68.11 / 68.11 | -2.01% | -0.60% | -0.60% |
| stressed | VOL | 26 | 136 | -1.76% | -114.3% | 13.0% | -8.77 | 0.45 | 28.8 | 89.57 / 89.57 | -2.64% | -0.79% | -0.79% |
| stressed | B2 | 26 | 136 | -1.52% | -98.4% | 15.0% | -6.57 | 0.61 | 153.8 | 480.45 / 499.96 | -3.13% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 26 | 0 | 2.943 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 27.13% | 0.00016 | 0.123 | 0.00000 |
| stressed | 26 | 0 | 2.203 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 15.92% | 0.00010 | 0.073 | -0.00007 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-08T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 5.7 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
