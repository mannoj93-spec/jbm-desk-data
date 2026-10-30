# Paper sizing experiment PS1

Generated 2026-10-30T14:57:22.518Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-30T12:21:47.083Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 906 physical; 906 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 27.62 days; 166 scheduled decisions; coverage 91.0%; execution delay after the 4H close: median 19.2 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 150 closed intervals over 660.0 h; extended intervals 6.

Outcomes: executed 151; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 151

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 150 | 660 | -2.89% | -38.9% | 11.6% | -3.36 | 0.33 | 4.6 | 37.45 / 37.45 | -3.74% | -1.36% | -0.71% |
| ordinary | VOL | 150 | 660 | -4.04% | -54.7% | 16.3% | -3.35 | 0.46 | 10.1 | 82.98 / 82.98 | -5.23% | -2.00% | -1.01% |
| ordinary | B2 | 150 | 660 | -3.60% | -48.7% | 14.8% | -3.30 | 0.53 | 134.2 | 1127.69 / 1127.69 | -5.34% | -1.31% | -0.89% |
| stressed | FIXED | 150 | 660 | -2.92% | -39.3% | 11.6% | -3.39 | 0.33 | 4.6 | 68.11 / 68.11 | -3.74% | -1.36% | -0.71% |
| stressed | VOL | 150 | 660 | -4.10% | -55.6% | 16.3% | -3.41 | 0.46 | 10.2 | 150.85 / 150.85 | -5.25% | -2.00% | -1.01% |
| stressed | B2 | 150 | 660 | -4.47% | -60.7% | 14.7% | -4.12 | 0.53 | 134.3 | 2020.94 / 2020.94 | -6.08% | -1.31% | -0.89% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 150 | 3 | 0.058 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 6.06% | 0.00003 | 0.025 | -0.00005 |
| stressed | 150 | 3 | -0.713 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -5.09% | -0.00003 | -0.021 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-30T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 27.6 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
