# Prospective research streams (repo 2.20; maintained in 2.21 and 2.22)

Three additions, each separately versioned and prospective from its first registration. None changes the range
model, contract RC1D, any registered forecast, score, fit, lab design, evaluation version or research clock.
Workflow: [`.github/workflows/research-streams.yml`](../.github/workflows/research-streams.yml). Records live under
`streams/`; reports under `reports/`.

| Stream | What it asks | Code | Records | Report |
|---|---|---|---|---|
| Companion B1 (`rc1d-b1`, companion-1.2.0) | How much of B2's range accuracy comes from DVOL? B2 vs B1 (same model without the DVOL term) beside B2 vs B0 | `desk/companion_job.py` | `streams/rc1d-b1/` | [`reports/companion_b1.md`](../reports/companion_b1.md) |
| Paper sizing PS1 (protocol PS1 v3, ps1-job-3.0.0) | Does sizing a synthetic BTC spot long by the B2 4h forecast beat trailing-volatility sizing after costs? | `desk/paper_ps1.py` | `streams/ps1/` | [`reports/paper_ps1.md`](../reports/paper_ps1.md) |
| Stage log (stream-ops-1.1.0) | Did every required stage of this run complete with its outputs? | `desk/stream_ops.py` | `streams/ops/` | the workflow verdict and step summary |
| Feasibility (feasibility-1.1.0) | Can each active hypothesis realistically accumulate evidence, and what limits it? | `feasibility.py` | none (read-only) | [`reports/feasibility.md`](../reports/feasibility.md) |

Forecast accuracy (RC1D, companion), simulated sizing performance (PS1) and demonstrated live decision
performance are three different things. The first two are measured here; the third is not measured anywhere in
this repository, and no status in these reports is a trading edge or an entry endorsement.

**Common report fields (2.22).** Every report carries `report`, `schema`, `generated_utc`, `source_cutoff_utc` (the
latest observation it is built from), `evidence_class`, `integrity` and `lifecycle` (feasibility: "not applicable").
Freshness is judged by `source_cutoff_utc`: a new generation time never makes old inputs fresh.

## Companion B1

- **Why.** RC1D registers B2 and B0 only, and its strict validator expects exactly those model identities, so the
  frozen contract cannot hold a third model. B1 is O21's middle step: HAR range terms plus weekend shares and the
  release count, without the DVOL-implied sigma.
- **Fit.** Monthly, after the RC1D fit for the month exists, on the same retained history chain, with the same
  cutoff (`range_model.fit`: rows whose target closed at or before the month start). `streams/rc1d-b1/fits/`.
  Each fit records its last training target and the RC1D fit's hash.
- **Forecast.** For each RC1D decision and horizon the job reads the registered RC1D record (manifest hash),
  its retained input bundle (content hash), and takes the features that bundle froze for that window: the same
  decision, snapshot, calendar terms and window. Point = exp(OLS value) in ln(high/low) units (loss-bearing);
  q10/q50/q90 from the fit residuals. Id `rc1d-b1-<h>-<decision>`, referencing `rc1d_id`, `snapshot_hash`,
  `start_utc`, `horizon_utc`.
- **Prospective rule.** Computed only while at least 120 s remain before the window start; confirmed by hash on
  `origin/main`; eligible only if prepared and confirmed before the start. A late or missing companion is recorded
  as missed and never computed on a later run.
- **Scoring.** When the RC1D record for the same window is scored, `range_contract.losses` is applied to the B1
  point with the realized range that record carries: the same window, loss function and point rule.
- **Integrity (1.1.0).** Each confirmation stores a binding: the forecast file's hash, decision time, preparation and
  window-start times, version (stream, job, model, fit), input snapshot (RC1D id, frozen-record hash, snapshot hash),
  contract, confirmation time and commit, and the binding's own hash. Scoring verifies the file against the registry
  and the binding; reporting re-verifies every scored file. A mismatch is recorded in `streams/rc1d-b1/integrity.jsonl`
  and the record is excluded; nothing is overwritten. The three 2026-10-01T00:00Z confirmations predate bindings and
  are verified against the registry hash and their own fields (labelled "legacy confirmation"; no binding is
  fabricated for them).
