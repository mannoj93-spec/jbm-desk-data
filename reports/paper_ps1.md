# Paper sizing experiment PS1

Generated 2026-10-03T20:07:29.143Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-03T20:07:28.625Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 24 physical; 24 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 0.84 days; 6 scheduled decisions; coverage 66.7%; execution delay after the 4H close: median 16.9 min, max 20.4 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 3 closed intervals over 19.8 h; extended intervals 1.

Outcomes: executed 4; missed: stale: processed after close + max_delay 2

Execution states: completed 4

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 3 | 20 | 0.10% | 43.1% | 1.3% | 32.67 | 0.34 | 150.7 | 37.45 / 37.45 | -0.01% | -0.01% | -0.01% |
| ordinary | VOL | 3 | 20 | 0.13% | 56.7% | 1.7% | 32.67 | 0.45 | 198.2 | 49.25 / 49.25 | -0.02% | -0.02% | -0.02% |
| ordinary | B2 | 3 | 20 | 0.23% | 103.0% | 3.2% | 32.47 | 0.82 | 384.4 | 95.49 / 109.90 | -0.03% | -0.03% | -0.03% |
| stressed | FIXED | 3 | 20 | 0.07% | 29.6% | 2.2% | 13.61 | 0.34 | 150.9 | 68.11 / 68.11 | -0.04% | -0.04% | -0.04% |
| stressed | VOL | 3 | 20 | 0.09% | 38.9% | 2.9% | 13.60 | 0.45 | 198.5 | 89.57 / 89.57 | -0.06% | -0.06% | -0.06% |
| stressed | B2 | 3 | 20 | 0.15% | 68.5% | 4.8% | 14.26 | 0.82 | 384.7 | 173.57 / 199.71 | -0.09% | -0.09% | -0.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 3 | 0 | -0.200 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 46.34% | 0.00035 | 0.537 | 0.00045 |
| stressed | 3 | 0 | 0.654 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 29.59% | 0.00022 | 0.320 | 0.00029 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-03T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 0.8 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
