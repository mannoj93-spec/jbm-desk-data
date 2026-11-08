# Paper sizing experiment PS1

Generated 2026-11-08T20:49:18.493Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-08T20:26:07.595Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1032 physical; 1032 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 36.87 days; 222 scheduled decisions; coverage 77.5%; execution delay after the 4H close: median 19.4 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 171 closed intervals over 884.1 h; extended intervals 8.

Outcomes: executed 172; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 36

Execution states: completed 172

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 171 | 884 | -3.53% | -35.6% | 10.9% | -3.26 | 0.33 | 3.4 | 37.45 / 37.45 | -4.30% | -1.36% | -0.72% |
| ordinary | VOL | 171 | 884 | -4.88% | -49.6% | 15.4% | -3.23 | 0.44 | 8.3 | 90.69 / 90.69 | -5.84% | -2.00% | -1.02% |
| ordinary | B2 | 171 | 884 | -5.68% | -58.0% | 14.0% | -4.15 | 0.59 | 120.9 | 1349.89 / 1362.76 | -7.41% | -2.24% | -1.06% |
| stressed | FIXED | 171 | 884 | -3.56% | -35.9% | 10.9% | -3.29 | 0.33 | 3.4 | 68.11 / 68.11 | -4.30% | -1.36% | -0.72% |
| stressed | VOL | 171 | 884 | -4.95% | -50.3% | 15.4% | -3.28 | 0.44 | 8.3 | 164.86 / 164.86 | -5.87% | -2.00% | -1.02% |
| stressed | B2 | 171 | 884 | -6.71% | -68.9% | 13.9% | -4.94 | 0.59 | 121.0 | 2420.88 / 2444.01 | -8.27% | -2.25% | -1.06% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 171 | 4 | -0.916 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -8.37% | -0.00005 | -0.033 | -0.00013 |
| stressed | 171 | 4 | -1.661 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -18.53% | -0.00011 | -0.073 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-08T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 36.9 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
