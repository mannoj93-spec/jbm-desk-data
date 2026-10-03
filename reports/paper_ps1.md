# Paper sizing experiment PS1

Generated 2026-10-03T04:17:44.600Z by ps1-job-3.1.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-03T04:17:44.084Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 12 physical; 12 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 0.18 days; 2 scheduled decisions; coverage 100.0%; execution delay after the 4H close: median 19.1 min, max 20.4 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 1 closed intervals over 4.0 h; extended intervals 0.

Outcomes: executed 2

Execution states: completed 2

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 1 | 4 | -0.01% | -26.7% | — | — | 0.34 | 753.9 | 37.45 / 37.45 | -0.01% | -0.01% | -0.01% |
| ordinary | VOL | 1 | 4 | -0.02% | -35.1% | — | — | 0.45 | 991.5 | 49.25 / 49.25 | -0.02% | -0.02% | -0.02% |
| ordinary | B2 | 1 | 4 | -0.03% | -55.5% | — | — | 0.71 | 1566.3 | 77.80 / 84.46 | -0.03% | -0.03% | -0.03% |
| stressed | FIXED | 1 | 4 | -0.04% | -94.6% | — | — | 0.34 | 754.6 | 68.11 / 68.11 | -0.04% | -0.04% | -0.04% |
| stressed | VOL | 1 | 4 | -0.06% | -124.4% | — | — | 0.45 | 992.4 | 89.57 / 89.57 | -0.06% | -0.06% | -0.06% |
| stressed | B2 | 1 | 4 | -0.09% | -196.6% | — | — | 0.71 | 1567.7 | 141.50 / 153.53 | -0.09% | -0.09% | -0.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 1 | 0 | — | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | -20.35% | -0.00009 | — | -0.00013 |
| stressed | 1 | 0 | — | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | -72.18% | -0.00033 | — | -0.00046 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-03T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 0.2 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
