# Paper sizing experiment PS1

Generated 2026-11-08T08:23:17.736Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-08T08:23:13.799Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1014 physical; 1014 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 36.35 days; 219 scheduled decisions; coverage 77.2%; execution delay after the 4H close: median 19.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 168 closed intervals over 872.0 h; extended intervals 8.

Outcomes: executed 169; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 36

Execution states: completed 169

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 168 | 872 | -3.53% | -36.1% | 11.0% | -3.27 | 0.33 | 3.5 | 37.45 / 37.45 | -4.30% | -1.36% | -0.72% |
| ordinary | VOL | 168 | 872 | -4.88% | -50.2% | 15.5% | -3.24 | 0.45 | 8.4 | 90.69 / 90.69 | -5.84% | -2.00% | -1.02% |
| ordinary | B2 | 168 | 872 | -5.66% | -58.5% | 14.1% | -4.16 | 0.59 | 122.0 | 1344.41 / 1344.41 | -7.41% | -2.24% | -1.06% |
| stressed | FIXED | 168 | 872 | -3.56% | -36.4% | 11.0% | -3.30 | 0.33 | 3.5 | 68.11 / 68.11 | -4.30% | -1.36% | -0.72% |
| stressed | VOL | 168 | 872 | -4.95% | -51.0% | 15.5% | -3.29 | 0.45 | 8.4 | 164.86 / 164.86 | -5.87% | -2.00% | -1.02% |
| stressed | B2 | 168 | 872 | -6.69% | -69.6% | 14.1% | -4.95 | 0.59 | 122.0 | 2411.06 / 2411.06 | -8.27% | -2.25% | -1.06% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 168 | 4 | -0.912 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -8.31% | -0.00005 | -0.033 | -0.00013 |
| stressed | 168 | 4 | -1.658 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -18.57% | -0.00011 | -0.073 | -0.00020 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-08T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 36.3 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
