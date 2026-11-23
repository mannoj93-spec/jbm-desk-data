# Paper sizing experiment PS1

Generated 2026-11-23T16:26:29.232Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-23T16:26:23.395Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1530 physical; 1530 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 51.69 days; 311 scheduled decisions; coverage 82.0%; execution delay after the 4H close: median 21.4 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 254 closed intervals over 1240.1 h; extended intervals 14.

Outcomes: executed 255; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 42

Execution states: completed 255

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 254 | 1240 | -9.13% | -67.6% | 14.3% | -4.71 | 0.33 | 2.8 | 42.58 / 42.58 | -13.01% | -1.73% | -0.95% |
| ordinary | VOL | 254 | 1240 | -10.74% | -80.2% | 15.9% | -5.04 | 0.40 | 7.4 | 110.14 / 110.14 | -14.01% | -2.00% | -1.06% |
| ordinary | B2 | 254 | 1240 | -12.84% | -97.0% | 15.7% | -6.19 | 0.51 | 104.5 | 1598.00 / 1605.79 | -16.76% | -2.24% | -1.17% |
| stressed | FIXED | 254 | 1240 | -9.16% | -67.9% | 14.4% | -4.73 | 0.33 | 2.8 | 77.42 / 77.42 | -13.02% | -1.73% | -0.95% |
| stressed | VOL | 254 | 1240 | -10.82% | -80.9% | 15.9% | -5.08 | 0.40 | 7.4 | 200.14 / 200.14 | -14.06% | -2.00% | -1.06% |
| stressed | B2 | 254 | 1240 | -13.97% | -106.3% | 15.7% | -6.78 | 0.51 | 104.6 | 2852.68 / 2866.66 | -17.75% | -2.25% | -1.18% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 254 | 6 | -1.154 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -16.81% | -0.00009 | -0.071 | -0.00016 |
| stressed | 254 | 6 | -1.706 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -25.41% | -0.00014 | -0.107 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-23T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 51.7 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
