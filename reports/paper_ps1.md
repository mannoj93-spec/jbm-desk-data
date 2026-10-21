# Paper sizing experiment PS1

Generated 2026-10-21T21:16:44.769Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-21T20:19:11.538Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 630 physical; 630 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 18.89 days; 114 scheduled decisions; coverage 92.1%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 104 closed intervals over 452.0 h; extended intervals 4.

Outcomes: executed 105; missed: no run 1; missed: stale: processed after close + max_delay 8

Execution states: completed 105

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 104 | 452 | -0.05% | -0.9% | 10.4% | -0.09 | 0.34 | 6.6 | 37.45 / 37.45 | -2.23% | -0.84% | -0.58% |
| ordinary | VOL | 104 | 452 | -0.30% | -5.8% | 14.4% | -0.40 | 0.45 | 11.8 | 66.21 / 66.21 | -3.05% | -1.25% | -0.82% |
| ordinary | B2 | 104 | 452 | 0.44% | 8.6% | 13.9% | 0.62 | 0.55 | 147.3 | 858.07 / 858.07 | -3.34% | -0.96% | -0.75% |
| stressed | FIXED | 104 | 452 | -0.08% | -1.5% | 10.4% | -0.14 | 0.34 | 6.6 | 68.11 / 68.11 | -2.23% | -0.84% | -0.58% |
| stressed | VOL | 104 | 452 | -0.35% | -6.9% | 14.4% | -0.48 | 0.45 | 11.8 | 120.36 / 120.36 | -3.06% | -1.25% | -0.82% |
| stressed | B2 | 104 | 452 | -0.24% | -4.7% | 13.8% | -0.34 | 0.55 | 147.3 | 1534.66 / 1534.66 | -3.82% | -0.96% | -0.75% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 104 | 2 | 1.021 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 14.34% | 0.00007 | 0.062 | 0.00005 |
| stressed | 104 | 2 | 0.138 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 2.15% | 0.00001 | 0.009 | -0.00002 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-21T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 18.9 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
