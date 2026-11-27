# Operational health

Generated 2026-11-27T22:00:27Z by health-1.5.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule (secondary trigger):** last scheduled collector run 2026-11-27T19:41:11Z (139.3 min); 10 silence(s) over 90 min in the last 72 h, longest 626 min. Native starts per closed day: 2026-11-24 3 of 97 automated runs; 2026-11-25 2 of 96 automated runs; 2026-11-26 3 of 97 automated runs. Each silence is in reports/health.json; incidents carry one summary row per day.

**Service continuity:** healthy; last persisted critical success 2026-11-27T21:58:28Z (2.0 min); last automated activity 2026-11-27T21:58:28Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 3, recovery 94; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 20.2 min.

**Range decisions:** 11-26T16:00 published; 11-26T20:00 published; 11-27T00:00 published; 11-27T04:00 published; 11-27T08:00 published; 11-27T12:00 published; 11-27T16:00 published; 11-27T20:00 published.

**PS1 decisions:** 11-26T16:00 executed; 11-26T20:00 executed; 11-27T00:00 executed; 11-27T04:00 executed; 11-27T08:00 executed; 11-27T12:00 executed; 11-27T16:00 executed; 11-27T20:00 executed.

**PS1 report coverage:** 0.8304 as of 2026-11-27T21:42:49.736Z; due since and not covered: none.

**Range availability:** status within expiry (expires 2026-11-28T00:30:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Native scheduled monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-11-27T15:37:29Z: success; last success 2026-11-27T15:37:13Z); range-monitor.yml heartbeat stale (last run 2026-11-27T10:10:30Z: success; last success 2026-11-27T10:10:20Z); range-readiness.yml heartbeat fresh (last run 2026-11-27T04:30:10Z: success; last success 2026-11-27T04:29:46Z); newest scheduled start of any workflow 2026-11-27T21:40:45Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-11-27T21:57:02Z. Arrivals only: whether each request was sent needs the provider's history.

**External timer token:** expiry not recorded - record token.expires_utc in docs/acceptance/timer.json; an expired token stops the primary trigger.

**Record integrity:** no malformed lines in the files read.

Recovery service-watch: fresh; passed; last check completion 2026-11-27T21:57:10Z.
Recovery study-watch: fresh; check failed; last check completion 2026-11-27T21:59:12Z.