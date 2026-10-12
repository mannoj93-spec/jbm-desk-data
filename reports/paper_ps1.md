# Paper sizing experiment PS1

Generated 2026-10-12T16:20:29.277Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-12T16:20:27.761Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 306 physical; 306 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 9.68 days; 59 scheduled decisions; coverage 86.4%; execution delay after the 4H close: median 18.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 50 closed intervals over 232.0 h; extended intervals 3.

Outcomes: executed 51; missed: stale: processed after close + max_delay 8

Execution states: completed 51

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 50 | 232 | -0.69% | -26.0% | 8.3% | -3.12 | 0.34 | 12.9 | 37.45 / 37.45 | -2.01% | -0.60% | -0.51% |
| ordinary | VOL | 50 | 232 | -0.91% | -34.3% | 11.1% | -3.08 | 0.46 | 19.0 | 55.22 / 55.22 | -2.64% | -0.79% | -0.67% |
| ordinary | B2 | 50 | 232 | -0.06% | -2.3% | 12.9% | -0.18 | 0.63 | 162.6 | 475.33 / 475.33 | -3.04% | -0.96% | -0.76% |
| stressed | FIXED | 50 | 232 | -0.72% | -27.1% | 8.3% | -3.25 | 0.34 | 12.9 | 68.11 / 68.11 | -2.01% | -0.60% | -0.51% |
| stressed | VOL | 50 | 232 | -0.95% | -36.1% | 11.2% | -3.23 | 0.46 | 19.0 | 100.40 / 100.40 | -2.64% | -0.79% | -0.67% |
| stressed | B2 | 50 | 232 | -0.45% | -16.9% | 12.8% | -1.32 | 0.63 | 162.7 | 862.09 / 862.09 | -3.13% | -0.96% | -0.76% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 50 | 1 | 2.906 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 32.08% | 0.00017 | 0.162 | 0.00013 |
| stressed | 50 | 1 | 1.916 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 19.15% | 0.00010 | 0.097 | 0.00005 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-12T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 9.7 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
