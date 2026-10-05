# Paper sizing experiment PS1

Generated 2026-10-05T01:06:18.712Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-05T00:12:21.446Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 36 physical; 36 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 2.05 days; 13 scheduled decisions; coverage 46.2%; execution delay after the 4H close: median 16.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 5 closed intervals over 47.9 h; extended intervals 2.

Outcomes: executed 6; missed: stale: processed after close + max_delay 7

Execution states: completed 6

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 5 | 48 | 0.70% | 128.6% | 4.9% | 26.41 | 0.34 | 62.2 | 37.45 / 37.45 | -0.01% | -0.01% | -0.01% |
| ordinary | VOL | 5 | 48 | 0.93% | 168.9% | 6.4% | 26.44 | 0.45 | 81.8 | 49.25 / 49.25 | -0.02% | -0.02% | -0.02% |
| ordinary | B2 | 5 | 48 | 1.79% | 324.1% | 9.7% | 33.31 | 0.90 | 234.6 | 141.44 / 171.51 | -0.03% | -0.03% | -0.03% |
| stressed | FIXED | 5 | 48 | 0.67% | 123.0% | 5.2% | 23.86 | 0.34 | 62.3 | 68.11 / 68.11 | -0.04% | -0.04% | -0.04% |
| stressed | VOL | 5 | 48 | 0.89% | 161.6% | 6.8% | 23.88 | 0.45 | 81.9 | 89.57 / 89.57 | -0.06% | -0.06% | -0.06% |
| stressed | B2 | 5 | 48 | 1.67% | 303.0% | 10.0% | 30.31 | 0.90 | 234.6 | 256.98 / 311.56 | -0.09% | -0.09% | -0.09% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 5 | 0 | 6.874 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 155.20% | 0.00170 | 0.672 | 0.00214 |
| stressed | 5 | 0 | 6.429 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 141.44% | 0.00155 | 0.609 | 0.00197 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-05T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 2.0 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
