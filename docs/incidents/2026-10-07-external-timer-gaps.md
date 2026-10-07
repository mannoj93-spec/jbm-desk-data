# External-timer arrival gaps, 2026-10-07 (repo 2.28)

A separate incident. It is not the Oct 3 native-schedule silence (root cause still unresolved), not the Oct 4-5
host-key HTTP 403 (repaired in 2.26, working since), and not the Oct 5 hosted-runner assignment outage (GitHub incident
`3q1yb5m7ltvb`; see 2026-10-03-native-schedule.md). The recovery design that kept service through those is unchanged.

Assessment clock: dispatcher runs retrieved 2026-10-07T20:00Z (`evidence/2026-10-07-dispatcher-runs.tsv`, 127 runs
created since 00:00Z); GitHub status incidents retrieved 20:02Z (`evidence/2026-10-07-githubstatus.json`); collector
records read from main at `634006260` (pushed 19:58:54Z).

## Observed (GitHub side only)

The external timer (cron-job.org, the designated primary trigger) should produce an external-titled
`workflow_dispatch` dispatcher run at :12/:27/:42/:57. On Oct 7, 79 opportunities 00:12-19:42Z:

| Opportunity | GitHub arrival | Note |
|---|---|---|
| 15:12Z | none | GitHub incident `djlmxz2zd0j7` (opened 15:14:45Z) states widespread impact 15:06-15:16Z |
| 16:12Z | 16:13:06Z (66 s) | inside the 90 s timer tolerance; the only lag over 2 s that day |
| 16:57Z | none | GitHub incident `qpfv5p86dmrl` (opened 17:17:05Z) states impact 16:52-17:01Z, a recurrence of the first |
| other 76 | 1-2 s after | on time |

Both absences fall inside the impact windows GitHub later stated. That is correlation in time. It does not show
whether cron-job.org sent each request, what GitHub answered, or whether a request was retried: the provider's job
execution history was not available to this assessment (the console was not signed in; no export supplied). The
absences are therefore recorded as "no arrival on GitHub", cause **unattributed at the delivery level**.

The native dispatcher also paused across the first window (15:00:06Z, then 15:38:34Z), as did native collection
(15:02:00Z, then 15:30:10Z).

## Effect on collection

- 15:12Z: interval 15:07-15:22Z held no record (15:02:00 -> 15:27:42, 25.7 min). One empty interval; it counts against
  the declared 2026-10-07 acceptance window (allowance 2 of 95).
- 16:57Z: covered - the recovery rooted in the native dispatcher (run 37656173173, 17:04:24Z) collected at 17:05:07Z
  (16:49:22 -> 17:05:07, 15.7 min).
- No critical failure, no lost output, no reconstruction.

## What changed in 2.28

Health reports external-timer arrivals apart from the native dispatcher, execution and persisted success
(`monitors.external_timer`: on time / delayed / absent per opportunity, `on_time_max_lag_s`, last arrival), and the
dashboard shows it as its own row, so service kept healthy by the native fallback no longer hides missing primary
arrivals. It is arrival evidence only. No new watchdog was added.

## Needed to attribute (operator)

The cron-job.org execution history for the job that calls
`POST /repos/mannoj93-spec/jbm-desk-data/actions/workflows/recovery.yml/dispatches`, covering 2026-10-07 15:00-17:15Z
(and, for acceptance, the whole declared window): per execution the scheduled and actual time, HTTP status, response
body or error, duration and any retry; plus the job id, to pin in `docs/acceptance/timer.json`. A 2xx at 15:12/16:57
would place the loss on GitHub's side; a failure or timeout recorded by the provider would show the request was sent
and refused; no execution would point at the provider.

## Update 2026-10-07 22:45Z (repo 2.28.1): attributed from the provider's history

The operator signed in to cron-job.org and asked for the history to be read. Job **8579326** ("JBM recovery
dispatcher", schedule in America/New_York) is now pinned in `docs/acceptance/timer.json`; its execution history,
10:12Z-22:27Z Oct 7 (50 executions, all the console still retained), is in
`docs/acceptance/receipts/2026-10-07-cron-job-org.json`.

| Opportunity | cron-job.org | GitHub |
|---|---|---|
| 15:12Z | sent at 15:12:00.892Z; **HTTP 500 Internal Server Error** after 557 ms | no run |
| 16:12Z | sent at 16:12:00.972Z; **no complete response within the 30 s timeout** | run 37650301673 created 16:13:06Z (65 s later) |
| 16:57Z | sent at 16:57:00.592Z; **HTTP 500 Internal Server Error** after 734 ms | no run |
| other 47 | HTTP 204 No Content in 1.5-2.4 s | one run each, created 0.4-1.5 s after the request; no unexplained dispatcher run |

**Attribution.** The timer sent every request on time. GitHub refused the two missing dispatches with HTTP 500, inside
its own stated impact windows (incidents `djlmxz2zd0j7` 15:06-15:16Z and `qpfv5p86dmrl` 16:52-17:01Z), and at 16:12Z
accepted the request but answered too slowly, creating the run 65 s later. The cause of the gaps is GitHub's API
during its incidents, not the timer and not this repository. The provider does not retry a failed execution; the
native dispatcher's fallback is what covered 16:57 (collection 17:05:07Z); 15:12's interval stayed empty.

**Limits.** Response bodies were not stored (the job's "save responses" option is off), so GitHub's error text is not
available. Executions before 10:12Z on Oct 7 and the whole Oct 6 window had already aged out of the console, so the
dispatcher runs of those hours stay timer-corroborated, not receipted. The request headers were not read (they hold
the token); method, ref and inputs are confirmed by GitHub having created a `workflow_dispatch` run with
`trigger=external` on `main` for every 204.