- **One verified path (1.2.0).** Scoring and evaluation both go through `verified_pair`: the forecast against the
  hash recorded at registration and the confirmation binding; the RC1D outcome against original records (the score
  row names the manifest's frozen forecast, its evidence file hashes to the value recorded at scoring, the realized
  range recomputes from that evidence, the B2/B0 losses recompute from the frozen forecast); and the B1 loss
  recomputed from both. A cached score row is re-validated on every consumption (`inputs_sha256` binds new rows to
  their inputs). Any failure in a horizon withholds every performance figure for that horizon - differences,
  win counts, effect sizes and intervals - while counts and diagnostics stay visible; the report stage then fails.
- **Report.** Per horizon: RC1D windows scored since the stream started, verified pairs, missing, late, unscored and
  integrity-excluded companions; overlap from the actual `[start, end)` windows of the verified pairs (how many
  overlap another, and the largest disjoint subset - a description of dependence that selects nothing; every valid
  pair stays in the registered analysis); B2−B1, B2−B0 and B1−B0 on the same windows with generic keys (`first`,
  `second`, `first_better`, `ties`, `first_worse`; schema `companion-eval-2`), relative MAE reduction, standardized
  difference, the uncertainty method, and the rc1d-eval-1 bootstrap interval only from 10 resampling blocks of 42
  decisions (a device for dependence, not a measured effective sample size).
  Evidence class: `descriptive` below the block minimum, at most `exploratory` above it (no pre-registered decision
  threshold exists), `unavailable` with no scored pair, `retired` once terminated.

## Paper sizing experiment PS1

The frozen protocol is [`desk/research/ps1/protocol.json`](../desk/research/ps1/protocol.json), PS1 v3 (sha256
`d0e8c837…`, recorded in `paper_ps1.py`; the job refuses to run on any drift). v1 (`00acb5bc…`) and v2 (`be015545…`)
were retired before launch with no decision, quote or execution recorded and are preserved byte-identical as
`protocol_v1_retired.json` and `protocol_v2_retired.json`; v2 had been approved on main (Oct 1) and never launched.
v3 changes the unequal-duration variance estimator and the cost/turnover scope, states the Sharpe as a log-return
Sharpe, and adds the verified consumption path, launch reconciliation, the expired-deadline pause rule and checkpoint
records. The question, arms, formulas, calibration, costs, start rule, missing-data rules, checkpoint timing and
evidence thresholds are v1's. Summary:

- **Instrument and policy.** A synthetic, unlevered BTCUSDT spot long on Binance. At every 4H decision three arms
  set a target weight - FIXED (constant), VOL (trailing 42-bar Parkinson sigma) and B2 (the registered RC1D 4h
  point) - each as `min(1, sigma* / sigma_hat)` at a 15% annualized risk target. Same decisions, same direction,
  same entry/exit/rebalance rule (trade only outside a 0.05 weight band). Primary comparison: B2 vs VOL. FIXED is
  a control.
- **Calibration.** `desk/research/ps1/calibrate.py` on retained history 2024-09-23 to 2026-09-23 (labelled
  training/calibration; not a holdout): k² = mean(r²/x²) per arm, the unconditional 4H return scale for FIXED.
  Range is not a standard deviation: the calibrated k for the range forecast (0.799) is used instead of the
  Brownian 0.627. No return, cost or turnover statistic entered any choice. No updates during PS1 v1.
