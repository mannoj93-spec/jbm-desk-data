# Operational health

Generated 2026-11-20T21:45:36Z by health-1.5.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule (secondary trigger):** last scheduled collector run 2026-11-20T16:28:28Z (317.1 min); 10 silence(s) over 90 min in the last 72 h, longest 544 min. Native starts per closed day: 2026-11-17 3 of 98 automated runs; 2026-11-18 3 of 97 automated runs; 2026-11-19 3 of 97 automated runs. Each silence is in reports/health.json; incidents carry one summary row per day.

**Service continuity:** healthy; last persisted critical success 2026-11-20T21:43:37Z (2.0 min); last automated activity 2026-11-20T21:43:37Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 3, recovery 94; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 16.9 min.

**Range decisions:** 11-19T16:00 published; 11-19T20:00 published; 11-20T00:00 published; 11-20T04:00 published; 11-20T08:00 published; 11-20T12:00 published; 11-20T16:00 published; 11-20T20:00 failed: attempt failed.

**PS1 decisions:** 11-19T16:00 executed; 11-19T20:00 executed; 11-20T00:00 executed; 11-20T04:00 executed; 11-20T08:00 executed; 11-20T12:00 executed; 11-20T16:00 executed; 11-20T20:00 no-rebalance.

**PS1 report coverage:** 0.8095 as of 2026-11-20T20:42:07.368Z; due since and not covered: 11-20T20:00 no-rebalance.

**Range availability:** status expired (expires 2026-11-20T21:15:00Z); 24h expired on this clock; 4h stale; 72h expired on this clock.

**Scoring backlog:** none.

**Native scheduled monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-11-20T17:18:59Z: success; last success 2026-11-20T17:18:45Z); range-monitor.yml heartbeat fresh (last run 2026-11-20T18:02:24Z: success; last success 2026-11-20T18:02:14Z); range-readiness.yml heartbeat fresh (last run 2026-11-20T03:42:29Z: success; last success 2026-11-20T03:42:10Z); newest scheduled start of any workflow 2026-11-20T20:40:51Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-11-20T21:42:03Z. Arrivals only: whether each request was sent needs the provider's history.

**External timer token:** expiry not recorded - record token.expires_utc in docs/acceptance/timer.json; an expired token stops the primary trigger.

**Record integrity:** no malformed lines in the files read.

Recovery service-watch: fresh; passed; last check completion 2026-11-20T21:42:15Z.
Recovery study-watch: fresh; passed; last check completion 2026-11-20T21:43:44Z.