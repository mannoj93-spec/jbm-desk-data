# Paper sizing experiment PS1

Generated 2026-11-07T20:35:24.877Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-07T20:06:35.374Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1002 physical; 1002 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 35.86 days; 216 scheduled decisions; coverage 77.3%; execution delay after the 4H close: median 19.3 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 166 closed intervals over 859.8 h; extended intervals 7.

Outcomes: executed 167; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 35

Execution states: completed 167

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 166 | 860 | -3.57% | -37.0% | 11.1% | -3.34 | 0.33 | 3.5 | 37.45 / 37.45 | -4.30% | -1.36% | -0.72% |
| ordinary | VOL | 166 | 860 | -4.92% | -51.4% | 15.6% | -3.30 | 0.45 | 8.5 | 90.69 / 90.69 | -5.84% | -2.00% | -1.02% |
| ordinary | B2 | 166 | 860 | -5.75% | -60.3% | 14.2% | -4.26 | 0.59 | 119.0 | 1294.63 / 1315.16 | -7.41% | -2.24% | -1.06% |
| stressed | FIXED | 166 | 860 | -3.60% | -37.3% | 11.1% | -3.37 | 0.33 | 3.5 | 68.11 / 68.11 | -4.30% | -1.36% | -0.72% |
| stressed | VOL | 166 | 860 | -4.99% | -52.2% | 15.6% | -3.35 | 0.45 | 8.5 | 164.86 / 164.86 | -5.87% | -2.00% | -1.02% |
| stressed | B2 | 166 | 860 | -6.74% | -71.1% | 14.1% | -5.03 | 0.59 | 119.1 | 2321.49 / 2358.43 | -8.27% | -2.25% | -1.06% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 166 | 3 | -0.963 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -8.96% | -0.00005 | -0.035 | -0.00014 |
| stressed | 166 | 3 | -1.685 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -18.92% | -0.00011 | -0.074 | -0.00020 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-07T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 35.9 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