- **Timing.** A decision becomes executable when its record is confirmed on `origin/main` (and after the RC1D
  forecast's own availability). Only a Binance spot depth quote requested after that instant is eligible; never an
  earlier quote, a candle or a retrospective quote. Recorded: decision close (data cutoff), the RC1D forecast's
  preparation, confirmation and window start, input retrieval times, decision computation start/end, the
  confirmation, the intended execution time, the quote's request/receipt times, HTTP Date and lastUpdateId, and
  the modeled fill time. GitHub start delays are recorded, not assumed away.
- **Quote validation (v2).** Every price and size a decimal string parsing to a finite number above zero (NaN, inf,
  empty, zero, negative and non-string values are rejected; unknown liquidity is never treated as available); at
  least 5 levels per side, strictly ordered, not crossed or locked; `lastUpdateId` an integer; the source names
  `symbol=BTCUSDT`; receipt after request and within 10 s of it; HTTP Date, when present, within 120 s of receipt.
  A failing quote is recorded with its reasons and is ineligible.
- **Confirmation binding (v2).** Each confirmation stores the decision row's hash, decision time, version (protocol,
  protocol hash, job), input snapshot (RC1D id, frozen-record hash, snapshot hash), contract, confirmation time and
  commit, plus the binding's hash. Execution and reporting recompute it; a mismatch excludes the decision, leaves the
  rows as found and is recorded in `streams/ps1/integrity.jsonl`.
- **Atomic execution (v2).** Execution id `<decision>#x<quote request ms>`. Before any ledger row the job records an
  immutable snapshot (decision, binding and quote hashes, prior ledger state and its hash, protocol hash) in
  `streams/ps1/execution_states.jsonl`, then writes all six rows in one atomic file replacement and records
  `completed` with the rows' hash. States: pending, running, completed, failed, partially_written, recovered. Only
  completed and recovered sets enter the ledger and the metrics, and a set whose rows no longer match its hash
  withholds the metrics. An interrupted execution is rebuilt from its snapshot (never a new quote): no rows written →
  `recovered` under its own id; some rows written → those rows stay in place, the execution is `partially_written`,
  and the full set is rebuilt under `<id>~r1`; a snapshot that no longer verifies → `failed`, the decision is a missed
  execution. A decision with any execution state is never executed again.
- **Verified consumption (v3).** Execution, recovery and reporting read the ledger only through `verify_chain`: per
  execution, in fill order - intact snapshot, protocol hash, decision row as snapshotted, present confirmation whose
  binding the decision reproduces and which the snapshot bound, quote as snapshotted and still eligible on
  re-validation, predecessor state equal to the verified ledger before it, exactly the six arm/scenario rows, and
  rows reproducible from the snapshot. Missing evidence is a failure, and a failed execution invalidates every later
  one. Recovery runs the same checks before writing. Any failure withholds every performance figure (arms, paired
  differences, win counts, intervals) and makes `execute` and `report` exit with class `error`.
- **Launch reconciliation (v3).** After the six rows and `completed`, `reconcile` derives `launch.json` and the
  lifecycle activation from the earliest verified execution (its decision and its fill time), idempotently on every
  pass; an interruption anywhere after the row write converges to what a clean run writes. A retry never trades
  again, fetches a replacement quote or uses its own time; a conflicting launch record is flagged, not overwritten.
- **Fills and costs.** Bid/ask walked through 20 captured levels, plus slippage; fee on the filled notional.
  Ordinary 10 bp fee + 1 bp slippage; stressed 10 bp + 10 bp; spread paid in both. Funding: not applicable (spot).
  Cash is USDT at 0%; equity marked at mid before each trade; costs charged on the actual change in holdings.
  These are simulated fills, not executions.
- **Missing data.** Every rule applies to all arms together: no eligible forecast, no bundle, a stale decision
  (after close + 90 min) or no eligible quote means no arm rebalances. An interval stays open until the next
  executed rebalance; an open interval is pending and never marked with an invented price.
