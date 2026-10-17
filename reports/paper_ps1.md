# Paper sizing experiment PS1

Generated 2026-10-17T09:11:16.869Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-17T08:18:25.293Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 474 physical; 474 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 14.38 days; 87 scheduled decisions; coverage 90.8%; execution delay after the 4H close: median 18.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 78 closed intervals over 344.0 h; extended intervals 3.

Outcomes: executed 79; missed: stale: processed after close + max_delay 8

Execution states: completed 79

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 78 | 344 | -1.16% | -29.8% | 10.6% | -2.81 | 0.34 | 8.7 | 37.45 / 37.45 | -2.16% | -0.84% | -0.70% |
| ordinary | VOL | 78 | 344 | -1.65% | -42.4% | 15.0% | -2.83 | 0.47 | 14.2 | 60.71 / 60.71 | -2.96% | -1.25% | -1.00% |
| ordinary | B2 | 78 | 344 | -0.88% | -22.6% | 13.5% | -1.67 | 0.56 | 152.5 | 659.33 / 667.40 | -3.04% | -0.96% | -0.84% |
| stressed | FIXED | 78 | 344 | -1.19% | -30.6% | 10.6% | -2.88 | 0.34 | 8.7 | 68.11 / 68.11 | -2.16% | -0.84% | -0.70% |
| stressed | VOL | 78 | 344 | -1.70% | -43.7% | 15.0% | -2.91 | 0.47 | 14.2 | 110.37 / 110.37 | -2.97% | -1.25% | -1.00% |
| stressed | B2 | 78 | 344 | -1.42% | -36.3% | 13.5% | -2.69 | 0.56 | 152.6 | 1194.75 / 1209.30 | -3.20% | -0.96% | -0.84% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 78 | 1 | 1.156 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 19.77% | 0.00010 | 0.079 | 0.00004 |
| stressed | 78 | 1 | 0.220 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 7.32% | 0.00004 | 0.030 | -0.00003 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-17T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 14.4 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
