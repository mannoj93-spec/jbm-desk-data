# Paper sizing experiment PS1

Generated 2026-11-07T08:23:13.096Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-07T08:23:08.280Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 984 physical; 984 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 35.35 days; 213 scheduled decisions; coverage 77.0%; execution delay after the 4H close: median 19.3 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 163 closed intervals over 848.0 h; extended intervals 7.

Outcomes: executed 164; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 35

Execution states: completed 164

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 163 | 848 | -3.42% | -36.0% | 11.2% | -3.22 | 0.33 | 3.6 | 37.45 / 37.45 | -4.30% | -1.36% | -0.72% |
| ordinary | VOL | 163 | 848 | -4.77% | -50.5% | 15.7% | -3.21 | 0.45 | 8.6 | 90.69 / 90.69 | -5.84% | -2.00% | -1.02% |
| ordinary | B2 | 163 | 848 | -5.42% | -57.6% | 14.3% | -4.04 | 0.58 | 119.8 | 1286.33 / 1286.33 | -7.32% | -2.24% | -1.06% |
| stressed | FIXED | 163 | 848 | -3.45% | -36.3% | 11.2% | -3.25 | 0.33 | 3.6 | 68.11 / 68.11 | -4.30% | -1.36% | -0.72% |
| stressed | VOL | 163 | 848 | -4.84% | -51.3% | 15.7% | -3.26 | 0.45 | 8.7 | 164.86 / 164.86 | -5.87% | -2.00% | -1.02% |
| stressed | B2 | 163 | 848 | -6.41% | -68.4% | 14.2% | -4.81 | 0.58 | 119.8 | 2306.56 / 2306.56 | -8.17% | -2.25% | -1.06% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 163 | 3 | -0.824 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -7.12% | -0.00004 | -0.028 | -0.00013 |
| stressed | 163 | 3 | -1.544 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -17.14% | -0.00010 | -0.067 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-07T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 35.3 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
