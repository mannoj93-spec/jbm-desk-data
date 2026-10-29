# Paper sizing experiment PS1

Generated 2026-10-29T21:03:52.470Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-29T20:23:08.014Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 882 physical; 882 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 26.88 days; 162 scheduled decisions; coverage 90.7%; execution delay after the 4H close: median 19.2 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 146 closed intervals over 644.0 h; extended intervals 6.

Outcomes: executed 147; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 147

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 146 | 644 | -1.73% | -23.7% | 10.3% | -2.31 | 0.33 | 4.7 | 37.45 / 37.45 | -2.68% | -0.84% | -0.58% |
| ordinary | VOL | 146 | 644 | -2.40% | -33.1% | 14.2% | -2.32 | 0.46 | 9.6 | 76.49 / 76.49 | -3.69% | -1.25% | -0.82% |
| ordinary | B2 | 146 | 644 | -2.38% | -32.8% | 14.0% | -2.35 | 0.53 | 135.7 | 1113.66 / 1113.66 | -4.48% | -0.99% | -0.79% |
| stressed | FIXED | 146 | 644 | -1.76% | -24.2% | 10.3% | -2.35 | 0.34 | 4.7 | 68.11 / 68.11 | -2.68% | -0.84% | -0.58% |
| stressed | VOL | 146 | 644 | -2.47% | -34.0% | 14.2% | -2.38 | 0.46 | 9.6 | 139.06 / 139.06 | -3.71% | -1.25% | -0.82% |
| stressed | B2 | 146 | 644 | -3.26% | -45.0% | 13.9% | -3.23 | 0.53 | 135.7 | 1995.67 / 1995.67 | -5.21% | -0.99% | -0.79% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 146 | 3 | -0.027 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 0.28% | 0.00000 | 0.001 | -0.00005 |
| stressed | 146 | 3 | -0.847 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -11.06% | -0.00006 | -0.052 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-29T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 26.9 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
