# Paper sizing experiment PS1

Generated 2026-10-21T09:21:28.865Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-21T08:19:02.910Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 618 physical; 618 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 18.39 days; 111 scheduled decisions; coverage 92.8%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 102 closed intervals over 440.0 h; extended intervals 3.

Outcomes: executed 103; missed: stale: processed after close + max_delay 8

Execution states: completed 103

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 102 | 440 | -0.62% | -12.4% | 10.4% | -1.19 | 0.34 | 6.8 | 37.45 / 37.45 | -2.23% | -0.84% | -0.58% |
| ordinary | VOL | 102 | 440 | -0.97% | -19.5% | 14.4% | -1.35 | 0.46 | 12.1 | 66.21 / 66.21 | -3.05% | -1.25% | -0.82% |
| ordinary | B2 | 102 | 440 | -0.32% | -6.4% | 13.8% | -0.47 | 0.55 | 151.3 | 858.07 / 858.07 | -3.34% | -0.96% | -0.75% |
| stressed | FIXED | 102 | 440 | -0.65% | -13.0% | 10.4% | -1.25 | 0.34 | 6.8 | 68.11 / 68.11 | -2.23% | -0.84% | -0.58% |
| stressed | VOL | 102 | 440 | -1.03% | -20.5% | 14.4% | -1.43 | 0.46 | 12.1 | 120.36 / 120.36 | -3.06% | -1.25% | -0.82% |
| stressed | B2 | 102 | 440 | -1.00% | -20.1% | 13.8% | -1.45 | 0.55 | 151.3 | 1534.66 / 1534.66 | -3.82% | -0.96% | -0.75% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 102 | 2 | 0.888 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 13.01% | 0.00006 | 0.055 | 0.00003 |
| stressed | 102 | 2 | -0.023 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 0.49% | 0.00000 | 0.002 | -0.00003 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-21T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 18.4 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
