# Paper sizing experiment PS1

Generated 2026-10-31T04:39:05.735Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-31T04:22:12.788Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 930 physical; 930 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 28.19 days; 170 scheduled decisions; coverage 91.2%; execution delay after the 4H close: median 19.3 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 154 closed intervals over 676.0 h; extended intervals 6.

Outcomes: executed 155; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 155

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 154 | 676 | -2.94% | -38.7% | 11.5% | -3.37 | 0.33 | 4.5 | 37.45 / 37.45 | -3.76% | -1.36% | -0.71% |
| ordinary | VOL | 154 | 676 | -4.10% | -54.3% | 16.1% | -3.36 | 0.46 | 9.9 | 82.98 / 82.98 | -5.23% | -2.00% | -1.01% |
| ordinary | B2 | 154 | 676 | -3.68% | -48.6% | 14.6% | -3.33 | 0.52 | 133.5 | 1147.76 / 1155.80 | -5.47% | -1.31% | -0.89% |
| stressed | FIXED | 154 | 676 | -2.97% | -39.1% | 11.5% | -3.40 | 0.33 | 4.5 | 68.11 / 68.11 | -3.76% | -1.36% | -0.71% |
| stressed | VOL | 154 | 676 | -4.17% | -55.2% | 16.2% | -3.42 | 0.46 | 9.9 | 150.85 / 150.85 | -5.25% | -2.00% | -1.01% |
| stressed | B2 | 154 | 676 | -4.57% | -60.6% | 14.6% | -4.16 | 0.52 | 133.6 | 2057.12 / 2071.59 | -6.22% | -1.31% | -0.89% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 154 | 3 | 0.034 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 5.70% | 0.00003 | 0.023 | -0.00005 |
| stressed | 154 | 3 | -0.742 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -5.40% | -0.00003 | -0.022 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-31T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 28.2 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
