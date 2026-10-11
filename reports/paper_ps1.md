# Paper sizing experiment PS1

Generated 2026-10-11T01:06:46.819Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-11T00:17:38.038Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 246 physical; 246 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 8.05 days; 49 scheduled decisions; coverage 83.7%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 40 closed intervals over 192.0 h; extended intervals 3.

Outcomes: executed 41; missed: stale: processed after close + max_delay 8

Execution states: completed 41

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 40 | 192 | -0.65% | -29.9% | 9.0% | -3.34 | 0.34 | 15.6 | 37.45 / 37.45 | -2.01% | -0.60% | -0.51% |
| ordinary | VOL | 40 | 192 | -0.86% | -39.3% | 11.9% | -3.32 | 0.46 | 23.0 | 55.22 / 55.22 | -2.64% | -0.79% | -0.67% |
| ordinary | B2 | 40 | 192 | -0.25% | -11.2% | 13.2% | -0.85 | 0.62 | 164.3 | 397.54 / 397.54 | -3.04% | -0.96% | -0.76% |
| stressed | FIXED | 40 | 192 | -0.68% | -31.3% | 9.0% | -3.50 | 0.34 | 15.6 | 68.11 / 68.11 | -2.01% | -0.60% | -0.51% |
| stressed | VOL | 40 | 192 | -0.90% | -41.4% | 11.9% | -3.49 | 0.46 | 23.0 | 100.40 / 100.40 | -2.64% | -0.79% | -0.67% |
| stressed | B2 | 40 | 192 | -0.57% | -26.0% | 13.2% | -1.98 | 0.62 | 164.4 | 721.13 / 721.13 | -3.13% | -0.96% | -0.76% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 40 | 0 | 2.470 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 28.14% | 0.00015 | 0.142 | 0.00010 |
| stressed | 40 | 0 | 1.513 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 15.41% | 0.00008 | 0.079 | 0.00003 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-11T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 8.0 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
