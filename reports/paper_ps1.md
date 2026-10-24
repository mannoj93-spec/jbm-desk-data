# Paper sizing experiment PS1

Generated 2026-10-24T08:49:10.391Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-24T08:19:20.008Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 684 physical; 684 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 21.37 days; 129 scheduled decisions; coverage 88.4%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 113 closed intervals over 512.0 h; extended intervals 6.

Outcomes: executed 114; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 114

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 113 | 512 | -1.55% | -26.8% | 10.4% | -2.58 | 0.34 | 5.9 | 37.45 / 37.45 | -2.25% | -0.84% | -0.61% |
| ordinary | VOL | 113 | 512 | -2.14% | -37.1% | 14.2% | -2.62 | 0.45 | 12.0 | 76.49 / 76.49 | -3.06% | -1.25% | -0.84% |
| ordinary | B2 | 113 | 512 | -1.53% | -26.3% | 13.8% | -1.91 | 0.54 | 138.4 | 911.32 / 918.11 | -3.34% | -0.96% | -0.78% |
| stressed | FIXED | 113 | 512 | -1.58% | -27.3% | 10.4% | -2.63 | 0.34 | 5.9 | 68.11 / 68.11 | -2.25% | -0.84% | -0.61% |
| stressed | VOL | 113 | 512 | -2.21% | -38.2% | 14.2% | -2.69 | 0.45 | 12.0 | 139.06 / 139.06 | -3.08% | -1.25% | -0.84% |
| stressed | B2 | 113 | 512 | -2.24% | -38.8% | 13.8% | -2.82 | 0.54 | 138.4 | 1630.79 / 1643.04 | -3.85% | -0.96% | -0.78% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 113 | 2 | 0.707 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 10.76% | 0.00006 | 0.050 | 0.00000 |
| stressed | 113 | 2 | -0.127 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | -0.61% | -0.00000 | -0.003 | -0.00006 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-24T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 21.4 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
