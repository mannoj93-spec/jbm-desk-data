# Paper sizing experiment PS1

Generated 2026-10-03T09:03:10.703Z by ps1-job-3.1.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-03T08:16:04.089Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 18 physical; 18 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 0.38 days; 3 scheduled decisions; coverage 100.0%; execution delay after the 4H close: median 17.7 min, max 20.4 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 2 closed intervals over 7.9 h; extended intervals 0.

Outcomes: executed 3

Execution states: completed 3

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 2 | 8 | -0.00% | -0.4% | 0.8% | -0.53 | 0.34 | 376.2 | 37.45 / 37.45 | -0.01% | -0.01% | -0.01% |
| ordinary | VOL | 2 | 8 | -0.00% | -0.5% | 1.0% | -0.53 | 0.45 | 494.7 | 49.25 / 49.25 | -0.02% | -0.02% | -0.02% |
| ordinary | B2 | 2 | 8 | -0.01% | -5.9% | 1.5% | -3.99 | 0.74 | 848.5 | 84.46 / 95.49 | -0.03% | -0.03% | -0.03% |
| stressed | FIXED | 2 | 8 | -0.03% | -34.3% | 1.8% | -18.95 | 0.34 | 376.6 | 68.11 / 68.11 | -0.04% | -0.04% | -0.04% |
| stressed | VOL | 2 | 8 | -0.04% | -45.1% | 2.4% | -18.95 | 0.45 | 495.3 | 89.57 / 89.57 | -0.06% | -0.06% | -0.06% |
| stressed | B2 | 2 | 8 | -0.07% | -82.3% | 3.4% | -23.98 | 0.74 | 849.0 | 153.53 / 173.57 | -0.09% | -0.09% | -0.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 2 | 0 | -3.465 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | -5.39% | -0.00002 | -0.255 | -0.00002 |
| stressed | 2 | 0 | -5.035 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | -37.19% | -0.00017 | -0.755 | -0.00022 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-03T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 0.4 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
