# Market studies v1

This is the operational expansion approved after PR #50. It preserves PS1, RC1D, the lab's frozen evaluation versions and their historical evidence. New records live in `streams/market-studies/v1/`; the report is `reports/market_studies.md` and its detailed JSON companion.

## Registration is not launch

Merging this revision authorizes the frozen protocol in `research_tools/market_studies/protocol.json`. The **Market studies** workflow runs after Collector and Range forecasts, with a quarter-hour fallback. It checks out main, passes the study tests, records the protocol and implementation hashes, and publishes them. Only after fetching and verifying their exact bytes on origin/main does it activate the next UTC-hour opportunity. Git author timestamps never establish availability.

Each forecast and its daily training artifact must be observed on main before the forecast deadline. Confirmation binds the exact record hash. The report derives separate launch records from the first on-time confirmed forecast for each predictive study and the first verified execution for turnover. A missed window cannot be recreated later. The first deployment run therefore registers the studies; subsequent runs can launch them. Before merge none of these new studies is claimed to be running.

No runtime stage runs locally or on PR branches. Pure functions and temporary-directory fixtures are available for development. No historical data is relabelled as prospective evidence.

## Four experiments

| Study | Primary comparison | Operational rule |
|---|---|---|
| Turnover | Stressed-cost, duration-weighted log-return Sharpe of B2 with 10% band minus B2 with 5% band | Four independent arms: B2 5%/10%, VOL 5%/10%; each in ordinary/stressed cost scenarios, same newly captured quote. Quotes must be requested after confirmation. Every 4h opportunity counted. |
| Range calibration | 24h calibrated 80% interval score minus original B2 interval score | Daily trailing-30-day residual quantiles, minimum 40 eligible matured scores known before midnight. Point/q50 unchanged. Same source forecast/window; width and coverage reported together. |
| Continuous state | 4h Brier score of full model minus price/volatility baseline | Hourly panel with original availability limits; entry at hour+30m, publish before +25m. Fixed daily logistic fits, 200 minimum training rows. Joint sample across baseline, +flow, +positioning, +funding. |
| Paired spot/perpetual | 60m Brier score of combined flow minus perpetual-only flow at synchronized clock | Concurrent requests for the same five closed minutes; 5s receipt join limit. Three arms distinguish information from waiting; 15m secondary. Joint failures/abstentions and equal-minute entry clocks reported. |

Turnover uses the existing frozen PS1 calibration and book-walking arithmetic, but **does not replay PS1's executions as new evidence**. Eight account rows, the captured quote and prior-state hash are written as one atomic record. Execution and reporting reproduce that record before consuming it. Missed opportunities retain holdings; elapsed time extends to the next execution. Costs and turnover of the last open interval are reported separately; no terminal price is invented.

Range training verifies original frozen records and outcome evidence. State training uses only historical as-of rows and outcomes available before its daily cutoff. These earlier observations are explicitly discovery/training, not confirmation. Fit members, outcomes, hashes and parameters are retained once in a daily artifact. No test performance selects a feature group, coefficient, window or threshold.

A2 is a minute-bar probability experiment, not a subsecond execution study. Entry is the first minute at or after receipt+5m, with separate original and synchronized receipt clocks. Publication must precede the earliest entry. This buffer allows GitHub publication, and minute rounding will often make the clock arms identical; the equal-entry share exposes that limitation. Scores require a complete outcome path for all arms. There are no simulated trade-profit claims for A2 or the state model.

## Three data pilots

* **Options:** unchanged RR25 liquidity/maturity/delta filters; per-leg quote age, spread, OI, delta distance, missing-size state and rejection reasons; per-expiry usability, 7d/30d constant-maturity RR25 and properly paired hourly changes. The all-instrument source does not include quote sizes; they remain explicitly unavailable, not inferred from OI. No predictive admission or relaxed filter.
* **Liquidation revisions:** source-specific OKX hour windows at first capture, +1h, +6h and +18h. Maximum 20 pages and 45 seconds per vintage; all response bodies and pagination status retained in hash-verified compressed captures. Missing/empty/truncated source coverage is unknown rather than zero. Compare size, direction and fixed 1,000-contract eligibility changes. Revised data is a retrospective diagnostic, never substituted into first-seen predictors.
* **Exchange stress:** public Binance symbol ADL risk and insurance-pool snapshots every 30m, with raw responses, request/receipt/source clocks, missing states and rating variation. ADL risk is a low/medium/high rating, **not an ADL event count**. Insurance pools may cover several symbols. Capability collection does not authorize a return-prediction test.

