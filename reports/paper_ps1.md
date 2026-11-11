# Paper sizing experiment PS1

Generated 2026-11-11T16:26:32.646Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-11T12:25:16.681Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1122 physical; 1122 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 39.69 days; 239 scheduled decisions; coverage 78.2%; execution delay after the 4H close: median 19.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 186 closed intervals over 948.1 h; extended intervals 9.

Outcomes: executed 187; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 38

Execution states: completed 187

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 186 | 948 | -4.30% | -40.6% | 10.8% | -3.77 | 0.33 | 3.2 | 37.45 / 37.45 | -5.25% | -1.36% | -0.69% |
| ordinary | VOL | 186 | 948 | -5.69% | -54.1% | 15.0% | -3.62 | 0.44 | 7.8 | 90.69 / 90.69 | -6.84% | -2.00% | -0.97% |
| ordinary | B2 | 186 | 948 | -6.84% | -65.4% | 13.7% | -4.76 | 0.58 | 121.3 | 1443.72 / 1443.72 | -8.71% | -2.24% | -1.03% |
| stressed | FIXED | 186 | 948 | -4.33% | -40.9% | 10.8% | -3.79 | 0.33 | 3.2 | 68.11 / 68.11 | -5.25% | -1.36% | -0.69% |
| stressed | VOL | 186 | 948 | -5.76% | -54.8% | 15.0% | -3.66 | 0.44 | 7.8 | 164.86 / 164.86 | -6.87% | -2.00% | -0.97% |
| stressed | B2 | 186 | 948 | -7.93% | -76.4% | 13.7% | -5.57 | 0.58 | 121.3 | 2589.39 / 2589.39 | -9.67% | -2.25% | -1.03% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 186 | 4 | -1.148 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -11.35% | -0.00007 | -0.045 | -0.00014 |
| stressed | 186 | 4 | -1.905 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -21.58% | -0.00013 | -0.085 | -0.00021 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-11T12:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 39.7 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
