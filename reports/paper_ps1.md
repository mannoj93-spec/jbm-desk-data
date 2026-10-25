# Paper sizing experiment PS1

Generated 2026-10-25T13:25:03.626Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-25T12:18:34.586Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 726 physical; 726 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 22.56 days; 136 scheduled decisions; coverage 89.0%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 120 closed intervals over 540.0 h; extended intervals 6.

Outcomes: executed 121; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 121

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 120 | 540 | -1.68% | -27.5% | 10.4% | -2.65 | 0.34 | 5.6 | 37.45 / 37.45 | -2.68% | -0.84% | -0.58% |
| ordinary | VOL | 120 | 540 | -2.33% | -38.3% | 14.2% | -2.69 | 0.46 | 11.4 | 76.49 / 76.49 | -3.69% | -1.25% | -0.80% |
| ordinary | B2 | 120 | 540 | -2.14% | -35.0% | 14.3% | -2.45 | 0.55 | 139.1 | 963.84 / 963.84 | -4.28% | -0.99% | -0.81% |
| stressed | FIXED | 120 | 540 | -1.71% | -28.0% | 10.4% | -2.70 | 0.34 | 5.6 | 68.11 / 68.11 | -2.68% | -0.84% | -0.58% |
| stressed | VOL | 120 | 540 | -2.39% | -39.3% | 14.2% | -2.77 | 0.46 | 11.4 | 139.06 / 139.06 | -3.71% | -1.25% | -0.80% |
| stressed | B2 | 120 | 540 | -2.89% | -47.5% | 14.2% | -3.34 | 0.55 | 139.1 | 1725.53 / 1725.53 | -4.87% | -0.99% | -0.82% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 120 | 2 | 0.241 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 3.25% | 0.00002 | 0.015 | -0.00004 |
| stressed | 120 | 2 | -0.576 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | -8.24% | -0.00004 | -0.038 | -0.00010 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-25T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 22.6 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