Public API references: [Binance market-data endpoints](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data), [OKX public liquidation orders](https://www.okx.com/docs-v5/en/#public-data-rest-api-get-liquidation-orders). HTTP processes have a 12-second wall-clock kill and a 4 MiB response limit; spot and perpetual requests have independent clocks. New collectors do not mutate the legacy collector or reset its evaluation identities.

## Interpretation and operations

Every scheduled opportunity stays in the denominator, including no run, missing source, warmup, joint abstention, late computation/publication and pending outcomes. Proper scores compare all arms on the same eligible observations. Neutral signal probabilities count in paired scores; source failures are reported separately. Blocks preserve scheduled missing positions, and no uncertainty interval is shown below the frozen minimum. Pilot records are never treated as independent predictive successes.

No automatic promotion is enabled. Turnover has 180-/365-day review checkpoints; its first possible support review needs 365 days, 20 blocks, a positive stressed primary interval, >=80% execution coverage, 10%-20% realized risk for both B2 arms and the drawdown guardrail. The other primary studies have a 180-day review floor plus their minimum blocks. Reviewing several primaries still requires multiplicity-aware judgement; a favourable descriptive chart alone is not support.

The workflow shares the repository-write queue, has a 12-minute job deadline, narrow writer permissions, and persists failure records before its final verdict. A failed required stage makes the workflow red. To pause new forecasts, paper execution and pilot requests, add `streams/market-studies/v1/paused.json` through a reviewed change; retained outcomes continue to be scored and reported. Delete that marker through review to resume. Do not edit protocol/implementation hashes in an active registration: changed research semantics require a new protocol version, directory and clock. Raw/evidence journals fail closed on broken chains or changed bindings.


## Operational recovery and diagnostics

The recovery dispatcher explicitly starts Market studies for each quarter-hour opportunity, with at most two
recovery attempts per slot. Main-branch successful or progressing runs suppress duplicate dispatches; failed or
stalled attempts can retry. Recovery-started range runs also explicitly dispatch studies after their source forecast
is confirmed and persisted, while the calibration deadline remains open. A study run created before that source
publication cannot suppress this follow-up. This avoids relying on workflow-run events from token-started runs.
The original forecast deadlines, first-seen inputs, and scoring populations are unchanged; missed slots stay missed.

`market_study_ops.py` is a separate, read-only diagnostic reader outside the frozen v1 implementation. Its `report`
command writes only `reports/market_study_health.md` and `.json`; its `check` command writes nothing and returns
nonzero for actionable alerts. The market-studies writer persists the reports, including an explicit integrity-failed
report if journal validation fails. The recovery workflow's independent `study-watch` job recomputes health from
main on its own clock, so a silent study workflow cannot hide behind an old report. A failed watch means an
operational problem, never an unsupported or failed research hypothesis.

Coverage uses the last 24 hours of opportunity times, after their deadlines and a five-minute persistence allowance.
Paired opportunities get the full possible 30-minute publication allowance; turnover gets 90 minutes, range/state
25, stress/liquidation captures 30, and options an hour to capture and persist. Pending outcomes are separate;
unscored eligible outcomes more than two hours past maturity remain a backlog even after leaving the coverage
window. No successful preparation for 45 minutes, two consecutive closed missed opportunities/capture times,
scoring backlogs, or invalid records raise alerts. Historical coverage below 80% is an operational warning, not a
change to the research protocol. A pause suppresses new-collection alerts but retains integrity and scoring checks.

The JSON also reports publication delays, calibration source-confirmation times, daily training readiness,
per-vintage liquidation coverage, and the time of the last successful capture. Raw missing-record placeholders
never count as captured market data. Paired diagnostics show unique entry times, repeated-entry groups, a largest
disjoint 60-minute subset and equal-clock frequency. The entry-grouped mean averages differences within each
shared entry before averaging across entries: it is a sensitivity diagnostic, not a replacement primary or an
independence claim. Options quality adds all-leg quote ages, spreads, delta distances, overlapping rejection
counts, selected-strike changes within expiry, and changes of interpolation expiries. These do not relax filters
or commission an options prediction experiment.

The dashboard's Data health view displays this operational report, expires it after 45 minutes on the viewer's
clock, and links to the original study results separately. Publication of the new health report triggers a dashboard
build directly, including when the study run was started by recovery. Missing reports remain unknown.
