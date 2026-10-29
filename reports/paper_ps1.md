# Paper sizing experiment PS1

Generated 2026-10-29T00:21:56.711Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-29T00:21:53.337Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 852 physical; 852 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 26.02 days; 157 scheduled decisions; coverage 90.5%; execution delay after the 4H close: median 19.1 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 141 closed intervals over 624.0 h; extended intervals 6.

Outcomes: executed 142; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 142

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 141 | 624 | -1.38% | -19.5% | 9.8% | -1.98 | 0.34 | 4.8 | 37.45 / 37.45 | -2.68% | -0.84% | -0.55% |
| ordinary | VOL | 141 | 624 | -1.89% | -26.8% | 13.5% | -1.98 | 0.46 | 9.9 | 76.49 / 76.49 | -3.69% | -1.25% | -0.76% |
| ordinary | B2 | 141 | 624 | -2.14% | -30.3% | 13.5% | -2.24 | 0.54 | 137.3 | 1093.01 / 1093.01 | -4.34% | -0.99% | -0.78% |
| stressed | FIXED | 141 | 624 | -1.41% | -19.9% | 9.8% | -2.02 | 0.34 | 4.8 | 68.11 / 68.11 | -2.68% | -0.84% | -0.55% |
| stressed | VOL | 141 | 624 | -1.95% | -27.6% | 13.5% | -2.04 | 0.46 | 9.9 | 139.06 / 139.06 | -3.71% | -1.25% | -0.76% |
| stressed | B2 | 141 | 624 | -2.99% | -42.7% | 13.5% | -3.16 | 0.54 | 137.4 | 1958.48 / 1958.48 | -5.00% | -0.99% | -0.78% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 141 | 3 | -0.265 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -3.56% | -0.00002 | -0.017 | -0.00005 |
| stressed | 141 | 3 | -1.120 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -15.02% | -0.00008 | -0.071 | -0.00012 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-29T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 26.0 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
