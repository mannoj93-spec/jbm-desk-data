# Paper sizing experiment PS1

Generated 2026-10-19T00:33:36.931Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-19T00:18:56.423Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 534 physical; 534 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 16.02 days; 97 scheduled decisions; coverage 91.8%; execution delay after the 4H close: median 18.5 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 88 closed intervals over 384.0 h; extended intervals 3.

Outcomes: executed 89; missed: stale: processed after close + max_delay 8

Execution states: completed 89

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 88 | 384 | -1.06% | -24.2% | 10.6% | -2.29 | 0.34 | 7.8 | 37.45 / 37.45 | -2.23% | -0.84% | -0.63% |
| ordinary | VOL | 88 | 384 | -1.51% | -34.7% | 14.9% | -2.33 | 0.46 | 12.7 | 60.71 / 60.71 | -3.05% | -1.25% | -0.89% |
| ordinary | B2 | 88 | 384 | -0.86% | -19.8% | 14.1% | -1.41 | 0.57 | 157.7 | 783.41 / 802.65 | -3.34% | -0.96% | -0.80% |
| stressed | FIXED | 88 | 384 | -1.09% | -24.9% | 10.6% | -2.36 | 0.34 | 7.8 | 68.11 / 68.11 | -2.23% | -0.84% | -0.63% |
| stressed | VOL | 88 | 384 | -1.56% | -35.8% | 14.9% | -2.41 | 0.46 | 12.7 | 110.37 / 110.37 | -3.06% | -1.25% | -0.89% |
| stressed | B2 | 88 | 384 | -1.48% | -34.0% | 14.0% | -2.42 | 0.57 | 157.7 | 1399.80 / 1434.57 | -3.82% | -0.96% | -0.80% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 88 | 2 | 0.926 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 14.88% | 0.00007 | 0.060 | 0.00002 |
| stressed | 88 | 2 | -0.013 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 1.83% | 0.00001 | 0.007 | -0.00005 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-19T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 16.0 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
