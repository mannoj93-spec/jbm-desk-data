# Paper sizing experiment PS1

Generated 2026-11-12T20:25:02.176Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-12T20:24:57.150Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1164 physical; 1164 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 40.85 days; 246 scheduled decisions; coverage 78.9%; execution delay after the 4H close: median 20.2 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 193 closed intervals over 980.1 h; extended intervals 10.

Outcomes: executed 194; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 38

Execution states: completed 194

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 193 | 980 | -5.27% | -48.4% | 10.8% | -4.48 | 0.33 | 3.1 | 37.45 / 37.45 | -5.94% | -1.36% | -0.69% |
| ordinary | VOL | 193 | 980 | -6.73% | -62.3% | 14.9% | -4.19 | 0.43 | 8.2 | 98.40 / 98.40 | -7.60% | -2.00% | -0.97% |
| ordinary | B2 | 193 | 980 | -8.01% | -74.7% | 13.7% | -5.44 | 0.57 | 118.9 | 1459.65 / 1466.70 | -9.63% | -2.24% | -1.03% |
| stressed | FIXED | 193 | 980 | -5.30% | -48.7% | 10.8% | -4.51 | 0.33 | 3.1 | 68.11 / 68.11 | -5.95% | -1.36% | -0.69% |
| stressed | VOL | 193 | 980 | -6.81% | -63.1% | 14.9% | -4.24 | 0.43 | 8.2 | 178.87 / 178.87 | -7.64% | -2.00% | -0.97% |
| stressed | B2 | 193 | 980 | -9.11% | -85.4% | 13.7% | -6.23 | 0.57 | 118.9 | 2618.03 / 2630.68 | -10.60% | -2.25% | -1.03% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 193 | 4 | -1.244 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -12.34% | -0.00007 | -0.050 | -0.00015 |
| stressed | 193 | 4 | -1.984 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -22.30% | -0.00013 | -0.089 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-12T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 40.9 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
