# Paper sizing experiment PS1

Generated 2026-11-17T02:55:01.330Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-17T00:25:52.574Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1302 physical; 1302 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 45.12 days; 271 scheduled decisions; coverage 80.1%; execution delay after the 4H close: median 20.6 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 216 closed intervals over 1080.1 h; extended intervals 12.

Outcomes: executed 217; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 217

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 216 | 1080 | -8.26% | -69.9% | 12.0% | -5.84 | 0.33 | 3.2 | 42.58 / 42.58 | -9.14% | -1.36% | -0.80% |
| ordinary | VOL | 216 | 1080 | -10.08% | -86.1% | 15.5% | -5.56 | 0.42 | 8.4 | 110.14 / 110.14 | -11.11% | -2.00% | -1.04% |
| ordinary | B2 | 216 | 1080 | -11.67% | -100.7% | 14.7% | -6.84 | 0.54 | 114.9 | 1555.10 / 1560.41 | -13.42% | -2.24% | -1.13% |
| stressed | FIXED | 216 | 1080 | -8.29% | -70.2% | 12.0% | -5.86 | 0.33 | 3.2 | 77.42 / 77.42 | -9.15% | -1.36% | -0.80% |
| stressed | VOL | 216 | 1080 | -10.16% | -86.9% | 15.5% | -5.61 | 0.42 | 8.4 | 200.14 / 200.14 | -11.15% | -2.00% | -1.04% |
| stressed | B2 | 216 | 1080 | -12.79% | -111.0% | 14.7% | -7.55 | 0.54 | 115.0 | 2775.88 / 2785.41 | -14.41% | -2.25% | -1.13% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 216 | 5 | -1.281 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -14.55% | -0.00008 | -0.059 | -0.00018 |
| stressed | 216 | 5 | -1.942 | unavailable: 5 complete block(s) of 42 intervals; PS1 needs 10 | -24.08% | -0.00014 | -0.098 | -0.00023 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-17T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 45.1 days, 5 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
