# Paper sizing experiment PS1

Generated 2026-10-12T12:18:19.690Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-12T12:18:18.104Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 300 physical; 300 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 9.51 days; 58 scheduled decisions; coverage 86.2%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 49 closed intervals over 228.0 h; extended intervals 3.

Outcomes: executed 50; missed: stale: processed after close + max_delay 8

Execution states: completed 50

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 49 | 228 | -0.53% | -20.6% | 8.4% | -2.46 | 0.34 | 13.1 | 37.45 / 37.45 | -2.01% | -0.60% | -0.51% |
| ordinary | VOL | 49 | 228 | -0.68% | -26.3% | 11.2% | -2.35 | 0.46 | 19.4 | 55.22 / 55.22 | -2.64% | -0.79% | -0.67% |
| ordinary | B2 | 49 | 228 | 0.16% | 6.0% | 13.0% | 0.47 | 0.63 | 165.5 | 475.33 / 475.33 | -3.04% | -0.96% | -0.76% |
| stressed | FIXED | 49 | 228 | -0.56% | -21.7% | 8.4% | -2.60 | 0.34 | 13.1 | 68.11 / 68.11 | -2.01% | -0.60% | -0.51% |
| stressed | VOL | 49 | 228 | -0.73% | -28.0% | 11.2% | -2.51 | 0.46 | 19.4 | 100.40 / 100.40 | -2.64% | -0.79% | -0.67% |
| stressed | B2 | 49 | 228 | -0.23% | -8.9% | 12.9% | -0.69 | 0.63 | 165.6 | 862.09 / 862.09 | -3.13% | -0.96% | -0.76% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 49 | 1 | 2.817 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 32.29% | 0.00017 | 0.162 | 0.00014 |
| stressed | 49 | 1 | 1.817 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 19.14% | 0.00010 | 0.096 | 0.00007 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-12T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 9.5 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
