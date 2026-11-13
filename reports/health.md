# Operational health

Generated 2026-11-13T15:30:08Z by health-1.5.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule (secondary trigger):** last scheduled collector run 2026-11-13T10:05:26Z (324.7 min); 12 silence(s) over 90 min in the last 72 h, longest 515 min. Native starts per closed day: 2026-11-10 4 of 97 automated runs; 2026-11-11 3 of 96 automated runs; 2026-11-12 4 of 98 automated runs. Each silence is in reports/health.json; incidents carry one summary row per day.

**Service continuity:** healthy; last persisted critical success 2026-11-13T15:28:27Z (1.7 min); last automated activity 2026-11-13T15:28:27Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 4, recovery 94; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 18.7 min.

**Range decisions:** 11-12T08:00 published; 11-12T12:00 published; 11-12T16:00 published; 11-12T20:00 published; 11-13T00:00 published; 11-13T04:00 published; 11-13T08:00 published; 11-13T12:00 published.

**PS1 decisions:** 11-12T08:00 executed; 11-12T12:00 executed; 11-12T16:00 executed; 11-12T20:00 executed; 11-13T00:00 executed; 11-13T04:00 executed; 11-13T08:00 executed; 11-13T12:00 no-rebalance.

**PS1 report coverage:** 0.788 as of 2026-11-13T12:42:18.442Z; due since and not covered: 11-13T12:00 no-rebalance.

**Range availability:** status within expiry (expires 2026-11-13T16:25:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Native scheduled monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-11-13T11:00:25Z: success; last success 2026-11-13T11:00:15Z); range-monitor.yml heartbeat fresh (last run 2026-11-13T08:48:47Z: success; last success 2026-11-13T08:48:37Z); range-readiness.yml heartbeat fresh (last run 2026-11-13T02:53:07Z: success; last success 2026-11-13T02:52:54Z); newest scheduled start of any workflow 2026-11-13T14:53:13Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-11-13T15:27:02Z. Arrivals only: whether each request was sent needs the provider's history.

**External timer token:** expiry not recorded - record token.expires_utc in docs/acceptance/timer.json; an expired token stops the primary trigger.

**Record integrity:** no malformed lines in the files read.

Recovery service-watch: fresh; passed; last check completion 2026-11-13T15:27:11Z.
Recovery study-watch: fresh; passed; last check completion 2026-11-13T15:28:25Z.