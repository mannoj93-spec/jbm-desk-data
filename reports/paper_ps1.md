# Paper sizing experiment PS1

Generated 2026-10-12T01:10:19.908Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-12T00:17:55.097Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 282 physical; 282 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 9.05 days; 55 scheduled decisions; coverage 85.5%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 46 closed intervals over 216.0 h; extended intervals 3.

Outcomes: executed 47; missed: stale: processed after close + max_delay 8

Execution states: completed 47

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 46 | 216 | -0.35% | -14.1% | 8.6% | -1.64 | 0.34 | 13.8 | 37.45 / 37.45 | -2.01% | -0.60% | -0.51% |
| ordinary | VOL | 46 | 216 | -0.41% | -16.5% | 11.4% | -1.44 | 0.46 | 20.4 | 55.22 / 55.22 | -2.64% | -0.79% | -0.67% |
| ordinary | B2 | 46 | 216 | 0.46% | 18.6% | 13.3% | 1.40 | 0.64 | 170.3 | 463.22 / 463.22 | -3.04% | -0.96% | -0.76% |
| stressed | FIXED | 46 | 216 | -0.38% | -15.4% | 8.6% | -1.79 | 0.34 | 13.9 | 68.11 / 68.11 | -2.01% | -0.60% | -0.51% |
| stressed | VOL | 46 | 216 | -0.45% | -18.4% | 11.5% | -1.60 | 0.46 | 20.5 | 100.40 / 100.40 | -2.64% | -0.79% | -0.67% |
| stressed | B2 | 46 | 216 | 0.08% | 3.2% | 13.2% | 0.24 | 0.64 | 170.4 | 840.14 / 840.14 | -3.13% | -0.96% | -0.76% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 46 | 1 | 2.843 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 35.06% | 0.00019 | 0.172 | 0.00018 |
| stressed | 46 | 1 | 1.847 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 21.58% | 0.00012 | 0.107 | 0.00010 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-12T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 9.0 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
