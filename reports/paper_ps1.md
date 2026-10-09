# Paper sizing experiment PS1

Generated 2026-10-09T05:04:24.255Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-09T04:20:44.896Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 180 physical; 180 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 6.21 days; 38 scheduled decisions; coverage 79.0%; execution delay after the 4H close: median 18.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 29 closed intervals over 148.0 h; extended intervals 3.

Outcomes: executed 30; missed: stale: processed after close + max_delay 8

Execution states: completed 30

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 29 | 148 | -0.85% | -50.8% | 10.0% | -5.09 | 0.34 | 20.2 | 37.45 / 37.45 | -2.01% | -0.60% | -0.60% |
| ordinary | VOL | 29 | 148 | -1.12% | -66.9% | 13.1% | -5.10 | 0.45 | 26.5 | 49.25 / 49.25 | -2.64% | -0.79% | -0.79% |
| ordinary | B2 | 29 | 148 | -0.74% | -43.8% | 14.8% | -2.95 | 0.59 | 155.6 | 291.07 / 300.07 | -3.04% | -0.96% | -0.96% |
| stressed | FIXED | 29 | 148 | -0.89% | -52.7% | 10.0% | -5.28 | 0.34 | 20.2 | 68.11 / 68.11 | -2.01% | -0.60% | -0.60% |
| stressed | VOL | 29 | 148 | -1.16% | -69.3% | 13.1% | -5.28 | 0.45 | 26.5 | 89.57 / 89.57 | -2.64% | -0.79% | -0.79% |
| stressed | B2 | 29 | 148 | -0.97% | -57.9% | 14.8% | -3.91 | 0.59 | 155.6 | 528.09 / 544.42 | -3.13% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 29 | 0 | 2.143 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 23.08% | 0.00013 | 0.107 | 0.00004 |
| stressed | 29 | 0 | 1.364 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 11.48% | 0.00007 | 0.054 | -0.00003 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-09T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 6.2 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
