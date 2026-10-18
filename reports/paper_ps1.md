# Paper sizing experiment PS1

Generated 2026-10-18T08:24:43.871Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-18T08:17:39.471Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 510 physical; 510 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 15.35 days; 93 scheduled decisions; coverage 91.4%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 84 closed intervals over 368.0 h; extended intervals 3.

Outcomes: executed 85; missed: stale: processed after close + max_delay 8

Execution states: completed 85

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 84 | 368 | -1.19% | -28.6% | 10.3% | -2.78 | 0.34 | 8.1 | 37.45 / 37.45 | -2.16% | -0.84% | -0.63% |
| ordinary | VOL | 84 | 368 | -1.69% | -40.6% | 14.5% | -2.79 | 0.47 | 13.2 | 60.71 / 60.71 | -2.96% | -1.25% | -0.89% |
| ordinary | B2 | 84 | 368 | -1.09% | -26.1% | 13.3% | -1.96 | 0.57 | 155.1 | 716.67 / 728.08 | -3.05% | -0.96% | -0.77% |
| stressed | FIXED | 84 | 368 | -1.22% | -29.3% | 10.3% | -2.85 | 0.34 | 8.2 | 68.11 / 68.11 | -2.16% | -0.84% | -0.63% |
| stressed | VOL | 84 | 368 | -1.74% | -41.8% | 14.5% | -2.87 | 0.47 | 13.2 | 110.37 / 110.37 | -2.97% | -1.25% | -0.89% |
| stressed | B2 | 84 | 368 | -1.67% | -40.0% | 13.3% | -3.02 | 0.57 | 155.1 | 1298.38 / 1318.97 | -3.47% | -0.96% | -0.77% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 84 | 2 | 0.832 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 14.51% | 0.00007 | 0.059 | 0.00001 |
| stressed | 84 | 2 | -0.144 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 1.75% | 0.00001 | 0.007 | -0.00005 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-18T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 15.4 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
