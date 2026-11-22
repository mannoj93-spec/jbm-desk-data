# Paper sizing experiment PS1

Generated 2026-11-22T08:25:52.402Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-22T08:25:47.378Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1482 physical; 1482 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 50.35 days; 303 scheduled decisions; coverage 81.5%; execution delay after the 4H close: median 21.4 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 246 closed intervals over 1208.1 h; extended intervals 14.

Outcomes: executed 247; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 42

Execution states: completed 247

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 246 | 1208 | -10.53% | -80.6% | 14.3% | -5.66 | 0.33 | 2.9 | 42.58 / 42.58 | -13.01% | -1.73% | -0.95% |
| ordinary | VOL | 246 | 1208 | -11.79% | -91.0% | 16.0% | -5.69 | 0.40 | 7.5 | 110.14 / 110.14 | -14.01% | -2.00% | -1.06% |
| ordinary | B2 | 246 | 1208 | -13.88% | -108.4% | 15.7% | -6.89 | 0.51 | 106.9 | 1598.00 / 1598.00 | -16.76% | -2.24% | -1.17% |
| stressed | FIXED | 246 | 1208 | -10.56% | -80.9% | 14.3% | -5.68 | 0.33 | 2.9 | 77.42 / 77.42 | -13.02% | -1.73% | -0.95% |
| stressed | VOL | 246 | 1208 | -11.88% | -91.7% | 16.0% | -5.73 | 0.40 | 7.6 | 200.14 / 200.14 | -14.06% | -2.00% | -1.06% |
| stressed | B2 | 246 | 1208 | -15.00% | -117.9% | 15.7% | -7.50 | 0.51 | 107.1 | 2852.68 / 2852.68 | -17.75% | -2.25% | -1.18% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 246 | 5 | -1.203 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -17.38% | -0.00010 | -0.073 | -0.00016 |
| stressed | 246 | 5 | -1.770 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -26.20% | -0.00015 | -0.109 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-22T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 50.4 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
