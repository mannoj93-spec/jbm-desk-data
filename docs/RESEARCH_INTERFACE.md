# Research interface, continuous panel and prospective directional stream (repo 2.30)

The modules live in `research_tools/`, outside `lab/`, so the lab's code identity and every evaluation version are
unchanged. They read stored data through `lab.data.Store` and never modify the lab. Nothing here is a trading result:
the lab's record has zero supported designs, and these components exist to find, reject or prospectively confirm
candidates under the existing evidence rules. Component states with their evidence: `docs/READINESS.md` (generated from
`research/readiness/*.json` by `scripts/readiness.py`); repo 2.30's repairs: `CHANGELOG.md`.

## Components and status

| Component | File (version) | Status |
|---|---|---|
| Shared evidence contract | `research_tools/evidence_contract.py` (evidence-1.0.0, byte-identical to the skill's `desk_evidence.py`) | implemented, tested |
| Data and provenance catalog | `research_tools/catalog.json`, `catalog.py` | implemented, validated |
| Per-feature admission funnel | `research_tools/funnel.py` | implemented, tested |
| Continuous feature panel | `research_tools/panel.py` (panel-1.1.0) | five families supported with per-source age and alignment; two gated |
| Research interface | `research_tools/research_api.py` (research-api-1.1.0) | implemented, tested |
| Search ledger | `research_tools/search_ledger.py` (search-ledger-1.1.0) | implemented, tested; anchored only when an evaluator side writes the anchor |
| Evaluator boundary | `research_tools/evaluator_service.py` (evaluator-service-1.0.0) | implemented, tested (OS-user case as root); **not deployed** |
| Directional stream parts | `research_tools/directional.py` (directional-1.1.0) | implemented, tested |
| DIR1 guarded runner | `research_tools/dir1_runner.py` (dir1-runner-1.0.0); protocol `research/registrations/dir1-prepared/` (revision 2) | implemented, fixture-tested; **prepared, not registered; frontier arm not commissioned** |
| Calibration | `research_tools/calibration.py` (1.1.0), `calibration_harness.py`; `research/calibration/dir1-primary-v1/` | criteria declared before the run; seed-33 run passed them |
| Options skew (family 6) | `research_tools/options_skew.py` (options-skew-0.1.0) | feasibility measured on stored captures; **not registered** |
| Replenishment (family 3) | `research_tools/replenishment.py` (replenishment-0.1.0) | contract and fixtures; **needs the uncommissioned E1 recorder** |
| A2 synchronized flow | `research_tools/a2_sync.py` (a2-sync-0.1.0); protocol revision 2 | **prepared** |
| PS1-T1 turnover control | `research_tools/ps1_t1_runner.py` (ps1-t1-runner-1.0.0); protocol revision 2 | **prepared; primary band needs an operator decision** |
| Raw retention + replay | `research_tools/archive_store.py` (archive-store-1.1.0) | implemented, tested; **not wired into the collector** |
| D1 rejection funnel | `research_tools/d1_diagnostics.py` | implemented |
| E1 pilot acceptance | `stream/pilot_e1.json`, `stream/pilot_acceptance.py` (pilot-acceptance-1.1.0) | criteria declared; **pilot not run (no host)** |
| O33 v3.1 | `research/registrations/o33-v3.1/` (effective 2026-10-19T19:51:07Z, `effective.json`) and `o33-v3.1-correction-1/` | v3.1 effective; correction 1 effective 2026-10-20T12:14:00Z (PR #48 merge, its `effective.json`) |

## Research interface

```
python -m research_tools.research_api --role researcher --actor actor.json open|panel|inspect|run|ablate|counterexamples|config|register|results --args args.json
python -m research_tools.research_api --role evaluator  --actor evaluator.json --anchor ANCHOR evaluate --args args.json
python -m research_tools.research_api --role researcher --actor actor.json verify --args args.json
python -m research_tools.evaluator_service --shared research/search --private /srv/evaluator --socket /run/eval.sock
```

`actor.json`: `{"kind": "model"|"human"|"system", "id", "version", "training_cutoff"}`. For a model, `version` is the
pinned identifier when one exists; an alias is recorded as an alias. `training_cutoff` is a provider claim.

**Candidates** (`validate_spec`) are strict: `{"family", "features": [ordered, distinct], "horizon_min": 15..1440 by 15,
"rule": {"type": "linear-score", "weights": {exactly the features}, "bias", "long_above", "short_below"}, "transform":
null | panel-transform/1}`. The transform is applied (its panel version must be the executing one, its training cutoff no
later than the experiment's discovery cutoff). Unsupported rule types and `code_path` are refused: a hash of code that
does not run proves nothing. Features are used only when `panel.eligible` says their state is ok.

**Registration** is transactional: validate, preflight the request id (a conflicting id writes nothing), store immutable
copies of the spec, transform and executing code in `objects/`, append the register event (the commit point), then
write the candidate file as a derived copy. `evaluate` loads the candidate from its event and objects, restores a
missing file, refuses an edited or orphaned one, and refuses when the executing code differs (register a successor).

**Prospective status** needs evidence outside the researcher's reach. A locally recorded registration time can be
edited, so results are "chronological confirmation (not externally anchored)" unless the ledger is anchored by the
evaluator side (`FileAnchor` in the service's private root, or a main-branch commit); then confirmation starts at the
anchor and the class is "prospective confirmation". An anchored ledger detects suffix deletion and rewrites; an
unanchored one is described as internally consistent only.

**Checkpoints** have fixed membership: checkpoint N is the first N scored confirmation decisions in decision-time order
(ties by row hash), a decision counting only if its label matured by t + horizon + `label_watermark_min`; it is released
once, when every earlier decision is settled. Repeated or differently timed `evaluate` calls add no looks. Scheduled,
eligible, missing, abstaining, unlabelled, taken and scored counts are separate. The provider receives the confirmation
start (no rolling window) and the candidate's horizon; the evaluator keeps a hash-chained observation log and reports a
later revision of an admitted observation instead of using it.

**Search** (`search_ledger.family_count`) counts registrations, runs (including errors and aborts), ablations,
counterexample packets, rejections, configurations (model, prompt, tool) and exposures across every session and model.
Every attempted configuration is kept whole in the object store. Ten prompts or ten models exploring the same history
are one family, not ten confirmations; a challenger inherits no evidence.

**Boundary.** Role and partition checks are conventions inside one process. `evaluator_service` runs the evaluator as
its own process answering only released results over a socket; started as a separate OS user with its private root
mode 0700, a researcher process cannot read unreleased results (tested with a setuid'd process when the suite runs as
root). On a single-user checkout or a CI runner it is a convention, and the readiness record says so.

**Model modes.** A research assistant's historical results are discovery evidence with an exposure label; a later model
may know these outcomes from training. A live forecaster runs through `dir1_runner` with every attempt retained.

## Continuous panel (panel-1.1.0)

One row every 15 minutes for every grid time. Each feature has its own state (`row["fstate"]`): ok, source-missing,
stale-*, misaligned-*, invalid-capture, insufficient-*, window-incomplete, flow-below-threshold, gated. Every source has a
declared policy (`panel.POLICY`, hashed into each panel): depth measured within 10 minutes of the flow window and no older
than 30; estimated funding no older than 60 minutes (bp per 8 h); mark and spot within 60 s of each other and no older
than 30 minutes; the OI change over an aligned hour whose price return and volume are of the same hour, its stamp no
older than 45 minutes. Valid zeros are values. `freeze()`/`compare()` keep an admitted panel version and report a
rebuild that differs. `labels()` builds forward returns with their availability; `fit_transform` learns only from rows
before its training cutoff.

## DIR1 (prepared; `dir1_runner.DIR1Runner`)

`run(decision)` reconciles the schedule, checks the protocol (operational mode needs a registered protocol whose
effective evidence the verifier confirms), checks the as-of panel row (instrument, eligibility, per-feature age),
retains the packet, runs each arm's adapter with every attempt in a child process killed at the timeout, publishes and
admits only through a verifier of first availability on main (`GitHubMainVerifier`, GitHub's activity records) or a
registry receipt, and records everything in a locked, hash-chained, recoverable opportunity log. `grade_matured(bars,
cutoff, funding)` grades only admitted forecasts whose outcome was available at the cutoff: Brier on one common target
for all arms, utility and net paper value on each arm's latency-aware entry (a bar-based price proxy), settled funding
(missing: net unavailable), inference USD beside them. `directional.compare_arms(graded, protocol, schedule)` computes the
registered pairs (primary: statistical minus baseline) on pair-specific intersections with the schedule as denominator.

## Deployment handoffs (each is a separate operator action; states as of repo 2.30.1)

1. **Repo 2.30 merged** (PR #48, 2026-10-20T12:14:00Z) and correction 1's effective time recorded (repo 2.30.1).
   Still open: observe a collector run on the 2.30 `commit_push.sh` whose push meets a moved main. The 12:11Z Oct 20
   run failed with the old signature because it had checked out the pre-merge code; its artifact (12263109593)
   expires 2026-10-27T12:15:43Z and has not been reconciled.
2. **PR #47** merged 2026-10-20T12:13:44Z (rows restored late under `data/restored/`).
3. **DIR1**: train and freeze the statistical artifact before `effective_utc`, add a publishing workflow, register by
   merge; the frontier arm needs an account, a pinned model identity and a transport (`CommandAdapter` or
   `HTTPJSONAdapter`).
4. **Evaluator service**: a host user separate from the researcher's, with a private root; until then the boundary is a
   convention.
5. **Raw retention**: wire `archive_store.ArchiveStore` with a `Budget` and a bucket (stream `S3Backend`, which now has
   `get` for restores).
6. **E1 pilot**: a persistent host (standing decision: none). Then `python -m stream.pilot_acceptance DIR --start ...
   --end ...`; a `--shocks` number is ignored.
7. **A2 / PS1-T1**: registration by merge; PS1-T1 first needs the primary-band decision recorded in its protocol.
8. **Hourly check**: install skill 12.4.21 and apply its prompt (`routines/hourly_refresh.md`) together.
