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

## Update 2026-10-05 (repo 2.26): timeline through recovery, cause status, primary scheduler

Evidence: every run created 2026-10-01 00:00 – 2026-10-05 14:00 UTC, retrieved 13:27Z in four sub-1,000 windows with
complete pagination (335 + 322 + 146 + 295 = 1,098 runs, matching `total_count`); job-level timing for the 101
collector runs since recovery activation; committed `data/runs/2026-10.jsonl` at `ad9df852`. A run absent from the
retrieved history is "not observed": the API cannot distinguish a schedule GitHub never created from one it dropped.

| Phase (UTC) | Scheduled starts, all workflows | Native collector starts / nominal slots | Notes |
|---|---|---|---|
| Normal, Oct 1 00:00 – Oct 3 10:00 (58.0 h) | 532 (9.2/h) | 215 / ~232 (93%) | 0 failures outside the test workflow |
| Onset + degraded, Oct 3 10:00 – Oct 4 20:41 (34.7 h) | 56 (1.6/h) | 10 / ~138 (7%) | range 4 late refusals; monitors failing correctly |
| Recovery active, Oct 4 20:41 – Oct 5 13:30 (16.8 h) | 208 (12.4/h, includes 39 of the dispatcher's own) | 51 / ~67 (76%) | 2 collector and 3 scoring persistence failures (host-key lookup, below) |

Delays: every run's `run_started_at` equals its `created_at` (no run-level queue); collector job start after run
creation p50 3 s, p90 21 s, max 88 s (the shared `repo-write` queue); job duration p50 134 s. Native collector starts
fall p50 8.9 min / p90 12.7 min after the nearest preceding nominal slot in normal operation and p50 7.5 / p90 13.2 min
since recovery - start times cannot be mapped to slots, so this is lateness relative to the nearest slot, not per-slot
delivery. No run was cancelled or skipped by concurrency in any phase.

External timer (cron-job.org -> `recovery.yml`, input `trigger=external`): 67 of 67 expected ticks from 20:57 Oct 4 to
13:27 Oct 5 observed, each created 2 s after its minute (:12/:27/:42/:57); one further owner dispatch at 20:41:40 was the
operator's test run. Recovery collector runs: 50 dispatched, 49 stored a record, 0 yielded, 1 lost to the host-key
failure. Redundancy: in the 64 slot intervals 21:07 Oct 4 – 13:07 Oct 5, all 64 hold a stored record and 31 hold two
(recovery at slot + 5 min, native at its usual slot + ~9 min); the native run does not yield. That costs one extra
collection (~2.3 runner-minutes, one set of exchange requests) per doubled interval and no research effect.

Persistence failures (a separate, demonstrated defect): runs 37241670422 (Oct 4 22:52, scoring), 37254784980 (Oct 5
02:16, native collector), 37267857320 (05:27, recovery collector), 37269928618 (05:55, scoring) and 37299609372
(10:55, scoring) collected or scored successfully, then failed in `scripts/commit_push.sh` on an unauthenticated
`api.github.com/meta` request: "HTTP Error 403: rate limit exceeded". Fixed in 2.26 (`scripts/github_host_keys.py`).
The two collector artifacts were verified against GitHub's digests and their 13 forward-only rows preserved under
`data/restored/` (receipt `data/restored/receipts.jsonl`); they do not count as on-time collection.

| Explanation for the missing native starts | Status | Evidence |
|---|---|---|
| Workflow disabled, wrong default branch, cron edited | ruled out | 12 workflows active; `main` default; collector cron unchanged since 90fce230 (Sep 23) |
| Concurrency cancellation or pending-run replacement | ruled out | 0 cancelled, 0 skipped runs in 1,098; no created-but-unstarted runs |
| Runner shortage / queueing | ruled out as the cause of absent runs | runs that exist started at creation; job queue p90 21 s |
| A repository change at onset | not supported | no workflow change between Oct 3 00:19 and 14:24; onset 10–11Z |
| Collector or persistence failure | ruled out for the absence; demonstrated for 5 later runs | absent runs leave no record at all; the 5 failures were created, ran and failed late |
| Account restrictions or Actions settings | not verified | `actions/permissions*` and billing are not served to this session |
| GitHub-side scheduler degradation | consistent, not demonstrated | all workflows affected together; created_at == started_at; status page not readable here; public reports of the same symptom since Aug 26 2026 (community discussion #207346), no GitHub acknowledgment found |

Root cause: **unresolved**. Next evidence: GitHub's answer for this repository's schedule events in the windows above
(support draft delivered with 2.26, not sent) and the account's Actions settings page.

### Primary scheduling decision (2.26)

Requirement: a collection start in every 15-minute interval (acceptance: >= 97% of intervals, gaps <= 45 min) and
range runs inside 60 minutes of each 4H close. Native scheduling delivered 76% of collector slots since recovery
(93% in normal operation) with p90 lateness ~13 min, so it cannot be the sole authority. The external timer delivered
67/67 ticks within 2 s.

Decision: the **external timer -> recovery dispatcher is the primary trigger authority** for the time-critical chain
(collector, range, research streams, scoring); GitHub's native schedules stay enabled as an independent, bounded
fallback and as the measurement of GitHub's scheduler. No cron, grace or workflow is changed for this decision: the
dispatcher already starts collection at slot + 5 min and range runs from close + 8 min, and the native runs that
arrive later are measured redundancy, not removed. What still depends on GitHub: the dispatch API, runners, the
workflow token and persistence. Credential: one fine-grained token, Actions read/write on this repository only,
expiring 2027. Failure detection: cron-job.org failure e-mail (refused calls), the dispatcher's `service-watch` job,
`monitors["recovery.yml"]` (stale after 45 min) and native watchdog runs. Idempotency: per-slot/per-decision keys,
yields and the jobs' own registration checks. Rollback: disable the cron-job.org job; native schedules continue
unchanged. Revisit when native delivery has met the 97% target unaided for 7 days, or on GitHub's answer.
