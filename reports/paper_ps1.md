# Paper sizing experiment PS1

Generated 2026-10-04T21:31:50.300Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-04T20:51:13.156Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 30 physical; 30 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 1.9 days; 12 scheduled decisions; coverage 41.7%; execution delay after the 4H close: median 17.7 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 4 closed intervals over 44.5 h; extended intervals 2.

Outcomes: executed 5; missed: stale: processed after close + max_delay 7

Execution states: completed 5

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 4 | 45 | 0.49% | 95.3% | 2.2% | 43.27 | 0.34 | 67.0 | 37.45 / 37.45 | -0.01% | -0.01% | -0.01% |
| ordinary | VOL | 4 | 45 | 0.64% | 125.2% | 2.9% | 43.28 | 0.45 | 88.1 | 49.25 / 49.25 | -0.02% | -0.02% | -0.02% |
| ordinary | B2 | 4 | 45 | 1.36% | 265.2% | 6.5% | 40.75 | 0.92 | 196.5 | 109.90 / 141.44 | -0.03% | -0.03% | -0.03% |
| stressed | FIXED | 4 | 45 | 0.45% | 89.3% | 2.8% | 31.61 | 0.34 | 67.1 | 68.11 / 68.11 | -0.04% | -0.04% | -0.04% |
| stressed | VOL | 4 | 45 | 0.60% | 117.4% | 3.7% | 31.60 | 0.45 | 88.2 | 89.57 / 89.57 | -0.06% | -0.06% | -0.06% |
| stressed | B2 | 4 | 45 | 1.27% | 247.5% | 7.7% | 32.27 | 0.92 | 196.6 | 199.71 / 256.98 | -0.09% | -0.09% | -0.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 4 | 0 | -2.524 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 139.95% | 0.00178 | 0.612 | 0.00216 |
| stressed | 4 | 0 | 0.671 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 130.15% | 0.00165 | 0.567 | 0.00201 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-04T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 1.9 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
