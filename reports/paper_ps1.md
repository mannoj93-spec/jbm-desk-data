# Paper sizing experiment PS1

Generated 2026-10-05T16:19:16.990Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-05T16:19:16.278Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 60 physical; 60 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 2.68 days; 17 scheduled decisions; coverage 58.8%; execution delay after the 4H close: median 14.6 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 9 closed intervals over 64.0 h; extended intervals 2.

Outcomes: executed 10; missed: stale: processed after close + max_delay 7

Execution states: completed 10

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 9 | 64 | 0.21% | 28.4% | 9.0% | 3.14 | 0.34 | 46.4 | 37.45 / 37.45 | -0.50% | -0.39% | -0.39% |
| ordinary | VOL | 9 | 64 | 0.27% | 37.3% | 11.9% | 3.14 | 0.45 | 61.0 | 49.25 / 49.25 | -0.66% | -0.51% | -0.51% |
| ordinary | B2 | 9 | 64 | 1.10% | 149.9% | 14.3% | 10.51 | 0.79 | 211.5 | 171.51 / 181.13 | -0.67% | -0.51% | -0.51% |
| stressed | FIXED | 9 | 64 | 0.18% | 24.2% | 9.1% | 2.66 | 0.34 | 46.5 | 68.11 / 68.11 | -0.50% | -0.39% | -0.39% |
| stressed | VOL | 9 | 64 | 0.23% | 31.8% | 11.9% | 2.67 | 0.45 | 61.1 | 89.57 / 89.57 | -0.66% | -0.51% | -0.51% |
| stressed | B2 | 9 | 64 | 0.96% | 130.8% | 14.3% | 9.13 | 0.79 | 211.5 | 311.56 / 329.05 | -0.70% | -0.51% | -0.51% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 9 | 0 | 7.371 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 112.57% | 0.00091 | 0.454 | 0.00099 |
| stressed | 9 | 0 | 6.465 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 98.98% | 0.00080 | 0.401 | 0.00086 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-05T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 2.7 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
