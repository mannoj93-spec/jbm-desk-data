# Paper sizing experiment PS1

Generated 2026-10-30T20:15:48.397Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-30T20:15:45.758Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 918 physical; 918 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 27.84 days; 168 scheduled decisions; coverage 91.1%; execution delay after the 4H close: median 19.2 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 152 closed intervals over 667.9 h; extended intervals 6.

Outcomes: executed 153; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 153

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 152 | 668 | -3.07% | -40.9% | 11.5% | -3.55 | 0.33 | 4.5 | 37.45 / 37.45 | -3.76% | -1.36% | -0.71% |
| ordinary | VOL | 152 | 668 | -4.27% | -57.3% | 16.2% | -3.53 | 0.46 | 10.0 | 82.98 / 82.98 | -5.23% | -2.00% | -1.01% |
| ordinary | B2 | 152 | 668 | -3.79% | -50.6% | 14.7% | -3.45 | 0.52 | 132.6 | 1127.69 / 1127.69 | -5.47% | -1.31% | -0.89% |
| stressed | FIXED | 152 | 668 | -3.10% | -41.3% | 11.5% | -3.58 | 0.33 | 4.5 | 68.11 / 68.11 | -3.76% | -1.36% | -0.71% |
| stressed | VOL | 152 | 668 | -4.34% | -58.2% | 16.2% | -3.58 | 0.46 | 10.0 | 150.85 / 150.85 | -5.25% | -2.00% | -1.01% |
| stressed | B2 | 152 | 668 | -4.66% | -62.5% | 14.7% | -4.27 | 0.52 | 132.7 | 2020.94 / 2020.94 | -6.22% | -1.31% | -0.89% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 152 | 3 | 0.080 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 6.64% | 0.00003 | 0.027 | -0.00005 |
| stressed | 152 | 3 | -0.687 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -4.38% | -0.00002 | -0.018 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-30T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 27.8 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
