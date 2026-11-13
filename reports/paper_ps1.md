# Paper sizing experiment PS1

Generated 2026-11-13T19:25:19.417Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-13T16:26:06.407Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1188 physical; 1188 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 41.81 days; 251 scheduled decisions; coverage 78.9%; execution delay after the 4H close: median 20.3 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 197 closed intervals over 1000.1 h; extended intervals 11.

Outcomes: executed 198; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 39

Execution states: completed 198

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 197 | 1000 | -6.42% | -58.1% | 11.2% | -5.17 | 0.33 | 3.0 | 37.45 / 37.45 | -7.15% | -1.36% | -0.76% |
| ordinary | VOL | 197 | 1000 | -8.21% | -75.0% | 15.4% | -4.88 | 0.43 | 8.0 | 98.40 / 98.40 | -9.15% | -2.00% | -1.06% |
| ordinary | B2 | 197 | 1000 | -9.35% | -86.0% | 14.2% | -6.06 | 0.56 | 118.1 | 1478.09 / 1478.09 | -11.00% | -2.24% | -1.10% |
| stressed | FIXED | 197 | 1000 | -6.45% | -58.4% | 11.2% | -5.20 | 0.33 | 3.0 | 68.11 / 68.11 | -7.15% | -1.36% | -0.76% |
| stressed | VOL | 197 | 1000 | -8.28% | -75.8% | 15.4% | -4.92 | 0.43 | 8.0 | 178.87 / 178.87 | -9.19% | -2.00% | -1.06% |
| stressed | B2 | 197 | 1000 | -10.45% | -96.6% | 14.2% | -6.81 | 0.56 | 118.2 | 2651.14 / 2651.14 | -11.97% | -2.25% | -1.10% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 197 | 4 | -1.179 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -10.99% | -0.00006 | -0.045 | -0.00016 |
| stressed | 197 | 4 | -1.893 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -20.90% | -0.00012 | -0.085 | -0.00022 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-13T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 41.8 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
