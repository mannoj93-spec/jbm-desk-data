# Validation record — desk forecast contract, revision 2.15

Validated 2026-09-26 with Python 3.11 (container). Earlier blocks below are kept as recorded.

| Check (2.15) | Result |
|---|---|
| Audited snapshot / base | Audit at `0a9ba0e` (package 11.2, repo 2.14); built on `09549f8`; main later moved only by collector data commits |
| 2.14 deployment (recorded here because 2.14's own row was left open) | PR #15 merged 2026-09-26 02:15:24Z (`e98692e`). Manual run #1 (id 36211132618) completed; forecast skipped (stale bar); it committed only `reports/range.md` (`0a9ba0e`); `state/forecast_manifest.json` was `{}` at `0a9ba0e` and still `{}` at `c6f8211` (Sep 26 ~03:15Z). No scheduled 2.14 run had occurred at that check |
| Reproductions on 2.14 code | Finding 1: three unregistered files, retry skipped them, no manifest. Finding 5: bogus fit registered three. Finding 3: q50/exp(p) = 0.956 / 0.965 / 0.954. Finding 4: 5 / 17 leaked validation targets. Finding 7: conflicting DVOL `ok` with the last value; decreasing notional `ok` |
| Same on 2.15 | Each case fails closed or registers completely; see CHANGELOG 2.15 table |
| Regression suite | 479 passed (332 + desk 147); fixtures 25 |
| Evaluation versions | Identical for all eight designs (lab loader, before vs after) |
| O21 replay | From `desk/research/o21/inputs` (hash-verified): zero differences from the original result |
| September fit | Reproduced exactly (coefficients, residual quantiles, B0 quantiles) from the retained O21 inputs; validates under `validate_fit` |
| Checksums | `SHA256SUMS` regenerated from its list plus the new code and docs (data, fits, bundles and research outputs excluded) |
| Deployment of 2.15 | Not merged at this record. Evidence goes here after merge: merge commit, the first scheduled run's attempt and publication rows, and the status file |

# Validation record — desk range forecasts, revision 2.14

Validated 2026-09-26 with Python 3.11 (container). Earlier blocks below are kept as recorded.

| Check (2.14) | Result |
|---|---|
| Default branch before the work | `9a7820f` (collector data commits since 2.13); baseline suite 332 passed, fixtures pass |
| Full regression suite with `desk/` | 447 passed (332 + 115: `test_jbm_measure` 40, `test_jbm_archive` 47, `test_range_model` 18, `test_range_job` 10) |
| Evaluation versions | Unchanged: no file hashed by `lab/versioning.py` edited; no root `*.py` added or edited |
| Frozen model | `desk/range_model.py` sha256 `ae6aa254c786d2dd6045fab098c4237dbe8bcc07d6626d20617366d386ff687d` = the O21 freeze (2026-09-26 01:10:22Z); `range_job.py` refuses to run otherwise (tested) |
| September fit | `desk/fits/2026-09.json` built from 80 archive files (checksums all matched) and DVOL, 14,610 bars to Aug 31 20:00Z; applied to the Sep 26 00:00Z decision it reproduces the desk's hand-registered forecast to the fifth decimal (4h -5.10356, 24h -4.34643, 72h -3.24601) |
| End-to-end dry run (disposable copy, live data, 01:41Z) | refit no-op; three forecasts written, schema-valid, registered through `registration.register` at 01:41:36Z with start 01:45Z; frozen bytes and manifest entries created; `reports/range.md` written |
| Scoring path | `scoring.score` on a registered file with synthetic 1-minute bars returns both `range` events with coverage, pinball, `abs_error_log_lr`, QLIKE |
| Registration safety (tests) | start at the next 5-minute boundary after registration; an attempt at or after start aborts; a second run is idempotent; a DVOL candle not closed at the decision cannot change the forecast; a stale decision (> 1 h) is refused |
| Checksums | `SHA256SUMS` regenerated from its own list plus the new code, docs, fixtures, calendar and workflow (fits excluded: they are data) |
| Deployment | Recorded below after the web upload and merge |

# Validation record — research-integrity revision 2.13 (lab-2.2, evidence completeness)

Validated 2026-09-25 with Python 3.11 and 3.12 (container). Earlier blocks below are kept as recorded.

| Check (2.13) | Result |
|---|---|
| Default branch before the work | `f402459`; since the reviewed `16cb49f` only collector data commits; code identical to the review |
| Reproduction on `16cb49f` (`scripts/repro_completeness_213.py`) | Supported 100/20 run; checkpoint file removed from the handoff: merge exit 0, published card `supported` citing look 1, no checkpoint, proposal published. Control files removed: merge exit 0, card `supported`, stored control fingerprint != the card's |
| Same on 2.13 | Both: merge exit 4, destination byte-identical, previous valid card current, no proposal |
| Regressions | `test_rev213.py` 8: on `16cb49f` 3 fail, 2 skip, 3 pass; on 2.13 8 pass. Full suite 332 on 3.11 and 3.12; fixtures 25 |
| Evaluation versions | Unchanged (no hashed file edited; all 8 ids identical to 2.12), so no clock resets |
| No-write lab run (disposable copy of main) | Exit 0, no file changed |
| Idempotency and preservation (disposable copy, two writing runs at one cutoff) | Exit 0 both. No file under `data/`, `registry/` or `state/hl_cohort_*` changed; registrations unchanged (current versions already registered); stored controls append-only (B1 46->47, C1 46->47, F1 66->67 lines, earlier bytes kept); no stored checkpoint, event or outcome rewritten. Second run: only the B1/C1/F1 cards, the report (selection states) and the run counter changed; inventories identical |
| Real-data handoff (disposable copies) | Complete batch: merge 0. C1 control files removed: merge 4 ("stored control fingerprint differs from the one the evaluation used"), destination unchanged |
| 2.10 hourly replay (pinned `934bb25` data, cutoff 15:31:56Z) | B1, C1, F1: 16 controls each, 0 closed eligible hours without a control |
| Checksums | 115 entries (112 + `regression/test_rev213.py`, `scripts/repro_completeness_213.py`, `docs/OPERATIONS.md`), all match |

Scope: the gate proves the published outputs are complete and consistent with what the lab recorded
and re-verifies promoted checkpoints; it does not re-run the evaluation itself.

# Validation record — research-integrity revision 2.12 (lab-2.2, publication gate)

Validated 2026-09-25 with Python 3.11 and 3.12 (container); GitHub workflows select Python 3.12,
whose AST the evaluation-version ids are computed from. Tables below the 2.12 block are the record
of earlier revisions and are kept as they were (one 2.11 claim is marked corrected in place).

| Check (2.12) | Result |
|---|---|
| Default branch before the work | `f73d620`; since the reviewed `b4db7d0` only automated data commits (data/, state/checkpoints.json, state/liq_recent_keys.json); code identical to the review |
| Reproductions on `b4db7d0` (`scripts/repro_publication_212.py pin`; synthetic observations through the real `lab.run.main`, `controls.apply`, checkpoint evaluation and verification, evidence, proposals and `merge_research.py`) | Stored control persisted 1 ms before its decision, run at the look-1 boundary (100 retained / 20 blocks): lab exit 1 with RESEARCH INTEGRITY FAILURE, yet checkpoint 1 `supported` in the lab output AND in the published repository, card `status: supported` with `research_integrity.ok: false`, a skill proposal, watermark advanced to the failed run's cutoff, merge exit 0. Formatting: a reformatted identical control -> RECONCILIATION CONFLICT, exit 3 |
| Same reproductions on 2.12 | Lab exit 1; no checkpoint (lab output or repository); card `blocked` - "research integrity failed: unresolved stored control for hour 2026-10-13T20:00Z: malformed: persisted before its own decision; this attempt evaluated and recorded no checkpoint and persisted no decision"; publication `evaluation_valid: false`, no proposal ("proposal suppressed"); watermark held at the previous valid cutoff; `last_valid_result` = the previous valid attempt; merge exit 0 publishing only the blocked diagnostics. Formatting: exit 0, one stored line, bytes unchanged; a genuinely different record still exits 3 |
| New regressions (`regression/test_rev212.py`, 21) | On `b4db7d0`: 9 fail (boundary, recovery, malformed timing, future-persisted winner, stored-vs-labelled mismatch, error in a later variant, three canonical-merge cases), 9 skip (2.12 interfaces), 3 pass (`*_preserved`). On 2.12: 21 pass |
| Full regression suite | 324 passed on Python 3.12 and on 3.11 (303 baseline + 21); numerical fixtures 25 passed |
| Existing cutoff and authority behaviour | The 2.11 tests (1 ms before / exactly at decision availability, competing writers through `run_design`) pass unchanged; new `*_preserved` test: a competing writer's stored :20 winner is what the recorded 100/20 checkpoint's reference rows use (no :00 proposal; every reference row a stored record, known only from its t_persisted), evidence agreement 0 mismatches |
| 2.10 hourly replay preserved (`scripts/replay_controls_210.py` with 2.12 code on the pinned `934bb25` data, cutoff 15:31:56Z) | B1, C1, F1: 16 controls each, 15 closed eligible hours, 0 closed eligible hours without a control |
| No-write lab run (disposable copy of main, `--no-write --summary`) | Exit 0; no file changed; summary: every design `exploratory`, B1/C1/F1 integrity `passed`, the five bar-based `not_required`, all publication-valid |
| Byte preservation and idempotency (disposable copy of main, two writing runs at one cutoff) | Exit 0 both times. No file under `data/`, `registry/` or `state/hl_cohort_*` changed; 27 registrations kept byte-for-byte, 8 added; every pre-existing `research/v2/<design>/<version>/` file (controls, events, outcomes) and every earlier card byte-identical (only the index gained entries); evidence agreement B1 45 / C1 45 / F1 65 checked, 0 mismatches. Second run: controls, events, outcomes, checkpoints, experiments and ledger byte-identical; only the B1/C1/F1 cards and report (selections now `stored` instead of `accepted`, one decision `frozen_used` instead of `new`) and the run counter changed |
| Compute -> merge handoff on real data (disposable copies) | Valid run: lab 0, merge 0. Then a malformed control appended to the live C1 version: lab 1, merge 0; C1 card `blocked` / `failed` / not valid with `last_valid_result` = the previous cutoff and no published phases; C1 watermark held, the other 7 advanced and valid; malformed record kept byte-identical; checkpoint files unchanged; data unchanged. Budget-exhausted run (`LAB_BUDGET=0`, all `not run`): lab 0, merge 0. `--reconstruct-days 2`: lab 0, merge 0 (A1/G1 reconstruction passes) |
| Tampered and incomplete handoffs (tests) | The 2.11 outputs of the same run (supported checkpoint, supported card, proposal, advanced watermark) injected into a 2.12 blocked batch; a missing / unreadable / old-schema / stale / version-mismatched / integrity-less / contradictory summary; a batch missing a card, the index or a report; unreadable, non-object, duplicate-key or out-of-range rows: all exit 4, repository unchanged |
| Adversarial review of the first draft (separate agent, read-only, including real-data compute/merge cycles) | No bypass of the gate; 1 medium (an error in a later variant left decisions and a checkpoint written) and 6 low findings, all fixed with regressions (see CHANGELOG). A second pass could not run (API rate limit) |
| Versions | Only `lab/experiments.py` among hashed files changed (COMMON): all 8 versions change - A1 `ev-c368833b5ae6`, B1 `ev-125c86066f05`, C1 `ev-eb20553bce1c`, D1 `ev-2b023a90293f`, E1 `ev-6f279983100b`, F1 `ev-1c53cfe81c9f`, G1 `ev-5cbc55c34b6d`, H1 `ev-02fcecefd1bf` |
| Checksums | `SHA256SUMS` regenerated from its own list plus `regression/test_rev212.py`, `regression/publication_fixture.py`, `scripts/repro_publication_212.py`: 112 entries, all match |
| Deployment (web upload to branch `mannoj93-spec-patch-8`, PR #12, merge commit `5b9b6c3`, 2026-09-25 17:32Z) | 5 branch commits (`ea35574`, `500c7c3`, `78390d9`, `f29c8cc`, `f5d10b5`) verified byte-for-byte against the tested tree (15 files); the branch clone passed 324 tests and 25 fixtures; main after the merge matched all 112 checksum entries. Intermediate runs `ea35574` and `500c7c3` failed as expected (lab and merge uploaded before the adapted tests); `78390d9`, `f29c8cc`, the pull_request run on `f5d10b5` and main after the merge (run 36167735983) passed. The concurrent collector commit `f38baa7` landed before the merge and was preserved (27 data lines added, 0 removed). No required reviews or status checks gate main |
| Research lab after deployment (run 36167818039, **manual** workflow_dispatch, reconstruct 0) | compute success, persist success (merge gate passed; "Fail if the lab reported an error" skipped); committed as `fd29761`. 8 new registrations (27 -> 35) at the versions above; every card `exploratory`, publication-valid, no proposal ("No change is proposed"); integrity `passed` for B1 / C1 / F1 (evidence agreement 46 / 46 / 66 checked, 0 mismatches), `not_required` for the five bar-based designs; watermarks = the run's cutoff; the report states the three separate signals. The 2.11 namespaces were not touched. The next scheduled research run (18:41Z) is not part of this record |
| Scheduled collector after deployment (run 36168885335, 17:43Z, code `fd29761`) | success in 112 s: 17/17 books, 288 requests, 0 failed, 0 rate-limited, critical inputs ok; committed as `896b3f4` without touching research outputs |

Scope limits of these checks: the failure scenarios run on synthetic data in temporary directories
(never on production data); the real-data runs used disposable copies. The merge gate verifies
consistency between the lab's outputs and its own summary; it cannot detect a lab that computes a
wrong but self-consistent result - that is what the regression suite and reviews are for.

# Validation record — research-integrity revision 2.11 (lab-2.2, control policy 2)

Validated 2026-09-25 with Python 3.11 and 3.12 (container); GitHub workflows select Python 3.12,
whose AST the evaluation-version ids are computed from. Tables below the 2.11 block are the record
of earlier revisions and are kept as they were.

| Check (2.11) | Result |
|---|---|
| Default branch before the work | `888ade3`; since the reviewed `8432df0` only automated data commits; code identical to the review |
| Reproductions on `8432df0` (`scripts/repro_controls_211.py pin`) | Cutoff: inputs 09:59:30, decision 10:00:30 - at 10:00:00 and 10:00:29.999 both C (liq_exposure) and F (options) return the control with its decision after the cutoff. Authority: writer A stores the :20 observation (t_persisted 10:25); worker B with an empty context proposes :10 - storage keeps A, B returns its :10 record (t_persisted 10:40); 60-minute labels differ (+4.749% vs -0.130%); B's context does not name the winner |
| Same reproductions on 2.11 | Cutoff: nothing returned at 10:00:00 and 10:00:29.999, the 09:00 hour reported `pending_processing`; at 10:00:30 returned in the 09:00 hour. Authority: B returns the stored :20 record byte-for-byte (t_persisted 10:25, label -0.130%), reports hour 10:00 superseded, accepted none, `used_equals_stored` true, context refreshed to the winner |
| Live evidence of finding 1 | In the lab-2.2 B1 namespace (`ev-9cffe8818c14`) one of 41 stored selections was frozen at 00:49:05 for a decision at 00:49:07 (2026-09-25). It is preserved byte-for-byte; the new B1 version recomputes that hour correctly |
| 2.10 hourly replay preserved (`scripts/replay_controls_210.py` with 2.11 code on the pinned `934bb25` data, cutoff 15:31:56Z) | B1, C1, F1: 16 controls each (2 on the reviewed 2.9 code), 0 closed eligible hours without a control; last decisions 15:19:32 / 15:19:32 / 15:18:49, within the cutoff |
| New tests against `8432df0` (`test_rev211.py` copied into the old tree) | 5 `*_common_api` tests fail (cutoff at 1 ms before / exactly, inputs exactly at the cutoff, UTC midnight, returned control vs stored winner, labels/baseline/reference rows through `experiments.run_design`); 13 skip (new interfaces). All pass on 2.11 |
| Offline regression suite | 303 passed (285 kept; 18 new; three adapted: two 2.10 replay expectations now withhold instead of recomputing or replacing, the 2.9 checkpoint-merge test expects a conflicting batch to be rejected), about 30 s; 2 runs on 3.11 and 2 on 3.12, no failures; numerical fixtures 25 passed |
| Adversarial review of the first draft (separate agent, read-only) | No high or medium findings; 4 low ones fixed with regressions (future hours reported withheld, missing hour reported withheld on replay, stored source time unchecked, merge false positive with a legacy duplicate). Checked sound: every return path passes `validate`; pending earliest never replaced; provisional path sound; write-read-back and lost-write error; lock released on exception; run.py integrity path including errored designs; merge has no key-order/whitespace false positives **[CORRECTED in 2.12: this was wrong - `conflicts()` compared raw lines, so the same record with other whitespace or key order was a conflict (exit 3); reproduced on `b4db7d0` and fixed, see the 2.12 block]** |
| Byte preservation and idempotency (disposable copy of main, lab run with `--now` and writes, then a second run at the same cutoff) | Exit 0 both times. No file under `data/` changed; 24 registrations kept, 3 added (B1, C1, F1); lab-2.2 namespaces `ev-9cffe8818c14` (2 files), `ev-1e8cf9f4e69a` (4), `ev-48a0f80de862` (2) and lab-2.1 `ev-448e00c8b90b` (3) byte-identical; A1, D1, E1, G1, H1 cards regenerated under unchanged versions. Integrity: labelled controls = stored selections for B1 (44 checked), C1 (44), F1 (64), 0 mismatches. Second run: controls, events and outcomes byte-identical |
| Versions (Python 3.12) | B1 `ev-5db159f025fd`, C1 `ev-2ace4c5a6647`, F1 `ev-33998e4f9082` (component changed: `lab/controls.py`); A1 `ev-c35cdb2bc9bc`, D1 `ev-ffa18ae355ef`, E1 `ev-79ea1d99704b`, G1 `ev-44a97c2d5259`, H1 `ev-e76cbdabf3f9` unchanged, clocks continue |
| Checksums | `SHA256SUMS` regenerated from its own list plus `regression/test_rev211.py` and `scripts/repro_controls_211.py`: 109 entries, all match |
| Deployment (web upload to branch `mannoj93-spec-patch-6`, PR #10, merge commit `84dd74a`, 2026-09-25 15:40Z) | 4 branch commits (`201a98e`, `9f9788d`, `905c603`, `e07e2e7`) verified byte-for-byte against the tested tree (12 files); main then matched all 109 checksum entries. Intermediate runs `201a98e` and `9f9788d` failed as expected (code uploaded before the adapted tests and merge script); `905c603`, the pull_request run on `e07e2e7` and main after the merge (run 36155807395) passed. No required reviews or status checks gate main |
| Research lab after deployment (manual dispatch, run 36155859960, no reconstruction) | compute and persist succeeded (15:41:23-15:42:00Z); the "Fail if the lab reported an error" step was skipped (lab exit 0, no integrity failure); committed as `d61d135`: 3 registrations added (B1 `ev-5db159f025fd`, C1 `ev-2ace4c5a6647`, F1 `ev-33998e4f9082`), the 24 older kept unchanged; stored selections 44 / 44 / 64, none malformed, one per hour; cards and `reports/research.md` show 44 / 44 / 64 accepted, 0 superseded, 0 pending, 0 withheld, `used_equals_stored` true, labelled controls = stored selections (44 / 44 / 64 checked, 0 mismatches), and each card's controls fingerprint equals the fingerprint of the stored file. The lab-2.2 B1 hour 2026-09-25 00:00 (frozen 00:49:05.939 for a decision at 00:49:07.097) is recomputed under the new version with the same decision, persisted 15:41:31 - after its decision. No file under `data/` or in the earlier B1/C1/F1 and lab-2.1 C1 namespaces changed |
| First scheduled collector run after the merge (run 36156027688, 15:42Z) | success; `collector-2.7`, 17/17 books, 288 requests, 0 failed, 0 rate-limited. The first scheduled research run under this code (next 18:41Z) is not part of this record |

| Check (2.10) | Result |
|---|---|
| Default branch before the work | `388bbc3`, later `35a329b`; since the reviewed `934bb25` only automated data commits; code identical to the review |
| Reproduction on the pinned data (`934bb25` code and data, cutoff 2026-09-24 15:31:56Z) | 59 successful scheduled collector runs on 2026-09-24; only 01:14 and 05:14 started before :15. B1, C1 and F1: 2 controls each; 16 of 16 hours had eligible records; 13 of 15 closed hours with eligible records had no control. Module B had the same gate (found by the search); bar-based controls (A, D, G, H) and E's stream controls do not |
| Same replay with 2.10 code, same data and cutoff (`scripts/replay_controls_210.py`) | B1, C1, F1: 16 controls each (15 closed hours + the partial 15:00 hour), 0 closed eligible hours without a control, 0 missing reasons. Every control's decision = required-input availability + 60 s (e.g. C1 10:16:01 source, 10:17:52 inputs, 10:18:52 decision); the 12:58:19 record whose inputs arrived 13:00:06 is the 13:00 control for B1/C1 |
| New tests against `934bb25` (`test_rev210.py` copied into the old tree) | 7 `*_common_api` tests (module paths only) fail there; 12 tests of the new interfaces skip (they do not exist). All pass on 2.10 |
| Offline regression suite | 285 passed (266 kept; 19 new), about 27 s; 3 consecutive runs on Python 3.11 and 3 on 3.12, no failures; numerical fixtures 25 passed. 2.9 checkpoint, funding-availability and per-horizon-baseline tests unchanged and passing |
| Adversarial review of the first draft (separate agent, read-only) | 4 findings, all fixed with regressions: frozen controls selected after a cutoff still trained that cutoff's baseline (baseline now uses selection time, like the reference); selections were persisted after the run's checkpoints and a diagnostics error could fail a design (now persisted at selection time; diagnostics isolated); a diagnostic flag was wrong on backfill (replaced by `hour_closed_at_selection`); a stored selection without a time was usable at every cutoff (now never). Checked sound: outcome-independence, availability buckets, no carry-over, missing-input fallthrough, F without funding, late-input exclusion, first-wins storage and merge, variant de-duplication, `label_all` wrapper restored and read-only |
| Byte preservation and idempotency (disposable copy of `35a329b`, lab run with `--now` and writes, then a second run at the same cutoff) | No file under `data/` changed; old registrations (16) kept unchanged, 8 added; `research/v2/C1-liquidation-cluster/ev-448e00c8b90b/` (the lab-2.1 C1 decision and outcomes) byte-identical; legacy and earlier-version cards untouched; experiments/ledger append-only; new `controls/` files for B1, C1, F1 (26 frozen C1 selections). Second run: controls, events and outcomes byte-identical; only cards/report (now counting the selections as frozen) and the run counter changed |
| Versions (Python 3.12, scratch run) | A1 `ev-c35cdb2bc9bc`, B1 `ev-9cffe8818c14`, C1 `ev-1e8cf9f4e69a`, D1 `ev-ffa18ae355ef`, E1 `ev-79ea1d99704b`, F1 `ev-48a0f80de862`, G1 `ev-44a97c2d5259`, H1 `ev-e76cbdabf3f9`. Changed components: B1/C1/F1 their module + `lab/controls.py` + `lab/baseline.py` + `lab/common.py`; the other five `lab/baseline.py` + `lab/common.py`. Editing `lab/controls.py` alone changes B1, C1, F1 only (tested) |
| Deployment (web upload to branch `mannoj93-spec-patch-4`, PR #8, merge commit `1c9b920`, 2026-09-24 22:11Z) | 5 branch commits (`8db8fe3`, `1d3124c`, `719ed95`, `1ae3040`, `a0271f9`) verified byte-for-byte against the tested tree (18 files); main then matched all 107 checksum entries. Intermediate branch runs `719ed95` and `1ae3040` failed as expected (tests uploaded before the report change); the branch head passed on push and on pull_request; main after the merge passed (run 36066040058). No required reviews or status checks gate main |
| Research lab after deployment (manual dispatch, run 36066085841, no reconstruction) | compute and persist both succeeded (22:12:14-22:12:43Z); committed as `c6ff5e1`: 8 lab-2.2 registrations at 22:12:23Z (ids equal to the scratch run above), 16 older registrations unchanged, B1/C1/F1 `controls/` with 26/26/46 frozen selections - for 2026-09-24 00:00-15:59 exactly the 16 per module of the replay, same source times - the lab-2.1 C1 decision recomputed under the new C1 version as reanalysis, cards with `comparison_coverage` and `horizons`, and `reports/research.md` showing the coverage lines (e.g. F1: 46 closed hours, 46 with eligible candidates, 46 selected, 0 without a control, availability 17.9 min after the hour, median). No file under `data/`, `research/evidence/cards` or `research/v2/C1-liquidation-cluster/ev-448e00c8b90b` changed |
| First scheduled collector run after the merge (run 36066395838, 22:15Z) | success; `collector-2.7`, 17/17 books, 286 requests, 0 failed, 0 rate-limited. The first scheduled research run under lab-2.2 is due at 00:41Z and is not part of this record |
| Report freshness label | `reports/latest.md` row reads "research lab (lab-2.2-2026-09-24)" from the recorded experiment row (was the literal "research lab (lab-2.0)") |
| Checksums | `SHA256SUMS` regenerated from its own list plus `lab/controls.py`, `regression/test_rev210.py`, `scripts/replay_controls_210.py`: 107 entries, all match |

| Check (2.9) | Result |
|---|---|
| Default branch before the work | `af73759` (and `4b49827` at deployment prep); since the reviewed `c9fff86` only automated data commits; code identical to the review |
| Reproductions on `c9fff86` (`scripts/repro_integrity_29.py old-tree`) | #1 n=100 look `retired` with the first 100 observations, `supported` after 100 later ones were appended (and `supported` in a single run with all 200); #2 the 09:45 option event (inputs 09:47) present with small, absent with large funding first observed at 10:00, in both the quote-qualified and mark-only variants; #3 mean test residuals at 30 / 60 / 240 min +47.7 / 0.0 / +33.4 bp with horizon-specific outcomes (60-minute model everywhere), and the 480-minute baseline 100% "identifiable" with no complete 480-minute control label |
| Same reproductions on 2.9 | #1 `retired` / `retired` / `retired`, checkpoint 1 recorded (n 100, p_long 0.0, cutoff before the later observations); #2 identical event (group, direction, features, t_inputs 09:47) for both funding values and both policies; #3 0.0 / 0.0 / 0.0 bp, 480-minute share 0.0 and comparison withheld |
| New tests against `c9fff86` (`test_rev29.py` copied into the old tree) | 15 of 28 fail or error there (10 failures, 5 errors: missing interfaces such as `collapse_as_known` or the `design` argument), 9 skip (new checkpoint/per-horizon interfaces absent), 4 pass on both (options guards: delayed current snapshot, later arrivals, missing funding, later use of a value). Every test passes on 2.9 |
| Offline regression suite | 266 passed (238 kept; 28 new in `test_rev29.py`), about 30 s; 19 local full-suite runs: 17 clean, 2 failed once each in the unchanged collector timing test `test_rev26 ... test_one_hung_venue_cannot_cost_every_venue_its_snapshot` (series stage 243.6 s against a 241 s bound); that test passed 12/12 alone on 2.8 and on 41 hash seeds, the reviewed tree passed 8/8 full-suite runs, and collector.py and test_rev26.py are byte-identical to 2.8, so the lab change is not implicated but the intermittency is recorded rather than dismissed. Numerical fixtures 25 passed |
| Adversarial review of the first draft (separate agent, read-only, scripts under a scratch directory) | 7 findings, all fixed with regressions (CHANGELOG 2.9, "Hardening"): episode collapse across freeze times, options controls moved by late snapshots, frozen-decision merge order, funding and spread availability in labels, record-level verification, registration-bounded multiplicity, concurrent checkpoint writes. Checked and found sound: the binary search for the cutoff (greedy thinning of equal-length intervals keeps the maximum, fuzzed on 3000 random sets), JSON float round trip and bootstrap determinism, supported-status gating, per-horizon cache keys and training rows |
| Byte preservation and idempotency (scratch copy of the repository at `4b49827`, lab run with `--now` and writes, then a second run at the same cutoff) | First run: no file under `data/`, `registry/`, `research/evidence/cards`, `research/experiments`, `research/ledger`, `research/evidence/v2/*@<lab-2.0 version>.json` or `state/lab_registered.json` changed; `research/v2/experiments` and `research/v2/ledger` append-only; 8 new cards; `state/lab_registrations.json` kept all 8 lab-2.0 entries unchanged and added 8. Second run: only the run counter in `state/lab_run_state.json` changed. Checkpoint files are appended once per look (tested: repeat runs leave every `.jsonl` byte-identical; a later look only appends) |
| Version migration | Every design gets a new `ev-...` version under lab-2.1 (scratch run: A1 `ev-807f3c751b86`, B1 `ev-7e4d0eed56aa`, C1 `ev-d9cbcefb4a31`, D1 `ev-dbc5dbdb0de9`, E1 `ev-839d57e8ed3e`, F1 `ev-7b9b890aebaf`, G1 `ev-0a974aa122b5`, H1 `ev-8120dafd44e3`; ids depend only on design + semantic code); the lab-2.0 versions are indexed `retired (superseded)` with `superseded_by`; no lab-2.0 version had frozen evaluation decisions or checkpoints to carry over |
| Research lab on current data | 8 designs in 2.5 s (writes, scratch copy); with a 5-day reconstruction, 21 s (read-only) |
| Checksums | `SHA256SUMS` regenerated from its own file list plus the two new files: 104 entries (was 102), all match |
| Deployment (GitHub, 2026-09-23/24, web upload to branch `mannoj93-spec-patch-2`, PR #6, merge commit `4bd180f`) | 5 branch commits (`eee7d79`, `837522c`, `256356f`, `9aac540`, `6494ba8`) verified byte-for-byte against the tested tree (18 files); main then matched all 104 checksum entries. No required reviews or status checks gate main. Intermediate branch runs failed as expected (code uploaded before its tests); the branch head passed (pull_request run on `6494ba8`: success, 23:57Z). Data commits between the base and the merge were preserved (54 inserted lines, 0 deleted, in data/) |
| Regression on main after the merge (run 35936298623, 00:02Z, attempt 2 at 00:02Z) | Failed both attempts in the unchanged 2.7 test `test_stream ... test_bybit_gap_resubscribes_and_disconnect_recorded`: a date dependency (it reads only the wall-clock day's gap partition, while the update-id gap is filed under its 2026-09-23 message time). Reproduced on `c9fff86` after midnight (fails standalone 25/25 and in the full suite); fixed in the test in the follow-up PR, full suite then 3/3 OK after midnight locally |
| Research lab on GitHub (run 35936372801, dispatch with a 60-day reconstruction, 00:00Z) | Success in 2 min 48 s; committed as `f984079`: 8 lab-2.1 cards, 8 new registrations (the 8 lab-2.0 entries byte-identical in content), index with every lab-2.0 version `retired (superseded)` and `superseded_by` the new id, 8 experiment rows, 28 ledger rows, `reports/research.md`, `reports/skill_proposals.md` ("No change is proposed") and `reports/latest.md` refreshed (input cutoff 23:54Z, lab-2.1 last run 00:00Z). No data, lab-1.0 or lab-2.0 card file changed. Every design exploratory with checkpoint 1 pending at 0/100; no `checkpoints.jsonl` exists yet (no evaluation observations). Reconstruction A1: 133 episodes, 6 retained (primary); G1: 49 episodes, 45 retained; its per-horizon baselines are all unidentifiable ("missing baseline input": no settled-funding history before collection began), as they were under 2.8 |
| Version ids and Python | Evaluation-version ids hash the AST dump, which differs by Python minor version: the same tree gives A1 `ev-807f3c751b86` on 3.11, `ev-13f30d25ede6` on 3.12 (the workflow's pin, the ids registered on GitHub), `ev-9946fc078800` on 3.13. Pre-existing since 2.8. Conservative (a different interpreter starts a separate clock, never merges evidence), but a lab run with writes must use Python 3.12 and a runner upgrade will start new versions |

| Check (2.8) | Result |
|---|---|
| Default branch before the work | `9a47d65`; since the reviewed `900d0b1` only automated data commits; code identical to the review |
| Reproductions on `900d0b1` (`scripts/repro_integrity.py old-tree`) | #2 same-bar entries counted {30m: 2, 60m: 2, 240m: 1, 480m: 1}; #3 module G event 48.0 min before its delayed input; #5 transition labelled `confirmed`; #6 exact 3 events + 1 control, jittered 0 + 0; #7 all quotes stale: event unchanged (`bearish_disagreement`), only counters moved |
| Same reproductions on 2.8 | #2 {1, 1, 1, 1}; #3 event 1.0 min after the input (input + assumed processing); #5 `none_observed`; #6 exact and jittered both 3 + 1; #7 event regrouped `bearish_disagreement_ineligible` with reason "stale", surface value unchanged |
| New tests against `900d0b1` | `test_integrity.py` cannot import there (`lab.asof` and the other lab-2.0 modules do not exist); the version-independent script above is the per-finding evidence |
| Offline regression suite | 238 passed (200 kept; 38 new), about 25 s, 3 consecutive runs, no flakes; numerical fixtures 25 passed |
| Earlier reliability cases | `test_stalled_venue_leaves_every_other_book_collected`, `test_one_hung_venue_cannot_cost_every_venue_its_snapshot` and `test_complete_snapshot_loss_is_critical_and_partial_loss_is_not` pass unchanged |
| Byte preservation and idempotency (scratch copy of live data, two runs at one cutoff) | First run creates only `research/v2`, `research/evidence/v2`, `research/evidence/index.json`, `state/lab_registrations.json`, `state/lab_run_state.json` and the two research reports; no data, legacy research or lab-1.0 state byte changed. Second run at the same cutoff adds no rows; only the commit hash in reports/cards and the run counter change |
| Version migration | Each design registered under a new `ev-...` version; `state/lab_registered.json` and the lab-1.0 cards untouched and indexed as legacy; a docstring/comment edit, a README edit and a data file leave versions unchanged; a detector constant, a cost value, or (for module B) the HL sampling policy start a new version (tested) |
| Research lab on current data (read-only) | 8 designs run in 2 s; with the 60-day reconstruction of A and G, 2 min 17 s (limit 30 min) |
| Coverage report refresh | `report.py --coverage-only` writes only `reports/latest.md` (report 2.5 with generation time, input cutoff, versions and 9 dataset freshness rows); no registry or scoring files touched |
| Deployment (GitHub, 2026-09-23, web upload to branch `mannoj93-spec-patch-1`, PR #5, merge commit `87268f3`) | 8 branch commits (`61e9131` ... `5d977b3`) verified byte-for-byte; main then matched all 102 checksum entries. Intermediate branch runs of the regression workflow failed as expected (tests uploaded before their modules and scripts); the branch head (`5d977b3`, push and pull_request) and main after the merge (`87268f3`) passed. Data commits between the base and the merge were preserved by the merge (139 inserted lines, 0 deleted, in data/) |
| Research lab on GitHub (run 35927653635, dispatch with a 60-day reconstruction) | Success in 3 min 31 s; committed as `5669cbd`: 8 versioned cards, index with the lab-1.0 cards marked legacy, 8 experiment rows, 28 ledger rows, 8 registrations, `reports/latest.md` refreshed to report 2.5 (input cutoff 22:17Z, lab-2.0 last run 22:19Z). No lab-1.0 file changed. Reconstruction A1: 13 firings, 7 episodes, 6 retained in 6 blocks (lab-1.0 reported "6 independent"); G1: 51 firings, 48 episodes, 44 retained in 33 blocks |
| First scheduled collection after the merge (22:22 slot, started 22:26Z, committed as `e078bb3`) | `collector-2.7`, 17/17 books, options and Hyperliquid complete, 279 requests, 0 rate-limited, 0 failed, 103 s; watchdog exit 0 "collector healthy" |

## Revision 2.7

| Check (2.7) | Result |
|---|---|
| Offline regression tests (`regression/`) | 200 passed (124 from 2.6.1; new: 20 `test_rev27.py`, 30 `test_lab.py`, 26 `test_stream.py`), about 20 s; numerical fixtures 25 passed |
| Schema compatibility | Option schema-1 fields and the v1 BTC position record still written; `OPTIONS_SCHEMA=1` and `HL_SAMPLING_POLICY=v1` restore the 2.6 code paths (tested) |
| Live collector run under the final 2.7 code, scratch copy (20:13Z) | 17/17 books; options complete (851 with OI, 123 zero-OI listed, panel 12/12, metadata refreshed); Hyperliquid 190 accounts (29 ok_btc, 138 ok_flat, 23 ok_other, 0 failed), fixed cohort of 100 selected, enrichment: 1 ledger + 9 TWAP checks; 1,500 bars per price series on first run, 0 missing minutes; 1 insurance row; 298 requests, 0 rate-limited, 0 failed; 170 s (series 41, liquidations 11, snapshot 18, forward 94, enrichment 7) of the 600 s budget. An earlier 2.7 build (19:23Z) gave the same counts in 173 s |
| Report and watchdog on that copy | Report 2.4 section 3c lists all new datasets; watchdog exit 0 (healthy), warning that the newest run was local |
| Record sizes per run (live) | options 36 KB (8 KB gz), HL accounts 36 KB (13 KB gz), v1 BTC map 5 KB, enrichment 2 KB, price batch ~1.4 KB per series; hourly quote record 68 KB (22 KB gz) |
| API behaviour verified live | Hyperliquid `twapHistory` answers (empty list for sampled accounts), fills carry `twapId`; OKX insurance fund `type=regular_update` is rejected (HTTP 400), `limit=1` used instead; Bybit REST 403 from the container but WebSocket reachable; Deribit summaries return null bid/ask with no resting order |
| Research lab on the live copy, prospective | All 8 designs ran in 1 s; states: A, B, C, D, F, G, H insufficient_data with the reason named; E unavailable (no streaming data) |
| Research lab, 60-day reconstruction (Binance 1-minute history, 4 series) | Fetch 170 s, compute ~65 s; A1: 6 weak vs 93 strong independent episodes over 41 days (exploratory only); G1: 44 test vs 1,437 control-time references; both flagged with contradictory evidence (chronological halves disagree in a variant) |
| Streaming service, live smoke tests (90 s, 2 x 45 s, 120 s) | 3 venues connected, 0 reconnects; Bybit 3,073 consecutive deltas with no sequence gap; restart gaps written; heartbeat check ok; 120 s: 2.3 s CPU, 29 MB max RSS, 373 KB written (351 KB raw, 21 KB derived) |
| S3 SigV4 signer | Matches botocore 1.35.0 on 4 fixed vectors (PUT/HEAD, two endpoints) |
| Skill evaluation on synthetic fixtures | Detects the dropped decision-status line and one overclaim; negated wording ("not yet supported") not flagged; refuses an output path inside the repository; live mode without a key reports "not run" |
| Deployment (GitHub, 2026-09-23, via the web upload page; no local git credentials) | Collector code `43b28c7` (20:20Z), fixtures `240a27f`, lab `631cfa1`, modules `e9e3928`, designs `7105a5d`, skill-eval fixtures `07c8139` `a0622f8` `ccd0d08`, stream `a9b76aa`, stream deploy files `fa3bb59`, tests `53f0381`, research workflow `d155cba`. Every file verified byte-for-byte against the local tree after fetch. Regression and numerical fixtures green on every push, including `53f0381` (the 200-test suite on GitHub's Python 3.12) |
| First scheduled 2.7 collection on GitHub (run 35916223074, 20:22 slot, started 20:28:50Z) | `collector-2.7`, `trigger: schedule`; 17/17 books; options complete (851 with OI, 123 zero-OI, panel 12/12); Hyperliquid 190 accounts (29 ok_btc, 138 ok_flat, 23 ok_other, 0 failed), fixed cohort of 100 selected and frozen (`state/hl_cohort_fixed_v2.json`, members sha256 `4e8dd2cf...`), 10 enrichment requests; 1,500 bars per price series; 1 insurance row; 297 requests, 0 rate-limited, 0 errors; 96.5 s (series 35, liquidations 6, snapshot 8, forward 44, enrichment 4); committed as `e5fd091` with every new dataset present |
| Second scheduled 2.7 collection (20:37 slot, committed as `e1de0f6`) | 17/17 books; fixed cohort file byte-identical (not re-selected); a different rotating block (17 ok_btc, 154 ok_flat, 19 ok_other, 0 failed); 13 new bars per price series from the checkpoint, 0 minutes behind; option metadata served from the daily cache; 294 requests, 0 rate-limited; 100 s |
| First research-lab run on GitHub (run 35915877912, dispatch with 60-day reconstruction) | Success in 3 min 6 s end to end; committed as `dbda592` (8 cards, 8 experiment rows, 27 ledger rows, registration stamps). Reconstruction figures identical to the container run (A1: 6 vs 93 episodes, same interval), so the pipeline reproduces across environments |
| Watchdog and report after deployment (on the fetched repository) | Watchdog exit 0: "last scheduled run 20:28Z, collector-2.7"; report 2.4 section 3c lists all new datasets with 0 missing minutes and the lab's first run |

| Check (2.6.1) | Result |
|---|---|
| Offline regression tests (`regression/`) | 124 passed; numerical fixtures 25 passed; 3 consecutive full runs, no flakes |
| Stalled Binance, snapshot stage only, fake clock (the review's case) | 2.6: 5 Binance attempts, 0 other requests, 0/17 books in 120 s. 2.6.1: 1 Binance attempt, 27 other requests, 14/17 books (all non-Binance) in 20 s; 7 requests skipped by the open circuit |
| Same stall inside a full run (`main()`) | 14/17 books; history stopped at its stage limit; forward books attempted |
| New and strengthened tests run against 2.6 (`62e51cc`) | 6 fail or error, as intended |
| Watchdog, 0/17 books with history intact | 2.6: exit 0 "healthy". 2.6.1: exit 2 "no open-interest book collected (0/17)"; 1/17 stays exit 0 with warnings |
| Live routine run under 2.6.1, scratch copy (16:49Z) | 17/17 books, no circuit opened; options and HL complete (7 Hyperliquid 429s on the container IP, retried and recorded); 169 s |

| Check (2.6) | Result |
|---|---|
| Numerical fixture checks (`test_fixtures.py`) | 25 passed |
| Offline regression tests (`regression/`) | 119 passed (50 from 2.1, 37 in `test_rev22.py`, 32 in `test_rev26.py`); 5 consecutive full runs, no flakes |
| `test_rev26.py` run against 2.5.1 code and workflows (`bcccf14`) | 26 of 32 fail or error, as intended; the 6 that pass pin behaviour 2.5.1 already had (native resolution, successful push, cadence arithmetic) |
| Simulated sustained outage of every venue, fake clock, 600 s budget | Run ends at 600.0 s, record written with every failure and `deadline_reached`; 14-minute job leaves 3.0 minutes for persistence and the recovery artifact |
| Simulated stall of one venue (Binance), fake clock | History stops at its 240 s stage limit; snapshot and forward books still run (2.5: history took all 600 s, snapshot skipped) |
| Hung remote, `PERSIST_BUDGET_S=8` | `commit_push.sh` exits 1 in under 20 s with "remote persistence not confirmed" (unbounded: four 30 s pushes plus rebases) |
| Live routine run under 2.6, scratch copy (15:58Z) | 17/17 books; options complete, 847 strikes; HL complete 200/200 in 82 s; 281 requests, 0 rate-limited; 154 s; stages: series 39 s, liquidations 17 s (daily probe), snapshot 15 s, forward 82 s |
| Report and watchdog on the live copy | Hourly period judged against hourly slots (16/16, upper bound); local run excluded from scheduled figures; watchdog healthy, warns that the newest run was local |
| `SHA256SUMS` | Covers code, docs, workflows, `cadence.json` and templates; data, state and reports change every run |
| Deployment (GitHub, 2026-09-23) | Workflows `90fce23` (16:06:13Z, the start of the 15-minute period in `cadence.json`), persistence script `2d12847`, test update `9327896`, code and docs `e3ff93a`, new tests `d98b842`. Tree verified byte-for-byte against `SHA256SUMS` after fetch. Regression and numerical fixtures runs #15–#19 all green, one per push |
| Manual collection on GitHub (run 35887308099, 16:14Z, manual deployment check) | `collector-2.6`, `trigger: workflow_dispatch`; 17/17 books; options and HL complete; 285 requests, 0 rate-limited; 104 s (series 36, liquidations 13 with the daily probe, snapshot 11, forward 44); committed as `8afc250` |
| Manual watchdog on GitHub (run 35887689676, 16:17Z) | Exit 0 "collector healthy" on the last pre-2.6 scheduled run (15:22Z); warning that the newest run was manual and not counted as scheduled; sparse checkout worked |
| Weekly report on GitHub (run 35887705789, 16:17Z) | Report 2.3 committed as `622a65f`: hourly period 16/16 slots (upper bound, trigger unrecorded), 15/15 intervals covered; 15-minute period listed with no slot yet due |
| First scheduled 15-minute run (run 35888255376, 16:22 slot) | Process start 16:22:51Z; `trigger: schedule`, cron recorded; 17/17 books; options and HL complete; no probe (already done that UTC day); 110 s; committed as `feee7c8`. The 16:07 slot, one minute after the workflow commit, did not run |

| Check (2.5.1 and earlier) | Result |
|---|---|
| Numerical fixture checks (`test_fixtures.py`) | 25 passed |
| `SHA256SUMS` | Now covers code, docs, workflows and templates only; data, state and reports change every hour |
| Offline regression tests (`regression/`) | 87 passed (50 from 2.1, 37 in `test_rev22.py`); 5 consecutive full runs, no flakes |
| 2.5.1 late-byte tests run against 2.5 (`9090fba`) | 503 case fails (2.30 s), as intended; 200 case passes on both |
| Live run under 2.5.1, scratch copy | 17/17 books; options and HL complete; no errors; 159 s |
| 2.5 slow-response tests run against 2.4 (`f6fa022`) | 3 trickle tests fail, as intended; prompt response passes on both |
| Local trickling server, 1.2 s budget | Body and headers: 1.20 s, rejected (2.4: 3.45 s and 3.57 s, accepted) |
| Live run under 2.5, scratch copy | 17/17 books; options complete; HL complete 200/200 in 97 s; no errors; 155 s |
| 2.4 outage tests run against 2.3 (`22d2c65`) | 6 of 6 fail or error, as intended |
| Simulated outage, fake clock, 2.4 | Hyperliquid only: 27 requests, 5.0 min. Every venue: 38 requests, 20.0 min, run record written (2.3: 400 requests / 190 min and 576 / 285 min) |
| Live run under 2.4, scratch copy | 17/17 books; options complete 850/850; HL degraded 3/200 on HTTP 429, then complete 200/200 in 93 s with the backoff |
| 2.3 tests run against `ed45dd2` | 9 of 23 in `test_rev22.py` fail or error, as intended |
| The 13 collector, scoring and schema tests run against the 2.1 code | 11 fail or error, as intended; the 2 that pass pin behaviour 2.1 already had |
| Live hourly run, updated collector, scratch copy of the repo | 17/17 books, 849 option strikes with OI, 29 HL BTC positions in top 200, no errors, 147 s |
| Live taker backfill with the pagination fix | 5m: 17 missing rows recovered, 0 gaps; 1h: 1 recovered, 0 gaps |
| Report generation on the live copy | Passed; retired books labelled, not alerted |
| Watchdog against the deployed repository data | "collector healthy" |
| Live hourly run under 2.3, scratch copy (00:45Z) | 17/17 books; options complete, 850/850 rows valid; HL complete, 200/200 accounts, 29 BTC positions; 160 s |
| End-to-end forecast, scratch copy | Registered before start, frozen, scored on 180 live 1m bars, evidence hash verified, idempotent; all seven event types formatted |
| First GitHub backfill under 2.2 (00:01Z, 434 s) | Taker 5m and 1h: 0 gaps in the repository. Found the 4xx-boundary regression fixed in 2.2.1 |

## Measurements behind the changes (live, 2026-09-22 23:30Z)

- Binance `/futures/data`, `endTime = X − 1`: taker returns up to X − 10m; ratio and OI endpoints up
  to X − 5m. The 1h ratio and OI rows equal the 5m rows at the same stamp. Taker 1h `buyVol` at T
  equals the sum of the twelve 5m rows from T (within 0.1%).
- Stored taker gaps: 17 × 5m at 500-row spacing from 2026-08-24 04:50Z; each present at the source.
- OKX liquidation feed: 50 of 2,493 stored timestamps carry two orders; `after = ts + 1` returns the
  boundary pair again, `after = ts` does not.
- OKX account ratio: the row stamped 23:00 was returned at 23:35.
- Bitget BTCUSD coin-margined perpetual: code 40309, "The symbol has been removed".
- BitMEX `/instrument/active`: XBT_USDT Delisted, XBT_USDC Unlisted; no open XBT perpetual.
- Deribit `get_book_summary_by_currency` (BTC options): 972 instruments, 849 with OI; ~30 KB compact.
- Hyperliquid leaderboard: 46,876 rows, 39 MB; `clearinghouseState` ~0.33 s per call.

## Scope limits

2.11: the lock is advisory and local (fcntl); GitHub runs stay serialized by the workflow's
concurrency group, and the merge rejects conflicting batches. A read-only replay withholds a slot
whose later stored winner differs from what it computes, using post-cutoff knowledge of that
winner only to decline, never to evaluate. Every design remains exploratory with no evaluation
observations; no skill change is warranted.

2.10: more comparison observations improve the reference and the baselines; they do not establish
any edge, and every design is still exploratory with no evaluation observations under the new
versions. Hours are still skipped when no record had its inputs available in time (the collector
runs 3-4 times an hour, so that needs an outage). A control's hour is the hour its inputs became
available, not the nominal schedule slot. The per-horizon accounting reads the labels by wrapping
`experiments.label_all` in `lab/run.py`, a presentation-only hook. The version ids still depend on
the Python minor version (2.9 limitation).

2.9: still no design has evaluation observations, so no checkpoint has completed and every status is
exploratory; no skill change is warranted. The checkpoint machinery is exercised on synthetic data
only until the first look completes. The 2.8 dependence-block rule is unchanged: if retained
test and reference intervals overlap continuously across midnight (e.g. hourly test firings with a
60-minute horizon), consecutive days chain into one block, which is conservative and can keep such
a design below its block minimum; at the designs' actual horizons with sparse firings the blocks
are one per day (measured on synthetic 60-day tapes). Funding used in cost attribution of a label is settled funding within the
label window; its availability is now in label_available, but a settlement missing from the
stored series (after the series has moved past it) still contributes zero rather than making the
label incomplete.

2.8: no design has evaluation observations yet; every status is exploratory and no skill change is
warranted. Decisions are as-of replays computed every 6 hours, not live executions. The
multiplicity adjustment and look schedule are conservative house rules, not a formal sequential
test. Streaming (module E) remains inactive.

2.7: no module has an evaluation episode yet; every status is exploratory, and the
reconstruction figures are not evidence of an advantage. The cost model's fee and slippage values
are assumptions (the Binance fee page could not be retrieved automatically). The streaming service
has run only as local smoke tests. Sustained collection of the new datasets is measured by the
weekly report from deployment on.


At the time of writing one scheduled 15-minute run has been observed; sustained scheduled
execution at this cadence (delays, dropped slots, queueing behind intake and report) is measured
by the weekly report from here on, not established by this record. Backlog pruning under an outage
and the watchdog's stale and failing states are verified offline only. Live endpoint behaviour is
dated and can change. This is a reliability revision, not a claim of forecasting skill.

## Reproduce

```sh
python test_fixtures.py
python -m unittest discover -s regression -v
python collector.py          # live; writes into this checkout
python report.py --days 7
```
