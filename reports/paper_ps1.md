# Paper sizing experiment PS1

Generated 2026-10-29T16:22:27.497Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-29T16:22:24.737Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 876 physical; 876 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 26.68 days; 161 scheduled decisions; coverage 90.7%; execution delay after the 4H close: median 19.2 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 145 closed intervals over 640.0 h; extended intervals 6.

Outcomes: executed 146; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 146

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 145 | 640 | -1.27% | -17.6% | 10.1% | -1.73 | 0.34 | 4.7 | 37.45 / 37.45 | -2.68% | -0.84% | -0.57% |
| ordinary | VOL | 145 | 640 | -1.74% | -24.0% | 14.1% | -1.71 | 0.46 | 9.6 | 76.49 / 76.49 | -3.69% | -1.25% | -0.80% |
| ordinary | B2 | 145 | 640 | -1.93% | -26.7% | 13.9% | -1.92 | 0.53 | 134.6 | 1098.50 / 1113.66 | -4.48% | -0.99% | -0.79% |
| stressed | FIXED | 145 | 640 | -1.30% | -18.0% | 10.2% | -1.77 | 0.34 | 4.7 | 68.11 / 68.11 | -2.68% | -0.84% | -0.57% |
| stressed | VOL | 145 | 640 | -1.80% | -24.9% | 14.1% | -1.77 | 0.46 | 9.6 | 139.06 / 139.06 | -3.71% | -1.25% | -0.80% |
| stressed | B2 | 145 | 640 | -2.80% | -38.8% | 13.9% | -2.80 | 0.53 | 134.7 | 1968.36 / 1995.67 | -5.21% | -0.99% | -0.79% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 145 | 3 | -0.214 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -2.71% | -0.00001 | -0.013 | -0.00005 |
| stressed | 145 | 3 | -1.029 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -13.95% | -0.00007 | -0.067 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-29T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 26.7 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
