# Paper sizing experiment PS1

Generated 2026-10-23T16:42:59.196Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-23T00:18:56.865Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 666 physical; 666 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 20.7 days; 125 scheduled decisions; coverage 88.8%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 110 closed intervals over 480.0 h; extended intervals 5.

Outcomes: executed 111; missed: no run 5; missed: stale: processed after close + max_delay 8; pending 1

Execution states: completed 111

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 110 | 480 | -1.37% | -25.2% | 10.5% | -2.40 | 0.34 | 6.3 | 37.45 / 37.45 | -2.23% | -0.84% | -0.61% |
| ordinary | VOL | 110 | 480 | -1.88% | -34.7% | 14.4% | -2.42 | 0.45 | 12.8 | 76.49 / 76.49 | -3.05% | -1.25% | -0.84% |
| ordinary | B2 | 110 | 480 | -1.19% | -21.9% | 14.0% | -1.56 | 0.54 | 141.5 | 875.17 / 887.95 | -3.34% | -0.96% | -0.78% |
| stressed | FIXED | 110 | 480 | -1.40% | -25.8% | 10.5% | -2.45 | 0.34 | 6.3 | 68.11 / 68.11 | -2.23% | -0.84% | -0.61% |
| stressed | VOL | 110 | 480 | -1.95% | -35.9% | 14.4% | -2.49 | 0.45 | 12.8 | 139.06 / 139.06 | -3.06% | -1.25% | -0.84% |
| stressed | B2 | 110 | 480 | -1.88% | -34.6% | 13.9% | -2.48 | 0.54 | 141.6 | 1565.52 / 1588.60 | -3.82% | -0.96% | -0.78% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 110 | 2 | 0.851 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 12.84% | 0.00006 | 0.057 | 0.00002 |
| stressed | 110 | 2 | 0.013 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 1.26% | 0.00001 | 0.006 | -0.00004 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-23T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 20.7 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
