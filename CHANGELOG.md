# Revision 2.30.5 — 2026-10-28 bounded persistence fetch in the shallow checkout

- **Root cause of the Oct 26 persistence failures.** Collector runs 40251817627, 40327143379 and 40414468575 each
  started minutes before a pull-request merge (#53, #55, #56). Their pushes were rejected because main moved; the
  repo 2.30 `scripts/commit_push.sh` then fetched main without `--depth` in the depth-1 checkout, which after a merge
  commit downloads the merged branch's history to the root (1.48 GB and unfinished after 150 s in a reproduction;
  `--depth=10`: 7 s, 14 MB). Both 45 s fetch attempts timed out and persistence stayed unconfirmed. This was a defect
  in the 2.30 repair, which was tested only from full clones.
- `scripts/commit_push.sh`: fetches are bounded (`PERSIST_FETCH_DEPTH`, default 10, also for the post-confirmation
  refresh); the rebase replays only this job's commits (`--onto <fetched tip> <previous tip>`), which needs no shared
  history with the fetched tip. Stages, classes, budget, guard checks and the never-force rule are unchanged.
- `regression/test_rev2305_persistence.py`: a depth-1 checkout against a long history and a merge whose branch forks
  below the boundary; it reruns every 2.30 persistence scenario from that checkout and adds the merge case (fails on the
  2.30 script: the fetch reaches the root commit), a landed push with a later commit on top (fails with depth 1: the
  read-back cannot see our commit), and a conflict after a merge. The 2.30 advance shim now catches up before pushing.
- Readiness: the persistence record names 2.30.5, unmerged and unobserved. `docs/OPERATIONS.md` and the Oct 26
  incident record carry the cause.

Not established: production behaviour; it is observed only when a collector run's push meets a merge on main.

# Revision 2.30.4 — 2026-10-26 recovery diagnostics and retained observations

- Preserve seven unique records from collector run 40251817627 in the late-restoration archive, with verified
  artifact digest and per-row receipts. Live inputs and on-time coverage are unchanged; see the
  [incident record](docs/incidents/2026-10-26-collector-persistence.md).
- Add a fixed comparison from PR #53's recovery deployment alongside rolling study coverage. Show verified
  successes awaiting deadline/grace closure separately; clear current miss alarms after a newer verified success
  while retaining historical misses and independent integrity, stale-run and scoring alerts.
- Add recorded state-depth ages and abstention reasons, plus quality summaries for the exact selected call/put
  legs at each 7d/30d RR25 interpolation expiry. Show the new diagnostics in Data health and its CSV export.
- Preserve the frozen study identity, selection rules, protocol, primary results and launch clocks.

# Revision 2.30.3 — 2026-10-25 market-study operations

- Extend recovery to market studies with bounded per-quarter retries and explicit follow-up after recovered range
  publication. A prior study run before source availability cannot suppress the calibration follow-up.
- Add an independent study watch and separate operational reports for closed-deadline coverage, publication
  latency, training readiness, capture success, and scoring backlogs. Missing records are not successful captures.
- Add paired unique-entry/overlap sensitivity and options leg-quality/stability diagnostics without changing
  the frozen v1 implementation, protocol, primary comparisons, launch clocks, or stored evidence.
- Show study health and report links in the dashboard. Viewer-clock expiry and malformed-data checks preserve
  unknown/stale states; publication of health reports refreshes the dashboard even for recovery-started studies.

