# Paper sizing experiment PS1

Generated 2026-10-28T15:33:30.446Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-28T12:21:24.452Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 834 physical; 834 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 25.65 days; 154 scheduled decisions; coverage 90.3%; execution delay after the 4H close: median 19.1 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 138 closed intervals over 612.0 h; extended intervals 6.

Outcomes: executed 139; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 139

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 138 | 612 | -1.47% | -21.3% | 9.8% | -2.16 | 0.34 | 4.9 | 37.45 / 37.45 | -2.68% | -0.84% | -0.58% |
| ordinary | VOL | 138 | 612 | -2.03% | -29.4% | 13.5% | -2.17 | 0.46 | 10.1 | 76.49 / 76.49 | -3.69% | -1.25% | -0.80% |
| ordinary | B2 | 138 | 612 | -2.03% | -29.4% | 13.6% | -2.16 | 0.54 | 133.1 | 1040.68 / 1053.29 | -4.34% | -0.99% | -0.81% |
| stressed | FIXED | 138 | 612 | -1.50% | -21.7% | 9.8% | -2.21 | 0.34 | 4.9 | 68.11 / 68.11 | -2.68% | -0.84% | -0.58% |
| stressed | VOL | 138 | 612 | -2.09% | -30.3% | 13.5% | -2.24 | 0.46 | 10.1 | 139.06 / 139.06 | -3.71% | -1.25% | -0.80% |
| stressed | B2 | 138 | 612 | -2.85% | -41.3% | 13.6% | -3.05 | 0.54 | 133.2 | 1864.14 / 1886.89 | -5.00% | -0.99% | -0.82% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 138 | 3 | 0.012 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -0.00% | -0.00000 | -0.000 | -0.00004 |
| stressed | 138 | 3 | -0.808 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -11.06% | -0.00006 | -0.053 | -0.00010 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-28T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 25.6 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
