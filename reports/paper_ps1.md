# Paper sizing experiment PS1

Generated 2026-10-18T13:19:01.478Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-18T12:18:40.767Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 516 physical; 516 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 15.55 days; 94 scheduled decisions; coverage 91.5%; execution delay after the 4H close: median 18.5 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 85 closed intervals over 372.0 h; extended intervals 3.

Outcomes: executed 86; missed: stale: processed after close + max_delay 8

Execution states: completed 86

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 85 | 372 | -1.05% | -24.8% | 10.3% | -2.41 | 0.34 | 8.1 | 37.45 / 37.45 | -2.16% | -0.84% | -0.63% |
| ordinary | VOL | 85 | 372 | -1.50% | -35.5% | 14.5% | -2.45 | 0.47 | 13.1 | 60.71 / 60.71 | -2.96% | -1.25% | -0.89% |
| ordinary | B2 | 85 | 372 | -0.81% | -19.2% | 13.3% | -1.44 | 0.57 | 155.8 | 728.08 / 764.27 | -3.05% | -0.96% | -0.77% |
| stressed | FIXED | 85 | 372 | -1.08% | -25.5% | 10.3% | -2.48 | 0.34 | 8.1 | 68.11 / 68.11 | -2.16% | -0.84% | -0.63% |
| stressed | VOL | 85 | 372 | -1.54% | -36.7% | 14.5% | -2.53 | 0.47 | 13.1 | 110.37 / 110.37 | -2.97% | -1.25% | -0.89% |
| stressed | B2 | 85 | 372 | -1.40% | -33.2% | 13.3% | -2.50 | 0.57 | 155.9 | 1318.97 / 1365.22 | -3.47% | -0.96% | -0.77% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 85 | 2 | 1.006 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 16.29% | 0.00008 | 0.066 | 0.00003 |
| stressed | 85 | 2 | 0.025 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 3.43% | 0.00002 | 0.014 | -0.00004 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-18T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 15.6 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
