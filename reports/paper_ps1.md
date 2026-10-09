# Paper sizing experiment PS1

Generated 2026-10-09T01:09:15.983Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-09T00:16:24.225Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 174 physical; 174 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 6.05 days; 37 scheduled decisions; coverage 78.4%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 28 closed intervals over 143.9 h; extended intervals 3.

Outcomes: executed 29; missed: stale: processed after close + max_delay 8

Execution states: completed 29

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 28 | 144 | -1.14% | -69.8% | 9.8% | -7.16 | 0.34 | 20.7 | 37.45 / 37.45 | -2.01% | -0.60% | -0.60% |
| ordinary | VOL | 28 | 144 | -1.50% | -92.0% | 12.8% | -7.17 | 0.45 | 27.3 | 49.25 / 49.25 | -2.64% | -0.79% | -0.79% |
| ordinary | B2 | 28 | 144 | -1.14% | -69.9% | 14.6% | -4.79 | 0.59 | 151.3 | 275.56 / 291.07 | -3.04% | -0.96% | -0.96% |
| stressed | FIXED | 28 | 144 | -1.17% | -71.7% | 9.8% | -7.35 | 0.34 | 20.7 | 68.11 / 68.11 | -2.01% | -0.60% | -0.60% |
| stressed | VOL | 28 | 144 | -1.54% | -94.5% | 12.8% | -7.36 | 0.45 | 27.3 | 89.57 / 89.57 | -2.64% | -0.79% | -0.79% |
| stressed | B2 | 28 | 144 | -1.36% | -83.6% | 14.6% | -5.74 | 0.59 | 151.4 | 499.96 / 528.09 | -3.13% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 28 | 0 | 2.380 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 22.10% | 0.00013 | 0.102 | -0.00000 |
| stressed | 28 | 0 | 1.621 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 10.96% | 0.00006 | 0.051 | -0.00007 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-09T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 6.0 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