- **Time accounting (v3).** An interval runs from one fill to the next. Elapsed hours come from the recorded quote
  receipt times; a skipped or missed decision lengthens the interval (flagged `extended`, with its decision steps);
  nothing is interpolated and no intermediate return is created. Working model: independent increments
  r = μh + σ√h·e. Drift rate μ̂ = Σr / Σh; variance rate σ̂² = Σ((r − μ̂h)² / h) / (n − 1), unbiased for σ² under
  the model for any durations (v2's Σ(r − μ̂h)² / (Σh·(n−1)/n) was unbiased only for equal durations: 0.49σ² for
  4h and 24h). Annualized log return 8760μ̂, volatility √(8760σ̂²); the Sharpe is their ratio - a log-return
  Sharpe, with no numerical equivalence to v1 (simple returns) claimed. Serial dependence is left to the block
  bootstrap. Exposure = Σ(weight held × hours) / Σhours. Costs and turnover use the same closed scope (the trades
  that opened closed intervals); the latest trade's cost is shown separately and the open interval is never given a
  terminal fill.
- **Metrics.** Primary: SR(B2) − SR(VOL), duration-weighted annualized after-cost Sharpe, ordinary costs. Also net
  returns, annualized return, drawdown, turnover, exposure, realized volatility, worst interval and 5% expected
  shortfall (log), paired differences (Sharpe, annualized return, mean log return, standardized), all under stressed
  costs too. Lower exposure or return alone is never called an improvement. The report states the sample count,
  the independent unit (complete 42-interval blocks), the dependence warning, the uncertainty method and the
  baselines (VOL primary, FIXED control).
- **Evidence.** Moving-block bootstrap of paired (return, hours) intervals (42-interval blocks, 5,000 resamples), 90% interval,
  reported only from 10 blocks. Checkpoint C1 at 180 days (descriptive), C2 at 365 days: the first review at which
  "paper-supported (sizing, simulated)", "paper-unfavourable" or "paper-inconclusive" can be assigned. No status is
  a trading edge.
- **Checkpoints (v3).** C1 and C2 are owned by the operator: `python desk/paper_ps1.py checkpoint C1|C2 "<note>"`
  writes an immutable row to `streams/ps1/checkpoints.jsonl`, refused unless the days, blocks and integrity
  conditions are met; C2 applies the protocol's rule mechanically for that review. The job prints progress only and
  never records a checkpoint or changes the status by itself.
- **Start.** The first decision at or after 2026-10-03T00:00Z that the deployed workflow executes
  (`streams/ps1/launch.json`, derived from the earliest verified execution). v3 keeps the start rule; v1 and v2
  recorded nothing, so no clock moves. ps1-job-3.0.0 refuses to decide, execute or report on a ledger launched under
  another protocol: if v2 were to launch before v3 is deployed, the operator terminates v2 and v3 starts as a new
  stream with a new clock.

## Lifecycle (both streams)

States `proposed → approved → active ⇄ paused → terminated → archived`, recorded append-only in
`streams/<stream>/lifecycle.jsonl` (PS1 keyed by its protocol hash; the companion by `rc1d-b1/companion-1`, active
since its first registration).

