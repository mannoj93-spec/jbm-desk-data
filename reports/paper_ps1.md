# Paper sizing experiment PS1

Generated 2026-10-06T20:23:38.015Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-06T20:22:35.476Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 96 physical; 96 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 3.85 days; 24 scheduled decisions; coverage 66.7%; execution delay after the 4H close: median 18.1 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 15 closed intervals over 92.0 h; extended intervals 3.

Outcomes: executed 16; missed: stale: processed after close + max_delay 8

Execution states: completed 16

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 15 | 92 | 0.39% | 37.5% | 8.2% | 4.56 | 0.34 | 32.3 | 37.45 / 37.45 | -0.50% | -0.39% | -0.39% |
| ordinary | VOL | 15 | 92 | 0.52% | 49.3% | 10.8% | 4.56 | 0.45 | 42.4 | 49.25 / 49.25 | -0.66% | -0.51% | -0.51% |
| ordinary | B2 | 15 | 92 | 1.23% | 116.2% | 12.2% | 9.49 | 0.68 | 173.9 | 203.18 / 215.83 | -0.67% | -0.51% | -0.51% |
| stressed | FIXED | 15 | 92 | 0.36% | 34.6% | 8.3% | 4.19 | 0.34 | 32.3 | 68.11 / 68.11 | -0.50% | -0.39% | -0.39% |
| stressed | VOL | 15 | 92 | 0.48% | 45.5% | 10.8% | 4.19 | 0.45 | 42.4 | 89.57 / 89.57 | -0.66% | -0.51% | -0.51% |
| stressed | B2 | 15 | 92 | 1.06% | 100.5% | 12.3% | 8.18 | 0.68 | 174.0 | 369.09 / 392.06 | -0.70% | -0.51% | -0.51% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 15 | 0 | 4.927 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 66.92% | 0.00047 | 0.287 | 0.00055 |
| stressed | 15 | 0 | 3.986 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 55.03% | 0.00039 | 0.238 | 0.00046 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-06T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 3.8 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
