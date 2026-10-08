# Paper sizing experiment PS1

Generated 2026-10-08T12:18:07.069Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-08T12:18:06.027Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 156 physical; 156 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 5.51 days; 34 scheduled decisions; coverage 76.5%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 25 closed intervals over 132.0 h; extended intervals 3.

Outcomes: executed 26; missed: stale: processed after close + max_delay 8

Execution states: completed 26

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 25 | 132 | -0.90% | -59.7% | 9.4% | -6.33 | 0.34 | 22.6 | 37.45 / 37.45 | -1.60% | -0.60% | -0.60% |
| ordinary | VOL | 25 | 132 | -1.18% | -78.7% | 12.4% | -6.34 | 0.45 | 29.7 | 49.25 / 49.25 | -2.10% | -0.79% | -0.79% |
| ordinary | B2 | 25 | 132 | -0.75% | -50.3% | 14.5% | -3.46 | 0.61 | 158.3 | 264.81 / 264.81 | -2.50% | -0.96% | -0.96% |
| stressed | FIXED | 25 | 132 | -0.93% | -61.8% | 9.4% | -6.54 | 0.34 | 22.6 | 68.11 / 68.11 | -1.60% | -0.60% | -0.60% |
| stressed | VOL | 25 | 132 | -1.22% | -81.4% | 12.4% | -6.56 | 0.45 | 29.7 | 89.57 / 89.57 | -2.10% | -0.79% | -0.79% |
| stressed | B2 | 25 | 132 | -0.97% | -64.5% | 14.5% | -4.46 | 0.61 | 158.4 | 480.45 / 480.45 | -2.59% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 25 | 0 | 2.876 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 28.43% | 0.00017 | 0.128 | 0.00006 |
| stressed | 25 | 0 | 2.099 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 16.86% | 0.00010 | 0.076 | -0.00002 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-08T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 5.5 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
