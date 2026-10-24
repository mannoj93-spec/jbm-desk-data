# Paper sizing experiment PS1

Generated 2026-10-24T03:49:16.651Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-24T00:19:13.650Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 672 physical; 672 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 21.16 days; 127 scheduled decisions; coverage 88.2%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 111 closed intervals over 504.0 h; extended intervals 6.

Outcomes: executed 112; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 112

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 111 | 504 | -1.51% | -26.5% | 10.5% | -2.53 | 0.34 | 6.0 | 37.45 / 37.45 | -2.23% | -0.84% | -0.61% |
| ordinary | VOL | 111 | 504 | -2.09% | -36.7% | 14.3% | -2.56 | 0.45 | 12.2 | 76.49 / 76.49 | -3.05% | -1.25% | -0.84% |
| ordinary | B2 | 111 | 504 | -1.42% | -24.8% | 13.9% | -1.79 | 0.54 | 136.8 | 887.95 / 902.18 | -3.34% | -0.96% | -0.78% |
| stressed | FIXED | 111 | 504 | -1.54% | -27.1% | 10.5% | -2.58 | 0.34 | 6.0 | 68.11 / 68.11 | -2.23% | -0.84% | -0.61% |
| stressed | VOL | 111 | 504 | -2.15% | -37.8% | 14.3% | -2.64 | 0.45 | 12.2 | 139.06 / 139.06 | -3.06% | -1.25% | -0.84% |
| stressed | B2 | 111 | 504 | -2.11% | -37.2% | 13.9% | -2.68 | 0.54 | 136.9 | 1588.60 / 1614.29 | -3.82% | -0.96% | -0.78% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 111 | 2 | 0.779 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 11.84% | 0.00006 | 0.055 | 0.00001 |
| stressed | 111 | 2 | -0.037 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 0.63% | 0.00000 | 0.003 | -0.00005 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-24T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 21.2 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
