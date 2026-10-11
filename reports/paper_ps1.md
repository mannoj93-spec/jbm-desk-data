# Paper sizing experiment PS1

Generated 2026-10-11T13:05:25.190Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-11T12:19:39.063Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 264 physical; 264 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 8.55 days; 52 scheduled decisions; coverage 84.6%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 43 closed intervals over 204.0 h; extended intervals 3.

Outcomes: executed 44; missed: stale: processed after close + max_delay 8

Execution states: completed 44

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 43 | 204 | -0.59% | -25.6% | 8.7% | -2.95 | 0.34 | 14.7 | 37.45 / 37.45 | -2.01% | -0.60% | -0.51% |
| ordinary | VOL | 43 | 204 | -0.77% | -33.2% | 11.5% | -2.89 | 0.46 | 21.6 | 55.22 / 55.22 | -2.64% | -0.79% | -0.67% |
| ordinary | B2 | 43 | 204 | -0.15% | -6.4% | 12.9% | -0.50 | 0.64 | 163.9 | 421.13 / 431.27 | -3.04% | -0.96% | -0.76% |
| stressed | FIXED | 43 | 204 | -0.62% | -26.9% | 8.7% | -3.10 | 0.34 | 14.7 | 68.11 / 68.11 | -2.01% | -0.60% | -0.51% |
| stressed | VOL | 43 | 204 | -0.82% | -35.2% | 11.5% | -3.06 | 0.46 | 21.7 | 100.40 / 100.40 | -2.64% | -0.79% | -0.67% |
| stressed | B2 | 43 | 204 | -0.49% | -21.2% | 12.8% | -1.66 | 0.64 | 164.0 | 763.88 / 782.26 | -3.13% | -0.96% | -0.76% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 43 | 1 | 2.392 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 26.78% | 0.00015 | 0.138 | 0.00010 |
| stressed | 43 | 1 | 1.403 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 13.98% | 0.00008 | 0.072 | 0.00003 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-11T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 8.5 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
