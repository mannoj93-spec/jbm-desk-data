# Paper sizing experiment PS1

Generated 2026-10-30T08:22:43.623Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-30T08:22:39.120Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 900 physical; 900 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 27.35 days; 165 scheduled decisions; coverage 90.9%; execution delay after the 4H close: median 19.2 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 149 closed intervals over 656.0 h; extended intervals 6.

Outcomes: executed 150; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 150

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 149 | 656 | -2.61% | -35.4% | 11.6% | -3.05 | 0.33 | 4.6 | 37.45 / 37.45 | -3.74% | -1.36% | -0.71% |
| ordinary | VOL | 149 | 656 | -3.69% | -50.2% | 16.3% | -3.08 | 0.46 | 10.2 | 82.98 / 82.98 | -5.23% | -2.00% | -1.01% |
| ordinary | B2 | 149 | 656 | -3.31% | -45.0% | 14.8% | -3.04 | 0.53 | 134.0 | 1119.60 / 1127.69 | -5.34% | -1.31% | -0.89% |
| stressed | FIXED | 149 | 656 | -2.65% | -35.8% | 11.6% | -3.09 | 0.33 | 4.6 | 68.11 / 68.11 | -3.74% | -1.36% | -0.71% |
| stressed | VOL | 149 | 656 | -3.76% | -51.1% | 16.3% | -3.13 | 0.46 | 10.2 | 150.85 / 150.85 | -5.25% | -2.00% | -1.01% |
| stressed | B2 | 149 | 656 | -4.18% | -57.0% | 14.7% | -3.87 | 0.53 | 134.1 | 2006.37 / 2020.94 | -6.08% | -1.31% | -0.89% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 149 | 3 | 0.031 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 5.21% | 0.00003 | 0.021 | -0.00005 |
| stressed | 149 | 3 | -0.737 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -5.91% | -0.00003 | -0.024 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-30T08:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 27.3 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
