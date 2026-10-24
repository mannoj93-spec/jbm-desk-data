# Paper sizing experiment PS1

Generated 2026-10-24T20:18:15.923Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-24T20:18:12.428Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 702 physical; 702 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 21.85 days; 132 scheduled decisions; coverage 88.6%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 116 closed intervals over 524.0 h; extended intervals 6.

Outcomes: executed 117; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 117

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 116 | 524 | -1.64% | -27.6% | 10.5% | -2.63 | 0.34 | 5.7 | 37.45 / 37.45 | -2.68% | -0.84% | -0.61% |
| ordinary | VOL | 116 | 524 | -2.27% | -38.4% | 14.4% | -2.66 | 0.45 | 11.7 | 76.49 / 76.49 | -3.69% | -1.25% | -0.85% |
| ordinary | B2 | 116 | 524 | -2.03% | -34.2% | 14.5% | -2.36 | 0.55 | 140.3 | 944.38 / 944.38 | -4.28% | -0.99% | -0.85% |
| stressed | FIXED | 116 | 524 | -1.67% | -28.2% | 10.5% | -2.67 | 0.34 | 5.7 | 68.11 / 68.11 | -2.68% | -0.84% | -0.61% |
| stressed | VOL | 116 | 524 | -2.33% | -39.5% | 14.4% | -2.74 | 0.45 | 11.7 | 139.06 / 139.06 | -3.71% | -1.25% | -0.85% |
| stressed | B2 | 116 | 524 | -2.76% | -46.9% | 14.4% | -3.25 | 0.55 | 140.4 | 1690.45 / 1690.45 | -4.87% | -0.99% | -0.85% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 116 | 2 | 0.300 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 4.19% | 0.00002 | 0.019 | -0.00003 |
| stressed | 116 | 2 | -0.512 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | -7.38% | -0.00004 | -0.033 | -0.00010 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-24T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 21.8 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
