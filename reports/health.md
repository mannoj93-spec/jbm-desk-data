# Operational health

Generated 2026-11-12T11:00:17Z by health-1.5.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule (secondary trigger):** last scheduled collector run 2026-11-12T07:36:17Z (204.0 min); 11 silence(s) over 90 min in the last 72 h, longest 631 min. Native starts per closed day: 2026-11-09 3 of 96 automated runs; 2026-11-10 4 of 97 automated runs; 2026-11-11 3 of 96 automated runs. Each silence is in reports/health.json; incidents carry one summary row per day.

**Service continuity:** healthy; last persisted critical success 2026-11-12T10:58:23Z (1.9 min); last automated activity 2026-11-12T10:58:23Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 3, recovery 93; 93 of 95 slot intervals hold an automated critical success (93 hold any automated activity); longest gap between successes 49.6 min.

**Range decisions:** 11-11T04:00 published; 11-11T08:00 published; 11-11T12:00 published; 11-11T16:00 published; 11-11T20:00 published; 11-12T00:00 published; 11-12T04:00 published; 11-12T08:00 published.

**PS1 decisions:** 11-11T04:00 executed; 11-11T08:00 executed; 11-11T12:00 executed; 11-11T16:00 no-rebalance; 11-11T20:00 executed; 11-12T00:00 executed; 11-12T04:00 executed; 11-12T08:00 executed.

**PS1 report coverage:** 0.786 as of 2026-11-12T08:24:17.986Z; due since and not covered: none.

**Range availability:** status within expiry (expires 2026-11-12T12:25:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Native scheduled monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-11-12T08:21:37Z: success; last success 2026-11-12T08:21:27Z); range-monitor.yml heartbeat fresh (last run 2026-11-12T08:52:14Z: success; last success 2026-11-12T08:52:02Z); range-readiness.yml heartbeat fresh (last run 2026-11-12T03:19:43Z: success; last success 2026-11-12T03:19:24Z); newest scheduled start of any workflow 2026-11-12T10:15:46Z.

**External timer (primary trigger):** gaps; 94 of 96 opportunities on time in 24 h, 0 delayed, absent 2026-11-11T20:27:00Z, 2026-11-11T20:42:00Z; last arrival 2026-11-12T10:57:02Z. Arrivals only: whether each request was sent needs the provider's history.

**External timer token:** expiry not recorded - record token.expires_utc in docs/acceptance/timer.json; an expired token stops the primary trigger.

**Record integrity:** no malformed lines in the files read.

Recovery service-watch: fresh; passed; last check completion 2026-11-12T10:57:10Z.
Recovery study-watch: fresh; passed; last check completion 2026-11-12T10:58:18Z.