# Paper sizing experiment PS1

Generated 2026-10-15T16:18:39.955Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-15T16:18:37.874Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 414 physical; 414 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 12.68 days; 77 scheduled decisions; coverage 89.6%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 68 closed intervals over 304.0 h; extended intervals 3.

Outcomes: executed 69; missed: stale: processed after close + max_delay 8

Execution states: completed 69

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 68 | 304 | -0.93% | -27.1% | 11.3% | -2.40 | 0.34 | 9.9 | 37.45 / 37.45 | -2.16% | -0.84% | -0.70% |
| ordinary | VOL | 68 | 304 | -1.35% | -39.1% | 15.9% | -2.45 | 0.47 | 16.0 | 60.71 / 60.71 | -2.96% | -1.25% | -1.00% |
| ordinary | B2 | 68 | 304 | -0.59% | -17.2% | 14.3% | -1.20 | 0.57 | 152.9 | 584.54 / 591.21 | -3.04% | -0.96% | -0.84% |
| stressed | FIXED | 68 | 304 | -0.97% | -27.9% | 11.3% | -2.48 | 0.34 | 9.9 | 68.11 / 68.11 | -2.16% | -0.84% | -0.70% |
| stressed | VOL | 68 | 304 | -1.40% | -40.5% | 15.9% | -2.54 | 0.47 | 16.0 | 110.37 / 110.37 | -2.97% | -1.25% | -1.00% |
| stressed | B2 | 68 | 304 | -1.07% | -30.9% | 14.3% | -2.16 | 0.57 | 153.0 | 1059.79 / 1071.86 | -3.13% | -0.96% | -0.84% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 68 | 1 | 1.257 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 21.92% | 0.00011 | 0.084 | 0.00005 |
| stressed | 68 | 1 | 0.381 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 9.60% | 0.00005 | 0.037 | -0.00002 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-15T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 12.7 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
