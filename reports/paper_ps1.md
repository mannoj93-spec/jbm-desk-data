# Paper sizing experiment PS1

Generated 2026-11-12T00:24:25.393Z by ps1-job-3.2.0 (PS1 v3, protocol sha256 d0e8c837be9c); source cutoff 2026-11-12T00:24:20.584Z.

> PAPER SIZING EXPERIMENT - simulated fills on captured quotes. Tests position sizing only; it does not test direction, does not execute, and authorizes no entry.

**Status: paused** · lifecycle paused (by job) · evidence class: descriptive · integrity: ok

Retired before launch, zero observations: `desk/research/ps1/protocol_v2_retired.json` (be015545540d), `desk/research/ps1/protocol_v1_retired.json` (00acb5bcf3e8)

Ledger rows: 1134 physical; 1134 verified, 0 quarantined, 0 excluded, 0 in progress.

Launched at decision 2026-10-03T00:00:00Z; 40.02 days; 241 scheduled decisions; coverage 78.4%; execution delay after the 4H close: median 20.0 min, max 60.6 min.

Time accounting: elapsed hours between fills; 8760 h/yr; drift and variance rates per hour (protocol v3); no interpolation; the interval opened by the latest trade is pending. 188 closed intervals over 960.1 h; extended intervals 10.

Outcomes: executed 189; missed: no run 6; missed: stale: processed after close + max_delay 8; no-rebalance: forecast unavailable 38

Execution states: completed 189

| scenario | arm | closed intervals | hours | net return | log return (ann.) | vol (ann.) | log-return Sharpe (ann.) | exposure | turnover (ann., closed) | costs closed / incl. open trade | max DD | worst (log) | ES5% (log) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ordinary | FIXED | 188 | 960 | -4.26% | -39.7% | 10.8% | -3.68 | 0.33 | 3.2 | 37.45 / 37.45 | -5.25% | -1.36% | -0.69% |
| ordinary | VOL | 188 | 960 | -5.64% | -53.0% | 14.9% | -3.55 | 0.43 | 7.7 | 90.69 / 90.69 | -6.84% | -2.00% | -0.97% |
| ordinary | B2 | 188 | 960 | -6.79% | -64.2% | 13.7% | -4.67 | 0.57 | 119.8 | 1443.72 / 1443.72 | -8.71% | -2.24% | -1.03% |
| stressed | FIXED | 188 | 960 | -4.29% | -40.0% | 10.8% | -3.70 | 0.33 | 3.2 | 68.11 / 68.11 | -5.25% | -1.36% | -0.69% |
| stressed | VOL | 188 | 960 | -5.71% | -53.7% | 14.9% | -3.59 | 0.43 | 7.7 | 164.86 / 164.86 | -6.87% | -2.00% | -0.97% |
| stressed | B2 | 188 | 960 | -7.89% | -75.0% | 13.7% | -5.47 | 0.57 | 119.9 | 2589.39 / 2589.39 | -9.67% | -2.25% | -1.03% |

| scenario | paired intervals | resampling blocks | Sharpe B2−VOL | 90% interval | ann. log return B2−VOL | mean log diff | standardized | B2−FIXED |
|---|---|---|---|---|---|---|---|---|
| ordinary | 188 | 4 | -1.127 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -11.20% | -0.00007 | -0.045 | -0.00014 |
| stressed | 188 | 4 | -1.875 | unavailable: 4 complete block(s) of 42 intervals; PS1 needs 10 | -21.30% | -0.00012 | -0.085 | -0.00020 |

Dependence: adjacent, non-overlapping intervals that are serially dependent (volatility clusters); 42-interval blocks are the bootstrap's resampling unit, not a measured effective sample size. Uncertainty: moving-block bootstrap of paired intervals (B2 and VOL (log return, dt_h) pairs resampled together), blocks of 42 intervals, 5,000 resamples, seed 20261003; 90% percentile interval of the duration-weighted Sharpe difference. Baseline: VOL (primary), FIXED (control).
Open interval since 2026-11-12T00:00:00Z: pending - not marked until the next executed rebalance.
Checkpoints: C1 after 180 days with ≥10 blocks (recorded: False); C2 after 365 days with ≥20 blocks (recorded: False). Owner: operator (paper_ps1.py checkpoint C1|C2 "<note>"); the job never records one. Progress: 40.0 days, 4 complete block(s).

Simulated fills on captured quotes; not executions. Sizing only - no direction is tested. No status here is a trading edge or an entry endorsement.
