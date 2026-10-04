# Native schedule degradation, from 2026-10-03 (repo 2.25)

Evidence-retrieval cutoff: 2026-10-04 18:40 UTC. Source: the GitHub Actions REST API (`/actions/runs`, every run created since
2026-10-02 00:00 UTC, 483 records), `git log` of `main`, and the repository settings that the API serves to this
session. Times are UTC. Run links: `https://github.com/mannoj93-spec/jbm-desk-data/actions/runs/<id>`.

## Timeline

| When (UTC) | Observation | Evidence |
|---|---|---|
| Oct 2 00:00 – Oct 3 09:59 | Normal native scheduling: 7–15 scheduled starts per hour across all workflows; collector 92 of 96 slots on Oct 2; hourly workflows 24 of 24 | run records |
| Oct 3 00:19 | Last workflow-file change before onset (2.23: node24 actions, release check) | commit 3390665d |
| Oct 3 10:00 – 11:59 | Onset: 4–5 scheduled starts per hour; collector 11:03:58 then silent to 13:26:49 | run 37118447964 |
| Oct 3 12:00 onward | 0–6 scheduled starts per hour, arriving in bursts several hours apart (e.g. Oct 4 02:35–02:49, 10:54–11:10, 17:59–18:24), every workflow affected together | run records |
| Oct 3 14:24 | First 2.24 workflow change, after onset | commit 8d3e35d3 |
| Oct 3 21:09:04 – Oct 4 17:50:49 | 82 nominal collector slots; 4 native collector runs (00:13:50, 03:51:18, 05:34:42, 11:07:58), all succeeded in 2.18–2.33 min including persistence; no manual dispatch | runs 37164299239, 37175258063, 37180295751, 37197684094 |
| Oct 4 03:09, 05:42, 15:26 | Range runs for 00:00, 04:00, 12:00 started 3.19, 1.75, 3.48 h late and refused publication (stale decision > 1.0 h) | runs 37173253178, 37180680176, 37213028052 |
| Oct 3 20:04 | Range 20:00 on time; PS1 3.2.0 eligible rebalance followed | runs 37150219746, 37150350498 |

## Explanations tested

| Explanation | Verdict | Evidence |
|---|---|---|
| Workflows disabled | Rejected | all twelve workflows `active` |
| Wrong default branch | Rejected | `default_branch: main`; scheduled runs that did start ran `main` |
| Schedule actor lost access | Rejected for the runs that start | scheduled runs carry actor `mannoj93-spec`, who also dispatched successfully on Oct 3 |
| Runs queued or cancelled by concurrency | Rejected | 0 queued, 0 in progress, 0 cancelled among 483 records; every recorded scheduled run started at its creation time |
| Job or persistence failures | Rejected for collection | every collector run in the window succeeded; failures elsewhere are the range freshness refusals and monitors reporting the silence |
| A repository change at onset | No change found | onset Oct 3 10–11; workflow files last changed Oct 3 00:19 and next at 14:24; push rate to `main` unchanged before onset |
| Actions minutes or account limits | Not verified | public repository (standard runners are not metered); the Actions permissions and billing endpoints are not served to this session |
| Platform-wide outage | Not established | GitHub's status page and other repositories' run histories were not reachable from this session |

Conclusion: the scheduler stopped creating most scheduled runs for this repository from Oct 3 10–11 UTC. Runs that were
created ran normally. No repository configuration explains it, and the root cause is not established. GitHub documents
that scheduled runs may be delayed or dropped under load; that permits, but does not prove, a platform cause.

Remedy (repo 2.25): an independently triggered recovery dispatcher (`recovery.py`, `.github/workflows/recovery.yml`) keeps
collection, range publication, the research streams and scoring on time while native scheduling is degraded, without
crediting itself as native cadence (`docs/OPERATIONS.md`, "Recovery dispatcher").
