# Paper sizing experiment PS1

Generated 2026-10-30T16:26:41.665Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-30T16:26:38.518Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 912 physical; 912 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 27.69 days; 167 scheduled decisions; coverage 91.0%; execution delay after the 4H close: median 19.2 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 151 closed intervals over 664.1 h; extended intervals 6.

Outcomes: executed 152; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 1

Execution states: completed 152

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 151 | 664 | -2.87% | -38.4% | 11.6% | -3.32 | 0.33 | 4.5 | 37.45 / 37.45 | -3.74% | -1.36% | -0.71% |
| ordinary | VOL | 151 | 664 | -4.01% | -54.0% | 16.3% | -3.32 | 0.46 | 10.1 | 82.98 / 82.98 | -5.23% | -2.00% | -1.01% |
| ordinary | B2 | 151 | 664 | -3.58% | -48.0% | 14.7% | -3.27 | 0.52 | 133.4 | 1127.69 / 1127.69 | -5.34% | -1.31% | -0.89% |
| stressed | FIXED | 151 | 664 | -2.90% | -38.8% | 11.6% | -3.36 | 0.33 | 4.5 | 68.11 / 68.11 | -3.74% | -1.36% | -0.71% |
| stressed | VOL | 151 | 664 | -4.08% | -54.9% | 16.3% | -3.38 | 0.46 | 10.1 | 150.85 / 150.85 | -5.25% | -2.00% | -1.01% |
| stressed | B2 | 151 | 664 | -4.45% | -60.0% | 14.7% | -4.09 | 0.52 | 133.5 | 2020.94 / 2020.94 | -6.08% | -1.31% | -0.89% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 151 | 3 | 0.055 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | 5.94% | 0.00003 | 0.024 | -0.00005 |
| stressed | 151 | 3 | -0.714 | unavailable: 3 complete block(s) of 42 intervals; PS1 needs 10 | -5.14% | -0.00003 | -0.021 | -0.00011 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-30T16:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 27.7 days, 3 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