See [operating rules](docs/MARKET_STUDIES.md#operational-recovery-and-diagnostics). Operational coverage is not
research support. Production recovery and first calibration publication must be observed after merge.

# Revision 2.30.2 — 2026-10-23 reliability follow-up

Base: `3343e1239931b1e82eb30a02f046d515c4d82b1e` (October 23 ET). The eight lab evaluation versions,
PS1 protocol, model specification, frozen registrations and live data are unchanged.

- A skipped/error lab attempt now renders as evaluation unavailable in feasibility, with no invented zero counts
  or ETA. Source-identity preflight tests use a reviewed fixture instead of mutable production evidence cards.
- Account attribution runs last; the lab budget grows from 20 to 40 minutes within a 50-minute compute job.
  Budget skips return nonzero after preserving completed outputs. This is scheduling mitigation, not a detector
  optimization: changing the account detector would start a new evaluation version.
- The research API resolves experiment settings from the verified hypothesis object and refuses an edited copy,
  including checkpoint, label-watermark and discovery-cutoff edits. The evaluator validates requests and bounds
  request bytes and receive time; one malformed, stalled or failed client cannot terminate the service loop.
- RC1D replay still verifies exact stored bytes and requires exact forecast events/windows. Recomputed float
  features alone permit relative/absolute roundoff of 1e-12; the replay result reports when it used that tolerance.
  The range job is 12.4.1; its updated hash is in the release manifest. Model/contract identities are unchanged.
- The existing required `release` check now depends on the complete regression workflow. Failed/cancelled tests
  produce a failing release context rather than allowing checksums alone to pass.
- Reconciled collector artifacts 12263109593 and 12513437522 against their GitHub SHA-256 digests. Preserved 8 and 7
  absent observations respectively, with receipts, under `data/restored/`. Superseded rows were left alone.
  Restored observations remain unavailable to live forecasts/research and do not repair historical coverage.

Validation and operational limits: `docs/incidents/2026-10-23-research-reliability.md`.

# Revision 2.30.1 (records only) — 2026-10-20

**Base.** `main` at `0abdbd11` (after PR #47 merged 12:13:44Z as `ad3f3d81` and PR #48 merged 12:14:00Z as
`d26ab329`; then data only). No code under `lab/`, `stream/`, `research_tools/` or the collector changes.

| Item | Evidence | Change | Tests |
|---|---|---|---|
| O33 v3.1 correction 1 effective | activity pr_merge `ad3f3d81`->`d26ab329` at 2026-10-20T12:14:00Z; `spec.json` absent at `ad3f3d81`, present at `d26ab329` | `research/registrations/o33-v3.1-correction-1/effective.json`; `scripts/o33_v31_manifest.py` checks both effective records (correction 1's now required); the pinned manifests are unchanged | `test_rev2301` (2) |
| Merges and a persistence failure | GitHub API pulls/47, pulls/48, check runs on `d26ab329` (tests, release, build, dashboard deploy success); job 118619765484 log | `desk/deployments.jsonl`: both merges; run 39420444969's persistence failure (it ran the pre-2.30 script from `7bde6a89`; artifact 12263109593, expires 2026-10-27T12:15:43Z, not yet reconciled) | release check |
| Readiness | the merges and correction 1's first-main record | `scripts/readiness.py`: merged with merge-commit evidence; correction 1 registered; the persistence blocker restated; records regenerated | `readiness.py check` |

**Not established.** The 2.30 `commit_push.sh` repair is merged, not yet observed: no collector run on it has met a
moved main.

# Revision 2.30 (crypto-desk 12.4.21 on the 12.4 release family) — 2026-10-20

**Base.** Brief pin `fec357f4` (Oct 19 23:44:51Z); branch base `main` at `b3b86e95` (Oct 19 23:59:05Z; only data,
state, streams and reports changed after the pin). **Unchanged:** the collector, PS1 v3, every frozen study and
evaluation version, the lab's code identity (`desk/test_streams.py` guard), the PR #45 dashboard design and the PR #46
hashed-asset build, `desk/release.json` (repo 2.28 identity of the shared modules), the O33 v3 and v3.1 frozen bytes.
Every defect below was reproduced on the base before it was changed (synthetic counterexamples unless stated).

| Item | Reproduced failure / cause | Change | Tests |
|---|---|---|---|
| 20A persistence | run 39333253907: `git pull --rebase` hung in fetch-pack at its 60 s cap, `rebase --abort` then failed with no rebase in progress, the push was lost (observed) | `scripts/commit_push.sh`: bounded, retried fetch; local rebase aborted only when in progress; failures classified; an uncertain push confirmed by reading the remote back; never force | `test_rev230_persistence` (13, real script, fake remote) |
| 20B recovery | artifact 12225253430 (sha256 `0a9d6fc2…`, expires Oct 26 22:16:16Z) | reconciled against `main`: 8 rows restorable, 21 metadata-only superseded, 399 frozen identical; data-only PR #47 (not merged) | release check on the PR head |
| F2 panel | all features `ok` with 00:07 snapshots and an 01:55 OI stamp | panel-1.1.0: per-source age, availability and alignment policy hashed into each panel; per-feature states; freeze/compare | `F2PanelFreshnessTests` (6) |
| F3 research API | a transform was ignored; a registered candidate could be mutated after registration | research-api-1.1.0: strict specs, transform applied, transactional registration with immutable objects, code identity, anchored prospective status, fixed checkpoints | `F3ResearchAPITests` (10) |
| F4 DIR1 runner | grading accepted unadmitted forecasts; `AttributeError` on a missing arm; NaN accepted | directional-1.1.0, dir1-runner-1.0.0 (durable chained log, child-process deadlines, verified publication); DIR1 protocol revision 2, prepared | `F4RunnerTests` (9) |
| F5 comparisons | frontier minus baseline (+0.11) reported as the primary | registered pairs only; statistical minus baseline is primary (-0.09 on the review fixture); pair-specific intersections | `F5ComparisonTests` (3) |
| F6 ledger and boundary | ledger truncation undetected; register written before its log event | search-ledger-1.1.0 (anchor, object store, lock, torn-line repair); evaluator-service-1.0.0 (separate process; OS-user case run as root) | `F6LedgerTests` (5) |
| F7 E1 acceptance | a pilot "passed" on a claimed shock count without coverage | pilot-acceptance-1.1.0 fails closed on window coverage, verified replay, clock samples (recorder stream-1.1) and computed shocks; E1 stays uncommissioned | `F7PilotAcceptanceTests` (6) |
| F8 O33 | a quoted pre-amendment conditional was classed original-rule | `o33-v3.1/effective.json` from first-main evidence (PR #44 merge `1864d3d9`, 2026-10-19T19:51:07Z); correction 1 prepared (classes by call type, rule and epoch; enforcement register-2.4.0) | `F8O33Tests` (2); `scripts/o33_v31_manifest.py check` |
| F9 archive | a whitespace-corrupted object replayed as valid | archive-store-1.1.0: verify on put, read-back, verified restore, integrity before replay, chained manifest; `S3Backend.get` | `F9ArchiveTests` (6) |
| 13 calibration | no declared criteria before a run | criteria committed first (`b3c7e68`); `calibration_harness.py`; dir1-primary-v1 seed 33 passed them (any-look FPR 0.0775 [0.055, 0.108]; power 0.84 at -0.01 Brier); one simulated world | attempts recorded in `research/calibration/` |
| 14 families | — | options-skew-0.1.0 (7-day 25-delta RR from stored captures; 78.6% of hourly captures computable Oct 13-19); replenishment-0.1.0 contract (needs the E1 recorder) | `Section14Tests` (3) |
| 15 successors | A2 and PS1-T1 were prose; stale `lab/*` paths | a2-sync-0.1.0, ps1-t1-runner-1.0.0 (reproduces PS1 exactly with PS1's own `rebalance()`); protocols revision 2, prepared; PS1-T1's primary band awaits an operator decision | `Section15Tests` (2) |
| 16 discovery | — | exposure labels, configuration and attempt counting across sessions and models (research API and search ledger) | in F3/F6 |
| 17, 20C readiness | states were asserted in prose | `scripts/readiness.py` (component-readiness/1; a test establishes only `tested`; stale code identity fails); `docs/READINESS.md`; the dashboard shows the records as recorded | `test_dashboard` (15 Python), `dashboard/model.test.mjs` (26) |

**Caught by an existing guard.** The first push placed the clock sample in `stream.service.Recorder`. The
E1-liquidity-recovery evaluation version hashes that class (`lab/versioning.py` DATA_DEPENDENCIES), so its version
moved (`ev-6f279983100b` -> `ev-8ac04d500791`) and `desk/test_streams.py` (test_lab_evaluation_versions_unchanged,
which runs only on Python 3.12, the production AST) failed in CI on PR #48. The sample is now the module-level
`record_clock`; `Recorder` is AST-identical to the base and the guard passes under 3.12.

**Observed at this revision** (read, not caused by it): report-2.6.2 is live — `reports/latest.md` generated
2026-10-20 01:31Z by `report-2.6.2-2026-10-19` (commit `03d8e22`). Merges of PRs #44-#46 recorded in
`desk/deployments.jsonl` from the GitHub API.

**States.** Implemented and tested on this branch; not merged; nothing deployed or registered; DIR1, A2, PS1-T1 and
O33 v3.1 correction 1 prepared; E1 and the evaluator service not commissioned; archive capture not wired in.

# Revision 2.29 (crypto-desk 12.4.20 on the 12.4 release family) — 2026-10-19

**Base.** `main` at `fce9fa2d` (Oct 19 17:47:53Z). Between the Oct 18 and Oct 19 review pins and this base, only data,
state, streams and reports changed; no Python or workflow file. Repository gates at the base all passed locally
(fixtures, regression suite, O21 verify, checksums, release identity, desk tests). **Unchanged:** the collector,
recovery, persistence, workflows, every research design and evaluation version, and the lab's code identity (`lab.common.code_hash`, which evidence
cards record): the new modules live in `research_tools/`, outside `lab/`, as `desk/test_streams.py` requires; they read
the lab through `lab.data` and `lab.asof` without changing it. `lab/modules/twap.py` is deliberately untouched, PS1 v3, the range
stream, the six shared modules and `desk/release.json`.

| Item | Evidence / cause | Change | Tests |
|---|---|---|---|
| Report tail counted intervals beyond its inputs as uncovered (670/671, the 13:22-13:37Z interval) | coverage buckets ran to the report clock, not the input cutoff | `report.collection_health(..., input_cutoff)`: intervals after the cutoff are "not yet assessed"; wall-clock lag is its own line (report-2.6.2) | `test_rev229.ReportTailTests` |
| PR #42 merge missing from `desk/deployments.jsonl` | the record stopped at PR opening | appended from the GitHub API (merged 2026-10-14T01:47:09Z, `7f97b6af`, checks green); merge is not commissioning | — |
| Shared evidence contract | helpers reimplemented weaker rules (skill findings A-K) | `research_tools/evidence_contract.py` = skill `desk_evidence.py`, pinned both sides | `ContractParityTests` |
| O33 v3.1 | the 12.4.19 amendment had no verifiable public record | `research/registrations/o33-v3.1/` spec, enforcement copies, manifest; effective at its first push to `main`; the "3-3 split" argument withdrawn | `scripts/o33_v31_manifest.py check` |
| Catalog, funnel, panel, research API, ledger, directional stream, calibration, turnover, archive, D1, E1 pilot | brief sections 8-16 | see `docs/RESEARCH_INTERFACE.md` | `test_rev229` (31 tests) |
| Stale D1 prose ("2 BTC programs in 272") | Oct 8 figure | `feasibility.py` cites the measured per-reason counts (282 programs, 280 not BTC, 2 BTC first seen finished) | — |

Measured at this base (`research/diagnostics/2026-10-19-repo-2.29.json`): spot later than perp in 1,440 of 1,440
paired minutes (median 909.5 ms, 756-1,513 ms); A1's optional spot ineligible at all 10,075 decision minutes in 7
days; decision-time input age median 180 s.

# Maintenance, revision 2.28.3 (crypto-desk 12.4.17 on the 12.4 release family) — 2026-10-14

**Base.** `main` at `a32ad3c3` (2.28.2 merged Oct 12 19:37:20Z as `69258f42`, then data only). Collection, recovery,
persistence, workflows, research definitions, the PS1 protocol and `desk/release.json` (repo 2.28) are unchanged.
The 3.2.0 collector and PS1 content-crediting fixes are kept unchanged. This revision applies the repository part of
an independent assessment of 12.4.16 / 2.28.2 (inspected at `028352ad`). The assessment's counterexample is
synthetic; no production incident is asserted.

| Finding (reproduced) | Verified cause | Change | Tests |
|---|---|---|---|
| **Range publication credited a manifest key, not its content.** In `World`, the Oct 4 20:00 decision's three manifest keys were first pushed at 20:48 as `{}` with no frozen files, and their valid entries and frozen bytes only at 22:00, after the windows started at 20:55. 3.2.0 returned range `published`, verdict `pass` and all nine checks true. | `range_decisions` used `first_seen_keys`: the first push of the key, whatever its value then. | acceptance-3.3.0. Each of the decision's forecasts needs its exact manifest entry (`first_seen_entries`, canonical JSON), its frozen bytes (`first_seen_blobs`, the git blob of the bytes validated at the cutoff) and its confirmation row (`first_seen_content`) first pushed strictly before its window start. Production check before the change: 0 of 294 manifest keys ever changed value after first appearance, and the confirmation rows are append-only (98 commits), so content crediting changes no real result. | `test_acceptance.RangeContentTests` (7): placeholder then late repair; a placeholder entry with its frozen bytes on time; late frozen bytes; a wrong frozen path first, corrected later; a confirmation row pushed late with its stored time unchanged; frozen bytes exactly at the start (fails) and one minute earlier (passes); on-time and no-op-rewrite controls. Run against unmodified 3.2.0, every defect test fails and the control passes. Mutation check: disabling each new guard in turn (entry content, frozen bytes, confirmation row, strict boundary, complete history, cutoff-limited history, and the kept 3.2.0 collector crediting) fails its intended test (8 of 8). |
| **Push history: post-cutoff pushes mattered, a missing earlier push did not** (the first documented in 2.28.2; the second found here) | `snapshot()` built its push history from every push in the evidence and required only the newest three commits locally. A post-cutoff commit absent from the clone made availability unestablished. A pushed commit missing inside the required history went unnoticed, and 3.2.0 returned verdict **pass** (reproduced on 3.2.0 by `AsOfHistoryTests`). | push history is limited to pushes at or before the cutoff, and `known` requires every one of those pushed commits (and each push's base, after the first) to be present (`present_commits`, one `git cat-file --batch-check` call). A gap in that history is unestablished (insufficient), never a pass and never a silent late attribution. | `test_acceptance.AsOfHistoryTests` (2) |
| **Declared windows re-checked** | — | Oct 6 and Oct 7: the 3.3.0 supplementary audits (same evidence and commits) are identical to 3.2.0 in every field. Results of record untouched; Oct 7 still not credited as a pass (receipts cover 10:12Z-22:27Z only). | `docs/acceptance/results/2026-10-0{6,7}/` |
| **Collector tests failed when the suite ran longer than 10 minutes** (5 tests in `test_rev22` and `test_rev26` read "deadline reached" in a 12-minute local run) | `collector.DEADLINE` is fixed at import to one run's budget; tests that do not patch it fail once the process outlives it | `setUpModule` in both modules starts a fresh run budget; test expectations unchanged | reproduced with an expired deadline (5 failures before, 0 after) |
| **PR #41 merge not in `desk/deployments.jsonl`** | the merge happened after the PR's own commits | retrospective row from the GitHub API: merged 2026-10-12T19:37:20Z as `69258f42`, by mannoj93-spec, checks green | — |

`research/o34/README.md`: the checksum command now runs from the study folder, `(cd research/o34 && sha256sum -c protocol.sha256)`, after the private protocol is placed there (verified against the package copy). The `World` fixture gains `publish(manifest_view=..., extra_cuts=...)` so a test can push placeholder or incomplete
manifest contents; default behaviour is unchanged. Timer receipts: no capture job exists. A window is certified
only if the operator exports the provider history within about 12 hours (docs/OPERATIONS.md).

# Maintenance, revision 2.28.2 (crypto-desk 12.4.16 on the 12.4 release family) — 2026-10-12

**Base.** `main` at `f13b35bc`: 2.28.1 merged on Oct 7 at 22:51Z as `4c6eb529`, followed by the O33 v3 PRs #38 and
#39, then data. Nothing changes in any research definition, model, contract, `range-job-12.4.0`, the PS1 protocol, the
collector, recovery, persistence, workflows or any recorded forecast, score or execution. Release identity
(`desk/release.json`, repo 2.28) is unchanged: no release module changed. The repository items come from the crypto-desk
12.4.16 handoff.

| Finding (reproduced) | Verified cause | Change | Tests |
|---|---|---|---|
| **Acceptance credited an identifier, not its content.** A collector row was pushed on time as a failure and replaced in place by a success after the 15-minute allowance. Separately, one of an execution's six PS1 rows was pushed on time and the other five late. 3.1.0 credited both as on time: the four-row replacement read `pass` with the 75-minute gap hidden, and the five-late-rows execution read `executed`/`pass`. | `PushHistory.first_seen` was keyed on `(run_id, t)` / `execution_id`, so the first push of *any* row carrying the key counted. | acceptance-3.2.0. A row is available from the first push whose diff added its exact content (canonical JSON). An execution is available from the latest such push across its six execution rows and its state-journal rows. A late collector entry names `identifier_first_pushed` when the identifier was on main earlier with other content. | `test_acceptance.ContentCreditingTests` (6): case A with one row and with four rows (verdict `fail`, gap > 45 min), plus a no-op-rewrite control; case B with five of six rows late, with the completion state late, and with all rows at exactly +15:00 (counts). All four defect tests failed on 3.1.0 and pass on 3.2.0. |
| **Declared windows re-checked** | — | Oct 6: the 3.2.0 audit (same evidence, `6ce0e82a`) is identical to the 3.1.0 audit except the availability label; the result of record stands. Oct 7: no evaluation existed, so this is the first one, 4 d 17 h after its earliest evaluation time. The 3.0.0 result of record, the 3.1.0 audit (amendment) and the 3.2.0 audit all read `insufficient` / service `pass`. The window is not credited as a pass: the receipt export covers 10:12Z-22:27Z only, so 92 critical-chain runs are timer-corroborated. | `docs/acceptance/results/2026-10-0{6,7}/` |
| **Merge events missing from `desk/deployments.jsonl`** (PRs #26-#28 and #34-#39, including #36, recorded only as "pull request opened") | not appended at merge time | appended retrospectively from the GitHub API (`merged_at`, `merge_commit_sha`, `merged_by`, check runs) and git first-parent, each labelled retrospective. PR #36: merged 2026-10-07T21:19:34Z as `0f6afe3f`. | — |
| **O34 study not in the repository** | — | `research/o34/`: runner, results, inputs record, v1.1 erratum and classifier, replay, evidence bundle (raw provider files, gzipped rows). `protocol.json` is withheld because its rationale records the operator's own positions and dollar results (public repository); its sha256 is published (`protocol.sha256`). The commit date is not proof of the freeze time. | replay from this layout: 0 differences in both raw and rows modes (6,942 bars) |

Found while evaluating, not changed: `snapshot()` decides push-history availability over every push in the evidence,
including pushes after the cutoff. If the local clone lacks the newest pushed commits, availability reads
"unestablished" (insufficient, never pass) until the clone is refreshed. This is fail-safe, and it is documented in the
Oct 7 README.

# Maintenance, revision 2.28 (crypto-desk 12.4.12 on the 12.4 release family) — 2026-10-07

**Base.** `main` at `d9eb3d16` (2.27 merged Oct 5 21:46Z as `f242b90e`, plus data). No research definition, model,
contract, `range-job-12.4.0`, PS1 protocol, lab design, calibration, cost, eligibility, deadline, forecast, score,
execution or missed-decision record changes. Collection, recovery, persistence and the 2.27 execution-stage logic are
unchanged.

| Finding (reproduced) | Verified cause | Change | Tests |
|---|---|---|---|
| **Acceptance passed a healthy World with no git history** | 3.0.0 fell back to stored timestamps | acceptance-3.1.0: repository read at the after-commit of the last push to main at the cutoff (GitHub activity API); no complete push history → `insufficient`, never `pass` | `test_acceptance.FalsePassTests` fp1 |
| **Records first committed an hour after the window passed** | availability never checked | a collector record counts only if the push that added it reached main within 15 min of its time (boundary: exactly 15:00 counts, 15:00 + 1 ms does not) | fp2, boundary |
| **Range publication `eligible:true` with start/confirmation after the window passed** | flag trusted | strict RC1D validation (`range_reader._verify`, `validate_rc1d`, `range_contract.eligibility`) and manifest key first pushed strictly before window start | fp3, manifest-at-start |
| **Unrelated receipts produced `timer-receipt`** | receipt format unvalidated | `timer-receipts/1`: pinned provider/job (`docs/acceptance/timer.json`), this repo's recovery.yml dispatch target, export provenance, unique ids, 2xx; any defect rejects the export | fp4 (10 variants) |
| **Monitor with setup ok, checkout failed, check skipped read "check executed"** | any executed step counted | `execution.check_outcome`, health-1.4.0: detected only when the check step ran, failed and carries a finding annotation | `test_rev228`, `test_rev227` (updated), `model.test.mjs` (19) |
| **External-timer gaps hidden by healthy service** (Oct 7 15:12Z, 16:57Z absent) | no arrival-level view | `monitors.external_timer` per opportunity, apart from native dispatcher, execution and persisted success; dashboard row; `docs/incidents/2026-10-07-external-timer-gaps.md` | `test_rev228` (real dispatcher runs) |
| **F1 warm-up compared raw records with a usable-record threshold** | parser took the first number | feasibility-1.2.0: `have` = usable (trailing z-score) records, raw reported apart | `test_rev228.FeasibilityWarmupTests` |
| **Retrospective lean-rule research not reproducible by a reviewer** | bundle outside the repository | `research/retrospective/lean-rules-2026-10-05/` with retained inputs, hashes and `replay.py` (REPLAY MATCH) | replay |
| **Declared windows** | — | Oct 6 result of record (3.0.0) and evidence preserved, supplementary 3.1.0 audit labelled; Oct 7 declaration amended append-only (both checkers; credited only if both pass) | `docs/acceptance/` |

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

