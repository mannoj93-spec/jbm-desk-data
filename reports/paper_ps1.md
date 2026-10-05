# Paper sizing experiment PS1

Generated 2026-10-05T08:12:48.998Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-05T08:12:48.355Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 48 physical; 48 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 2.34 days; 15 scheduled decisions; coverage 53.3%; execution delay after the 4H close: median 14.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 7 closed intervals over 55.9 h; extended intervals 2.

Outcomes: executed 8; missed: stale: processed after close + max_delay 7

Execution states: completed 8

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 7 | 56 | 0.72% | 111.8% | 6.1% | 18.26 | 0.34 | 53.2 | 37.45 / 37.45 | -0.16% | -0.16% | -0.16% |
| ordinary | VOL | 7 | 56 | 0.94% | 146.8% | 8.0% | 18.28 | 0.45 | 69.9 | 49.25 / 49.25 | -0.21% | -0.21% | -0.21% |
| ordinary | B2 | 7 | 56 | 1.77% | 275.1% | 10.8% | 25.44 | 0.84 | 242.7 | 171.51 / 171.51 | -0.24% | -0.24% | -0.24% |
| stressed | FIXED | 7 | 56 | 0.68% | 107.0% | 6.3% | 17.09 | 0.34 | 53.3 | 68.11 / 68.11 | -0.16% | -0.16% | -0.16% |
| stressed | VOL | 7 | 56 | 0.90% | 140.6% | 8.2% | 17.10 | 0.45 | 70.0 | 89.57 / 89.57 | -0.21% | -0.21% | -0.21% |
| stressed | B2 | 7 | 56 | 1.63% | 253.3% | 11.2% | 22.64 | 0.84 | 242.7 | 311.56 / 311.56 | -0.26% | -0.26% | -0.26% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 7 | 0 | 7.163 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 128.32% | 0.00117 | 0.520 | 0.00149 |
| stressed | 7 | 0 | 5.545 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 112.74% | 0.00103 | 0.455 | 0.00133 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-05T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 2.3 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
