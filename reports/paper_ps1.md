# Paper sizing experiment PS1

Generated 2026-10-14T20:18:19.942Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-10-14T20:18:18.057Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: collecting (descriptive)** · lifecycle active · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 384 physical; 384 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 11.85 days; 72 scheduled decisions; coverage 88.9%; execution delay after the 4H close: median 18.8 min, max 51.2 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 63 closed intervals over 284.0 h; extended intervals 3.

Outcomes: executed 64; missed: stale: processed after close + max_delay 8

Execution states: completed 64

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 63 | 284 | -1.09% | -33.7% | 11.1% | -3.02 | 0.34 | 10.5 | 37.45 / 37.45 | -2.01% | -0.84% | -0.70% |
| ordinary | VOL | 63 | 284 | -1.50% | -46.5% | 15.8% | -2.94 | 0.47 | 15.6 | 55.22 / 55.22 | -2.69% | -1.25% | -1.00% |
| ordinary | B2 | 63 | 284 | -0.43% | -13.2% | 14.6% | -0.90 | 0.59 | 153.4 | 548.30 / 560.80 | -3.04% | -0.96% | -0.84% |
| stressed | FIXED | 63 | 284 | -1.12% | -34.6% | 11.1% | -3.11 | 0.34 | 10.6 | 68.11 / 68.11 | -2.01% | -0.84% | -0.70% |
| stressed | VOL | 63 | 284 | -1.54% | -47.9% | 15.8% | -3.03 | 0.47 | 15.6 | 100.40 / 100.40 | -2.70% | -1.25% | -1.00% |
| stressed | B2 | 63 | 284 | -0.87% | -27.0% | 14.6% | -1.85 | 0.59 | 153.5 | 994.20 / 1016.82 | -3.13% | -0.96% | -0.84% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 63 | 1 | 2.042 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 33.38% | 0.00017 | 0.132 | 0.00011 |
| stressed | 63 | 1 | 1.181 | unavailable: 1 complete block(s) of 42 intervals; PS1 needs 10 | 20.97% | 0.00011 | 0.084 | 0.00004 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-10-14T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 11.8 days, 1 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
