# Paper sizing experiment PS1

Generated 2026-10-12T04:18:41.800Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-12T04:12:49.137Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 288 physical; 288 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 9.18 days; 56 scheduled decisions; coverage 85.7%; execution delay after the 4H close: median 18.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 47 closed intervals over 219.9 h; extended intervals 3.

Outcomes: executed 48; missed: stale: processed after close + max_delay 8

Execution states: completed 48

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 47 | 220 | -0.44% | -17.7% | 8.5% | -2.08 | 0.34 | 13.6 | 37.45 / 37.45 | -2.01% | -0.60% | -0.51% |
| ordinary | VOL | 47 | 220 | -0.55% | -21.9% | 11.4% | -1.93 | 0.46 | 20.1 | 55.22 / 55.22 | -2.64% | -0.79% | -0.67% |
| ordinary | B2 | 47 | 220 | 0.29% | 11.5% | 13.2% | 0.87 | 0.64 | 167.3 | 463.22 / 463.22 | -3.04% | -0.96% | -0.76% |
| stressed | FIXED | 47 | 220 | -0.47% | -19.0% | 8.5% | -2.23 | 0.34 | 13.6 | 68.11 / 68.11 | -2.01% | -0.60% | -0.51% |
| stressed | VOL | 47 | 220 | -0.59% | -23.8% | 11.4% | -2.09 | 0.46 | 20.1 | 100.40 / 100.40 | -2.64% | -0.79% | -0.67% |
| stressed | B2 | 47 | 220 | -0.09% | -3.6% | 13.1% | -0.27 | 0.64 | 167.3 | 840.14 / 840.14 | -3.13% | -0.96% | -0.76% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 47 | 1 | 2.804 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 33.41% | 0.00018 | 0.165 | 0.00016 |
| stressed | 47 | 1 | 1.817 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 20.17% | 0.00011 | 0.100 | 0.00008 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-12T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 9.2 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
