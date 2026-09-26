# Desk hardening, revision 2.16 (crypto-desk package 12.1) — 2026-09-26

Response to the assessment of package 12.0 / repo 2.15 at `cabc40d` (deployment evidence through `fe27eb2`);
built on `3433ec9`. Collection cadence, API budgets, research designs and skills are unchanged. **No evaluation
version changes**: all eight lab evaluation ids are identical before and after (computed with `lab/versioning.py`
on `3433ec9` and on this branch). The three 04:00Z forecasts' frozen bytes, manifest, attempt and publication rows
are untouched; they read, replay and score under 2.16. Contract ids are unchanged (`contract-12.0.0`); the
implementation versions move (contract-12.1.0, reader-12.1.0, range-job-12.1.0, scoring-2.4, retained-12.1.0).

| # | Finding (reproduced on 2.15) | Fix | Tests |
|---|---|---|---|
| 1 | Cached status carried a 24h forecast as `valid_until` 13:15Z (window end + grace) against 09:15Z by the forecast's own decision; cached and fresh reads disagreed | `expiry = min(window end, decision + 4h + 75 min)`; `valid_until_utc` in every result; `range_reader.revalidate(result, now)` re-derives state, elapsed share and label on the consumer's clock; full-window label kept, `remaining` always None | `TestExpiry` (before / at / after expiry, missed runs, grace) |
| 2 | Refit raised "klines not admissible: missing" when the last archive day was unpublished, with no live fallback | `archive_with_tail`: only a trailing run of missing days is filled, from closed, validated live bars that must match the archive on an overlap of up to six bars; provenance stored as `live_tail` in the refit delta; interior gap, interior hole, malformed archive, conflicting overlap, unavailable source, unclosed or malformed live bar each stop the refit | `TestRefitTail` (fill equals the direct fit; seven failure cases) |
| 3 | A mislabelled 4h record (24h window) read `valid-current`; a record missing a B0 point raised `KeyError` in the reader | `range_contract.validate_rc1d` (id/horizon, decision on a 4H close, window span, start delay 5–70 min on the 5-minute grid, made time, reference price, input bundle = snapshot hash, exactly one finite, ordered B2 and B0 event, manifest entry and publication row) — returns problems, never raises; reader and scoring report `integrity-failed` / "integrity failure — not scored"; legacy `range-b2-*` schema unchanged | `TestStrictValidator`, `TestReaderNeverCrashes` |
| 4 | Replay failed with "calendar changed since the forecast" after any refresh | Calendar versions retained as `desk/calendars/<sha256>.csv` at forecast time (the 04:00Z version back-filled, verified equal to the bundle's `calendar_sha256` and to Git history); `retained.calendar_bytes` resolves current → retained → Git history; altered or missing bytes fail | `TestCalendarReplay` |
| 5 | The refit chain used the O21 root inputs without checking their manifest hashes (an altered root was accepted) | `retained.load_o21_inputs`, shared by `o21_reanalysis.load_inputs` and `range_job.history_chain`; every refit delta verified (name = hash, structure, no duplicate months) before use | `TestRetainedRoot` (altered root refused; the real root reproduces the September fit) |
| 6 | Deployment state lived in `release.json` and prose | `release.json` is identity only (adds `base_commit`, `audited_snapshot`, `range_stream_start_utc`); `desk/deployments.jsonl` records the 2.14/2.15 merges, the first scheduled 2.15 publication (run 36217120108, frozen 04:13:17.546Z, confirmed 04:13:19.582Z on the runner clock, window 04:20Z, eligible) and the offline replays; `reports/range_status.json` separates `due_decisions` from `current_decision` (in-progress vs outcome) and keeps the runner-clock disclosure | `TestReaderNeverCrashes` (due vs current), `TestReleaseChecker` |
| 7 | Release check passed with no calendar; fits from any contract accepted; Holm fallback undisclosed; no numerical replay; integrity workflow blind to desk changes | `make_release.check` fails on a missing calendar, verifies retained calendars and the deployment log; `validate_fit` accepts only the 12.0 contract ids, or `job == range-job-11.2.0` for a fit without a contract field (the pre-12.0 rule); `research/o21/holm_addendum_12.1.json` (72h fallback comparison, raw p 9.65e-05, adjusted in the declared family of 10 and the predeclared complete family of 13); `o21_reanalysis.py verify` (byte integrity, then numerical replay within abs/rel 1e-9, runtime reported); `fixtures.yml` triggers on `desk/**` and `SHA256SUMS`; `range.yml` persists `desk/calendars` | `TestFitContract`, `TestReleaseChecker`, `verify` run |

**Tests.** 496 regression tests (332 + desk 164: measure 40, archive 50, range model 18, contract 10, range job 26,
release 3, hardening 17) on Python 3.11; 25 numerical fixtures unchanged; O21 replay zero differences;
`o21_reanalysis.py verify` max abs difference 0.0 in ~42 s.

# Desk forecast contract, revision 2.15 (crypto-desk package 12.0) — 2026-09-26

Response to the audit of package 11.2 / repo 2.14 (audited at `0a9ba0e`; built on `09549f8`, main since
then has only collector data commits). Collection cadence, API budgets, research designs and skills are
unchanged. **No evaluation version changes**: all eight lab evaluation ids are identical before and after
(computed with the lab's own loader); `schema.py`, `scoring.py` and `registration.py` were edited, but
nothing hashed by `lab/versioning.py` changed and no `tests/` forecast test is registered, so no research
clock restarts. The scoring implementation hash changes (scoring-2.3); no score exists yet.

| # | Finding (reproduced on 2.14) | Fix | Tests |
|---|---|---|---|
| 1 | `forecast()` wrote three sources before its final time check; a clock sequence of 00:07:05 (validation) then 00:11 (registration) left three unregistered files; a retry skipped them by filename and left the manifest absent | One freeze time for the whole batch; `registration.register_batch`: validate all → frozen bytes → one atomic manifest write (commit point) → sources (rolled forward from frozen bytes); rollback before the commit point. Attempt log `state/range_attempts.jsonl`; a decision whose attempt recorded a window is refused, not retried. Publication confirmed on `origin/main` before the window starts (`confirm`, `state/range_publications.jsonl`); scoring requires it | `desk/test_range_job.py` `TestTransaction`, `TestEligibility` (the audit sequence, injected failures at three points, retry, roll-forward, orphan conflict, late/unconfirmed publication, scoring by publication) |
| 2 | Threads were told to read raw `registry/` files | `desk/range_reader.py`: manifest → frozen bytes → schema, instrument, contract, decision, window, freshness, eligibility → `valid-current` / `stale` / `missing` / `unregistered` / `ineligible` / `integrity-failed`; full-window label, no remaining-range figure. `reports/range_status.json` reconciles expected decisions with outcomes (production vs other runs, legacy records) | `TestReaderStates`, `TestStatus` |
| 3 | Evaluation lost on `p`, live scoring on q50 (3.5–4.6% lower, reproduced from the September fit); windows and calendar terms differed; coherence only in `forecast_now` | `desk/range_contract.py`: RC1 (evaluated) and RC1D (live, delayed window, calendar terms for the scored window); registered `point` is the loss-bearing forecast; one `losses` function used by evaluation and `scoring.py`; coherence reported, not applied | `desk/test_range_contract.py` (parity of windows, features, points, quantiles and losses across the three paths within 1e-8; boundary release; coherence case) |
| 4 | Periods selected by decision time: 5 (24h) and 17 (72h) validation targets matured in the holdout | Maturity-bounded periods; O21 replayed from retained inputs (zero differences), then reanalysed: selection unchanged (B2 everywhere, also under Holm), holdout skill 18.2 / 16.9 / 10.8% | `TestSplits`; `desk/research/o21/reanalysis_12.0.json` |
| 5 | A fit with zeroed hashes and month 1999-01 registered three forecasts | `range_contract.validate_fit` before any use (month, spec, models, term order, coefficient shape and finiteness, residual quantiles, cutoff, calendar prefix, provenance) | `TestFitValidation` (the reproduced case and ten corruptions; the committed September fit validates) |
| 6 | Forecast and research inputs not replayable | Per-decision input bundles (`desk/inputs/`), refit history chain, O21 inputs and results retained (`desk/research/o21/`); `range_job.py replay`, `o21_reanalysis.py replay` | `TestReplay`, `TestResearchRetention`, `TestChainedRefit` |
| 7 | Conflicting DVOL hours kept the last row; decreasing cumulative notional passed; non-`ok` inputs admitted without a policy | archive-12.0.0: conflicts → `malformed`, hour dropped, row order irrelevant; depth and notional both monotone; `range_contract.admit_dvol` overrides named and recorded | `TestAudit12`, `TestAdmissibility` |
| 8 | Contradictory status and release text | `desk/release.json` (written and checked by `make_release.py`), README, registry README, OPERATIONS updated; skill package synchronized and drift-checked | `desk/test_release.py` |

**Tests.** 479 regression tests (332 + desk 147: measure 40, archive 50, range model 18, contract 10,
range job 26, release 3) on Python 3.11; 25 numerical fixtures unchanged.

# Desk range forecasts, revision 2.14 (crypto-desk package 11.2) — 2026-09-26

Adds the crypto desk's range model as an automated, registered forecast stream. Collection cadence,
API budgets, research designs, hypotheses, thresholds and skills are unchanged. **No evaluation
version changes**: nothing hashed by `lab/versioning.py` was edited, and every new file lives under
`desk/` (root `*.py` files are untouched, so the registration clock of `tests/` and the scoring
implementation hash are unchanged).

| Added | What it does |
|---|---|
| `desk/range_model.py` (range-11.1.0) | The model tested once in the desk's O21 (frozen spec sha256 `ae6aa254c786…`): B0 persistence and B2 (HAR-range + weekend share + scheduled releases + DVOL), direct per horizon. On the never-fitted year it beat persistence by 18.2% / 16.8% / 10.7% (4h / 24h / 72h, mean absolute log error), 10-90 coverage 81-85%. Status: exploratory, holdout-consistent |
| `desk/jbm_archive.py`, `desk/jbm_measure.py` | The desk's validated loaders (4H klines with provider checksums, DVOL) and measurement functions |
| `desk/range_job.py` (range-job-11.2.0) | `refit` (one frozen fit per month in `desk/fits/`), `forecast` (three registry files per 4H close, each with a B2 and a B0 `range` event on the same window, registered through `registration.register` before the window starts), `summary` (`reports/range.md`) |
| `desk/fits/2026-09.json` | The September fit (targets closed before Sep 1); it reproduces the desk's hand-registered Sep 26 00:00Z forecast exactly |
| `.github/workflows/range.yml` | Two minutes after each 4H close: desk tests, refit, forecast, summary, persist through `scripts/commit_push.sh` under `repo-write` |
| `regression/test_desk_range.py` | Runs the desk suites (115 tests) inside the regression workflow |

The registry rule (start strictly after registration) is what makes these forecasts honest: the
window opens at the next five-minute boundary after registration, a few minutes after the close
the model was trained on; the offset is recorded in each note, and a run more than an hour late
does not forecast. Scores come from the unchanged `scoring.py` (`range` events: coverage, pinball,
`abs_error_log_lr`, QLIKE) in the weekly report.

**Tests.** 447 regression tests (332 + 115) on Python 3.11; 25 numerical fixtures unchanged.

# Research-integrity revision 2.13 (lab-2.2, evidence completeness; GitHub presentation) — 2026-09-25

Response to the review of 2.12 (`16cb49f`); main since then had only collector data commits.
Collection cadence, API budgets, hypotheses, costs, thresholds, horizons, minimums and skills are
unchanged. **No evaluation version changes**: no hashed file (`lab/versioning.py`) was edited - the
fix lives in the publication path (`lab/evidence.py`, `lab/run.py`, `scripts/merge_research.py`),
which does not change what any evaluation computes - so every research clock continues.

| # | Finding (reproduced on 16cb49f) | Fix | Tests (`regression/test_rev213.py`) |
|---|---|---|---|
| 1 | From a valid supported 100/20 run, removing the incoming checkpoint file still merged (exit 0) and published a `supported` card and a proposal citing a checkpoint that did not exist; removing the incoming control files still merged although the stored controls no longer had the fingerprint the evaluation reported. The merge only checked files that arrived | The lab records, per design, an **evidence inventory** read back from its own writes (`evidence.inventory`): the checkpoints its card references (look, verdict, manifest sha256, canonical record sha256), the control hours used at the cutoff and the fingerprint of their first-stored winners (`controls.fingerprint`, the one the control policy reports), and the count/set-sha256 of frozen decisions persisted by the cutoff and of their outcomes. It travels in the card and in `lab-summary.json` (schema `lab_summary/3`). Before any write the merge builds the **proposed resulting repository** for each design version (checkout records + incoming records, merged by the same rules) in a temporary directory, recomputes the inventory there with the same function and loaders, and rejects (exit 4) any difference; every checkpoint a card or proposal references must exist with the declared design, version, look and hashes and re-verify (`experiments.verify_checkpoint`) when it supports a status or proposal; the proposal's checkpoint must be such a record; the control fingerprint must equal the evaluation's. Dependencies already present and identical in the checkout satisfy this | complete handoff publishes; missing checkpoint file; missing control files; dropped control rows, a checkpoint cut mid-line, missing decisions; altered checkpoint or control content; wrong declared record hash or control fingerprint; missing inventory; dependencies already present (accepted, destination byte-identical); a conflicting stored winner (exit 3). Every rejection leaves the destination byte-identical |

**GitHub presentation.** The README is now a short entry page: title, workflow badges, a
two-sentence purpose, "Start here" links (coverage, research results, proposals, weekly reports,
validation, changelog, setup), the four separate signals (workflow success, data freshness,
research integrity, evidence maturity - a green badge is not evidence of an edge), a short "how it
works", a collapsible repository map and a quick start. The previous README body moved unchanged to
`docs/OPERATIONS.md`; release history stays here. `reports/research.md` opens with an "At a glance"
table keeping those signals apart, states that all times are UTC, uses consistent `##` sections and
labels values that cannot be computed yet as `—` with a legend; `reports/skill_proposals.md` gains
`## Result` / `## Why each design has no proposal` sections. Counts and statuses stay in the
generated reports only.

**Before / after** (`python scripts/repro_completeness_213.py [tree]`): 16cb49f - checkpoint file
removed: merge exit 0, card `supported` referencing look 1, no checkpoint published, proposal
published; control files removed: merge exit 0, card `supported`, stored control fingerprint differs
from the card's. 2.13 - both exit 4 ("PUBLICATION BLOCKED"), destination unchanged, the previous
valid card stays current, no proposal.

**Tests.** 332 regression tests (324 + 8) on Python 3.11 and 3.12; 25 numerical fixtures. On
16cb49f the new file gives 3 failures (the reproductions), 2 skips (new interfaces) and 3 passes
(complete handoff, dependencies already present, conflicting winner - behaviour kept). The merge-only
test fixture now carries the (empty) inventory of `lab_summary/3`.

# Research-integrity revision 2.12 (lab-2.2, publication gate) — 2026-09-25

Response to the review of 2.11 (commit `b4db7d0`). Current main was inspected first: since
`b4db7d0` only automated data commits had landed, so both findings applied to the running code.
Both were reproduced on `b4db7d0` with `scripts/repro_publication_212.py` and with
`regression/test_rev212.py` (runs against any code tree). Collection cadence, API budgets,
hypotheses, thresholds, costs, horizons, sample/block minimums and skills are unchanged.

| # | Finding (reproduced on b4db7d0) | Fix | Tests (`regression/test_rev212.py`) |
|---|---|---|---|
| 1 | A stored control persisted 1 ms before its own decision was withheld and reported as an unresolved conflict, yet at the checkpoint boundary (normal 100 retained / 20 blocks) the same run recorded a verified **supported** checkpoint, wrote a card with `status: supported` and `research_integrity.ok: false`, generated a skill proposal and advanced the watermark; the lab exited 1 but `merge_research.py` published all of it. Cause: the integrity check ran in `lab/run.py` after `run_design` had persisted decisions and appended checkpoints; proposals ignored it; the persist job merged before the red step | `experiments.input_integrity` runs on the primary prospective pass after labelling and BEFORE anything is written: control-policy conflicts (unresolved, malformed in either mode, ready-but-unselected), writing-run controls = stored selections, every labelled control = the selection it came from (`controls.evidence_agreement`), and a missing policy report or window = `incomplete`. Failed or incomplete -> the evaluation is **blocked**: no decision, outcome or checkpoint written, no look consumed, status `blocked` with the reasons; earlier records shown as history only. `experiments.next_run_state` (hashed) holds the watermark of a blocked design. All of a design's evaluation writes are deferred until every variant has run without error. `evidence.publication` is the single publication decision used by card, index, report, proposals and the summary; proposals require a valid evaluation, so an earlier recorded "supported" checkpoint cannot produce one while integrity fails. The lab writes `--summary lab-summary.json` (`lab_summary/2`); the merge refuses (exit 4, nothing merged) a batch whose checkpoints, decisions, outcomes, watermarks, cards, index, reports or proposals are missing, stale or contradict it | boundary reproduction through `lab.run.main` + merge; recovery (look 2 completed by a later valid run, look 1 bytes identical, the decisions of the blocked run evaluated as new, not late replays); malformed timing (missing / string / impossible source time); future-persisted winner; stored-versus-labelled mismatch; missing diagnostics; missing window; an error in a later variant; read-only replay; tampered handoff (2.11 outputs injected); missing / unreadable / old-schema / stale / contradictory summary; partial artifact; bar-based designs `not_required` |
| 2 | `conflicts()` compared raw lines: the same record with other whitespace or key order was a `RECONCILIATION CONFLICT` (exit 3). A batch whose first record for a key was a legacy loser was accepted | Equality is `canon()`: parsed JSON, keys sorted at every depth, no whitespace; values, array order, types (1 / 1.0 / "1" / true, -0.0) and all fields significant, no tolerance; non-objects, duplicate keys and out-of-range numbers are unreadable. Same rule for controls, checkpoints and unkeyed logs; a reformatted copy is neither appended nor rewritten (stored bytes kept). A new record for an existing key must equal the stored FIRST record; the batch's first record per key must be that record; one batch may not carry two records for a key; a legacy duplicate repeated verbatim is tolerated | whitespace, nested key order, padded lines; checkpoints and ledger rows; value / array order / string-vs-number / int-vs-float / extra or missing field conflicts with no partial mutation; legacy duplicate files verbatim and reformatted (merge) vs legacy loser first, reversed order, a third record (conflict); two records in one batch; unreadable rows |

**How an integrity-failed evaluation is kept from publishing a supported result or proposal.**
(1) In the lab, `run_design` computes `input_integrity` from the labels it just built; unless it
passes (or is not required) the checkpoint walk is never run, `persist` is never called and the
status is `blocked`, so no new checkpoint, verdict or frozen decision exists to publish.
(2) `lab/run.py` keeps the watermark and exits 1. (3) `evidence.publication` marks the attempt not
valid, so the card, index and report say BLOCKED, the proposal list suppresses it even when an
older recorded checkpoint is supported, and the summary records the same decision. (4) The persist
job's merge checks the whole batch against that summary before writing: any new checkpoint,
decision or outcome row, advanced watermark, supported status or proposal for a design that is not
valid - or any missing, stale or contradictory metadata - rejects the batch (exit 4) and the commit
step never runs. A correct blocked batch is published, so the failure stays visible, and the
workflow still ends red (lab exit 1).

**Adversarial review of the first 2.12 draft** (separate agent, read-only; also ran real-data
compute/merge cycles): no bypass of the gate; one medium and six low findings, all fixed with
regressions - an error in a later variant left the primary pass's decisions and checkpoint written
(writes are now deferred); a read-only replay passed a malformed record that a writing run failed;
a missing comparison window counted as passed; the merge checked only files present (a partial
artifact could leave an older card or proposal current); unreadable/overflow rows ended in a
traceback; the watermark rule was outside the version hash; blocked cards still carried descriptive
intervals from the unvalidated inputs (now withheld, ledger numbers nulled). A second review pass
could not run (API rate limit); the fixes were verified by the new tests and by real-data runs.

**Behaviour changes in existing tests.** Four merge tests now supply publication metadata
(`regression/publication_fixture.py`); without it the merge exits 4 (they assert that too). The
2.9 proposal test's card now carries its (bar-based, `not_required`) integrity result: a card
without one is refused a proposal.

**Before / after** (`python scripts/repro_publication_212.py [tree]`): b4db7d0 - lab exit 1, lab
output and published repository both hold checkpoint 1 `supported`, card `supported` with
`research_integrity.ok: false`, a proposal, watermark advanced, merge exit 0. 2.12 - lab exit 1,
no checkpoint, card `blocked` ("research integrity failed: unresolved stored control for hour
2026-10-13T20:00Z: malformed: persisted before its own decision"), no proposal, watermark held,
last valid result named, merge exit 0 publishing only the blocked diagnostics. Formatting:
b4db7d0 exit 3 for a reformatted identical control; 2.12 exit 0, one stored line, bytes unchanged;
a genuinely different record exits 3 on both.

**Versions.** `lab/experiments.py` (COMMON, hashed into every design) changed, so all eight
evaluation versions and clocks change: A1 `ev-c368833b5ae6`, B1 `ev-125c86066f05`, C1
`ev-eb20553bce1c`, D1 `ev-2b023a90293f`, E1 `ev-6f279983100b`, F1 `ev-1c53cfe81c9f`, G1
`ev-5cbc55c34b6d`, H1 `ev-02fcecefd1bf` (from `ev-c35cdb2bc9bc`, `ev-5db159f025fd`,
`ev-2ace4c5a6647`, `ev-ffa18ae355ef`, `ev-79ea1d99704b`, `ev-33998e4f9082`, `ev-44a97c2d5259`,
`ev-e76cbdabf3f9`). The dependency scheme hashes whole files, so the bar-based designs' clocks
cannot be preserved without excluding changed evaluation logic, which is not done. Observations
before each new registration are reanalysis. Old namespaces, registrations and cards are kept.
`lab/evidence.py`, `lab/run.py` and the merge are presentation / persistence and unhashed.

**Tests.** 324 regression tests (303 + 21 in `test_rev212.py`) on Python 3.11 and 3.12; 25
numerical fixtures. On b4db7d0 the new file gives 9 failures (the reproductions), 9 skips (new
interfaces) and 3 passes (`*_preserved`: a valid run still reaches a supported 100/20 checkpoint;
a competing writer's stored winner is what labels, baseline and checkpoint reference rows use;
real differences still conflict).

# Research-integrity revision 2.11 (lab-2.2, control policy 2) — 2026-09-25

Response to the review of 2.10 (commit `8432df0`). Current main was inspected first: since
`8432df0` only automated data commits had landed, so both findings applied to the running code.
Both were reproduced on `8432df0` with `scripts/repro_controls_211.py` (runs against any code tree).
Collector, schedules, request budgets, hypotheses, thresholds, fees, horizons and skills are
unchanged.

| # | Finding (reproduced on 8432df0) | Fix | Tests (`regression/test_rev211.py`) |
|---|---|---|---|
| 1 | Inputs at 09:59:30, cutoff 10:00:00: the C and F modules returned the control although its decision is 10:00:30 (also at 10:00:29.999); stored selections had no decision-time check. The live B1 lab-2.2 namespace holds one such record, frozen at 00:49:05 for a decision at 00:49:07 | A control is usable at cutoff N only if its inputs AND decision are <= N; stored records also need their persistence time <= N and well-formed times (persisted before its own decision, a missing or non-integer time, or an hour that is not the inputs' hour -> withheld). A pending earliest candidate makes the hour `pending_processing` (never a later candidate instead, never frozen); the hour bucket stays the inputs' hour (09:00 in the example); nothing is back-dated and the 60 s assumption is unchanged. A stored record not usable at the cutoff is withheld, never rewritten or replaced | 1 ms before, exactly at and after the decision; inputs exactly at the cutoff; UTC midnight; pending then selected on a later run with no duplicate and the same hour; stored records with later persistence (read-only: provisional when identical), persisted before their decision, missing or string times; a writing run with a winner persisted after its cutoff (withheld, unresolved conflict) |
| 2 | Worker B (empty context) proposed the :10 observation after writer A had stored :20 for the hour; storage kept A but B returned its :10 proposal, whose 60-minute label differed (+4.75% vs -0.13% in the reproduction) | In a writing run proposals are appended under a scoped `fcntl` lock and read back; the returned controls are the stored records in full (identity, times, features, input hash, t_persisted), the context is refreshed for later calls and variants, and proposals are reported as `accepted` or `superseded` (only accepted ones enter `ctx["new"]`). A lost write raises `ControlIntegrityError`. Read-only runs never write and mark selections they compute as `provisional`; one that differs from a later stored winner is withheld | the competing-write interleaving through `module.run` and through `experiments.run_design` (labels, baseline rows and reference rows all use the :20 winner); repeated calls with a refreshed and with a stale context; multiple proposals; unchanged winner bytes; persistence failure and silently lost write; the lock around read-and-replace; read-only non-mutation |

**Safeguards.** Before any control leaves `lab/controls.py` (so before labelling and before the
long/short expansion) `validate` checks every control's times against the cutoff, decision >=
inputs + 60 s, one per hour, and - in a writing run - byte equality with the stored record;
violations raise `ControlIntegrityError` and fail the design. `lab/run.py` also compares the
labelled control rows of the primary pass with the stored selections field by field
(`evidence_agreement`) and records sha256 fingerprints of the controls used and of the stored
records. Diagnostics add pending processing, accepted and superseded proposals, withheld stored
records, unresolved conflicts, ready-but-unselected hours and the fingerprints. Any unresolved
conflict, ready-but-unselected hour or evidence mismatch is a RESEARCH INTEGRITY FAILURE: printed
in `reports/research.md` and on the card (`research_integrity`), and the lab exits 1 so the research
workflow fails visibly even when collection is healthy. `scripts/merge_research.py` refuses an
incoming batch whose control selections or checkpoints conflict with a different record already
in the checkout (the batch's evidence, checkpoints and reports were computed from the loser):
nothing is merged, the conflict is printed, and it exits 3; committed evidence stands.

**Adversarial review of the first 2.11 draft** (separate agent, read-only): no high or medium
findings; four low ones fixed with regressions - stored hours not yet reached at a cutoff were
reported as withheld; a closed hour with no record at a replay cutoff was reported as withheld
instead of missing; a stored record's source time was not checked (decision must be >= source +
60 s); a legacy duplicate key already in a checkout made every later merge a conflict.

**Behaviour changes in existing tests.** Two 2.10 tests expected a read-only replay to recompute a
slot whose later stored winner differs, and a timeless stored record to be silently replaced;
both now expect the slot to be withheld. The 2.9 checkpoint-merge test now expects a conflicting
batch to be rejected whole (a non-conflicting batch still merges). Two helpers without an explicit
cutoff now use the latest decision the data allow (inputs + 60 s).

**Before / after** (`python scripts/repro_controls_211.py [tree]`): cutoff at 10:00:00 and
10:00:29.999 - 8432df0 returns the control (decision after the cutoff) for both modules, 2.11
returns nothing and reports the 09:00 hour pending; at 10:00:30 both return it in the 09:00 hour.
Competing writes - 8432df0 returns the :10 proposal (t_persisted 10:40) while storage holds the :20
winner (t_persisted 10:25); 2.11 returns the stored :20 record byte-for-byte, reports it
superseded, and its context names the winner. The 2.10 hourly replay on the pinned 934bb25 data is
preserved: B1, C1, F1 16 controls each (2 before 2.10), 0 closed eligible hours without a control.

**Versions.** `lab/controls.py` changed (policy `hourly-first-available-2`), so B1, C1 and F1 get
new evaluation versions and clocks; A1, D1, E1, G1 and H1 are unchanged (their versions and clocks
continue). The lab-2.2 B1/C1/F1 namespaces - including the B1 record frozen before its decision
and the recomputed C1 decision - stay byte-for-byte; their data are recomputed under the new
versions as reanalysis.

**Tests.** 303 regression tests (285 kept, 18 new; three existing tests adapted as described)
plus 25 numerical fixtures. Five `*_common_api` tests fail on `8432df0`; the other 13 new tests
exercise interfaces the reviewed code does not have.

# Research-integrity revision 2.10 (lab-2.2) — 2026-09-24

Response to the review of 2.9 (commit `934bb25`, lab-2.1). Current main was inspected first: since
`934bb25` only automated data commits had landed, so the defect applied to the running code. The
collector, its schedule, request budgets, serialized writes and watchdog are unchanged; no API
request was added.

**Defect (reproduced on the pinned data).** Modules C (`liq_exposure`), F (`options_disagreement`)
and - found by the search for the same assumption - B (`accounts`) kept a collection record as a
comparison observation (control) only if its run's source time fell before minute 15 of the UTC
hour. GitHub starts the nominal :07 run later than that most hours. On 2026-09-24 00:00-15:31 UTC
the pinned snapshot holds 59 successful scheduled runs and every one of the 16 hours had at least
one record with the required inputs available in time, yet each of B1, C1 and F1 had two controls
(01:14 and 05:14): 13 of 15 closed hours had eligible records and no control. Bar-based hourly
controls (A flow absorption, D TWAP, G cross-asset, H deleveraging: one per whole-hour bar close)
and E's second-slot stream controls do not have the defect and are unchanged.

**Policy `hourly-first-available-1` (new `lab/controls.py`, modules B-3, C-3, F-3).**
- Candidates carry their REQUIRED inputs only: C the account observation and the same run's
  Hyperliquid mark; F the option record (never funding, never a signal); B both account
  observations of the transition. Required-input availability a = the latest observed_at of those.
- One control per UTC hour of a: the eligible candidate with the smallest a; ties by source time,
  then by the candidate's input key. The existing >60-minute late-input exclusion still applies; a
  candidate missing an input is skipped and the next one considered; an hour with none has no
  control and a recorded reason; nothing is carried between hours.
- Decision time = a + the existing 60 s assumed processing, never re-dated to the hour: inputs at
  10:18 give a decision at 10:19. Source 23:58:30 with inputs at 00:00:30 belongs to the new day's
  00:00 hour; inputs at 09:59:30 decide at 10:00:30 and stay in the 09:00 hour.
- Selection reads no outcome, label status, baseline fit or profitability.
- The first lab run that selects an hour's control freezes it (append-only
  `research/v2/<design>/<version>/controls/YYYY-MM.jsonl`, keyed by policy and hour, written at
  selection time before any checkpoint of that run; first record wins, also in
  `scripts/merge_research.py`). Later runs use the stored record, so a late-committed record with
  an older source time or earlier availability, a later price, funding or label change, a rerun or
  a concurrent merge cannot displace it. A stored selection is used only at cutoffs at or after its
  `t_persisted`; a record without one is never used.
- Frozen controls count as known from their selection time: checkpoint reference rows already used
  max(label_available, t_persisted), and the shared baseline (`lab/baseline.py`) now does the same
  for its training rows, so a control selected after a cutoff never trains that cutoff's baseline
  (found by the adversarial review of the first draft; for designs whose controls are not frozen the
  rule changes nothing).
- `lab/controls.py` is hashed in full into the versions of the modules that call it
  (`versioning.MODULE_HELPERS`), not only through their import line.

**Diagnostics and reports.** Evidence cards gain `horizons` (primary and secondary, with the rule
that only the primary decides status and proposals) and `comparison_coverage`: the policy, window,
hours covered, closed hours and the partial hour, hours with eligible candidates, selected times
(availability and decision), missing hours with reasons, delay from the hour to availability, an
explicit flag for a closed hour with eligible candidates but no control (must stay empty), and per
horizon and phase the controls selected / mature / incomplete / scorable / retained / baseline-usable
(so an immature label or overlap thinning is never read as a collection gap), plus decision timing
(source, assumed decision and actual persistence times; decision-lag summary). The per-horizon
accounting reads the labels the lab actually computed (`lab/run.py` wraps `experiments.label_all`
read-only; a failure there cannot fail a design). `reports/research.md` shows all of it per design;
`reports/skill_proposals.md` states the primary-horizon rule. `report.py` (report-2.6) labels the
research-lab freshness row with the recorded lab version instead of a hard-coded "lab-2.0".
Promotion thresholds are unchanged.

**Before / after** (`scripts/replay_controls_210.py CODE DATA 1790263916213`, pinned data and cutoff
2026-09-24 15:31:56Z, window from 00:00Z: 16 hours, 15 closed). Eligibility is derived from the raw
records, independent of either policy: 16 hours with eligible candidates for each module.

| Design | 2.9 controls | 2.9 closed eligible hours without control | 2.10 controls | 2.10 closed eligible hours without control |
|---|---|---|---|---|
| B1 | 2 (01:14, 05:14) | 13 | 16 (one per hour) | 0 |
| C1 | 2 (01:14, 05:14) | 13 | 16 | 0 |
| F1 | 2 (01:14, 05:14) | 13 | 16 | 0 |

**Versions and clocks.** `lab-2.2-2026-09-24`. Every design gets a new evaluation version: B1, C1
and F1 because their control selection changed; all eight because the shared baseline gained the
selection-time rule and the lab version changed. A1, D1, E1, G1 and H1 had no evaluation
observations; the lab-2.1 C1 version (`ev-448e00c8b90b`) had one frozen evaluation decision
(2026-09-24 01:27Z, long_cluster) with its outcomes - it stays byte-for-byte under that version and
is recomputed under the new C1 version as reanalysis, never rewritten. Old registrations, cards,
events, outcomes and legacy files are untouched; superseded versions are indexed as such.

**Tests.** 285 regression tests (266 kept; 19 in `regression/test_rev210.py`; one assertion in
`test_integrity.py` now checks the running report version instead of the literal "report-2.5")
plus 25 numerical fixtures. Seven `*_common_api` tests drive only `module.run` and fail on
`934bb25`; the rest pin the new interfaces.

# Research-integrity revision 2.9 (lab-2.1) — 2026-09-23

Response to the review of 2.8 (commit `c9fff86`). The default branch was inspected first: from
`c9fff86` to the start of this work only automated data commits had landed, so all three issues
applied to the running code. Each was reproduced on `c9fff86` with `scripts/repro_integrity_29.py`
(runs against any code tree) before it was fixed. The collector is unchanged (`collector-2.7`):
schedule, budgets, source isolation, serialized writes, watchdog and request limits are untouched,
and no stored observation, cohort, frozen decision or earlier evidence file is rewritten.

| # | Issue (reproduced on c9fff86) | Fix | Tests (`regression/test_rev29.py`) |
|---|---|---|---|
| 1 | The first 100 test observations gave `retired`; appending 100 later ones gave `supported` at the same n=100 look (the look reused the first 100 outcomes but took the long share, reference, severity and controls from the whole sample) | A verdict exists only as a recorded checkpoint. Cutoff C = the earliest time the look's n retained test observations were known (outcome available and decision frozen); test, reference or controls, direction mix, severity, blocks, baseline training rows and predictions, data quality and the family's variant count are all bounded by C. The manifest (every input row and prediction, criteria, cutoff, version), its sha256, the checks and the verdict are appended to `research/v2/<design>/<version>/checkpoints.jsonl` once and never recomputed; later data is audited against it (drift, with what differs) but cannot change it. Pending = n not yet known. A correction is a new evaluation version (automatic on any semantic change), which leaves the old records in place | `CheckpointTests`: n=100 verdict unchanged after appending (also via a single run with all 200); later direction flips, severities, outcomes, controls and appended controls leave the manifest hash identical; delayed outcomes move the cutoff and stay out; exact boundaries; freeze time; pending; quality window; later looks use their own additional observations and cutoffs; idempotent repeat runs; multiplicity as of the cutoff; drift reported not rewritten; new version keeps the old record; tampered manifests fail verification; skill proposals quote a verified checkpoint only. `CheckpointMergeTests` |
| 2 | Funding first observed at 10:00 changed whether a 09:45 option event (inputs complete 09:47) existed: the z-score history stamped every feature with the option record's time | Each history feature carries its own availability (rr25: the option record's `observed_at`; funding: its snapshot's `observed_at`). The window is the last `z_window` earlier records already observed at the decision; within it a funding value counts only if its snapshot was observed by then, otherwise it is missing (never filled) and the 70% coverage rule applies; funding with no snapshot time is unknown | `OptionsAvailabilityTests`: 10:00 funding cannot change the 09:47 event (existence, direction, features, eligibility; quote-qualified and mark-only); it is used by the 10:00 decision; exact cutoff (equal counts, +1 ms does not); missing funding stays missing and can fail coverage; a delayed current snapshot delays the decision; late records and later records do not revise the event |
| 3 | A baseline trained on 60-minute control outcomes predicted the 30, 240 and 480-minute outcomes | One OLS model per horizon, trained only on same-horizon control labels whose `label_available` (new on every label: the latest availability of the bars it read) was no later than the prediction's UTC day and, at a checkpoint, its cutoff; cache keyed by (horizon, day, cutoff). Each outcome is routed to its horizon's model; each summary reports the model's training target, training rows, identifiable share and unidentified reasons; a horizon without enough labels is unidentifiable and its comparison withheld (never borrowed from another horizon). A single model for a multi-horizon design is refused | `HorizonBaselineTests`: horizon-specific outcomes give ~0 residuals at 30/60/240 (2.8: +47.7 and +33.4 bp); training rows same-horizon and known by the bound; a control that ended before the day but was available after it is excluded; missing 480-minute labels stay unidentifiable; the primary-horizon checkpoint uses its own model and is blocked, not rescued, when that model is unidentifiable |

**Before / after** (`python scripts/repro_integrity_29.py [tree]`): #1 `retired` -> `supported` on
c9fff86 after appending, `retired` / `retired` on 2.9 with the n=100 checkpoint recorded (p_long 0.0);
#2 the 09:45 event present with small future funding and absent with large future funding on c9fff86,
identical on 2.9 for both policies; #3 mean 30/240-minute test residuals +47.7 / +33.4 bp and the
480-minute baseline "identifiable" with no 480-minute controls on c9fff86, 0.0 / 0.0 bp and
unidentifiable on 2.9.

**Other changes.** `summarize` takes a baseline per horizon; `status` reads recorded checkpoints
only (a terminal record that fails re-verification yields `blocked`, never a verdict) (the pass's data state no longer gates promotion; the in-window quality check does, and the
pass state stays on the card); a checkpoint verdict of `blocked` shows as status `blocked`.
`scripts/merge_research.py` never adds a second record for a look already in the checkout.
Evidence cards carry `checkpoints` (records without the per-row manifest, `verified`, pending,
drift); the index records `superseded_by` for superseded versions; `reports/skill_proposals.md`
proposes only from a supported checkpoint whose manifest re-verifies and quotes that checkpoint.

**Hardening from an adversarial review of the first 2.9 draft** (each with a regression in
`test_rev29.py`): (a) episodes of the primary prospective pass are built in the order decisions
became known (`events.collapse_as_known`), so a decision frozen after a cutoff can join an episode
but never displaces a known head or removes a known observation (`KnowledgeOrderTests`); (b) an
option control's only required input is its option record, so a late or missing funding snapshot
no longer moves, delays or drops a control; (c) the first stored freeze of a decision wins when
frozen decisions are loaded, and `merge_research.py` keys frozen-decision lines by
`decision_key`; (d) `label_available` also covers the settled funding a label attributes (as
`(t, rate, avail)`), a label whose window contains a settlement time the funding series has not
reached is immature rather than completed without it, and the spread snapshot used for costs must
have been observed by the decision; (e) `verify_checkpoint` also checks record/manifest
consistency (n rows, cutoff, every row known by the cutoff, adjusted alpha, look schedule, and
against the design: n per look, version, horizon, sign); the sha256 is tamper-evident, not a
signature; (f) the family's variant count at a cutoff includes current versions only if
registered by then; (g) a checkpoint already stored by another writer is re-read and used.

**Test-suite date dependency found at deployment.** The first regression run on main after the
merge (00:02Z on 2026-09-24) failed in the unchanged 2.7 test
`test_stream.ConnectionTests.test_bybit_gap_resubscribes_and_disconnect_recorded`: the service
files each gap under the UTC day of its own time (the update-id jump under its message time,
2026-09-23; the disconnect under the wall clock), while the test read only today's partition, so
it could pass only on 2026-09-23. It fails identically on `c9fff86` after midnight. The test now
reads both days; `stream/` is unchanged.

**Migration.** `lab-2.1` changes the semantic code, so the first lab-2.1 run registers a new
evaluation version for every design; the lab-2.0 versions are marked `retired (superseded)` with
`superseded_by`, and their registrations, cards, experiment and ledger rows stay byte-for-byte. No
lab-2.0 version had a frozen evaluation decision or a completed look (no `research/v2/<design>/`
directory existed), so no verdict needed re-deriving. Recomputations of data collected before the
new registration are labelled `reanalysis`.

**Versions.** `lab-2.1-2026-09-23`; collector and report unchanged. Tests: 266 regression tests
(238 kept; 28 in `test_rev29.py`; four 2.8 promotion tests in `test_lab.py` and the summaries in
`test_integrity.py` were ported to the checkpoint and per-horizon interfaces with the same intent,
none removed; the one assertion that an `insufficient_data` pass cannot promote became an
assertion that incomplete labels inside the checkpoint window block it; the synthetic funding
series of `test_costs_direction_and_funding` gained a zero settlement at 08:00 so it reaches the
end of its 8-hour window) plus 25 numerical fixtures.

# Research-integrity revision 2.8 (lab-2.0) — 2026-09-23

Response to the review of 2.7 (commit `900d0b1`). The default branch was inspected first: from
`900d0b1` to the start of this work only automated data commits had landed, so every finding
applied to the running code. Each was reproduced on `900d0b1` with `scripts/repro_integrity.py`
(runs against any code tree) before it was fixed. The collector is unchanged (still
`collector-2.7`): schedule, budgets, source isolation, serialized writes, recovery artifacts,
watchdog, the fixed/rotating account policy, the six-hour ranking cache and request limits are
untouched, and no stored observation, checkpoint, frozen forecast or lab-1.0 output is rewritten.

| # | Finding (reproduced on 900d0b1) | Fix | Tests |
|---|---|---|---|
| 2 | Two events an hour apart whose inputs arrive together enter at the same bar, yet counted as 2 independent observations at 30 and 60 min | Thinning on actual label intervals `[entry_t, exit_t)`; dependence blocks (overlap or same UTC day, across groups) drive the bootstrap; firings / episodes / scorable / retained / blocks reported separately; nothing called independent | `test_integrity.OverlapTests` (identical entry, partial overlap, touching boundaries, all four horizons, delayed batch, outage catch-up, opposite directions, cross-group blocks, outcome-blind selection) |
| 3 | A prior BTC bar delayed 49 min left a module G event dated 48 min before that input existed (the check used only the final bar) | Every module computes `t_inputs` over every required input (windows, prior sigma/return windows, threshold and volume history, marks, cohort records, insurance rows); > 60 min of delay excludes; optional inputs (funding, spot, spreads) only if already available; decisions frozen at the first lab run (`t_persisted`), late replays excluded from evaluation; the 60 s processing time is labelled an assumption | `AvailabilityTests` (G delayed/excluded, funding as-of, A prior bar and optional spot, C mark), `FreezeTests` (recomputation cannot alter a frozen decision; late replay excluded) |
| 4 | 7 of 8 designs had no baseline predictors, so "supported" needed no added value; registration keyed on design JSON only | Out-of-sample baseline for every design (OLS on prior return, volatility, aligned funding, fitted on controls matured before each UTC day); unidentifiable baseline or quality blocks promotion; severity comparability for event references; Bonferroni over variants x 4 scheduled looks; evaluation versions bind design + semantic code + data dependencies; versioned namespaces for events, outcomes, registrations and cards | `VersionTests` (code-only change = new version; docstring, comment, README and data edits = same; superseded evidence stays), `test_lab.ExperimentTests` (promotion, blocking, multiplicity, severity) |
| 5 | Ledger query 0-80 min with a deposit at minute 5 labelled a 60-75 min transition "confirmed transfer" | Per-transaction filtering to `(t0, t1]`, account/coin/side matching, `liquidatedPositions` and `liquidatedUser` checks, explicit covered / partial / failed / not_attempted / unchecked states, knowledge at decision vs later confirmation (`lab/hlevidence.py`) | `AttributionTests` |
| 6 | 1-2 ms of timing jitter turned 3 liquidity events and 1 control into 0 and 0 | Nearest-second slots within 250 ms, deterministic duplicate resolution, 2 s freshness, 5 s availability; gaps and missing or stale seconds still fail coverage | `StreamTimingTests` (Recorder -> LocalStore -> module; exact vs jittered identical; missing, stale, sequence gap) |
| 7 | All 12 panel quotes stale changed only counters; the event was unchanged | Descriptive mark-IV surface separated from a quote-qualified signal: the 25-delta legs of the ~7-day expiry must be fresh, two-sided, uncrossed, within 10% spread, > 1 day to expiry and have mark IV inside the quotes; failures regroup events as `*_ineligible`; unobserved quality stays unknown; a mark-only variant is labelled descriptive and never promotable | `OptionQualityTests` |
| 8 | `reports/latest.md` was report 2.3 from 16:17Z after the 2.7 deployment | `report.py --coverage-only` refreshed every 6 hours by the Research lab workflow; every report states generation time, input cutoff, versions and per-dataset freshness; outputs merged into a fresh checkout without rewinding newer content (`scripts/merge_research.py`) | `PersistenceTests` |

Qualifications. Finding 3 reproduces at 48 minutes with the repository's own synthetic
construction (the review reported 49; the mechanism is identical). Finding 7 is a policy gap, not
evidence that the mark-IV values were stale: mark IV is collected independently of the panel and is
still reported, now labelled descriptive. Hyperliquid spot transfers are stored by the collector
only as counts without times, so they cannot be attributed to an interval; they do not move perp
margin and are excluded from transfer attribution.

**Migration.** The first lab-2.0 run registers a new evaluation version for every design
(`state/lab_registrations.json`); lab-1.0 registrations (`state/lab_registered.json`) and outputs
(`research/evidence/cards`, `research/experiments`, `research/ledger`) are kept byte-for-byte,
marked legacy in `research/evidence/index.json`, and never written again. Design files moved to
`version: 2` (baseline block, `min_retained_observations`, `min_dependence_blocks`). No lab-1.0
decision had been persisted (no module had prospective events), so nothing needed reinterpreting.
Recomputations of data collected before registration are labelled `reanalysis`, never evaluation.

**Versions.** `lab-2.0-2026-09-23`, `report-2.5-2026-09-23`; collector unchanged. Tests: 238
regression tests (200 kept, 3 added to `test_lab.py`, 35 in `test_integrity.py`; eight 2.7
lab tests were adapted to the new APIs with the same intent, none removed) plus 25 numerical fixtures.

# Research-data revision 2.7 — 2026-09-23

Adds the data and the machinery to look for testable trading advantages and to review changes to
the desk's skill files against evidence. It is additive: no stored observation, checkpoint,
frozen forecast, score or provenance field is rewritten, every new record is versioned, and each
new collection path can be switched back without a code change. The 15-minute schedule, stage
budgets, serialized writes, deadline handling, recovery artifacts, dedup and watchdog behaviour
are unchanged; the six-hour ranking cache and the 200-account Hyperliquid budget are kept.

**Collector (`collector-2.7`)**

- *Deribit options, schema 2* (`optionsbook.py`). The per-run record keeps the schema-1 fields
  (`[instrument, OI, mark IV]` rows, `underlying`) and adds: zero-OI instruments by name, listed
  instruments absent from the summary, past-expiry names, instrument metadata status, the
  per-expiry underlying (`underlying_v2`), estimated delivery price, and a 12-ticker quote panel
  (expiries near 2/7/30 days, call/put at Black-76 delta 0.50/0.25). Full quotes (bid, ask, mark,
  last, rolling-24h volume in BTC and USD, source time offset) go to a separate hourly record
  `options/deribit_btc_quotes`; listing changes to `options/deribit_btc_listing`. Rolling 24h
  volume is labelled as such and never presented as interval volume; null bid/ask means no resting
  order, zero OI is listed, not omitted. Revert: `OPTIONS_SCHEMA=1`.
- *Hyperliquid sampling policy `hl-sample-v2`* (`hlsample.py`). Same 200-request budget: a fixed
  cohort of 100 (the top 100 of the first ranking seen under v2, frozen with its selection time,
  ranking hash and member hash in `state/hl_cohort_fixed_v2.json`, never re-selected), 90 rotating
  accounts from the top 1,000 (cursor in state), and at most 10 enrichment requests (fills, ledger,
  TWAP history; weight-capped at 400). Every sampled account is recorded as ok_btc / ok_flat /
  ok_other / failed / not_attempted, with margin summary and BTC/ETH/SOL positions, in
  `hl_accounts/`; enrichment results in `hl_enrich/`. No account is selected by later performance.
  The v1 BTC position record is still written (with `sampling_policy`). Revert:
  `HL_SAMPLING_POLICY=v1`.
- *Enrichment stage* (`enrich.py`, 10% of the budget, after forward books, failures isolated):
  closed 1-minute bars for Binance USD-M BTCUSDT (last and mark), spot BTCUSDT, ETHUSDT and
  SOLUSDT perps as batch records in `data/prices/<series>/` (checkpointed, first observation
  wins, malformed pages rejected); OKX BTC-USDT swap insurance fund rows (balance plus every
  bankruptcy-loss, ADL and liquidation-deposit row newer than the last) in `okx_insurance/`.
- *Cross-asset snapshot sources*: Hyperliquid and Binance ETH and SOL mark, funding (with its
  interval) and OI in base and quote units.

**Research lab (`lab/`, `lab-1.0`)** - a separate package, run by the new *Research lab* workflow
every 6 hours (compute without the write lock; commit through `repo-write`).

- Layers with provenance: events (with their feature records), outcomes, experiments, a variants
  ledger that keeps null results, and evidence cards. Every record carries `t_event`,
  `t_first_observed` and `t_available`; historical reconstructions are labelled as such.
- Outcome labels at 30 m, 1 h, 4 h, 8 h: return, range, MFE/MAE, realised volatility, and net
  return after an explicit cost model (`costs-1`: fees and slippage are stated assumptions,
  spread from the nearest depth snapshot, funding from settled rates). Entry is the first bar at
  or after availability; immature and incomplete labels are never stored or filled.
- Episodes are collapsed; scheduled controls give baselines; test-minus-reference intervals use a
  day-block bootstrap; outcomes are thinned to non-overlapping windows. Designs are frozen by hash
  and registered on first sight; only episodes after registration can move a design toward
  "supported". Statuses: exploratory, under prospective evaluation, supported, retired.
- Eight modules (A flow absorption, B account behaviour, C liquidation exposure, D TWAP lifecycle,
  E liquidity recovery, F options/perp disagreement, G cross-asset, H exchange deleveraging), each
  reporting available / insufficient_data / unavailable with the reason.
- `reports/research.md` and `reports/skill_proposals.md`; a change to the skill files is proposed
  only for a supported design. `lab/skill_eval.py` compares a current and a revised skill offline
  (case checks and an evidence audit that flags overclaims); live comparison is optional, needs
  an API key, and writes only outside the repository.

**Streaming service (`stream/`, `stream-1.0`)** - implemented, tested and live-smoke-tested, not
deployed: Deribit, Bybit and Hyperliquid books, trades and forced-flow messages with sequence
checks, gap log, heartbeat, rolling pre/post capture buffer, hourly controls, gzip partitions and
an optional S3-compatible durable copy. Needs an always-on host (see `stream/README.md`).

**Report** `report-2.4`: section 3c covers the new datasets and the lab's last run.

**Fixes found while testing this revision.** Module H could judge a 5-minute liquidation bucket
before the bucket had closed; it is now judged at max(first observation, bucket close). Module D
could value a TWAP with a later price; it now uses only bars available at first observation.

**Tests**: 76 new (`test_rev27.py` 20, `test_lab.py` 30, `test_stream.py` 26); the full suite is
200 tests plus 25 numerical fixtures, offline, about 20 s.

# Collection cadence revision 2.6.1 — 2026-09-23

From the review of 2.6 (commit `62e51cc`), two failure cases found by simulated faults; neither
occurred in a deployed run.

**One stalled venue could still cost every venue its snapshot.** The 2.6 stage limit kept time
for the snapshot stage but did not isolate venues inside it. Binance is requested first; with every
Binance request stalled, the 120 s stage made 5 Binance attempts, 0 requests to any other venue,
and stored 0/17 books (reproduced). Two controls now apply to snapshot sources:

- Each source has its own time cap (`SNAP_SOURCE_S` = 15 s; a normal source answers in under 2 s).
- A host whose request failed at the transport level on every attempt (timeout, reset, DNS) is
  skipped for the rest of the snapshot stage ("circuit open"), so its other sources fail at once.
  HTTP error statuses and malformed bodies are fast and do not open the circuit. The circuit is
  limited to the snapshot stage, so one Hyperliquid account timing out still cannot reject the
  200-account map, and it resets each run.

Same simulation under 2.6.1: 1 Binance attempt, 27 requests to other venues, 14/17 books
collected (every non-Binance book), stage done in 20 s. Run records add `circuit_open` (hosts) and
`http.circuit_skipped`.

**A total snapshot loss was reported healthy.** With history intact and 0/17 books, the watchdog
exited 0 with warnings. `cadence.failure_summary` now treats a run with no open-interest book as
critical (watchdog exit 2, "no open-interest book collected (0/17)"; counted in the report's
critical line). A partly degraded snapshot stays a warning. The collector's own exit code is
unchanged: it still fails the workflow only when the critical Binance share series fails.

**Tests**: 5 new, 1 strengthened (`regression/test_rev26.py`). The stalled-venue tests now supply
valid answers for every other venue and require all 14 unaffected books to be collected, not
merely attempted. 6 of the new or strengthened tests fail or error on 2.6.

# Collection cadence revision 2.6 — 2026-09-23

The collector runs every 15 minutes (`7,22,37,52 * * * *`) instead of hourly. This revision is
about cadence and operational reliability only: no forecast, scoring rule, trading rule or stored
observation changes, and every existing data file, checkpoint, frozen forecast, score and provenance
field is kept as it was.

**Schedule and time budget**

- `collect.yml` keeps its file name, so the workflow's run history and dispatch URL carry over;
  its display name is now **Collector**. Manual runs and backfill are unchanged.
- Routine run: 10-minute network budget (`COLLECTOR_BUDGET_S=600`), collection step limit 11
  minutes, persistence bounded at 100 s, job limit 14 minutes. Backfill keeps its own budget:
  30 minutes of network, 35-minute step, 45-minute job. The previous 20-minute budget inside a
  30-minute job would not fit a 15-minute slot.
- Stage limits inside a routine run (shares of the budget): history series 40%, liquidations 15%,
  snapshot 20%, forward books the rest. History and liquidations are checkpointed and recover next
  run; snapshots and forward books cannot be fetched later. In simulation under 2.5, one stalled
  venue (Binance) spent the whole budget on history and left 0 s for the 17-book snapshot; under
  2.6 history stops at 240 s and the snapshot and forward books still run.
- `scripts/commit_push.sh` bounds its whole push/rebase loop (`PERSIST_BUDGET_S`, 100 s for the
  collector, 240 s default) and gives each network step at most the time left, so a hung remote
  cannot run persistence past the job limit. Success still requires a successful push.
- The daily liquidation boundary probe keys on the UTC day it last succeeded
  (`state/checkpoints.json: liq_probe_day`) instead of the 00Z hour, which at the new cadence
  would have paged the full feed four times; a failed probe is retried on the next run.

**Queueing** (checked against GitHub's current concurrency documentation before the change)

- Scheduled collector runs share one workflow-level group with GitHub's default queue: at most one
  running and one pending, and a newer pending run cancels the older pending one. During an outage
  or a long backfill, obsolete scheduled runs are dropped instead of accumulating. Nothing running is
  ever cancelled. Manual and backfill runs have their own groups, so a scheduled run never cancels
  a manual check.
- Every repository writer (collector, backfill, forecast intake, weekly report) now takes
  `repo-write` at job level with `queue: max` (up to 100 waiting jobs), so writes stay serialized
  and intake and report work is never dropped behind collector runs. Job level also keeps a skipped
  intake job (an issue that is not a forecast) out of the queue.

**Provenance and health**

- Run records carry `mode: "routine"` (`"hourly"` in older records, still read as routine),
  `trigger` (`schedule`, `workflow_dispatch`, or `local`), the cron entry that fired, the Actions
  run id and attempt, the budget, per-stage seconds, stages cut by their limit, whether the budget
  was reached, and request accounting: requests, failures, deadline skips, and rate-limit
  incidents by host (HTTP 429/418 and OKX code 50011).
- `cadence.json` records every schedule the collector has run under. Health figures use the
  cadence in force at each moment, so the hourly period is not reported as three runs in four
  missing.
- The weekly report separates **scheduled execution** (scheduler starts counted against nominal
  slots; manual runs excluded; starts are never matched to slots, because GitHub's start delay is
  unrecorded) from **snapshot coverage** (slot intervals holding a stored snapshot, whatever started
  it). Pre-2.6 records do not say what started them, so their scheduled share is shown as an upper
  bound, not a count. It also reports actual intervals between runs and between snapshots, runtime
  percentiles, budget hits and rate limits, and groups alerts by source (count, first, last, latest
  message) instead of one line per run.
- Watchdog every 30 minutes (`17,47`), stale limit 90 minutes (`WATCHDOG_STALE_MIN`, repository
  variable or dispatch input). Exit 1: stale or missing, judged on runs the schedule could have
  started; a recent manual run does not hide a dead schedule. Exit 2: running but the latest
  scheduled run lost critical data. Exit 0 with warnings: source failures, degraded books or rate
  limits in recent runs. It checks out only `data/runs` and the code.

**Tests**: 32 new (`regression/test_rev26.py`): cadence transition, delayed, dropped and manual
runs, aggregation, watchdog states and threshold, workflow budgets and queues parsed from the YAML,
a sustained outage finishing inside the budget with the persistence window left, a single stalled
venue, bounded persistence against a hung remote, the once-a-day probe, provenance and rate-limit
accounting, and native 5m/1h resolution without duplicates across quarter-hour runs. One 2.5
watchdog assertion changed deliberately: a run 2 hours old is now stale (limit 90 minutes, was 3
hours).

**Limitations**

- Repository growth: about 44 KB of text per routine run (12 KB gzipped), roughly 125 MB a month
  in the working tree, mostly the Deribit option book. Git storage grows by the compressed
  amount, but every run checks out the full tree, so checkout time grows too. A later revision
  should compress or relocate the forward-only books; nothing here changes their format.
- GitHub may start scheduled runs late or skip them under load; the health figures report that
  rather than prevent it. Actions minutes are free for this public repository; a private copy
  would use about 8,600 billed minutes a month at this cadence.
- A manual run can wait behind a running scheduled run (one `repo-write` queue); it is never
  cancelled by one.

# Reliability revision 2.5.1 — 2026-09-23

From the review of 2.5: cleaning up an abandoned HTTP-error response could overrun the deadline.
`_abort()` looked for the socket at `resp.fp.raw._sock`, which is right for a normal response, but
an `HTTPError` wraps the response one level deeper, so the shutdown failed silently and the
following `close()` waited on the lock held by the worker's receive. Reproduced with a local server
that sends headers, one body byte 0.1 s before a 1.2 s deadline, then stalls:

| Status | 2.5 | 2.5.1 |
|---|---|---|
| 503 | 2.31 s, rejected | 1.20 s, rejected; worker released at once |
| 200 | 1.20 s, rejected | 1.20 s, rejected |

- `_find_socket()` follows `fp`/`raw`/`_sock` through any wrappers to the socket.
- `_abort()` only shuts the socket down. It no longer calls `close()` from the waiting thread, so
  cleanup cannot block even if a future wrapper hides the socket; the worker closes its own
  response once released, or ends at its socket timeout.
- Tests: two late-byte stall cases (503 and 200) assert the caller returns within 0.15 s of the
  deadline and that the abandoned worker finishes within 0.5 s, which only a shutdown that reached
  the socket achieves. The 503 case fails on 2.5.

# Reliability revision 2.5 — 2026-09-23

From the review of 2.4: the deadline capped the socket timeout, but a socket timeout limits each
blocking operation, not the request. Reproduced on a local server with a 1.2-second budget:

| Server behaviour | 2.4 | 2.5 |
|---|---|---|
| Body sent one byte every 70 ms | 3.45 s, response accepted | 1.20 s, rejected: deadline |
| Headers sent one byte every 50 ms | 3.57 s, response accepted | 1.20 s, rejected: deadline |
| DNS lookup stalled 3 s (no socket exists yet) | not bounded | 1.2 s, rejected: deadline |

- **Whole-request limit.** `fetch()` runs each request in a daemon worker thread and waits for it
  only until the deadline, covering DNS, connection, TLS, headers, body, and HTTP error bodies.
  On expiry it shuts the socket down to release the worker, discards any late result, and the
  request counts as failed. Bodies are read in `read1` chunks with a deadline check between them,
  so the worker also stops itself.
- **Monotonic deadlines.** The run and Hyperliquid deadlines use `time.monotonic()`; a wall-clock
  step can no longer lengthen or shorten them. Stored timestamps stay on wall-clock UTC.
- **README** now states what the limit covers and what it does not (local writes after the
  deadline; the workflow's commit and push; an abandoned thread's lifetime).
- Tests: `SlowResponseTests` uses real sockets on 127.0.0.1 — trickled body, trickled headers,
  trickled 503 body, stalled DNS, and a prompt response that must still succeed. The three trickle
  tests fail on 2.4. The fake-clock helper now patches the clock only inside `with`, after a
  failing test in development left it installed for the tests that followed.

# Reliability revision 2.4 — 2026-09-23

From the review of 2.3: the Hyperliquid map had no time limit. Measured on a simulated clock where
every request hangs for its full timeout:

| Simulated outage | 2.3 | 2.4 |
|---|---|---|
| Hyperliquid only | 400 requests, 190 min | 27 requests, 5.0 min, stopped at its budget |
| Every venue, whole hourly run | 576 requests, 285 min | 38 requests, 20.0 min, run record written |

The workflow kills the job at 30 minutes and persists only after the collector exits, so 2.3 could
lose the whole hour's data in a long outage.

- **Run-wide budget.** `get()` starts no request after the run deadline (20 minutes, or
  `COLLECTOR_BUDGET_S`) and caps each socket timeout and retry pause by the time remaining; every
  later stage fails fast and the run record is still written, leaving about 10 minutes for the
  commit and push.
- **Hyperliquid budget.** The map has 300 seconds (a normal map takes 70–120 s), 10-second request
  timeouts, and stops as soon as failures reach half the accounts, when the map could no longer be
  stored. Accounts not reached are listed as `not attempted: deadline` or `not attempted: rejection
  inevitable`; each snapshot records `stopped`, `elapsed_s` and `rate_limited`.
- **Rate limits.** A live run hit HTTP 429 on 3 of 200 accounts (the audit container's IP, after
  repeated runs). A 429 now gets one retry after a 5-second backoff inside the budget; the next
  live map was complete (200/200, 93 s).
- Tests: 7 in `OutageBudgetTests`; the 6 that predate the 429 change all fail on 2.3.

# Reliability revision 2.3 — 2026-09-23

From the external review of `ed45dd2`. Each item has a regression test that fails on `ed45dd2`
(9 of 23 tests in `test_rev22.py` fail or error there; all 73 tests pass here).

- **Range median error, named for its scale.** The review read `abs_log_error` (|ln q50 − ln
  realized|) as a mistake for |q50 − realized|. Both are legitimate on different scales: runbook
  E2 fits its baselines on ln lr ("B1 HAR-range — OLS on logs") and names "mean absolute error of
  ln range" as the primary loss, which is the log-scale figure; the lr-scale figure is what a
  reader of q50 in ln(H/L) units expects. The old field name let either reading pass. Now:
  `abs_error_lr` (|q50 − realized|), `abs_error_log_lr` (E2 primary), and `qlike` (E2 secondary).
  No range forecast had been scored. `scoring-2.2`.
- **Report formatting.** Scored events print per type: range events show realized ln(H/L),
  q10–q90 coverage, pinball losses, both median errors and QLIKE (2.2 printed `None`); interval
  events show the interval score. `report-2.2`.
- **Forward-book validation.** A Hyperliquid response without `marginSummary.accountValue` and an
  `assetPositions` list is a failed account (`{}` was stored as an account with no positions);
  a malformed BTC position fails its account; any failure marks the snapshot `degraded`, names
  the addresses, and reports an error; half or more failing (100 of 200 had passed with
  `err: null`) stores nothing. A Deribit option with OI but no positive mark IV or underlying, or a
  malformed name, is excluded and named, and the snapshot is `degraded`; over 5% invalid stores
  nothing. `collector-2.3`. The live run under 2.3 was complete: 850 of 850 option rows and 200 of
  200 accounts valid.
- **End-to-end scoring exercised** on live prices in a scratch copy: a synthetic forecast with all
  seven event types was registered before its start, frozen, scored on 180 Binance 1m bars,
  evidence hash-verified, and not rescored on a second pass. Not committed to the public registry.

# Reliability revision 2.2.1 — 2026-09-23

- The first GitHub backfill under 2.2 failed `binance_openInterestHist_5m` with
  `HTTP 400 (binance code -1130: parameter 'endTime' is invalid.)`: 2.2 began appending the venue's
  reason to 4xx errors, and the measured old-history boundary was matched as exactly `"HTTP 400"`.
  It now matches the prefix. Hourly runs were unaffected (they stop at the checkpoint first); no
  stored row was lost. Test: `test_backfill_boundary_400_with_reason_still_ends_history`.
- The same backfill closed every taker gap: 5m and 1h taker history now have 0 missing intervals.

# Reliability revision 2.2 — 2026-09-23

Audit of the deployed 2.1 repository against the live sources. Every defect below was measured,
reproduced by a regression test that fails on 2.1 (`regression/test_rev22.py`), and fixed.

## Data loss

- **Taker history lost one row per 500-row page.** Binance's taker endpoint filters `endTime` on
  the interval close; the ratio and OI endpoints filter on the stamp. Paging with
  `endTime = oldest − 1` skipped `oldest − step` on every taker page: 17 missing 5m intervals and
  1 missing 1h interval in the stored history, each exactly 500 rows apart. Paging is now
  endpoint-aware. A live backfill with the fix recovered all 18 rows; the oldest ages out of
  Binance's ~30-day window around 2026-09-23 04:50Z, so run one manual backfill after deploying.
- **Liquidation pages could drop the second order of a same-millisecond pair.** OKX `after`
  returns records strictly earlier than the given ts; ~2% of stored timestamps (50 of 2,493)
  carry two orders. Pages now re-request the boundary millisecond and deduplicate by key.
- **One unexpected response aborted the rest of the history run.** An exception inside any series
  block (for example a missing `fundingRate` key) skipped every later series that hour. Each
  series is now isolated; its error is recorded and the others proceed.

## Meaning of timestamps

- **Snapshot series were scored one interval late.** Measured: the Binance 1h ratio and OI rows
  equal the 5m rows at the same stamp, and the OKX account-ratio row stamped T is published before
  T+1h — they are values *as of* the stamp. 2.1 read every series at stamp + step, so a predicate
  "top notional under 68% at 06Z" (the template's own example) was scored on the 05:00 value.
  `schema.SERIES_KIND` now classifies each series; predicates read snapshots at their stamp and
  intervals at their close; research views admit snapshots at stamp + 5 minutes (M-01) instead of
  stamp + 1 hour. Scoring version `scoring-2.1`. No forecast had been registered under 2.1.
- The hourly snapshot series are now collected once published (stamp + 5m) rather than an hour later.

## Forward-only books (desk requirement 50)

- Deribit per-strike BTC option open interest with mark IV, hourly, daily files.
- Hyperliquid position map: BTC positions of the top 200 accounts by account value, with
  liquidation price and leverage type; ranking cached six hours.
- Both are isolated from the critical path; failures are reported per run and in the weekly report.

## Sources

- Retired `bitget_COIN` (Bitget 40309 "The symbol has been removed") and `bitmex` (XBTUSD and
  XBTUSDT settled 2026-09-16; no XBT perpetual open). The report lists them as retired, not failing.
- 4xx responses now keep the venue's own error code and message.

## Scoring and monitoring

- `range` event type: q10/q50/q90 of ln(high/low) over the window — the desk's E2 target — scored
  by coverage, pinball loss, and absolute log error of the median.
- `interval` events carry the interval (Winkler) score.
- `watchdog.py` and the Collector watchdog workflow: fail when the last hourly run is over 3 hours old.
- The report adds a forward-books section and per-run forward-book alerts.

## Not changed, and open

- The repository and the crypto-desk skill (package 10.1, `baserates.md` §4) each describe a
  forecast registry: this repository's issue intake and the skill's registry artifact. One must be
  chosen as the place forecasts are registered and scored; this revision changes neither.
- Action versions (`checkout@v4`, `setup-python@v5`, `upload-artifact@v4`) are unchanged; no run
  annotation was available to show a deprecation.
- Bybit is unreachable from US runners (CloudFront 403); its funding stays via Hyperliquid's aggregator.

# Reliability revision 2.1 — 2026-09-22

## Correctness and recovery

- Complete aligned price coverage is required before scoring; missing history cannot
  count as a forecast loss or false predicate. Failed observations remain retryable.
- Price API responses, JSON numbers, nested event schemas, default start times,
  predicate cadence, and UTC alignment are validated.
- Terminal comparisons are strict; flat leans are separate; race ties include Brier bounds.
- Interval predicates use closing timestamps and require complete observation coverage.
- Failed backward pages, stalled cursors, and page caps preserve prior checkpoints.
- DVOL fetches use checked daily grids and deduplicate inclusive response boundaries.
- Per-file atomic persistence and row identity checks make retries safe without
  rewriting legacy observations. Corrupt state and JSON lines fail visibly.

## Audit trail

- Forecasts are frozen by full SHA-256 and indexed by a persistent manifest.
- Scores retain forecast/evidence hashes and normalized observations for reproduction.
- Deleting or editing a registry source cannot selectively remove its frozen forecast.
- New observations include code version, commit, and completed-fetch availability time.
- Research fingerprints include local root Python dependencies. Mature results are
  labeled post-registration; point-in-time helpers exclude unstamped legacy observations.

## Operations

- Shared workflows use explicit queueing and the current default branch checkout.
- Push retry exhaustion fails explicitly; forecast acknowledgement follows successful push.
- Intake supports edited/reopened issues and reconciles unprocessed open issues hourly.
- Recovery artifacts retain unpushed data on workflow failures for seven days.
- Reports disclose all recorded collection errors, source failures, gaps, duplicates,
  stale histories, missing deployment evidence, and test failures.
- Coverage uses distinct scheduled slots rather than counting extra manual runs as uptime.
- Software regressions now run on code/workflow pushes and pull requests.

## Compatibility and limits

- Preserve newer live data/state when installing this archive; its captured history is
  unchanged from the supplied ZIP. Legacy report copies are under reports/legacy/.
- Three duplicate DVOL records remain in legacy history and are explicitly reported.
- Predicates now refer to interval close times; review any old, unfrozen designs.
- Invalid legacy forecasts must be corrected under a new ID; old scores need explicit
  review and are not overwritten. No forecasts or research designs were registered in
  the supplied snapshot.
- Research episodes now require input_cutoff and outcome_at; the template documents this.
- A hash registry is not tamper-proof against repository writers. Free text in public
  issues is not privacy-filtered. Live API/GitHub execution has not been verified here.
- No autonomous trading, path model, CRPS, bootstrap uncertainty, or skill installation
  has been added. The original numerical formulas remain substantively unchanged.
