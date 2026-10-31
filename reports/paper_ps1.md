# Paper sizing experiment PS1

Generated 2026-10-31T00:20:38.480Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-31T00:20:33.647Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 924 physical; 924 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 28.01 days; 169 scheduled decisions; coverage 91.1%; execution delay after the 4H close: median 19.2 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 153 closed intervals over 672.0 h; extended intervals 6.

Outcomes: executed 154; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 154

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 153 | 672 | -2.92% | -38.7% | 11.5% | -3.36 | 0.33 | 4.5 | 37.45 / 37.45 | -3.76% | -1.36% | -0.71% |
| ordinary | VOL | 153 | 672 | -4.08% | -54.3% | 16.2% | -3.35 | 0.46 | 10.0 | 82.98 / 82.98 | -5.23% | -2.00% | -1.01% |
| ordinary | B2 | 153 | 672 | -3.63% | -48.3% | 14.7% | -3.29 | 0.52 | 131.9 | 1127.69 / 1147.76 | -5.47% | -1.31% | -0.89% |
| stressed | FIXED | 153 | 672 | -2.95% | -39.1% | 11.5% | -3.39 | 0.33 | 4.5 | 68.11 / 68.11 | -3.76% | -1.36% | -0.71% |
| stressed | VOL | 153 | 672 | -4.15% | -55.2% | 16.2% | -3.41 | 0.46 | 10.0 | 150.85 / 150.85 | -5.25% | -2.00% | -1.01% |
| stressed | B2 | 153 | 672 | -4.51% | -60.1% | 14.6% | -4.11 | 0.52 | 131.9 | 2020.94 / 2057.12 | -6.22% | -1.31% | -0.89% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 153 | 3 | 0.059 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 6.07% | 0.00003 | 0.025 | -0.00005 |
| stressed | 153 | 3 | -0.704 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -4.88% | -0.00002 | -0.020 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-31T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 28.0 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
