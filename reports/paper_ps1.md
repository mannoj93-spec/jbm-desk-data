# Paper sizing experiment PS1

Generated 2026-11-15T12:28:44.401Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-15T12:28:38.512Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1248 physical; 1248 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 43.52 days; 262 scheduled decisions; coverage 79.4%; execution delay after the 4H close: median 20.4 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 207 closed intervals over 1044.1 h; extended intervals 12.

Outcomes: executed 208; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 208

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 207 | 1044 | -7.83% | -68.4% | 11.9% | -5.73 | 0.33 | 3.3 | 42.58 / 42.58 | -9.09% | -1.36% | -0.80% |
| ordinary | VOL | 207 | 1044 | -9.75% | -86.1% | 15.7% | -5.49 | 0.43 | 8.6 | 110.14 / 110.14 | -11.11% | -2.00% | -1.04% |
| ordinary | B2 | 207 | 1044 | -11.45% | -102.0% | 14.9% | -6.84 | 0.55 | 117.5 | 1543.56 / 1543.56 | -13.36% | -2.24% | -1.13% |
| stressed | FIXED | 207 | 1044 | -7.86% | -68.7% | 11.9% | -5.75 | 0.33 | 3.3 | 77.42 / 77.42 | -9.10% | -1.36% | -0.80% |
| stressed | VOL | 207 | 1044 | -9.84% | -86.9% | 15.7% | -5.54 | 0.43 | 8.6 | 200.14 / 200.14 | -11.15% | -2.00% | -1.04% |
| stressed | B2 | 207 | 1044 | -12.55% | -112.5% | 14.9% | -7.56 | 0.55 | 117.6 | 2755.16 / 2755.16 | -14.34% | -2.25% | -1.13% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 207 | 4 | -1.353 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -15.90% | -0.00009 | -0.064 | -0.00019 |
| stressed | 207 | 4 | -2.021 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -25.67% | -0.00015 | -0.103 | -0.00025 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-15T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 43.5 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
