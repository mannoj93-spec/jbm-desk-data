# Paper sizing experiment PS1

Generated 2026-11-15T00:21:56.448Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-15T00:21:50.793Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1230 physical; 1230 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 43.02 days; 259 scheduled decisions; coverage 79.1%; execution delay after the 4H close: median 20.4 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 204 closed intervals over 1032.0 h; extended intervals 12.

Outcomes: executed 205; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 205

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 204 | 1032 | -8.44% | -74.9% | 11.8% | -6.36 | 0.33 | 3.3 | 42.58 / 42.58 | -9.09% | -1.36% | -0.80% |
| ordinary | VOL | 204 | 1032 | -10.27% | -92.0% | 15.7% | -5.87 | 0.43 | 8.2 | 103.56 / 103.56 | -11.11% | -2.00% | -1.04% |
| ordinary | B2 | 204 | 1032 | -11.82% | -106.7% | 14.9% | -7.15 | 0.56 | 117.8 | 1516.36 / 1543.56 | -13.36% | -2.24% | -1.13% |
| stressed | FIXED | 204 | 1032 | -8.48% | -75.2% | 11.8% | -6.39 | 0.33 | 3.3 | 77.42 / 77.42 | -9.10% | -1.36% | -0.80% |
| stressed | VOL | 204 | 1032 | -10.35% | -92.7% | 15.7% | -5.92 | 0.43 | 8.2 | 188.25 / 188.25 | -11.15% | -2.00% | -1.04% |
| stressed | B2 | 204 | 1032 | -12.91% | -117.3% | 14.9% | -7.87 | 0.56 | 117.9 | 2719.87 / 2755.16 | -14.34% | -2.25% | -1.13% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 204 | 4 | -1.279 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -14.73% | -0.00009 | -0.059 | -0.00018 |
| stressed | 204 | 4 | -1.952 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -24.59% | -0.00014 | -0.099 | -0.00024 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-15T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 43.0 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
