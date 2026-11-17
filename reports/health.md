# Operational health

Generated 2026-11-17T21:15:51Z by health-1.5.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule (secondary trigger):** last scheduled collector run 2026-11-17T12:29:43Z (526.1 min); 11 silence(s) over 90 min in the last 72 h, longest 610 min. Native starts per closed day: 2026-11-14 4 of 100 automated runs; 2026-11-15 5 of 99 automated runs; 2026-11-16 3 of 92 automated runs. Each silence is in reports/health.json; incidents carry one summary row per day.

**Service continuity:** healthy; last persisted critical success 2026-11-17T21:13:56Z (1.9 min); last automated activity 2026-11-17T21:13:56Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 2, recovery 95; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 16.3 min.

**Range decisions:** 11-16T16:00 published; 11-16T20:00 published; 11-17T00:00 published; 11-17T04:00 published; 11-17T08:00 published; 11-17T12:00 published; 11-17T16:00 published; 11-17T20:00 published.

**PS1 decisions:** 11-16T16:00 executed; 11-16T20:00 executed; 11-17T00:00 executed; 11-17T04:00 executed; 11-17T08:00 executed; 11-17T12:00 executed; 11-17T16:00 executed; 11-17T20:00 executed.

**PS1 report coverage:** 0.8043 as of 2026-11-17T20:25:57.388Z; due since and not covered: none.

**Range availability:** status within expiry (expires 2026-11-18T00:25:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Native scheduled monitors:** fresh (GitHub Actions API, scheduled runs); watchdog.yml heartbeat fresh (last run 2026-11-17T20:56:54Z: success; last success 2026-11-17T20:56:42Z); range-monitor.yml heartbeat fresh (last run 2026-11-17T14:56:07Z: success; last success 2026-11-17T14:55:50Z); range-readiness.yml heartbeat fresh (last run 2026-11-17T04:45:37Z: success; last success 2026-11-17T04:45:15Z); newest scheduled start of any workflow 2026-11-17T21:14:54Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-11-17T21:12:02Z. Arrivals only: whether each request was sent needs the provider's history.

**External timer token:** expiry not recorded - record token.expires_utc in docs/acceptance/timer.json; an expired token stops the primary trigger.

**Record integrity:** no malformed lines in the files read.

Recovery service-watch: fresh; passed; last check completion 2026-11-17T21:12:09Z.
Recovery study-watch: fresh; check failed; last check completion 2026-11-17T21:13:37Z.