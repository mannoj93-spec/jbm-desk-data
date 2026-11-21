# Paper sizing experiment PS1

Generated 2026-11-21T13:07:01.256Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-21T12:28:02.590Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1452 physical; 1452 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 49.55 days; 298 scheduled decisions; coverage 81.2%; execution delay after the 4H close: median 21.2 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 241 closed intervals over 1188.1 h; extended intervals 14.

Outcomes: executed 242; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 42

Execution states: completed 242

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 241 | 1188 | -11.12% | -86.9% | 14.0% | -6.19 | 0.33 | 2.9 | 42.58 / 42.58 | -13.01% | -1.73% | -0.95% |
| ordinary | VOL | 241 | 1188 | -12.25% | -96.3% | 16.0% | -6.03 | 0.41 | 7.7 | 110.14 / 110.14 | -14.01% | -2.00% | -1.06% |
| ordinary | B2 | 241 | 1188 | -14.33% | -114.1% | 15.7% | -7.27 | 0.52 | 108.5 | 1598.00 / 1598.00 | -16.76% | -2.24% | -1.17% |
| stressed | FIXED | 241 | 1188 | -11.16% | -87.2% | 14.0% | -6.21 | 0.33 | 2.9 | 77.42 / 77.42 | -13.02% | -1.73% | -0.95% |
| stressed | VOL | 241 | 1188 | -12.33% | -97.0% | 16.0% | -6.07 | 0.41 | 7.7 | 200.14 / 200.14 | -14.06% | -2.00% | -1.06% |
| stressed | B2 | 241 | 1188 | -15.45% | -123.7% | 15.7% | -7.89 | 0.52 | 108.6 | 2852.68 / 2852.68 | -17.75% | -2.25% | -1.18% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 241 | 5 | -1.240 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -17.73% | -0.00010 | -0.074 | -0.00015 |
| stressed | 241 | 5 | -1.819 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -26.69% | -0.00015 | -0.111 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-21T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 49.5 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
