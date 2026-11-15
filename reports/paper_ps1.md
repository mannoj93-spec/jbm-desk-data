# Paper sizing experiment PS1

Generated 2026-11-15T05:28:57.295Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-15T04:24:52.193Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1236 physical; 1236 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 43.23 days; 260 scheduled decisions; coverage 79.2%; execution delay after the 4H close: median 20.4 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 205 closed intervals over 1036.1 h; extended intervals 12.

Outcomes: executed 206; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 40

Execution states: completed 206

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 205 | 1036 | -8.12% | -71.6% | 11.8% | -6.06 | 0.33 | 3.3 | 42.58 / 42.58 | -9.09% | -1.36% | -0.80% |
| ordinary | VOL | 205 | 1036 | -9.97% | -88.8% | 15.7% | -5.66 | 0.43 | 8.2 | 103.56 / 110.14 | -11.11% | -2.00% | -1.04% |
| ordinary | B2 | 205 | 1036 | -11.63% | -104.6% | 14.9% | -7.01 | 0.56 | 118.3 | 1543.56 / 1543.56 | -13.36% | -2.24% | -1.13% |
| stressed | FIXED | 205 | 1036 | -8.15% | -71.9% | 11.8% | -6.09 | 0.33 | 3.3 | 77.42 / 77.42 | -9.10% | -1.36% | -0.80% |
| stressed | VOL | 205 | 1036 | -10.05% | -89.5% | 15.7% | -5.71 | 0.43 | 8.2 | 188.25 / 200.14 | -11.15% | -2.00% | -1.04% |
| stressed | B2 | 205 | 1036 | -12.74% | -115.2% | 14.9% | -7.74 | 0.56 | 118.4 | 2755.16 / 2755.16 | -14.34% | -2.25% | -1.13% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 205 | 4 | -1.352 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -15.82% | -0.00009 | -0.064 | -0.00019 |
| stressed | 205 | 4 | -2.029 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -25.72% | -0.00015 | -0.103 | -0.00025 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-15T04:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 43.2 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
