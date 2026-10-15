# Paper sizing experiment PS1

Generated 2026-10-15T20:25:50.094Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-15T20:14:33.007Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 420 physical; 420 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 12.85 days; 78 scheduled decisions; coverage 89.7%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 69 closed intervals over 307.9 h; extended intervals 3.

Outcomes: executed 70; missed: stale: processed after close + max_delay 8

Execution states: completed 70

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 69 | 308 | -0.94% | -26.9% | 11.2% | -2.41 | 0.34 | 9.7 | 37.45 / 37.45 | -2.16% | -0.84% | -0.70% |
| ordinary | VOL | 69 | 308 | -1.35% | -38.8% | 15.8% | -2.46 | 0.47 | 15.8 | 60.71 / 60.71 | -2.96% | -1.25% | -1.00% |
| ordinary | B2 | 69 | 308 | -0.61% | -17.3% | 14.2% | -1.21 | 0.57 | 152.7 | 591.21 / 602.24 | -3.04% | -0.96% | -0.84% |
| stressed | FIXED | 69 | 308 | -0.97% | -27.8% | 11.2% | -2.48 | 0.34 | 9.7 | 68.11 / 68.11 | -2.16% | -0.84% | -0.70% |
| stressed | VOL | 69 | 308 | -1.40% | -40.2% | 15.8% | -2.54 | 0.47 | 15.8 | 110.37 / 110.37 | -2.97% | -1.25% | -1.00% |
| stressed | B2 | 69 | 308 | -1.08% | -31.0% | 14.2% | -2.19 | 0.57 | 152.7 | 1071.86 / 1091.83 | -3.13% | -0.96% | -0.84% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 69 | 1 | 1.241 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 21.53% | 0.00011 | 0.083 | 0.00005 |
| stressed | 69 | 1 | 0.358 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 9.21% | 0.00005 | 0.036 | -0.00002 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-15T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 12.9 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
