# Paper sizing experiment PS1

Generated 2026-10-29T04:22:16.937Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-29T04:22:13.252Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 858 physical; 858 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 26.18 days; 158 scheduled decisions; coverage 90.5%; execution delay after the 4H close: median 19.2 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 142 closed intervals over 628.0 h; extended intervals 6.

Outcomes: executed 143; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 143

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 142 | 628 | -1.90% | -26.7% | 10.0% | -2.67 | 0.34 | 4.8 | 37.45 / 37.45 | -2.68% | -0.84% | -0.57% |
| ordinary | VOL | 142 | 628 | -2.65% | -37.5% | 13.8% | -2.71 | 0.46 | 9.8 | 76.49 / 76.49 | -3.69% | -1.25% | -0.80% |
| ordinary | B2 | 142 | 628 | -2.77% | -39.2% | 13.7% | -2.86 | 0.54 | 136.4 | 1093.01 / 1093.01 | -4.48% | -0.99% | -0.79% |
| stressed | FIXED | 142 | 628 | -1.93% | -27.2% | 10.0% | -2.71 | 0.34 | 4.8 | 68.11 / 68.11 | -2.68% | -0.84% | -0.57% |
| stressed | VOL | 142 | 628 | -2.71% | -38.3% | 13.8% | -2.77 | 0.46 | 9.8 | 139.06 / 139.06 | -3.71% | -1.25% | -0.80% |
| stressed | B2 | 142 | 628 | -3.63% | -51.5% | 13.7% | -3.77 | 0.54 | 136.5 | 1958.48 / 1958.48 | -5.21% | -0.99% | -0.79% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 142 | 3 | -0.152 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -1.78% | -0.00001 | -0.008 | -0.00006 |
| stressed | 142 | 3 | -0.993 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -13.17% | -0.00007 | -0.062 | -0.00012 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-29T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 26.2 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
