# Paper sizing experiment PS1

Generated 2026-11-21T16:22:43.083Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-21T16:22:38.113Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1458 physical; 1458 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 49.68 days; 299 scheduled decisions; coverage 81.3%; execution delay after the 4H close: median 21.3 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 242 closed intervals over 1192.0 h; extended intervals 14.

Outcomes: executed 243; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 42

Execution states: completed 243

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 242 | 1192 | -10.44% | -81.0% | 14.2% | -5.70 | 0.33 | 2.9 | 42.58 / 42.58 | -13.01% | -1.73% | -0.95% |
| ordinary | VOL | 242 | 1192 | -11.73% | -91.7% | 16.1% | -5.71 | 0.41 | 7.6 | 110.14 / 110.14 | -14.01% | -2.00% | -1.06% |
| ordinary | B2 | 242 | 1192 | -13.82% | -109.3% | 15.8% | -6.93 | 0.52 | 108.2 | 1598.00 / 1598.00 | -16.76% | -2.24% | -1.17% |
| stressed | FIXED | 242 | 1192 | -10.48% | -81.3% | 14.2% | -5.72 | 0.33 | 2.9 | 77.42 / 77.42 | -13.02% | -1.73% | -0.95% |
| stressed | VOL | 242 | 1192 | -11.81% | -92.4% | 16.1% | -5.75 | 0.41 | 7.6 | 200.14 / 200.14 | -14.06% | -2.00% | -1.06% |
| stressed | B2 | 242 | 1192 | -14.94% | -118.9% | 15.8% | -7.54 | 0.52 | 108.3 | 2852.68 / 2852.68 | -17.75% | -2.25% | -1.18% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 242 | 5 | -1.216 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -17.61% | -0.00010 | -0.073 | -0.00016 |
| stressed | 242 | 5 | -1.789 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -26.55% | -0.00015 | -0.110 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-21T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 49.7 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
