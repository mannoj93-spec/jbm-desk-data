# Operational health

Generated 2026-11-28T02:00:13Z by health-1.5.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule (secondary trigger):** last scheduled collector run 2026-11-27T19:41:11Z (379.0 min); 9 silence(s) over 90 min in the last 72 h, longest 626 min. Native starts per closed day: 2026-11-25 2 of 96 automated runs; 2026-11-26 3 of 97 automated runs; 2026-11-27 3 of 95 automated runs. Each silence is in reports/health.json; incidents carry one summary row per day.

**Service continuity:** healthy; last persisted critical success 2026-11-28T01:58:31Z (1.7 min); last automated activity 2026-11-28T01:58:31Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 2, recovery 94; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 20.2 min.

**Range decisions:** 11-26T20:00 published; 11-27T00:00 published; 11-27T04:00 published; 11-27T08:00 published; 11-27T12:00 published; 11-27T16:00 published; 11-27T20:00 published; 11-28T00:00 published.

**PS1 decisions:** 11-26T20:00 executed; 11-27T00:00 executed; 11-27T04:00 executed; 11-27T08:00 executed; 11-27T12:00 executed; 11-27T16:00 executed; 11-27T20:00 executed; 11-28T00:00 no-rebalance.

**PS1 report coverage:** 0.8279 as of 2026-11-28T00:27:59.358Z; due since and not covered: 11-28T00:00 no-rebalance.

**Range availability:** status within expiry (expires 2026-11-28T04:25:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Native scheduled monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-11-27T23:44:56Z: success; last success 2026-11-27T23:44:45Z); range-monitor.yml heartbeat fresh (last run 2026-11-27T22:22:28Z: success; last success 2026-11-27T22:22:16Z); range-readiness.yml heartbeat fresh (last run 2026-11-27T04:30:10Z: success; last success 2026-11-27T04:29:46Z); newest scheduled start of any workflow 2026-11-27T23:55:49Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-11-28T01:57:02Z. Arrivals only: whether each request was sent needs the provider's history.

**External timer token:** expiry not recorded - record token.expires_utc in docs/acceptance/timer.json; an expired token stops the primary trigger.

**Record integrity:** no malformed lines in the files read.

Recovery service-watch: fresh; passed; last check completion 2026-11-28T01:57:10Z.
Recovery study-watch: fresh; passed; last check completion 2026-11-28T01:58:46Z.