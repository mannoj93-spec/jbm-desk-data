# Paper sizing experiment PS1

Generated 2026-11-13T04:24:26.669Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-13T04:24:21.824Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1176 physical; 1176 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 41.18 days; 248 scheduled decisions; coverage 79.0%; execution delay after the 4H close: median 20.3 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 195 closed intervals over 988.1 h; extended intervals 10.

Outcomes: executed 196; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 38

Execution states: completed 196

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 195 | 988 | -6.35% | -58.2% | 11.3% | -5.16 | 0.33 | 3.1 | 37.45 / 37.45 | -7.02% | -1.36% | -0.76% |
| ordinary | VOL | 195 | 988 | -8.13% | -75.1% | 15.5% | -4.86 | 0.43 | 8.1 | 98.40 / 98.40 | -8.98% | -2.00% | -1.06% |
| ordinary | B2 | 195 | 988 | -9.29% | -86.5% | 14.3% | -6.06 | 0.57 | 118.6 | 1466.70 / 1478.09 | -10.88% | -2.24% | -1.10% |
| stressed | FIXED | 195 | 988 | -6.39% | -58.5% | 11.3% | -5.18 | 0.33 | 3.1 | 68.11 / 68.11 | -7.02% | -1.36% | -0.76% |
| stressed | VOL | 195 | 988 | -8.20% | -75.9% | 15.5% | -4.91 | 0.43 | 8.1 | 178.87 / 178.87 | -9.02% | -2.00% | -1.06% |
| stressed | B2 | 195 | 988 | -10.38% | -97.1% | 14.2% | -6.82 | 0.57 | 118.6 | 2630.68 / 2651.14 | -11.85% | -2.25% | -1.10% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 195 | 4 | -1.195 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -11.30% | -0.00007 | -0.046 | -0.00016 |
| stressed | 195 | 4 | -1.908 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -21.24% | -0.00012 | -0.085 | -0.00022 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-13T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 41.2 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
