# Paper sizing experiment PS1

Generated 2026-10-10T01:07:44.244Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-10T00:18:11.169Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 210 physical; 210 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 7.05 days; 43 scheduled decisions; coverage 81.4%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 34 closed intervals over 168.0 h; extended intervals 3.

Outcomes: executed 35; missed: stale: processed after close + max_delay 8

Execution states: completed 35

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 34 | 168 | -0.81% | -42.4% | 9.7% | -4.38 | 0.34 | 17.8 | 37.45 / 37.45 | -2.01% | -0.60% | -0.60% |
| ordinary | VOL | 34 | 168 | -1.09% | -57.1% | 12.8% | -4.46 | 0.45 | 26.2 | 55.22 / 55.22 | -2.64% | -0.79% | -0.79% |
| ordinary | B2 | 34 | 168 | -0.62% | -32.4% | 14.2% | -2.28 | 0.57 | 156.3 | 331.35 / 367.36 | -3.04% | -0.96% | -0.96% |
| stressed | FIXED | 34 | 168 | -0.84% | -44.0% | 9.7% | -4.54 | 0.34 | 17.8 | 68.11 / 68.11 | -2.01% | -0.60% | -0.60% |
| stressed | VOL | 34 | 168 | -1.13% | -59.5% | 12.8% | -4.64 | 0.45 | 26.3 | 100.40 / 100.40 | -2.64% | -0.79% | -0.79% |
| stressed | B2 | 34 | 168 | -0.89% | -46.5% | 14.1% | -3.29 | 0.57 | 156.4 | 601.14 / 666.46 | -3.13% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 34 | 0 | 2.175 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 24.65% | 0.00014 | 0.120 | 0.00006 |
| stressed | 34 | 0 | 1.351 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 12.95% | 0.00007 | 0.063 | -0.00001 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-10T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 7.0 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
