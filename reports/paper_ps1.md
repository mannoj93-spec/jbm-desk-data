# Paper sizing experiment PS1

Generated 2026-11-26T20:28:09.616Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-26T20:28:04.269Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1638 physical; 1638 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 54.85 days; 330 scheduled decisions; coverage 82.7%; execution delay after the 4H close: median 21.6 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 272 closed intervals over 1316.1 h; extended intervals 15.

Outcomes: executed 273; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 43

Execution states: completed 273

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 272 | 1316 | -10.08% | -70.8% | 14.3% | -4.96 | 0.33 | 2.7 | 42.58 / 42.58 | -13.01% | -1.73% | -0.93% |
| ordinary | VOL | 272 | 1316 | -11.46% | -81.0% | 15.6% | -5.20 | 0.39 | 7.0 | 110.14 / 110.14 | -14.01% | -2.00% | -1.03% |
| ordinary | B2 | 272 | 1316 | -13.45% | -96.2% | 15.3% | -6.28 | 0.49 | 101.6 | 1637.33 / 1642.77 | -16.76% | -2.24% | -1.13% |
| stressed | FIXED | 272 | 1316 | -10.12% | -71.0% | 14.3% | -4.98 | 0.33 | 2.7 | 77.42 / 77.42 | -13.02% | -1.73% | -0.93% |
| stressed | VOL | 272 | 1316 | -11.54% | -81.6% | 15.6% | -5.24 | 0.39 | 7.0 | 200.14 / 200.14 | -14.06% | -2.00% | -1.03% |
| stressed | B2 | 272 | 1316 | -14.61% | -105.1% | 15.3% | -6.86 | 0.49 | 101.8 | 2923.25 / 2933.00 | -17.75% | -2.25% | -1.14% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 272 | 6 | -1.080 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -15.15% | -0.00008 | -0.066 | -0.00014 |
| stressed | 272 | 6 | -1.628 | unavailable: 6 complete block(s) of 42 intervals; PS1 needs 10 | -23.50% | -0.00013 | -0.101 | -0.00019 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-26T20:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 54.9 days, 6 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
