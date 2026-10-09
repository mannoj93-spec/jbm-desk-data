# Paper sizing experiment PS1

Generated 2026-10-09T21:03:16.641Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-09T20:11:28.705Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 204 physical; 204 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 6.88 days; 42 scheduled decisions; coverage 81.0%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 33 closed intervals over 163.9 h; extended intervals 3.

Outcomes: executed 34; missed: stale: processed after close + max_delay 8

Execution states: completed 34

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 33 | 164 | -0.90% | -48.6% | 9.8% | -4.97 | 0.34 | 18.2 | 37.45 / 37.45 | -2.01% | -0.60% | -0.60% |
| ordinary | VOL | 33 | 164 | -1.23% | -66.2% | 12.9% | -5.12 | 0.45 | 26.9 | 55.22 / 55.22 | -2.64% | -0.79% | -0.79% |
| ordinary | B2 | 33 | 164 | -0.75% | -40.2% | 14.4% | -2.80 | 0.58 | 154.3 | 319.22 / 331.35 | -3.04% | -0.96% | -0.96% |
| stressed | FIXED | 33 | 164 | -0.94% | -50.2% | 9.8% | -5.14 | 0.34 | 18.2 | 68.11 / 68.11 | -2.01% | -0.60% | -0.60% |
| stressed | VOL | 33 | 164 | -1.27% | -68.6% | 12.9% | -5.30 | 0.45 | 26.9 | 100.40 / 100.40 | -2.64% | -0.79% | -0.79% |
| stressed | B2 | 33 | 164 | -1.01% | -54.1% | 14.3% | -3.78 | 0.58 | 154.4 | 579.16 / 601.14 | -3.13% | -0.96% | -0.96% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 33 | 0 | 2.320 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 25.94% | 0.00015 | 0.125 | 0.00005 |
| stressed | 33 | 0 | 1.521 | unavailable: 0 complete block(s) of 42 intervals; PS1 needs 10 | 14.48% | 0.00008 | 0.070 | -0.00002 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-09T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 6.9 days, 0 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
