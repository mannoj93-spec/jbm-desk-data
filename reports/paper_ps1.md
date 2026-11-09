# Paper sizing experiment PS1

Generated 2026-11-09T04:22:55.689Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-09T04:22:51.061Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1038 physical; 1038 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 37.18 days; 224 scheduled decisions; coverage 77.2%; execution delay after the 4H close: median 19.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 172 closed intervals over 892.0 h; extended intervals 9.

Outcomes: executed 173; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 37

Execution states: completed 173

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 172 | 892 | -3.91% | -39.1% | 10.9% | -3.58 | 0.33 | 3.4 | 37.45 / 37.45 | -4.59% | -1.36% | -0.72% |
| ordinary | VOL | 172 | 892 | -5.27% | -53.2% | 15.3% | -3.47 | 0.44 | 8.2 | 90.69 / 90.69 | -6.16% | -2.00% | -1.02% |
| ordinary | B2 | 172 | 892 | -6.44% | -65.4% | 14.1% | -4.65 | 0.59 | 121.1 | 1362.76 / 1392.34 | -8.09% | -2.24% | -1.08% |
| stressed | FIXED | 172 | 892 | -3.94% | -39.4% | 10.9% | -3.61 | 0.33 | 3.4 | 68.11 / 68.11 | -4.59% | -1.36% | -0.72% |
| stressed | VOL | 172 | 892 | -5.34% | -53.9% | 15.3% | -3.52 | 0.44 | 8.2 | 164.86 / 164.86 | -6.19% | -2.00% | -1.02% |
| stressed | B2 | 172 | 892 | -7.48% | -76.3% | 14.0% | -5.44 | 0.59 | 121.1 | 2444.01 / 2497.19 | -9.00% | -2.25% | -1.08% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 172 | 4 | -1.180 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -12.21% | -0.00007 | -0.048 | -0.00016 |
| stressed | 172 | 4 | -1.922 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -22.39% | -0.00013 | -0.087 | -0.00022 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-09T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 37.2 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
