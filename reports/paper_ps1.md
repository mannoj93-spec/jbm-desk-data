# Paper sizing experiment PS1

Generated 2026-11-16T05:27:31.171Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-16T04:24:59.042Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1272 physical; 1272 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 44.23 days; 266 scheduled decisions; coverage 79.7%; execution delay after the 4H close: median 20.5 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 211 closed intervals over 1060.1 h; extended intervals 12.

Outcomes: executed 212; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 212

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 211 | 1060 | -7.99% | -68.8% | 12.0% | -5.75 | 0.33 | 3.3 | 42.58 / 42.58 | -9.09% | -1.36% | -0.80% |
| ordinary | VOL | 211 | 1060 | -9.88% | -85.9% | 15.6% | -5.51 | 0.42 | 8.5 | 110.14 / 110.14 | -11.11% | -2.00% | -1.04% |
| ordinary | B2 | 211 | 1060 | -11.55% | -101.4% | 14.8% | -6.85 | 0.55 | 115.9 | 1543.56 / 1543.56 | -13.36% | -2.24% | -1.13% |
| stressed | FIXED | 211 | 1060 | -8.03% | -69.1% | 12.0% | -5.78 | 0.33 | 3.3 | 77.42 / 77.42 | -9.10% | -1.36% | -0.80% |
| stressed | VOL | 211 | 1060 | -9.96% | -86.7% | 15.6% | -5.56 | 0.42 | 8.5 | 200.14 / 200.14 | -11.15% | -2.00% | -1.04% |
| stressed | B2 | 211 | 1060 | -12.66% | -111.8% | 14.8% | -7.56 | 0.55 | 116.0 | 2755.16 / 2755.16 | -14.34% | -2.25% | -1.13% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 211 | 5 | -1.339 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -15.51% | -0.00009 | -0.063 | -0.00019 |
| stressed | 211 | 5 | -2.000 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -25.14% | -0.00014 | -0.102 | -0.00024 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-16T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 44.2 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
