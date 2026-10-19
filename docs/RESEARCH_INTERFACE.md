# Research interface, continuous panel and prospective directional stream (repo 2.29)

The modules live in `research_tools/`, outside `lab/`, so the lab's code identity and every evaluation version are
unchanged. They read stored data through `lab.data.Store` and never modify the lab.

This document is the integration guide for the repo 2.29 research assets. It says what each component does, how to
call it, what it does and does not enforce, and what remains uncommissioned. Nothing here is a trading result:
the lab's record has zero supported designs, and these components exist to find, reject or prospectively confirm
candidates under the existing evidence rules.

## Components and status

| Component | File | Status |
|---|---|---|
| Shared evidence contract | `research_tools/evidence_contract.py` (byte-identical to the skill's `desk_evidence.py`, evidence-1.0.0) | implemented, tested (parity pinned both sides) |
| Data and provenance catalog | `research_tools/catalog.json`, `research_tools/catalog.py` | implemented, validated |
| Per-feature admission funnel | `research_tools/funnel.py` | implemented, tested, run on stored data |
| Continuous feature panel | `research_tools/panel.py` (panel-1.0.0) | five families supported; two gated |
| Research interface + search ledger | `research_tools/research_api.py`, `research_tools/search_ledger.py` | implemented, tested; CLI smoke-run on stored data |
| Prospective directional stream | `research_tools/directional.py`; protocol `research/registrations/dir1-prepared/protocol.json` | implemented and offline-replayed; **prepared, not registered; frontier arm not commissioned** |
| Calibration diagnostics | `research_tools/calibration.py` | implemented, tested |
| Turnover-control successor | `research_tools/turnover.py`; `research/registrations/ps1-t1-prepared/protocol.json` | **prepared, not registered** |
| Synchronized-input A1 successor | `research/registrations/a2-synchronized-prepared/protocol.json` | **prepared, not registered** |
| Raw-response retention + replay | `research_tools/archive_store.py` | implemented, tested; **not wired into the collector** |
| D1 rejection funnel | `research_tools/d1_diagnostics.py` | implemented, run on stored data |
| E1 pilot acceptance | `stream/pilot_e1.json`, `stream/pilot_acceptance.py` | criteria declared; **pilot not run (no host)** |
| O33 v3.1 amendment record | `research/registrations/o33-v3.1/` | **prepared; effective at its first push to `main`** |

Measured diagnostics at the repository cutoff of this build: `research/diagnostics/2026-10-19-repo-2.29.json`.

## Research interface

```
python -m research_tools.research_api --role researcher --actor actor.json open     --args open.json
python -m research_tools.research_api --role researcher --actor actor.json inspect  --args inspect.json
python -m research_tools.research_api --role researcher --actor actor.json run      --args run.json
python -m research_tools.research_api --role researcher --actor actor.json register --args register.json
python -m research_tools.research_api --role researcher --actor actor.json results  --args results.json
python -m research_tools.research_api --role evaluator  --actor evaluator.json evaluate --args evaluate.json
python -m research_tools.research_api --role researcher --actor actor.json verify   --args verify.json
```

`actor.json` names who acts: `{"kind": "model"|"human"|"system", "id", "version", "training_cutoff"}`. For a model,
`version` is the pinned identifier when the provider has one. If you only have an alias, write that down, because an
alias can point to a different model later. `training_cutoff` is the provider's claim, recorded as a claim.

**Partitions.** `open` fixes the experiment's discovery cutoff. Researcher operations return only rows decided
before it, and only labels available before it. `register` freezes a candidate: its spec hash, the code hashes,
any fitted transform artifact, the actor and the registration time. The candidate's confirmation rows are the ones
decided at or after that time, so their outcomes did not exist when it was frozen. The evaluator scores those rows
and releases results only at the experiment's declared checkpoint counts.

**What is enforced, and where.** The role check and partition filters are enforced inside the API and its tests.
No researcher operation returns a confirmation row, a confirmation label or an unreleased result, and the alternate
routes are refused: `inspect` past the cutoff, `run` with `partition="confirmation"`, a researcher calling
`evaluate`. Refusals are written to the ledger. Results are hash-chained, so an edited record fails `verify`.
**The filesystem is not sandboxed.** A process with the repository checked out can read `data/` directly. Reading
past the discovery cutoff outside the API is exposure: log it as a `query` entry with the dates. It does not reset
the experiment. The strongest protection is temporal: confirmation outcomes arrive after registration.

**Search ledger.** `research/search/ledger.jsonl` is append-only and hash-chained. It records hypotheses, queries
with the dates exposed, runs (including errors and aborts), results viewed, registrations, rejections and
retirements. Prompts and outputs are referenced by sha256 and a storage label, and private desk content stays out
of the public repository. The same `request_id` with the same payload is a traceable repeat; with a different
payload it is refused. `family_count()` counts every registered candidate and run in a family across sessions and
models. Ten prompts or ten models exploring the same history are one family, not ten confirmations.

**Model modes.** A *research assistant* explores history and proposes a reproducible candidate. Its historical
results are discovery evidence and carry the exposure label: a later model may have learned these outcomes in
training, and an as-of packet does not remove that knowledge. A *live forecaster* emits forecasts prospectively
through `research_tools/directional.py`, and every attempt is retained. A simulation that uses a later model on historical
rows is labelled as one. It is never a clean holdout.

## Continuous panel

`panel.build(Store(base, cutoff), start, end)` gives one row every 15 minutes for every grid time, in ordinary and
event periods alike. Each row carries feature values or explicit states (`source-missing`, `stale-inputs`,
`window-incomplete`, `insufficient-depth`, `flow-below-threshold`, `gated`), plus the input clocks it read. A row at
time T depends only on inputs whose `avail` is at or before T. The test `test_panel_rows_are_as_of_their_own_time`
checks that a later store cutoff leaves every earlier row unchanged. `labels()` builds forward returns separately,
with their availability. `fit_transform` learns scaling only from rows before a declared training cutoff and
records that cutoff, and `apply_transform` refuses an artifact that breaks the rule. Rows overlap and share shocks:
`session_utc`, `block_4h` and `event` are kept so that evaluation can respect dependence.

## Prospective directional stream (DIR1, prepared)

The contract is `research/registrations/dir1-prepared/protocol.json`. It uses hourly decisions at :00 UTC, a
240-minute horizon and P(up) forecasts. The horizon was chosen from measured input age at the decision clock
(median 180 s; p90 300 s at :00). Every expected opportunity is created from the schedule by `reconcile()`, so a
worker that never runs still leaves "missed" records. States move only along the allowed transitions. Every
inference attempt is kept, and the selection rule is the first valid parse. Publication counts only when a durable
copy binds the forecast's content hash. Grading starts from the first executable quote after publication. Forecast
quality (Brier score), directional utility and net value after costs are reported separately, each over the full
opportunity denominator per arm, with the paired intersection beside them.

## Deployment handoffs (each is a separate operator action; none is done by this branch)

1. **Merge this branch.** Merging sets the O33 v3.1 effective time: its first push to `main`. After the merge,
   record the merge commit and time in `research/registrations/o33-v3.1/effective.json` (read them from the GitHub
   API). Calls registered earlier stay original-rule corrections or retrospective reassessments.
2. **Register DIR1** (optional, when the frontier arm or the baseline-vs-statistical comparison is wanted): change
   `status` to `registered`, set `effective_utc` and `effective_evidence` from the merge commit, freeze the
   statistical artifact with `fit_logistic` on data before `effective_utc`, and add a scheduled workflow that runs
   reconcile → inputs → infer → publish → grade each hour. The frontier arm needs a model account and a pinned
   model identifier. Neither exists in this repository, so that arm stays uncommissioned until they are provided.
3. **Raw retention.** Wire `lab/archive_store.ArchiveStore` into `collector.py` with a bucket. The stream
   recorder's S3 backend is reused, and credentials come from environment variables. Set a budget before enabling
   it: the measured compact data is about 20 MB per month for snapshots, and raw responses will be several times
   larger. Check growth with `ArchiveStore.growth()`.
4. **E1 pilot.** This needs a persistent host. Under the operator's standing decision no always-on host is
   authorised, so the pilot stays prepared. If a host is approved, run `python -m stream.service --config ...` for
   the declared 14 days, then `python -m stream.pilot_acceptance STREAM_DATA_DIR --shocks N`.
5. **A2 and PS1-T1.** Each is registered by its own merge with status `registered` and a launch record. Until
   then, PS1 v3 and A1 continue unchanged.
6. **Hourly check** (skill package 12.4.20 `routines/hourly_refresh.md`). Replace the stored prompt with the new
   one and attach the conditional export the full read writes. Then confirm the first run's ledger line. The task
   stays hourly and notify-only.
