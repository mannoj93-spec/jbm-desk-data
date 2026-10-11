# Paper sizing experiment PS1

Generated 2026-10-11T20:21:52.397Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-11T20:21:50.962Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 276 physical; 276 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 8.85 days; 54 scheduled decisions; coverage 85.2%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 45 closed intervals over 212.0 h; extended intervals 3.

Outcomes: executed 46; missed: stale: processed after close + max_delay 8

Execution states: completed 46

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 45 | 212 | -0.39% | -16.1% | 8.7% | -1.86 | 0.34 | 14.1 | 37.45 / 37.45 | -2.01% | -0.60% | -0.51% |
| ordinary | VOL | 45 | 212 | -0.47% | -19.4% | 11.6% | -1.68 | 0.46 | 20.8 | 55.22 / 55.22 | -2.64% | -0.79% | -0.67% |
| ordinary | B2 | 45 | 212 | 0.39% | 15.9% | 13.4% | 1.19 | 0.64 | 173.5 | 463.22 / 463.22 | -3.04% | -0.96% | -0.76% |
| stressed | FIXED | 45 | 212 | -0.42% | -17.4% | 8.7% | -2.00 | 0.34 | 14.1 | 68.11 / 68.11 | -2.01% | -0.60% | -0.51% |
| stressed | VOL | 45 | 212 | -0.51% | -21.2% | 11.6% | -1.84 | 0.46 | 20.8 | 100.40 / 100.40 | -2.64% | -0.79% | -0.67% |
| stressed | B2 | 45 | 212 | 0.01% | 0.3% | 13.3% | 0.02 | 0.64 | 173.5 | 840.14 / 840.14 | -3.13% | -0.96% | -0.76% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 45 | 1 | 2.862 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 35.26% | 0.00019 | 0.172 | 0.00017 |
| stressed | 45 | 1 | 1.857 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 21.52% | 0.00012 | 0.105 | 0.00009 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-11T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 8.8 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
