# Paper sizing experiment PS1

Generated 2026-10-26T20:20:44.257Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-26T20:20:40.711Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 774 physical; 774 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 23.85 days; 144 scheduled decisions; coverage 89.6%; execution delay after the 4H close: median 18.9 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 128 closed intervals over 572.0 h; extended intervals 6.

Outcomes: executed 129; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 129

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 128 | 572 | -1.90% | -29.4% | 10.1% | -2.91 | 0.34 | 5.3 | 37.45 / 37.45 | -2.68% | -0.84% | -0.58% |
| ordinary | VOL | 128 | 572 | -2.66% | -41.2% | 13.9% | -2.98 | 0.46 | 10.8 | 76.49 / 76.49 | -3.69% | -1.25% | -0.80% |
| ordinary | B2 | 128 | 572 | -2.53% | -39.2% | 13.9% | -2.81 | 0.54 | 136.6 | 1000.60 / 1000.60 | -4.28% | -0.99% | -0.81% |
| stressed | FIXED | 128 | 572 | -1.93% | -29.9% | 10.1% | -2.96 | 0.34 | 5.3 | 68.11 / 68.11 | -2.68% | -0.84% | -0.58% |
| stressed | VOL | 128 | 572 | -2.72% | -42.2% | 13.9% | -3.05 | 0.46 | 10.8 | 139.06 / 139.06 | -3.71% | -1.25% | -0.80% |
| stressed | B2 | 128 | 572 | -3.30% | -51.5% | 13.9% | -3.70 | 0.54 | 136.7 | 1791.85 / 1791.85 | -4.91% | -0.99% | -0.82% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 128 | 3 | 0.168 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 2.07% | 0.00001 | 0.010 | -0.00005 |
| stressed | 128 | 3 | -0.655 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -9.25% | -0.00005 | -0.043 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-26T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 23.8 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
