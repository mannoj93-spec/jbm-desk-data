# Paper sizing experiment PS1

Generated 2026-10-17T12:18:05.247Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-17T12:18:03.921Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 480 physical; 480 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 14.51 days; 88 scheduled decisions; coverage 90.9%; execution delay after the 4H close: median 18.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 79 closed intervals over 348.0 h; extended intervals 3.

Outcomes: executed 80; missed: stale: processed after close + max_delay 8

Execution states: completed 80

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 79 | 348 | -1.24% | -31.4% | 10.5% | -2.98 | 0.34 | 8.6 | 37.45 / 37.45 | -2.16% | -0.84% | -0.70% |
| ordinary | VOL | 79 | 348 | -1.75% | -44.5% | 14.9% | -2.99 | 0.47 | 14.0 | 60.71 / 60.71 | -2.96% | -1.25% | -1.00% |
| ordinary | B2 | 79 | 348 | -1.08% | -27.3% | 13.5% | -2.03 | 0.56 | 152.6 | 667.40 / 677.04 | -3.04% | -0.96% | -0.84% |
| stressed | FIXED | 79 | 348 | -1.27% | -32.2% | 10.5% | -3.05 | 0.34 | 8.6 | 68.11 / 68.11 | -2.16% | -0.84% | -0.70% |
| stressed | VOL | 79 | 348 | -1.80% | -45.7% | 14.9% | -3.07 | 0.47 | 14.0 | 110.37 / 110.37 | -2.97% | -1.25% | -1.00% |
| stressed | B2 | 79 | 348 | -1.62% | -41.1% | 13.4% | -3.05 | 0.56 | 152.7 | 1209.30 / 1226.74 | -3.23% | -0.96% | -0.84% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 79 | 1 | 0.957 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 17.14% | 0.00009 | 0.069 | 0.00002 |
| stressed | 79 | 1 | 0.015 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 4.67% | 0.00002 | 0.019 | -0.00004 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-17T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 14.5 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
