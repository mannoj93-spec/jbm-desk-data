# Paper sizing experiment PS1

Generated 2026-10-10T04:19:31.381Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-10T04:19:30.152Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 216 physical; 216 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 7.18 days; 44 scheduled decisions; coverage 81.8%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 35 closed intervals over 172.0 h; extended intervals 3.

Outcomes: executed 36; missed: stale: processed after close + max_delay 8

Execution states: completed 36

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 35 | 172 | -0.79% | -40.2% | 9.5% | -4.22 | 0.34 | 17.4 | 37.45 / 37.45 | -2.01% | -0.60% | -0.60% |
| ordinary | VOL | 35 | 172 | -1.06% | -54.0% | 12.6% | -4.28 | 0.45 | 25.6 | 55.22 / 55.22 | -2.64% | -0.79% | -0.79% |
| ordinary | B2 | 35 | 172 | -0.60% | -30.7% | 14.0% | -2.19 | 0.58 | 169.3 | 367.36 / 381.54 | -3.04% | -0.96% | -0.96% |
| stressed | FIXED | 35 | 172 | -0.82% | -41.8% | 9.5% | -4.38 | 0.34 | 17.4 | 68.11 / 68.11 | -2.01% | -0.60% | -0.60% |
| stressed | VOL | 35 | 172 | -1.10% | -56.4% | 12.6% | -4.46 | 0.45 | 25.7 | 100.40 / 100.40 | -2.64% | -0.79% | -0.79% |
| stressed | B2 | 35 | 172 | -0.90% | -45.9% | 13.9% | -3.30 | 0.58 | 169.4 | 666.46 / 692.13 | -3.13% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 35 | 0 | 2.089 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 23.36% | 0.00013 | 0.114 | 0.00005 |
| stressed | 35 | 0 | 1.163 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 10.42% | 0.00006 | 0.051 | -0.00002 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-10T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 7.2 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
