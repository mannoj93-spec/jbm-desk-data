# Paper sizing experiment PS1

Generated 2026-10-03T01:02:17.566Z by ps1-job-3.0.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-03T00:20:25.236Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Launched at decision 2026-10-03T00:00:00Z; 0.04 days; 1 scheduled decisions; coverage 100.0%; execution delay after the 4H close: median 20.4 min, max 20.4 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 0 closed intervals over 0.0 h; extended intervals 0.

Outcomes: executed 1

Execution states: completed 1

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 0 | 0 | — | — | — | — | — | — | 0.00 / 37.45 | 0.00% | — | — |
| ordinary | VOL | 0 | 0 | — | — | — | — | — | — | 0.00 / 49.25 | 0.00% | — | — |
| ordinary | B2 | 0 | 0 | — | — | — | — | — | — | 0.00 / 77.80 | 0.00% | — | — |
| stressed | FIXED | 0 | 0 | — | — | — | — | — | — | 0.00 / 68.11 | 0.00% | — | — |
| stressed | VOL | 0 | 0 | — | — | — | — | — | — | 0.00 / 89.57 | 0.00% | — | — |
| stressed | B2 | 0 | 0 | — | — | — | — | — | — | 0.00 / 141.50 | 0.00% | — | — |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 0 | 0 | — | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | — | — | — | — |
| stressed | 0 | 0 | — | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | — | — | — | — |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-03T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 0.0 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
