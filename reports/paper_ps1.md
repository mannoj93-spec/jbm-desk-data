# Paper sizing experiment PS1

Generated 2026-11-06T20:22:51.318Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-06T20:22:46.330Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 966 physical; 966 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 34.85 days; 210 scheduled decisions; coverage 76.7%; execution delay after the 4H close: median 19.3 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 160 closed intervals over 836.0 h; extended intervals 7.

Outcomes: executed 161; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 35

Execution states: completed 161

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 160 | 836 | -3.55% | -37.9% | 11.3% | -3.36 | 0.33 | 3.6 | 37.45 / 37.45 | -4.30% | -1.36% | -0.72% |
| ordinary | VOL | 160 | 836 | -4.91% | -52.7% | 15.9% | -3.32 | 0.45 | 8.8 | 90.69 / 90.69 | -5.84% | -2.00% | -1.02% |
| ordinary | B2 | 160 | 836 | -5.64% | -60.8% | 14.4% | -4.23 | 0.58 | 117.3 | 1244.19 / 1252.57 | -7.30% | -2.24% | -1.06% |
| stressed | FIXED | 160 | 836 | -3.59% | -38.3% | 11.3% | -3.39 | 0.33 | 3.6 | 68.11 / 68.11 | -4.30% | -1.36% | -0.72% |
| stressed | VOL | 160 | 836 | -4.98% | -53.5% | 15.9% | -3.37 | 0.45 | 8.8 | 164.86 / 164.86 | -5.87% | -2.00% | -1.02% |
| stressed | B2 | 160 | 836 | -6.59% | -71.4% | 14.3% | -4.98 | 0.58 | 117.4 | 2230.75 / 2245.81 | -8.12% | -2.25% | -1.06% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 160 | 3 | -0.909 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -8.11% | -0.00005 | -0.032 | -0.00014 |
| stressed | 160 | 3 | -1.608 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -17.89% | -0.00011 | -0.070 | -0.00020 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-06T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 34.8 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
