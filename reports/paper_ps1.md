# Paper sizing experiment PS1

Generated 2026-10-20T05:19:33.408Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-20T04:22:10.988Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 576 physical; 576 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 17.22 days; 104 scheduled decisions; coverage 92.3%; execution delay after the 4H close: median 18.7 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 95 closed intervals over 412.0 h; extended intervals 3.

Outcomes: executed 96; missed: stale: processed after close + max_delay 8

Execution states: completed 96

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 95 | 412 | -0.97% | -20.6% | 10.4% | -1.98 | 0.34 | 7.3 | 37.45 / 37.45 | -2.23% | -0.84% | -0.63% |
| ordinary | VOL | 95 | 412 | -1.38% | -29.5% | 14.6% | -2.03 | 0.46 | 12.9 | 66.21 / 66.21 | -3.05% | -1.25% | -0.89% |
| ordinary | B2 | 95 | 412 | -0.80% | -17.1% | 13.8% | -1.24 | 0.56 | 153.0 | 814.19 / 814.19 | -3.34% | -0.96% | -0.80% |
| stressed | FIXED | 95 | 412 | -1.00% | -21.3% | 10.4% | -2.04 | 0.34 | 7.3 | 68.11 / 68.11 | -2.23% | -0.84% | -0.63% |
| stressed | VOL | 95 | 412 | -1.43% | -30.7% | 14.6% | -2.11 | 0.46 | 12.9 | 120.36 / 120.36 | -3.06% | -1.25% | -0.89% |
| stressed | B2 | 95 | 412 | -1.44% | -30.9% | 13.8% | -2.24 | 0.56 | 153.0 | 1455.40 / 1455.40 | -3.82% | -0.96% | -0.80% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 95 | 2 | 0.791 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 12.41% | 0.00006 | 0.052 | 0.00002 |
| stressed | 95 | 2 | -0.131 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | -0.19% | -0.00000 | -0.001 | -0.00005 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-20T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 17.2 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
