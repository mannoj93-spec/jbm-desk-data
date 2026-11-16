# Paper sizing experiment PS1

Generated 2026-11-16T18:09:57.079Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-16T16:25:41.329Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1290 physical; 1290 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 44.76 days; 269 scheduled decisions; coverage 79.9%; execution delay after the 4H close: median 20.6 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 214 closed intervals over 1072.1 h; extended intervals 12.

Outcomes: executed 215; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 215

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 214 | 1072 | -8.16% | -69.5% | 12.0% | -5.80 | 0.33 | 3.2 | 42.58 / 42.58 | -9.14% | -1.36% | -0.80% |
| ordinary | VOL | 214 | 1072 | -10.00% | -86.1% | 15.5% | -5.54 | 0.42 | 8.4 | 110.14 / 110.14 | -11.11% | -2.00% | -1.04% |
| ordinary | B2 | 214 | 1072 | -11.60% | -100.8% | 14.8% | -6.82 | 0.55 | 115.3 | 1550.06 / 1555.10 | -13.42% | -2.24% | -1.13% |
| stressed | FIXED | 214 | 1072 | -8.19% | -69.8% | 12.0% | -5.82 | 0.33 | 3.2 | 77.42 / 77.42 | -9.15% | -1.36% | -0.80% |
| stressed | VOL | 214 | 1072 | -10.09% | -86.9% | 15.6% | -5.59 | 0.42 | 8.4 | 200.14 / 200.14 | -11.15% | -2.00% | -1.04% |
| stressed | B2 | 214 | 1072 | -12.71% | -111.1% | 14.8% | -7.53 | 0.55 | 115.4 | 2766.82 / 2775.88 | -14.41% | -2.25% | -1.13% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 214 | 5 | -1.283 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -14.65% | -0.00008 | -0.060 | -0.00018 |
| stressed | 214 | 5 | -1.943 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -24.23% | -0.00014 | -0.098 | -0.00024 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-16T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 44.8 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
