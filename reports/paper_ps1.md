# Paper sizing experiment PS1

Generated 2026-10-07T13:08:11.252Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-07T12:17:39.492Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 120 physical; 120 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 4.55 days; 28 scheduled decisions; coverage 71.4%; execution delay after the 4H close: median 18.1 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 19 closed intervals over 108.0 h; extended intervals 3.

Outcomes: executed 20; missed: stale: processed after close + max_delay 8

Execution states: completed 20

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 19 | 108 | -0.44% | -35.6% | 10.0% | -3.57 | 0.34 | 27.5 | 37.45 / 37.45 | -1.14% | -0.60% | -0.60% |
| ordinary | VOL | 19 | 108 | -0.57% | -46.8% | 13.1% | -3.58 | 0.45 | 36.2 | 49.25 / 49.25 | -1.50% | -0.79% | -0.79% |
| ordinary | B2 | 19 | 108 | -0.13% | -10.7% | 15.6% | -0.69 | 0.65 | 186.5 | 256.08 / 264.81 | -1.88% | -0.96% | -0.96% |
| stressed | FIXED | 19 | 108 | -0.47% | -38.1% | 10.0% | -3.82 | 0.34 | 27.6 | 68.11 / 68.11 | -1.14% | -0.60% | -0.60% |
| stressed | VOL | 19 | 108 | -0.62% | -50.1% | 13.1% | -3.82 | 0.45 | 36.2 | 89.57 / 89.57 | -1.50% | -0.79% | -0.79% |
| stressed | B2 | 19 | 108 | -0.34% | -27.6% | 15.6% | -1.77 | 0.65 | 186.6 | 464.61 / 480.45 | -1.98% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 19 | 0 | 2.891 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 36.09% | 0.00023 | 0.151 | 0.00016 |
| stressed | 19 | 0 | 2.059 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 22.51% | 0.00015 | 0.095 | 0.00007 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-07T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 4.5 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
