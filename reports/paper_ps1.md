# Paper sizing experiment PS1

Generated 2026-11-21T01:51:15.185Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-21T00:28:01.100Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1434 physical; 1434 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 49.08 days; 295 scheduled decisions; coverage 81.0%; execution delay after the 4H close: median 21.1 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 238 closed intervals over 1176.1 h; extended intervals 14.

Outcomes: executed 239; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 42

Execution states: completed 239

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 238 | 1176 | -10.86% | -85.6% | 12.7% | -6.75 | 0.33 | 3.0 | 42.58 / 42.58 | -11.50% | -1.36% | -0.88% |
| ordinary | VOL | 238 | 1176 | -12.05% | -95.6% | 15.3% | -6.23 | 0.41 | 7.7 | 110.14 / 110.14 | -12.87% | -2.00% | -1.03% |
| ordinary | B2 | 238 | 1176 | -13.82% | -110.7% | 14.7% | -7.54 | 0.52 | 108.3 | 1580.68 / 1592.26 | -15.33% | -2.24% | -1.12% |
| stressed | FIXED | 238 | 1176 | -10.90% | -85.9% | 12.7% | -6.77 | 0.33 | 3.0 | 77.42 / 77.42 | -11.50% | -1.36% | -0.88% |
| stressed | VOL | 238 | 1176 | -12.13% | -96.3% | 15.4% | -6.27 | 0.41 | 7.7 | 200.14 / 200.14 | -12.92% | -2.00% | -1.04% |
| stressed | B2 | 238 | 1176 | -14.92% | -120.4% | 14.7% | -8.20 | 0.52 | 108.4 | 2821.59 / 2842.38 | -16.32% | -2.25% | -1.13% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 238 | 5 | -1.306 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -15.11% | -0.00009 | -0.064 | -0.00014 |
| stressed | 238 | 5 | -1.929 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -24.05% | -0.00014 | -0.101 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-21T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 49.1 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
