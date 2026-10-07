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
