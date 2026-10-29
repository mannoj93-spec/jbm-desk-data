# Paper sizing experiment PS1

Generated 2026-10-29T12:20:49.598Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-29T12:20:46.377Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 870 physical; 870 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 26.51 days; 160 scheduled decisions; coverage 90.6%; execution delay after the 4H close: median 19.2 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 144 closed intervals over 636.0 h; extended intervals 6.

Outcomes: executed 145; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 145

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 144 | 636 | -1.82% | -25.3% | 9.9% | -2.54 | 0.34 | 4.7 | 37.45 / 37.45 | -2.68% | -0.84% | -0.57% |
| ordinary | VOL | 144 | 636 | -2.53% | -35.3% | 13.7% | -2.57 | 0.46 | 9.7 | 76.49 / 76.49 | -3.69% | -1.25% | -0.80% |
| ordinary | B2 | 144 | 636 | -2.68% | -37.4% | 13.6% | -2.74 | 0.53 | 134.7 | 1093.01 / 1098.50 | -4.48% | -0.99% | -0.79% |
| stressed | FIXED | 144 | 636 | -1.85% | -25.7% | 9.9% | -2.58 | 0.34 | 4.7 | 68.11 / 68.11 | -2.68% | -0.84% | -0.57% |
| stressed | VOL | 144 | 636 | -2.60% | -36.2% | 13.7% | -2.64 | 0.46 | 9.7 | 139.06 / 139.06 | -3.71% | -1.25% | -0.80% |
| stressed | B2 | 144 | 636 | -3.53% | -49.5% | 13.6% | -3.64 | 0.53 | 134.8 | 1958.48 / 1968.36 | -5.21% | -0.99% | -0.79% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 144 | 3 | -0.170 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -2.03% | -0.00001 | -0.010 | -0.00006 |
| stressed | 144 | 3 | -1.006 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -13.27% | -0.00007 | -0.063 | -0.00012 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-29T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 26.5 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
