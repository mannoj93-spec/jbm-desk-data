# Paper sizing experiment PS1

Generated 2026-10-08T20:18:53.935Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-08T20:18:52.863Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 168 physical; 168 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 5.85 days; 36 scheduled decisions; coverage 77.8%; execution delay after the 4H close: median 18.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 27 closed intervals over 140.0 h; extended intervals 3.

Outcomes: executed 28; missed: stale: processed after close + max_delay 8

Execution states: completed 28

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 27 | 140 | -1.12% | -70.2% | 9.9% | -7.06 | 0.34 | 21.3 | 37.45 / 37.45 | -2.01% | -0.60% | -0.60% |
| ordinary | VOL | 27 | 140 | -1.47% | -92.4% | 13.1% | -7.07 | 0.45 | 28.0 | 49.25 / 49.25 | -2.64% | -0.79% | -0.79% |
| ordinary | B2 | 27 | 140 | -1.12% | -70.2% | 14.9% | -4.72 | 0.60 | 155.5 | 275.56 / 275.56 | -3.04% | -0.96% | -0.96% |
| stressed | FIXED | 27 | 140 | -1.15% | -72.1% | 9.9% | -7.25 | 0.34 | 21.3 | 68.11 / 68.11 | -2.01% | -0.60% | -0.60% |
| stressed | VOL | 27 | 140 | -1.51% | -95.0% | 13.1% | -7.26 | 0.45 | 28.0 | 89.57 / 89.57 | -2.64% | -0.79% | -0.79% |
| stressed | B2 | 27 | 140 | -1.34% | -84.2% | 14.8% | -5.68 | 0.60 | 155.6 | 499.96 / 499.96 | -3.13% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 27 | 0 | 2.351 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 22.26% | 0.00013 | 0.101 | -0.00000 |
| stressed | 27 | 0 | 1.585 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 10.81% | 0.00006 | 0.050 | -0.00007 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-08T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 5.8 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
