# Paper sizing experiment PS1

Generated 2026-11-13T12:42:18.442Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-13T08:23:58.229Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1182 physical; 1182 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 41.53 days; 250 scheduled decisions; coverage 78.8%; execution delay after the 4H close: median 20.3 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 196 closed intervals over 992.1 h; extended intervals 10.

Outcomes: executed 197; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 39

Execution states: completed 197

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 196 | 992 | -6.49% | -59.2% | 11.3% | -5.26 | 0.33 | 3.1 | 37.45 / 37.45 | -7.15% | -1.36% | -0.76% |
| ordinary | VOL | 196 | 992 | -8.30% | -76.5% | 15.4% | -4.96 | 0.43 | 8.1 | 98.40 / 98.40 | -9.15% | -2.00% | -1.06% |
| ordinary | B2 | 196 | 992 | -9.41% | -87.2% | 14.2% | -6.13 | 0.57 | 119.1 | 1478.09 / 1478.09 | -11.00% | -2.24% | -1.10% |
| stressed | FIXED | 196 | 992 | -6.52% | -59.5% | 11.3% | -5.28 | 0.33 | 3.1 | 68.11 / 68.11 | -7.15% | -1.36% | -0.76% |
| stressed | VOL | 196 | 992 | -8.37% | -77.2% | 15.4% | -5.01 | 0.43 | 8.1 | 178.87 / 178.87 | -9.19% | -2.00% | -1.06% |
| stressed | B2 | 196 | 992 | -10.50% | -98.0% | 14.2% | -6.89 | 0.57 | 119.1 | 2651.14 / 2651.14 | -11.97% | -2.25% | -1.10% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 196 | 4 | -1.168 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -10.77% | -0.00006 | -0.043 | -0.00016 |
| stressed | 196 | 4 | -1.887 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -20.75% | -0.00012 | -0.083 | -0.00022 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-13T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 41.5 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
