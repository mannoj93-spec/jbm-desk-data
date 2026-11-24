# Paper sizing experiment PS1

Generated 2026-11-24T00:28:40.622Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-24T00:28:34.228Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1536 physical; 1536 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 52.02 days; 313 scheduled decisions; coverage 81.8%; execution delay after the 4H close: median 21.4 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 255 closed intervals over 1248.1 h; extended intervals 15.

Outcomes: executed 256; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 43

Execution states: completed 256

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 255 | 1248 | -9.80% | -72.4% | 14.4% | -5.03 | 0.33 | 2.8 | 42.58 / 42.58 | -13.01% | -1.73% | -0.96% |
| ordinary | VOL | 255 | 1248 | -11.25% | -83.7% | 15.9% | -5.26 | 0.40 | 7.3 | 110.14 / 110.14 | -14.01% | -2.00% | -1.06% |
| ordinary | B2 | 255 | 1248 | -13.19% | -99.2% | 15.7% | -6.34 | 0.50 | 104.4 | 1605.79 / 1613.04 | -16.76% | -2.24% | -1.17% |
| stressed | FIXED | 255 | 1248 | -9.83% | -72.7% | 14.4% | -5.05 | 0.33 | 2.8 | 77.42 / 77.42 | -13.02% | -1.73% | -0.96% |
| stressed | VOL | 255 | 1248 | -11.33% | -84.4% | 15.9% | -5.30 | 0.40 | 7.3 | 200.14 / 200.14 | -14.06% | -2.00% | -1.06% |
| stressed | B2 | 255 | 1248 | -14.32% | -108.5% | 15.6% | -6.93 | 0.50 | 104.5 | 2866.66 / 2879.67 | -17.75% | -2.25% | -1.18% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 255 | 6 | -1.082 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -15.52% | -0.00009 | -0.066 | -0.00015 |
| stressed | 255 | 6 | -1.635 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -24.11% | -0.00013 | -0.102 | -0.00020 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-24T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 52.0 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
