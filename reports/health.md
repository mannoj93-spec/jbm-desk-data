# Operational health

Generated 2026-11-25T18:45:39Z by health-1.5.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule (secondary trigger):** last scheduled collector run 2026-11-25T16:09:36Z (156.0 min); 9 silence(s) over 90 min in the last 72 h, longest 724 min. Native starts per closed day: 2026-11-22 4 of 98 automated runs; 2026-11-23 2 of 97 automated runs; 2026-11-24 3 of 97 automated runs. Each silence is in reports/health.json; incidents carry one summary row per day.

**Service continuity:** healthy; last persisted critical success 2026-11-25T18:43:33Z (2.1 min); last automated activity 2026-11-25T18:43:33Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 3, recovery 94; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 19.6 min.

**Range decisions:** 11-24T12:00 published; 11-24T16:00 published; 11-24T20:00 published; 11-25T00:00 published; 11-25T04:00 published; 11-25T08:00 published; 11-25T12:00 published; 11-25T16:00 published.

**PS1 decisions:** 11-24T12:00 executed; 11-24T16:00 executed; 11-24T20:00 executed; 11-25T00:00 executed; 11-25T04:00 executed; 11-25T08:00 executed; 11-25T12:00 executed; 11-25T16:00 executed.

**PS1 report coverage:** 0.8235 as of 2026-11-25T16:38:59.926Z; due since and not covered: none.

**Range availability:** status within expiry (expires 2026-11-25T20:25:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Native scheduled monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-11-25T12:58:23Z: success; last success 2026-11-25T12:58:11Z); range-monitor.yml heartbeat fresh (last run 2026-11-25T10:32:42Z: success; last success 2026-11-25T10:32:29Z); range-readiness.yml heartbeat fresh (last run 2026-11-25T05:01:07Z: success; last success 2026-11-25T05:00:45Z); newest scheduled start of any workflow 2026-11-25T16:08:23Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-11-25T18:42:03Z. Arrivals only: whether each request was sent needs the provider's history.

**External timer token:** expiry not recorded - record token.expires_utc in docs/acceptance/timer.json; an expired token stops the primary trigger.

**Record integrity:** no malformed lines in the files read.

Recovery service-watch: fresh; passed; last check completion 2026-11-25T18:42:14Z.
Recovery study-watch: fresh; check failed; last check completion 2026-11-25T18:43:38Z.