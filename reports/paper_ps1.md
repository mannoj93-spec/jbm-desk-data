# Paper sizing experiment PS1

Generated 2026-10-28T00:20:19.720Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-28T00:20:16.619Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 816 physical; 816 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 25.01 days; 151 scheduled decisions; coverage 90.1%; execution delay after the 4H close: median 19.0 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 135 closed intervals over 600.0 h; extended intervals 6.

Outcomes: executed 136; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 136

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 135 | 600 | -1.57% | -23.1% | 9.9% | -2.32 | 0.34 | 5.0 | 37.45 / 37.45 | -2.68% | -0.84% | -0.58% |
| ordinary | VOL | 135 | 600 | -2.17% | -32.0% | 13.6% | -2.35 | 0.46 | 10.3 | 76.49 / 76.49 | -3.69% | -1.25% | -0.80% |
| ordinary | B2 | 135 | 600 | -2.11% | -31.2% | 13.7% | -2.28 | 0.54 | 133.0 | 1020.65 / 1028.16 | -4.34% | -0.99% | -0.81% |
| stressed | FIXED | 135 | 600 | -1.60% | -23.5% | 9.9% | -2.37 | 0.34 | 5.0 | 68.11 / 68.11 | -2.68% | -0.84% | -0.58% |
| stressed | VOL | 135 | 600 | -2.23% | -32.9% | 13.6% | -2.41 | 0.46 | 10.3 | 139.06 / 139.06 | -3.71% | -1.25% | -0.80% |
| stressed | B2 | 135 | 600 | -2.91% | -43.2% | 13.7% | -3.16 | 0.54 | 133.1 | 1828.01 / 1841.55 | -5.00% | -0.99% | -0.82% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 135 | 3 | 0.069 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 0.78% | 0.00000 | 0.004 | -0.00004 |
| stressed | 135 | 3 | -0.744 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -10.25% | -0.00005 | -0.049 | -0.00010 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-28T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 25.0 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