| | PS1 | Companion |
|---|---|---|
| approved | the first production run after the protocol is on `main` records it (the operator's merge) | — (already active) |
| active | the first completed execution | since 2026-10-01 |
| paused | by the job when the last six scheduled decisions whose 90-minute deadline has passed were all unexecuted (a decision still in its window is pending and never counts; it keeps trying and resumes at the next verified execution), or by the operator (stops decisions and executions until the operator resumes) | by the operator |
| terminated | **operator only**: `python desk/paper_ps1.py lifecycle terminated "<reason>"`, or, from a phone, a file `streams/ps1/terminated.json` committed on GitHub | **operator only**: `companion_job.py lifecycle terminated "<reason>"` or `streams/rc1d-b1/terminated.json` |
| archived | operator only, after termination | operator only, after termination |

After termination no decision, forecast or execution starts; an execution in progress is recorded `failed` and writes
no ledger row; the open PS1 interval stays pending; companions frozen before termination are still scored; reports
keep running and label the stream (evidence class `retired` unless a checkpoint status was already assigned). No
lifecycle change deletes or rewrites a record. A terminated stream never restarts under the same key: a new protocol
version is a new stream with a new clock.

## Stage log and verdict

Every step of `research-streams.yml` runs through `desk/stream_ops.py run`, which appends to
`streams/ops/stages-YYYY-MM.jsonl`: run id and attempt, stage, required or optional, start and end times, status
(`completed`, `failed`, `skipped`), exit code, error tail, each declared artifact (exists, written by this stage,
sha256) and, for the test stage, test counts. A stage whose needed stage did not complete is `skipped` and its
command is not run. The final `verdict` step fails the workflow if any required stage failed, was skipped, was not
run, lost its artifact, or if the persist step failed. The only optional stage is the feasibility report; when it
does not complete the verdict says so and does not count it.

2.22: the stream jobs print one machine-readable line, `OUTCOME {"outcome", "class"}`, with class `done` (work
performed), `expected` (pre-launch, operator pause, nothing new, no newly matured observation, missing market data
under the protocol) or `error` (integrity failure or refusal); they exit 3 on `error`. Stages run with `--semantic`
fail on class `error` even at exit 0 and on a missing OUTCOME line. The verdict re-checks every recorded artifact
(present, same sha256) and, with `--check-persisted`, that the record paths are committed and the run's commit is on
`origin/main`. The job holds the `repo-write` queue for its whole run, so other writers wait meanwhile; the logged
stage span was 15-24 s on the first twelve production runs of 2.21 (queue wait is not logged). No narrowing of the
critical section is justified by that measurement.

Test counts are reported as ran (unittest's "Ran N", which includes skipped tests), executed (ran − skipped), passed,
failed, errors and skipped; "unavailable" means the suite produced no result (did not run or could not load).

## Evidence classes

`hypothesis` (registered, no observation), `descriptive` (collecting, below the uncertainty minimum or before a
checkpoint), `exploratory` (an interval exists but no pre-registered decision rule applies), `prospectively supported`
(a pre-registered rule met at its checkpoint on prospective data - for PS1 either direction of the C2 rule),
`inconclusive` (a checkpoint reached, neither rule met), `unavailable` (no usable data, or integrity failed),
`retired` (terminated before a classification). PS1 maps its protocol statuses onto these; neither stream can reach
`prospectively supported` before its rule exists and is met.

## Feasibility report

Read-only. For each lab design: coverage (hourly controls ÷ hours since registration), eligible observation
time, raw candidates and episodes, the module's recorded counters, rates, warm-up progress, checkpoint progress
and the limiting factor (time, absent events, missing data, infrastructure capability). Time-to-checkpoint is
printed only from five qualifying observations with a 90% Poisson interval; zero events give no ETA; a zero the
collection cannot observe is "not observable". lab-2.2 records exclusion reasons by name; per-reason counts are
shown only where a module recorded a counter, and adding them elsewhere would change evaluation versions, so it
is not done here. The report also covers the RC1D, companion and PS1 streams.

2.22: exposure is reported twice - calendar time since registration (reference only) and observable exposure (hours
with a selected hourly control, the lab's own coverage count, ÷ 24). Rates and ETAs use observable exposure only;
an unobservable design (E1) and a warm-up zero get a null rate, never 0.0; a design with recorded evidence during
warm-up (G1) reports that evidence beside its limitation.

TWAP (D1) and liquidity (E1) are addressed explicitly: D1 polls fixed-cohort `twapHistory` every 15 minutes, so
programs that start and finish between polls are first seen finished and excluded; observing starts would need an
event stream. E1 needs second-scale depth from the `stream/` recorder, which is not deployed. Neither is
commissioned here.
