# Paper sizing experiment PS1

Generated 2026-10-19T04:19:07.771Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-19T04:19:06.244Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 540 physical; 540 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 16.18 days; 98 scheduled decisions; coverage 91.8%; execution delay after the 4H close: median 18.5 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 89 closed intervals over 388.0 h; extended intervals 3.

Outcomes: executed 90; missed: stale: processed after close + max_delay 8

Execution states: completed 90

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 89 | 388 | -0.87% | -19.7% | 10.6% | -1.86 | 0.34 | 7.7 | 37.45 / 37.45 | -2.23% | -0.84% | -0.63% |
| ordinary | VOL | 89 | 388 | -1.26% | -28.6% | 14.8% | -1.93 | 0.46 | 12.6 | 60.71 / 66.21 | -3.05% | -1.25% | -0.89% |
| ordinary | B2 | 89 | 388 | -0.68% | -15.4% | 14.0% | -1.10 | 0.57 | 160.0 | 802.65 / 808.40 | -3.34% | -0.96% | -0.80% |
| stressed | FIXED | 89 | 388 | -0.90% | -20.4% | 10.6% | -1.93 | 0.34 | 7.7 | 68.11 / 68.11 | -2.23% | -0.84% | -0.63% |
| stressed | VOL | 89 | 388 | -1.31% | -29.7% | 14.8% | -2.00 | 0.46 | 12.6 | 110.37 / 120.36 | -3.06% | -1.25% | -0.89% |
| stressed | B2 | 89 | 388 | -1.31% | -29.9% | 14.0% | -2.14 | 0.57 | 160.1 | 1434.57 / 1444.94 | -3.82% | -0.96% | -0.80% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 89 | 2 | 0.825 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 13.14% | 0.00007 | 0.053 | 0.00002 |
| stressed | 89 | 2 | -0.132 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | -0.13% | -0.00000 | -0.001 | -0.00005 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-19T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 16.2 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
