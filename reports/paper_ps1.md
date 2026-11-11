# Paper sizing experiment PS1

Generated 2026-11-11T00:24:06.135Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-11T00:24:03.395Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1104 physical; 1104 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 39.02 days; 235 scheduled decisions; coverage 78.3%; execution delay after the 4H close: median 19.7 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 183 closed intervals over 936.1 h; extended intervals 9.

Outcomes: executed 184; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 37

Execution states: completed 184

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 183 | 936 | -4.45% | -42.6% | 10.8% | -3.93 | 0.33 | 3.2 | 37.45 / 37.45 | -5.25% | -1.36% | -0.69% |
| ordinary | VOL | 183 | 936 | -5.84% | -56.3% | 15.1% | -3.74 | 0.44 | 7.9 | 90.69 / 90.69 | -6.84% | -2.00% | -0.97% |
| ordinary | B2 | 183 | 936 | -6.99% | -67.8% | 13.8% | -4.91 | 0.58 | 122.7 | 1443.72 / 1443.72 | -8.71% | -2.24% | -1.03% |
| stressed | FIXED | 183 | 936 | -4.48% | -42.9% | 10.9% | -3.95 | 0.33 | 3.2 | 68.11 / 68.11 | -5.25% | -1.36% | -0.69% |
| stressed | VOL | 183 | 936 | -5.91% | -57.0% | 15.1% | -3.78 | 0.44 | 7.9 | 164.86 / 164.86 | -6.87% | -2.00% | -0.97% |
| stressed | B2 | 183 | 936 | -8.09% | -78.9% | 13.8% | -5.72 | 0.58 | 122.7 | 2589.39 / 2589.39 | -9.67% | -2.25% | -1.03% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 183 | 4 | -1.168 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -11.53% | -0.00007 | -0.046 | -0.00015 |
| stressed | 183 | 4 | -1.931 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -21.90% | -0.00013 | -0.086 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-11T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 39.0 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
