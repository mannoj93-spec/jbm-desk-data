# Paper sizing experiment PS1

Generated 2026-10-22T08:19:49.336Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-22T08:19:46.165Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 648 physical; 648 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 19.35 days; 117 scheduled decisions; coverage 92.3%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 107 closed intervals over 464.0 h; extended intervals 4.

Outcomes: executed 108; missed: no run 1; missed: stale: processed after close + max_delay 8

Execution states: completed 108

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 107 | 464 | -1.03% | -19.6% | 10.7% | -1.84 | 0.34 | 6.5 | 37.45 / 37.45 | -2.23% | -0.84% | -0.61% |
| ordinary | VOL | 107 | 464 | -1.46% | -27.7% | 14.5% | -1.91 | 0.45 | 11.5 | 66.21 / 66.21 | -3.05% | -1.25% | -0.84% |
| ordinary | B2 | 107 | 464 | -0.78% | -14.9% | 14.1% | -1.05 | 0.55 | 145.4 | 869.46 / 875.17 | -3.34% | -0.96% | -0.78% |
| stressed | FIXED | 107 | 464 | -1.06% | -20.2% | 10.7% | -1.90 | 0.34 | 6.5 | 68.11 / 68.11 | -2.23% | -0.84% | -0.61% |
| stressed | VOL | 107 | 464 | -1.51% | -28.8% | 14.5% | -1.98 | 0.45 | 11.5 | 120.36 / 120.36 | -3.06% | -1.25% | -0.84% |
| stressed | B2 | 107 | 464 | -1.47% | -27.9% | 14.1% | -1.98 | 0.55 | 145.5 | 1555.22 / 1565.52 | -3.82% | -0.96% | -0.78% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 107 | 2 | 0.857 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 12.89% | 0.00006 | 0.056 | 0.00002 |
| stressed | 107 | 2 | -0.002 | unavailable: 2 complete block(s) of 42 intervals; PS1 needs 10 | 0.84% | 0.00000 | 0.004 | -0.00004 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-22T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 19.3 days, 2 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
