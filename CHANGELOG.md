# Maintenance, revision 2.27 (crypto-desk 12.4.10 on the 12.4 release family) — 2026-10-05

**Base.** `main` at `b2298393` (2.26 plus data; no implementation change since PR #34). No research definition, model,
contract, `range-job-12.4.0`, PS1 protocol, calibration, cost, eligibility, deadline, forecast, score, execution or
missed-decision record changes. The 2.26 host-key repair, strict SSH checking, writer guard, production branch filter
and restored observations are kept unchanged.

| Finding (reproduced) | Verified cause | Change | Tests |
|---|---|---|---|
| **Runs created but never executed** (Oct 5 from ~18:55Z: jobs `runner_id` 0, no steps, cancelled; run conclusion "failure") | GitHub-hosted runner assignment (incident 3q1yb5m7ltvb) | `execution.py`: trigger accepted, runner assigned, steps executed, critical success, persisted and yield as separate facts; a never-started collector is a missed execution, not a persistence loss | `test_rev227.StageTests` (real job metadata) |
| **Dead attempts suppressed recovery** (a failed/never-started run counted as covering its slot) | `live()` = "not cancelled" | recovery 1.3.0 `progressing()`: success, in progress ≤ 40 min or queued ≤ 10 min; failed, never-started and long-queued runs do not suppress; ≤ 2 dispatches per slot / decision; never cancels | `test_rev227.RecoveryRetryTests`, `test_recovery` |
| **A failed record covered a slot; failed records made full coverage** | `covered()` and `cadence.coverage` counted any record | `cadence.critical_success` (one definition) for coverage, health, watchdog, recovery yield and acceptance; activity kept as a separately labelled heartbeat | `test_rev227.SharedSuccessTests`, `YieldTests` |
| **Yield exempted by title** | acceptance skipped titled recovery runs without proof | durable yield receipt (`state/recovery_yields.jsonl`, collector writer) naming slot, run and covering record hash; pre-receipt yields need equivalent job evidence | `test_acceptance.ExecutionTests` |
| **Fresh failures shown "within cadence"; monitor that never ran shown "detected a problem"; stale report called scheduler silence** | presentation used age only; heartbeat had no execution evidence | health 1.3.0: data freshness vs activity, 45-min target beside the stale limit, monitor job/step evidence; dashboard rows for data and activity; watchdog stale on persisted critical success; corrected wording | `test_rev227.HealthAndWatchdogTests`, `model.test.mjs` (18) |
| **PS1 acceptance false passes** (launch removed; corrupt actions, no executions; fills after the window) | expected set from records; permissive `ps1_ok` | acceptance 3.0.0 `ps1_evaluate`: launch/protocol/lifecycle validated first, expected decisions from launch + schedule, explicit valid outcomes, `paper_ps1.verify_chain`, deadline and cutoff enforced; real PS1 chain fixture | `test_acceptance.PS1Tests` (9) |
| **Lineage: owner workflow_run child unknown; bot child verified without parent; timer-corroborated counted unattended** | actor identity used as lineage | named parent in research-streams titles (event payload, `branches: [main]`), verified against the run list; pre-2.27 unique-parent inference excluding token-started runs; multihop and out-of-window roots; branch must be main; strict certification only with timer receipts | `test_acceptance.LineageTests` (8, real run metadata) |
| **Verdict not bound to its evidence** | only count/flag/time recorded | normalized Actions evidence hashed and saved (`--save-evidence`), offline replay (`--actions-evidence`, `--commit`), per-file hashes, code hashes, evidence cutoff via git commit time | `test_acceptance.BindingTests` (4) |
| **Independent pre-release review of acceptance 3.0** (6 false passes, binding gaps, crashes) | re-runs credited as scheduled; records not bound to their run; backdated/unvalidated lifecycle rows and bare no-rebalance rows resolved PS1 decisions; yield receipts not checked against their run; decision-time (not deadline) inclusion; unbounded cutoff; `storage.py` outside the code digest | re-run = person; record bound to its collect.yml run, once, in its lifetime; lifecycle transition chain + git availability before the deadline for operator excuses and no-rebalance; receipt inside its run and consistent with its jobs; deadline inclusion; publishing run's lineage for range decisions; cutoff ≤ end + 120 min; malformed evidence = insufficient | `test_acceptance.ReviewFindingTests` (7) and PS1 additions |
| **Research run 37359675540 outputs unpublished** (persist job never got a runner) | runner outage | artifact verified and preserved (`data/restored/research-37359675540/`), publication gate dry run passed, not merged (freeze-time honesty) | — |

# Maintenance, revision 2.26 (crypto-desk 12.4.9 on the 12.4 release family) — 2026-10-05

**Base.** `main` at `ad9df852` (2.25.1 plus data). No research definition, model, contract, `range-job-12.4.0`, PS1
protocol, clock, calibration, deadline, forecast, score, execution or missed-decision record changes.

| Finding (reproduced) | Verified cause | Change | Tests |
|---|---|---|---|
| **Persistence failed after successful work** (5 runs Oct 4 22:52 – Oct 5 10:55) | unauthenticated `api.github.com/meta` host-key lookup in `commit_push.sh` hit the 60/h shared-IP limit: "HTTP Error 403: rate limit exceeded" | `scripts/github_host_keys.py`: job token (`DESK_META_TOKEN` on all 9 persistence steps), retries honouring retry-after/reset within a 40 s share of the budget, key validation, reuse within the job; still strict host checking, fail closed | `test_host_keys` (14, incl. end-to-end through `commit_push.sh` against a mock server) |
| **Two failed collector runs' observations** | push failed (above) | artifacts 11322590457 / 11326693263 verified against GitHub digests; 13 forward-only rows kept byte-identical in `data/restored/` with a receipt; never counted as on time | `test_restore` (3) |
| **Acceptance gate passed a 1 h window, credited `critical_ok:false` records, checked people only in the collector** | gate design (2.25) | `service_acceptance` 2.0: >= 24 h completed windows only; persisted critical success; lineage verified against the run list; decisions expected from the schedule; persistence join; people and unknown lineage across the chain; verdict bound to commit, input hash and evidence; "at most 2 of 95" | `test_acceptance` (11) |
| **Human-started dispatcher's children counted as automated** | `source` alone decided | provenance 1.1.0: root lineage carried through every hop (`<root>:<label>[:<parent>]`), titles end "via <origin>"; human root = human-assisted | `test_recovery.LineageTests` |
| **Foreign-branch run suppressed main recovery** | listing without branch filter | runs listed with `branch=main`, `head_branch` kept, non-main or unstated runs ignored; malformed listings are errors | `test_recovery.BranchScopeTests` |
| **Monitor that ran and failed read as stale** | heartbeat used last success | health 1.2.0: heartbeat = last completed run, `last_result` separate; dashboard says "ran; detected a problem" | `test_health.MonitorHeartbeatTests`, `model.test.mjs` |
| **Monitor incident aging (verified, unchanged)** | 12 h window anchored to last_due, 75-min grace | fixed-clock fixtures: inclusive boundary 09:14/09:15, historical evidence kept, ongoing outage still fails, freshness/integrity/backlog independent | `test_monitor_aging` (6) |
| **Primary scheduling** | native 76% of collector slots since recovery; external timer 67/67 ticks | decision: external timer -> dispatcher is primary, native schedules a measured fallback; no workflow change for it (`docs/incidents/2026-10-03-native-schedule.md`) | — |

# Maintenance, revision 2.25.1 — 2026-10-04 (recovery chain to the research streams)

**Why.** The first production recovery cycle (Oct 4 20:41–20:47Z: dispatcher run 37233076237 started by a test run of the external
cron; collector, range and scoring runs started by `github-actions[bot]`) published the 20:00Z range decision eligibly,
but no "Research streams" run followed: a run started with the workflow token raises no `workflow_run` event. The
companion would have missed its window; the streams were dispatched by hand at 20:50:21Z (run 37233634940, recorded
as `human`), the companion registered eligibly and PS1 executed. No research rule, deadline or record changes.

| Change | Tests |
|---|---|
| `range.yml` (`actions: write`): a recovery run dispatches the research streams for its decision as soon as it has persisted (`recovery.py chain`, recovery-1.1.0; inputs trigger=recovery, origin `<range run>:range-recovery`) | `test_recovery.ChainTests` |
| Known, not changed: the research dashboard, also chained by `workflow_run`, refreshes on its own schedule only while recovery is active | — |

# Maintenance, revision 2.25 (crypto-desk 12.4.8 on the 12.4 release family) — 2026-10-04

**Base.** `main` at `af9b0868` (2.24.1; later commits since the Oct 4 review `bf947639` are data only). Nothing here
changes the range model, contracts RC1D/RC1, `range-job-12.4.0`, PS1 protocol v3 or its clock, calibration, statistical
rules, deadlines, registered forecasts, scores or any recorded execution. Missed decisions stay missed.

| Finding (reproduced) | Change | Tests |
|---|---|---|
| **Native schedule degraded.** 82 collector slots Oct 3 21:09 – Oct 4 17:50 UTC, 4 scheduled runs; range decisions Oct 4 00:00, 04:00, 12:00 arrived 3.19, 1.75, 3.48 h late and were refused; no queued, cancelled or failed collector run; no repository cause found (`docs/incidents/2026-10-03-native-schedule.md`) | `recovery.py` + `recovery.yml`: an externally triggered dispatcher starts collection, range publication, research streams and scoring when due and uncovered, inside the contracts' deadlines; recovery collector runs have their own concurrency group and yield when their slot is already collected | `test_recovery` (23): dropped and late native starts over a simulated day, queue/in-progress coverage, one dispatch per key, range window +8…+45 min and bounded retries, streams/PS1 deadline, scoring, permission/5xx/unavailable API, yield, provenance, wiring |
| **Provenance not recorded.** A collector record said only `trigger` | `provenance.py`; collector-2.8 records `provenance` (native-schedule / recovery authenticated by `github-actions[bot]` / human / chained); the dispatcher passes `origin` | same |
| **Health could not tell native cadence from service.** | `health-1.1.0`: `source` stays native; `source.service` automated continuity with its own gaps and `service_gap` incidents; `source.coverage_24h`; dispatcher monitor (`recovery.yml`, 45 min). `watchdog.py` fails on a service silence, warns on a native one; a person's run counts in neither. Dashboard rows for service and 24 h coverage | `test_recovery`, `test_health`, `test_rev26`, `model.test.mjs` |
| **Index leak in `commit_push.sh`.** An unrelated staged `collector.py` was committed and pushed with `data` | `DESK_WRITER` + `scripts/writers.json` + `scripts/push_guard.py`: staged changes and every outgoing commit checked before each push and after a rebase; deletions, symlinks, merges and release-manifest files refused | `test_push_guard` (12), `test_push_credential` (writer per step) |
| **Calendar copies vs. checksums.** `range_job` writes `desk/calendars/<sha>.csv`, which the release manifest scope included | scope excludes the content-addressed copies (self-verifying, `make_release.py check`); the range writer may add, never modify, them | `test_push_guard`, `test_checksums` |
| **PR enforcement overstated.** Docs said every change goes through a pull request; the ruleset has only the required `release` check | `docs/OPERATIONS.md` corrected; an import file adding a `pull_request` rule is delivered (operator choice; not applied) | review |
| **No stated acceptance target.** | `scripts/service_acceptance.py`: the 24 h target (≥ 97% of intervals with an automated stored run, longest gap ≤ 45 min, every range decision published, every PS1 decision resolved, no backlog, no person-started run), measured values reported, a partial window pending | `test_recovery` |
| **Receipt.** | `desk/deployments.jsonl`: PRs #29/#30 merged, release gate active, deploy-key persistence from a scheduled run, first eligible PS1 execution under 3.2.0 | release check |

# Maintenance, revision 2.24.1 — 2026-10-03 (push credential for the release gate)

**Why.** Importing the release-gate ruleset failed: GitHub rejects the GitHub Actions app as a bypass actor, so a
required check on `main` would have blocked every data push made with the workflow token. Release identity
(`desk/release.json`) is unchanged: no desk module, protocol or artifact changes.

| Change | Tests |
|---|---|
| `scripts/commit_push.sh` pushes over SSH with the deploy key in `DESK_DEPLOY_KEY` when set (host keys from `api.github.com/meta`; key removed at exit; `origin/<branch>` refreshed for the persistence check), else with the workflow token as before | `regression/test_push_credential.py` |
| The secret is passed to the nine persistence steps only (collector, range ×2, scoring, research streams ×2, research lab, weekly report, intake) | same (workflow scan) |
| Deploy-key pushes trigger push workflows: `fixtures.yml` skips `desk/inputs`, `desk/fits`; `release-check.yml` push also skips `registry/`, `tests/`, `desk/deployments.jsonl` | review |
| `docs/OPERATIONS.md` "Release gate": the deploy-key design, operator order, residual risk, phone edits under the gate | review |

# Maintenance, revision 2.24 (crypto-desk 12.4.7 on the 12.4 release family) — 2026-10-03

**Base.** `main` at `24e6dcaf` (2.23). Nothing here changes the range model, contracts RC1D/RC1, PS1 protocol v3, its
calibration, statistical methods, promotion criteria, registered forecasts, scores, the launch clock or any recorded
execution; earlier executions are reproduced under the job their snapshot records (3.0.0, 3.1.0).

| Finding (reproduced) | Change | Tests |
|---|---|---|
| **Unknown journal state ignored.** With two executions, the second's final state edited `completed` → `completd`: `ok=true`, integrity `verified`, 6 verified and 6 unaccounted rows; a third decision executed on balances that skipped the second (fixture; production records verify) | `history_problem()` validates every history on read (recognized state names, integer times, start at pending, allowed transitions, nothing after a terminal state, row counts on failed/partial, rows hash on completion); malformed journal rows are grouped and fail; conservation: physical rows must equal assigned rows; every journal reader guarded (ps1-job-3.2.0) | `TestJournalValidationOnRead` (10) |
| **Silence invisible after recovery.** No scheduled run of any workflow 11:17:56Z–13:26:49Z on Oct 3; the watchdog turned green on resumption; no record of the missed 12:00Z decisions survived | `health.py` (five separate questions, explicit clock, durable deduplicated `state/incidents.jsonl`, written by each collector run); `cadence.scheduled_gaps`; watchdog warns about recovered gaps for a day; range monitor lookback parameter (monitor-12.3.1); dashboard health panel; PS1 coverage as of its report plus later due decisions | `regression/test_health.py` (8), node tests |
| **Dashboard refresh.** `market.bars = [null]` passed validation, replaced the good snapshot, threw in `drawMarket()` and left Refresh disabled | finite-bar and timestamp validation; chart geometry staged for every period; post-commit rollback; chart failures contained; controls restored in `finally`; legacy report schemas keep their clock meanings | node tests, browser acceptance |
| **Required check could not be required.** `release-check.yml` skipped data-only pull requests | runs on every pull request | workflow review |
| **A late stale skip hid a missed decision** (found while re-verifying: the 12:00Z Range schedule arrived 2 h 57 min late and recorded `skipped`, which the health check treated as resolved) | a stale-skipped range decision is `missed: skipped` and recorded once | `test_health` |
| **Gate described as configured.** `release-check.yml` said a ruleset required it; none exists | comment corrected; `docs/OPERATIONS.md` "Release gate" gives the ruleset, its bot bypass, the probe procedure and the residual risk | review |

# Maintenance, revision 2.23 (crypto-desk 12.4.6 on the 12.4 release family) — 2026-10-03

**Base.** `main` at `dd5ca024` (reviewed snapshot), merged with `7444d65c`. 2.22 merged Oct 2 02:37Z (PR #26) and
production-observed (ten runs, every stage completed); the research dashboard merged Oct 2 19:06Z (PR #27). PS1 v3
launched at the Oct 3 00:00Z decision under ps1-job-3.0.0; 3.1.0 verifies that execution unchanged. Each item was reproduced before it was changed. Nothing here changes the range model, contracts
RC1D/RC1, `range_job.py`, any registered forecast, score, fit or bundle, the lab, the collector, PS1 protocol v3 or its
calibration; job versions record the code (ps1-job-3.1.0, companion-1.3.0, reader-12.4.6).

| Finding (reproduced) | Change | Tests |
|---|---|---|
| **PS1 ledger rows outside verification; duplicate execution.** With a second execution's state records removed, verification returned ok on 6 of 12 rows and a retry wrote 6 more (18) | `account()` reconciles ledger rows and states both ways (verified, recoverable, quarantined, excluded; anything else fails); a decision with any ledger row is never executed again; balances unavailable on failure; rows rebuilt under the snapshot's job | `TestLedgerReconciliation` |
| **Recovery overrode an operator pause.** A zero-row interruption then an operator pause: recovery wrote 6 rows and `launch.json` | bookkeeping (rows persisted) separated from completion (lifecycle-gated; held under operator pause, closed under termination); lifecycle re-read at the write boundary; the action taken is reported | `TestRecoveryLifecycleAuthority` |
| **Companion legacy downgrade.** A modern confirmation stripped of its binding (+1 ms) verified as legacy 1.0.0 | only the three Oct 1 00:00Z confirmations, pinned to their first-committed hashes, verify unbound | `TestCompanionBindingDowngrade` |
| **Exclusions invisible.** A failed zero-row recovery left `integrity.ok: true` with no reason on later runs | integrity `state`, `excluded_decisions`, `ledger_rows`; "excluded" schedule outcome; execute outcome lists exclusions | `TestHistoricalExclusions` |
| **Checksums.** README.md and .gitignore mismatched; 13 maintained files unlisted; no CI check | scope defined in `scripts/check_checksums.py`; manifest refreshed; `release-check.yml` | `regression/test_checksums.py` |
| **Clocks.** Companion `source_cutoff_utc` was scoring time; dashboard aged generation with a 6 h rule and labelled the index update a cutoff | named clocks (`processed_utc`, observation cutoff, outcome-window end); one freshness table; builder reads card cutoffs | `TestOverlapAndClocks2_23`, `model.test.mjs` |
| **Dashboard.** No companion integrity; intervals hidden; a malformed refresh replaced the good snapshot | integrity, exclusions and ledger accounting shown; intervals rendered; staged, validated refresh | `model.test.mjs`, browser acceptance |
| **Action runtimes** on node20 | setup-node v6, upload-pages-artifact v5, deploy-pages v5 (node24) | workflow review |
| **RC1D overlap** described theoretically | actual [start, end) diagnostics shared with the companion | `TestOverlapAndClocks2_23`, `test_ops` |

# Maintenance, revision 2.22 (crypto-desk 12.4.5 on the 12.4 release family) — 2026-10-02

**Base.** `main` at `dea47603` (2.21 merged Oct 1 01:26:51Z as `c805152d`; twelve production research-streams runs on
2.21 logged in `streams/ops/`, all stages completed). PS1 v2 approved on main, not launched (no decision, quote or
execution). Each item below was reproduced on 2.21 with an offline fixture before it was changed. Nothing here
changes the range model, contracts RC1D/RC1, `range_job.py`, any registered forecast, score, fit or bundle, the lab,
the collector or the PS1 calibration.

| Finding (reproduced on 2.21) | Change | Tests |
|---|---|---|
| **Integrity not verified on every consuming path.** Recovery wrote six rows and the launch before noticing an altered confirmation; an altered quote or a deleted confirmation after completion left `integrity.ok: true`; after corrupted confirmations the paired figures stayed; an altered companion confirmation and a cached companion B2 error of 0 were still paired (100% "improvement") | PS1: one verified path (`verify_chain`) for execution, recovery and reporting - snapshot, protocol, decision, present bound confirmation, quote re-validation, predecessor, six identities, reproducible rows; descendants of a failure fail; recovery validates before writing. Companion: one path (`verified_pair`) for scoring and evaluation, verifying the RC1D outcome against its evidence and re-validating cached scores. Any failure withholds every performance figure | `TestPS1VerifiedConsumption`, `TestCompanionVerifiedConsumption` |
| **Launch lost after a crash.** A crash at the launch write left rows, an active lifecycle and no launch; the report said "not launched" | `reconcile` derives launch and activation from the earliest verified execution, idempotently; a conflicting launch is flagged, not overwritten | `TestLaunchReconciliation` (interruptions after the row write, after completion, around the launch write, after activation) |
| **Green runs with failed semantics.** `execute` printed a refusal and exited 0; a deleted report after its stage still passed | machine-readable `OUTCOME` (done/expected/error), exit 3 on error; `--semantic` stages; the verdict re-checks artifact hashes and that the records reached `origin/main` | `TestSemanticOutcomesThroughTheWrapper` (real CLIs) |
| **Auto-pause never fired at the real cadence** (active at +28h50m after six expired misses) | only decisions past their deadline count | `TestAutoPauseCadence` (+20/+50/+65/+91 min, job resume, operator pause) |
| **Variance estimator biased for unequal durations** (expected 0.49σ² for 4h and 24h) | PS1 protocol v3 frozen before launch (v2 kept byte-identical): σ̂² = Σ((r−μ̂h)²/h)/(n−1); log-return Sharpe labelled; closed-scope costs/turnover | `TestUnequalDurationStatistics` (exact, simulation, invalid durations) |
| **Overlap from fixed ratios** (`n//1` said 3 disjoint 4h windows where the actual windows give 2) | overlap and largest disjoint subset from the verified windows; generic comparison keys (schema `companion-eval-2`) | `TestActualWindowOverlap` |
| **Feasibility semantics** (E1 rate 0.0; G1 "cannot qualify" beside a retained episode; calendar days as observable time) | capability, calendar and observable exposure separated; unobservable and warm-up rates null; G1 evidence reported with its limitation | report check |
| **Checkpoint ownership and the repo-write claim** | operator-reviewed immutable C1/C2 records; the "never waits while holding repo-write" claim removed and the logged span reported | `TestCheckpointRecords` |

Release tooling: `make_release.py` repo 2.22, base `dea47603`, `protocol_v2_retired.json` an artifact; `release.json` rewritten.

# Maintenance, revision 2.21 (crypto-desk 12.4.4 on the 12.4 release family) — 2026-10-01

**Base.** `main` at `8e8e3c14` (2.20 deployed: PR #24 merged Sep 30 23:47:50Z; first research-streams run 36795851380; first eligible companion registrations Oct 1 00:23Z).

**Purpose.** Make the evidence the research streams collect from now on trustworthy. Each item was reproduced on the deployed code before it was changed. Nothing here changes the range model, contracts RC1D/RC1, `range_job.py`, any registered forecast, score, fit or bundle, the lab, or the PS1 calibration. Shared modules are byte-identical, so the release family stays 12.4.

| Finding (reproduced on 2.20) | Change | Tests |
|---|---|---|
| **PS1 execution not atomic.** Six rows appended one at a time; an interruption after the first left 1 of 6 and the retry skipped the decision | ps1-job-2.0.0: an immutable snapshot, explicit states (`streams/ps1/execution_states.jsonl`: pending, running, completed, failed, partially_written, recovered), all six rows in one atomic replacement, a completion hash; recovery rebuilds from the snapshot only; partial rows stay as a record; duplicates refused | `TestAtomicExecution` |
| **PS1 time accounting.** Annualization assumed 4h per interval | PS1 protocol v2, frozen before launch (v1 never recorded an observation and is kept byte-identical as `protocol_v1_retired.json`): elapsed hours between fills, duration-weighted estimators on log returns, 8760 h/yr, hour-weighted exposure, extended intervals flagged, nothing interpolated | `TestTimeAccounting` |
| **Confirmations not bound.** A tampered confirmed companion was scored; a tampered PS1 weight was executed | integrity bindings (record hash, decision time, version, input snapshot, contract, confirmation time, commit) verified before execution, scoring and reporting; failures excluded and written to `integrity.jsonl`; originals untouched; companion-1.1.0 | `TestConfirmationIntegrity`, `TestCompanionIntegrity` |
| **Quote validation.** NaN size passed and filled | finite positive decimal strings, ordering, crossing, depth, update id, symbol, request/receipt and HTTP Date timing; the fill model refuses an invalid book | `TestQuoteValidation` |
| **No lifecycle.** `execute` and `report` ignored termination | `stream_util` lifecycle: proposed, approved, active, paused, terminated, archived; operator-only termination (CLI, or `terminated.json` committed from a phone); every stage checks it; no restart under the same key | `TestLifecycle` |
| **Workflow green with failed steps.** Steps were continue-on-error; only preflight failed the job | `desk/stream_ops.py` stage log (`streams/ops/stages-YYYY-MM.jsonl`) and a verdict step that fails on any failed, skipped, missing or artifact-less required stage or an unpersisted run | `TestWorkflowStages` |
| **Test counts.** "Executed" included skipped tests | ran, executed, passed, failed, errors, skipped and unavailable reported separately (`stream_ops.parse_counts`; the package's `check_package.py`; this record) | `TestStartupRunner` (package), `test_test_counts_are_reported_separately` |
| **Reports.** No independent-sample count, effect size or evidence class | companion: non-overlapping windows, overlap warning, relative MAE reduction, standardized difference, B1−B0, uncertainty method, class; PS1: block unit, dependence warning, Sharpe/return/standardized differences, baselines, class | report and dry-run checks |

Release tooling: `make_release.py` repo 2.21, base `8e8e3c14`, `stream_ops.py` repo-only, `protocol_v1_retired.json` an artifact; `release.json` rewritten.

# Research upgrade, revision 2.20 (crypto-desk 12.4.3 on the 12.4 release family) — 2026-09-30

**Base.** `main` at `89fde1a7` (2.19 deployed: PR #23 merged Sep 30 17:34Z; deployment rows `921264da`).

**Purpose.** Make decision-relevant evidence arrive sooner and false confidence harder to sustain. Better range
forecasts alone do not show an after-cost advantage, so 2.20 adds the smallest experiment that tests whether they
improve a concrete decision, a stronger forecast benchmark, and a report of which research can accumulate evidence
at all. Nothing here trades or authorizes a trade.

**Unchanged.** `range_model.py` (spec `ae6aa254…`), contracts RC1D/RC1 and their ids, `range_job.py`
(range-job-12.4.0), every registered forecast, score, fit, calendar and bundle, the lab's code, designs, evaluation
versions and research clocks, `range.yml`, `range-score.yml`, `range-monitor.yml`, the collector. Shared modules
are byte-identical, so the release family stays 12.4 (`release.json` `package`); the skill package documentation
moves to 12.4.3.

| Addition | What | Tests |
|---|---|---|
| **Companion B1** (`desk/companion_job.py`, companion-1.0.0, `streams/rc1d-b1/`) | B1 (HAR/calendar without DVOL) registered beside every RC1D batch: same decision, input snapshot, calendar terms and window, read from the RC1D record and bundle by hash. Monthly fit with the B2 fit's cutoff. Computed only 120 s or more before the window start and confirmed by hash on the remote; late = missed, never computed later. Scored with `range_contract.losses` on the realized range of the paired RC1D score. Report: B2 vs B1 beside B2 vs B0 on the same windows, rc1d-eval-1 block rules | `test_streams`: look-ahead, late registration, remote mismatch, missed-stays-missed, frozen-window features, RC1D files byte-identical |
| **Paper sizing PS1** (`desk/paper_ps1.py`, ps1-job-1.0.0, protocol `desk/research/ps1/protocol.json`, `streams/ps1/`) | Synthetic unlevered BTC spot long; three arms (FIXED, VOL = trailing Parkinson, B2 = registered 4h point) at the same 15% ex-ante risk target; primary B2 vs VOL on after-cost Sharpe; quotes captured only after the decision is confirmed on the remote; bid/ask-walked fills, ordinary and stressed costs; joint missing-data rules; pending intervals never marked; bootstrap interval only from 10 blocks of 42 intervals; checkpoints at 180 and 365 days. The protocol, calibration and calibration script are hash-frozen; the job refuses on drift | `test_streams`: hindsight quotes, retrospective quotes, deadlines, crossed books, joint missingness, accounting (spread, slippage, fee, no borrowing, no shorting, band, depth walk), idempotent retries, protocol drift |
| **PS1 calibration** (`desk/research/ps1/calibrate.py`, `calibration.json`) | Variance calibration of the range-to-sigma constant (0.799 vs Brownian 0.627) and the VOL constant on retained history 2024-09-23 to 2026-09-23, walk-forward B2 points; labelled training/calibration, not a holdout; `verify` recomputes exactly | `calibrate.py verify` (both Pythons); look-ahead guard test |
| **Feasibility report** (`feasibility.py`, `reports/feasibility.{json,md}`) | Read-only, outside `lab/` (the lab's code hash is unchanged): per design coverage, eligible time, candidates, episodes, recorded counters, rates, warm-up, checkpoint progress, limiting factor; ETAs only from five qualifying observations with a Poisson interval; "not observable" kept apart from observed zeros; D1 (TWAP polling) and E1 (streaming depth) capability notes | `TestFeasibility` |
| **Workflow** (`research-streams.yml`) | `workflow_run` after Range forecasts plus a fallback 50 min after each 4H close; tests first; writes only `streams/**` and its reports; never waits while holding `repo-write` | regression suite |
| **Release tooling** | `make_release.py`: repo 2.20, base `89fde1a7`, the three repo-only modules, PS1 artifacts, routing for the new streams. `release.json` rewritten | `make_release.py check`; `TestIdentityPreserved` |

# Maintenance, revision 2.19 (crypto-desk 12.4) — 2026-09-30

**Base.** `main` at `a1341401`, which is `12575d3` (reviewed Sep 30 16:40Z) plus data commits. Revisions 2.18 (PR #21) and the Node 24 actions (PR #22) are deployed.

**What changed.**
- Shared modules changed (`range_reader.py`), so the package moves to 12.4.
- `range_job.py` moves to 12.4.0; the version bump keeps it in the package's release family.
- Unchanged: contract ids, model, fits, calendars, frozen records, scores and evidence, lab code and evaluation ids.

| Finding | Change | Tests |
|---|---|---|
| **Nondeterministic archive test stopped production.** The Sep 29 04:00Z forecast run (36520641829) failed preflight in `test_pinned_bytes_detect_revision`: it read `revised` for identical content. `zip_of` used `ZipFile.writestr(name, …)`, which stamps members with the wall clock at 2-second resolution. The 08:00Z run recovered with no code change | Synthetic archives are built with fixed `ZipInfo` metadata (time, system, attributes, deflate level); the changed-content case is kept. Reproduced on 2.18 by patching the clock across a boundary (fails), and fixed in 2.19 (passes). The missed 04:00Z decision is not back-filled | `test_synthetic_archives_are_clock_independent`; 40 repeated runs |
| **Package label in new forecasts.** The 2.18 job kept `PACKAGE = "crypto-desk 12.2"` beside `range-job-12.3.0`. All 36 forecasts it wrote by Sep 30 16:00Z carry the stale label | `range_job.py` reads the package from `release.json` and refuses to forecast on a family mismatch. `make_release.py check` refuses a typed package or a job outside the package family (it catches the 2.18 file). An append-only `desk/provenance_corrections.jsonl` defines the affected set by rule (code version `range-job-12.3.0`) and lists the 36 ids as of 17:05Z. Frozen bytes, ids, hashes and scores are unchanged, and the status shows the correction | `TestGenerationIdentity` (literal, family, every production record agrees or is covered); `test_range_job` asserts the recorded package |
| **Scoring states.** "Unscored" read as backlog | The states are `waiting-maturity`, `ready` (for the next hourly scorer), `overdue` (more than 150 min after maturity, unattempted) and `scoring-failed`. Only the last two form the backlog | `TestScoringStatesAndEvidence.test_states_across_time` |
| **Evidence reporting.** Pooled MAE and skill only | Status `evaluation` block and `reports/range.md` table, method `rc1d-eval-1`, dated Sep 30 before any claim. Per horizon it shows the mean absolute error of ln range for B2 and B0, paired differences (mean, median, better/tie/worse), coverage with 10-90 width for both, and window overlap. It adds a moving-block bootstrap interval (42-decision blocks) only once 10 complete blocks exist; otherwise "unavailable". It reproduces the audit's figures at `12575d3`: 24/19/8 windows, 19.2/15.1/30.4%, B2 better 15/24, 6/19, 7/8 | `test_evidence_block`, `test_interval_reported_only_with_enough_blocks` |
| **Wording and links.** | `report.py` (report-2.6.1) and README no longer say range forecasts are scored weekly. Range scoring and range monitor badges are added. `reports/range.md` separates current availability, evidence, the scoring pipeline and recent history. OPERATIONS lists the two range workflows | regression suite |
| **Deployment log.** | Retrospective rows: the PR #21 and #22 merges; the first scoring, monitor and publication runs on 2.18; the Sep 29 04:00Z failure; the 08:00Z recovery | `make_release check` |

The skill's startup command (a shell loop that returned only the last test file's status) is replaced by `check_package.py` in the package. That change is package-only; the repository preflight already stops on the first failure.

# Maintenance, revision 2.18 (crypto-desk 12.3) — 2026-09-28

Base: `main` at `0215ee17` (after PR #19, repo 2.17.1). Shared modules changed (`range_contract.py`, `range_reader.py`),
so the package moves to 12.3; `range_job.py` and `range_monitor.py` are repository-only. Contract ids, evaluation ids,
the model, the September fit, calendars, frozen records, scores and evidence are unchanged.

| Finding | Change | Tests |
|---|---|---|
| **Preflight time bomb.** `test_hardening.TestLiveRecords` scored a copy of production at a synthetic Sep 29 time and required new `scored` rows for the three 04:00Z records. Once the real scorer scores the 72h window (matures Sep 29 04:25Z; hourly scoring at :41), no new rows exist and the forecast preflight fails from the 08:00Z run on. Reproduced by running the real scorer on a disposable copy past 04:25Z: the 2.17 test fails, the 2.18 tests pass | Production records keep their hash, validation and replay checks. Existing production scores of those records are validated as they stand (complete record, frozen hash, window, publication, loss basis, evidence hash, uniqueness) with no new rows required. Scoring behaviour moves to `test_ops.TestScoringStates` on the immutable fixture with explicit initial states | `TestLiveRecords` (2); `TestScoringStates` (5): unscored→full, partial→remaining (history byte-prefix kept), fully scored adds nothing across repeats, repeated at one instant, additional batch after full scoring |
| **Status clock precision.** `range_job._now()` dropped microseconds; the status step after a confirmation in the same second read "before" it (00:00Z Sep 28: confirmed 00:21:15.778Z, status evaluated 00:21:15.000Z, reported the 20:00Z batch) | `_now()` keeps full precision; report clocks (`now_utc`, `generated_utc`) are written with milliseconds (`range_contract.iso_ms`); `parse_utc`, the reader's and the monitor's parsers accept both forms. Stored forecast timestamps, windows and as-of filtering unchanged | `test_asof.TestSubSecondAvailability` (4): 1 ms before / at / after / later in the same second; JSON and Markdown agree; post-confirmation status shows the confirmed batch; job clock keeps microseconds; serialization round trip and 2.17 files still parse |
| **Monitor: current availability was informational.** A corrupted latest 4h frozen file made status `integrity-failed` and `check()` returned no problems; a fresh-stamped report carrying a stale current state also passed | monitor-12.3.0 `current` check on the monitor's clock: `integrity-failed` always alerts; `valid-current` alerts once its `valid_until_utc` has passed; any other state is a transition (info) only inside the run window of the interval the status was generated in, else persistent (alert); a status past `status_expires_utc` alerts | `test_integrity_failed_current_alerts_despite_publications`, `test_expired_cached_status_cannot_imply_health`, `test_transition_is_info_persistent_is_a_problem` |
| **Monitor: incident lifetime undefined.** Unrecorded failed runs stayed alarms while among the last 20 | Active while inside `LOOKBACK_H` (12 h, the runs check's window) or while no later scheduled run succeeded; otherwise historical (`info.historical_failures`). A failed latest scheduled run alarms even when recorded or acknowledged | `test_incident_lifetime` (resolved/out-of-window, never recovered, recent with later success, acknowledged-but-latest, the legacy Sep 26 incident); `test_sparse_checkout_covers_every_input` (`INPUTS` vs `range-monitor.yml`, no forecasting imports); existing subprocess test with broken forecasting code |
| Deployment log gaps | Appended, marked retrospective: PR #18 merge; first hourly production scoring (run 36249850242); first scheduled 2.17 publication (run 36254628462); PR #19 merge; first successful monitor execution (run 36367972798, scheduled). This deployment's rows are appended after it merges and is observed | `make_release check` (row shape) |

Separate (CI runtime only, its own PR): GitHub Actions Node.js 20 deprecation — `actions/checkout@v5`,
`actions/setup-python@v6`, `actions/upload-artifact@v6`, `actions/download-artifact@v7` (first majors whose
`action.yml` runs on `node24`; no input used here changed).

# Monitor fix, revision 2.17.1 (crypto-desk 12.2, package unchanged) — 2026-09-28

All eight scheduled runs of the range monitor (Sep 26 17:56Z – Sep 27 21:56Z) failed on one line: "actions: range.yml
run 36241307098 ... concluded failure with no record in the repository". That run (the 12:00Z preflight failure)
predates the run log; its verified cause is in `desk/deployments.jsonl`, which the monitor did not read, so it would
have alarmed on every run until the run left GitHub's 20-run list. The range stream itself was healthy: eight
scheduled runs published and were confirmed eligible (Sep 26 16:00Z – Sep 27 20:00Z); hourly scoring ran.

| Change | Tests |
|---|---|
| `desk/range_monitor.py` (monitor-12.2.1): runs recorded in the deployment log are acknowledged in the Actions check (listed under `acknowledged_runs`); a new unrecorded failure still alarms; a due decision whose failure is in the deployment log is reported with that cause instead of "no record". `range-monitor.yml` checks out `desk/deployments.jsonl` | `test_ops.TestMonitor.test_failure_recorded_in_the_deployment_log_is_acknowledged` |

No other module changed; shared skill modules are identical to package 12.2. Evaluation ids unchanged.

