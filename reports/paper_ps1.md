# Paper sizing experiment PS1

Generated 2026-11-12T17:10:07.007Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-12T16:26:06.531Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1158 physical; 1158 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 40.72 days; 245 scheduled decisions; coverage 78.8%; execution delay after the 4H close: median 20.2 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 192 closed intervals over 976.1 h; extended intervals 10.

Outcomes: executed 193; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 38

Execution states: completed 193

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 192 | 976 | -5.15% | -47.4% | 10.8% | -4.38 | 0.33 | 3.1 | 37.45 / 37.45 | -5.82% | -1.36% | -0.69% |
| ordinary | VOL | 192 | 976 | -6.57% | -61.0% | 14.9% | -4.09 | 0.43 | 7.6 | 90.69 / 98.40 | -7.44% | -2.00% | -0.97% |
| ordinary | B2 | 192 | 976 | -7.88% | -73.7% | 13.8% | -5.36 | 0.57 | 118.5 | 1450.10 / 1459.65 | -9.50% | -2.24% | -1.03% |
| stressed | FIXED | 192 | 976 | -5.18% | -47.7% | 10.8% | -4.41 | 0.33 | 3.1 | 68.11 / 68.11 | -5.82% | -1.36% | -0.69% |
| stressed | VOL | 192 | 976 | -6.64% | -61.6% | 14.9% | -4.14 | 0.43 | 7.6 | 164.86 / 178.87 | -7.47% | -2.00% | -0.97% |
| stressed | B2 | 192 | 976 | -8.97% | -84.4% | 13.7% | -6.14 | 0.57 | 118.6 | 2600.86 / 2618.03 | -10.47% | -2.25% | -1.03% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 192 | 4 | -1.262 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -12.75% | -0.00007 | -0.051 | -0.00015 |
| stressed | 192 | 4 | -2.002 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -22.74% | -0.00013 | -0.091 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-12T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 40.7 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
