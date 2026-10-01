# JBM desk data

[![Collector](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/collect.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/collect.yml)
[![Research lab](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/research.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/research.yml)
[![Regression and numerical fixtures](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/fixtures.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/fixtures.yml)
[![Collector watchdog](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/watchdog.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/watchdog.yml)
[![Range forecasts](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range.yml)
[![Range scoring](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-score.yml)
[![Range monitor](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/range-monitor.yml)
[![Research streams](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/research-streams.yml/badge.svg)](https://github.com/mannoj93-spec/jbm-desk-data/actions/workflows/research-streams.yml)

This repository preserves public crypto-market history, freezes forecasts before they start, and
tests pre-registered research questions against that history. Its reports are evidence for human
review of trading skill files; nothing here trades, holds credentials, or edits a skill.

> **A green badge means a workflow ran and its checks passed. It is not evidence of a trading
> edge.** Whether any research design is supported is stated only in the generated research report.

## Start here

| I want to see | Open |
|---|---|
| Is collection running and fresh? | [reports/latest.md](reports/latest.md) - coverage, data age, cadence |
| What did the research find? | [reports/research.md](reports/research.md) - every design, its status, integrity and evidence |
| Is any skill change proposed? | [reports/skill_proposals.md](reports/skill_proposals.md) - proposals, or why there are none |
| Weekly forecast scores (issue-intake streams) | [reports/](reports/) - dated weekly reports; desk range forecasts are scored hourly (next row) |
| How is the desk's range model doing? | [reports/range.md](reports/range.md) - current availability, scoring pipeline, paired B2 vs persistence evidence (descriptive) and recent decisions ([status JSON](reports/range_status.json), [desk/](desk/README.md)) |
| Does DVOL add to the range forecast? | [reports/companion_b1.md](reports/companion_b1.md) - B2 vs B1 (no DVOL) beside B2 vs B0, same windows (descriptive) |
| Do the range forecasts improve a sizing decision? | [reports/paper_ps1.md](reports/paper_ps1.md) - paper sizing experiment PS1: simulated fills, sizing only, never an entry signal ([protocol](desk/research/ps1/protocol.json)) |
| Can each research question accumulate evidence? | [reports/feasibility.md](reports/feasibility.md) - coverage, events, warm-up, limiting factor, cautious time-to-checkpoint |
| How was this version tested and deployed? | [VALIDATION.md](VALIDATION.md) |
| What changed, release by release | [CHANGELOG.md](CHANGELOG.md) |
| How to run and operate it | [Quick start](#quick-start) and [docs/OPERATIONS.md](docs/OPERATIONS.md) |

## Four separate signals

| Signal | Where | What it does **not** mean |
|---|---|---|
| Workflow success | badges above, the Actions tab | that data is fresh, or that any result is supported |
| Data freshness | [reports/latest.md](reports/latest.md) (latest observation, age, cadence coverage) | that research has enough observations |
| Research integrity | the Integrity column of [reports/research.md](reports/research.md) | that a result exists; it only says the inputs of the latest attempt validated |
| Evidence maturity | the Status column of [reports/research.md](reports/research.md) (`exploratory`, `under prospective evaluation`, `supported`, `retired`, `blocked`) | profitability: `supported` means pre-declared descriptive criteria held on prospective replays |

Counts, ages and statuses change every run, so they live only in the generated reports.

## How it works

1. **Collector** (every 15 minutes) appends raw observations under `data/` with the time each was
   written; history is never rewritten.
2. **Research lab** (every 6 hours) replays each design in `lab/designs/` as of the data it could
   have seen, freezes its decisions, records checkpoints once, and writes evidence cards and
   reports. Evaluation versions are hashes of the semantic code, so a logic change starts a new
   clock; presentation changes do not.
3. **Persist** merges the lab's outputs into the latest checkout only if they are complete and
   consistent with the lab's own publication metadata; otherwise nothing is published.
4. **Weekly report** scores the issue-intake forecasts and summarises; **forecast intake** freezes new ones
   from issues. Desk range forecasts are scored **hourly** by `range-score.yml` (step 5), not weekly.
5. **Range forecasts** (after every 4H close) run the crypto desk's range model in `desk/`, register
   its 4h, 24h and 72h forecasts with a persistence baseline in one transaction, and confirm the
   publication before the windows open.
6. **Research streams** (after each range run; 2.20) register a B1 companion forecast for every RC1D window,
   run the paper sizing experiment PS1 on quotes captured after each decision is confirmed, and refresh the
   feasibility report ([docs/RESEARCH_STREAMS.md](docs/RESEARCH_STREAMS.md)). Paper results are simulations.
   Since 2.21 each run logs every stage and fails when a required stage or output fails; PS1 runs protocol v2.

<details>
<summary>Repository map</summary>

| Path | Contents |
|---|---|
| `collector.py`, `enrich.py`, `hlsample.py`, `optionsbook.py`, `schema.py`, `storage.py` | collection, sampling, storage |
| `data/`, `state/`, `registry/` | collected history, run state, registered forecasts (append-only) |
| `lab/` | research lab: designs, evaluation, controls, evidence, reports |
| `research/` | frozen decisions, outcomes, checkpoints, control selections, evidence cards |
| `reports/` | generated reports (coverage, research, proposals, weekly) |
| `report.py`, `scoring.py`, `intake.py`, `watchdog.py` | reports, scoring, forecast intake, watchdog |
| `scripts/` | persistence, merge gate, before/after reproductions |
| `regression/`, `test_fixtures.py` | offline regression tests and numerical fixtures |
| `desk/` | the crypto desk's range model, loaders, monthly fits and forecast job (see desk/README.md); companion and PS1 jobs (2.20) |
| `streams/`, `feasibility.py` | prospective research streams (companion B1, paper sizing PS1) and the read-only feasibility report |
| `stream/` | optional streaming recorder (not deployed) |
| `docs/OPERATIONS.md` | detailed operations and research reference |

</details>

## Quick start

Python 3.12, standard library only; no exchange keys or trading credentials.

```sh
python test_fixtures.py                          # numerical fixtures
python -m unittest discover -s regression        # offline regression suite
python -m lab.run update --no-write              # research lab, compute and print only
python report.py --coverage-only                 # refresh the coverage report
```

Deployment, schedules, backfill, forecast submission, scoring and the research-lab rules are in
[docs/OPERATIONS.md](docs/OPERATIONS.md).
