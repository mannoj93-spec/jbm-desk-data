# Paper sizing experiment PS1

Generated 2026-10-08T08:20:19.040Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-08T08:19:17.882Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 150 physical; 150 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 5.35 days; 33 scheduled decisions; coverage 75.8%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 24 closed intervals over 128.0 h; extended intervals 3.

Outcomes: executed 25; missed: stale: processed after close + max_delay 8

Execution states: completed 25

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 24 | 128 | -0.64% | -43.8% | 9.4% | -4.67 | 0.34 | 23.3 | 37.45 / 37.45 | -1.50% | -0.60% | -0.60% |
| ordinary | VOL | 24 | 128 | -0.84% | -57.6% | 12.3% | -4.68 | 0.45 | 30.6 | 49.25 / 49.25 | -1.97% | -0.79% | -0.79% |
| ordinary | B2 | 24 | 128 | -0.41% | -28.0% | 14.5% | -1.94 | 0.62 | 163.2 | 264.81 / 264.81 | -2.37% | -0.96% | -0.96% |
| stressed | FIXED | 24 | 128 | -0.67% | -45.9% | 9.4% | -4.90 | 0.34 | 23.3 | 68.11 / 68.11 | -1.50% | -0.60% | -0.60% |
| stressed | VOL | 24 | 128 | -0.88% | -60.4% | 12.3% | -4.91 | 0.45 | 30.6 | 89.57 / 89.57 | -1.97% | -0.79% | -0.79% |
| stressed | B2 | 24 | 128 | -0.62% | -42.7% | 14.4% | -2.96 | 0.62 | 163.3 | 480.45 / 480.45 | -2.46% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 24 | 0 | 2.747 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 29.61% | 0.00018 | 0.131 | 0.00010 |
| stressed | 24 | 0 | 1.949 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 17.68% | 0.00011 | 0.079 | 0.00002 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-08T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 5.3 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
