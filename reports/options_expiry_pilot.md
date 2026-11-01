# Prospective options expiry pilot

State: active. Captures: 107/107 closed hours.

Control: nearest listed expiries. Alternate: nearest eligible expiries, capped at 14/35-day spans for 7d/30d.
Identical frozen leg filters and source capture; no extrapolation. Later books do not alter quote eligibility.

| Horizon | Both usable | Gained | Lost | Neither | Missing capture |
|---|---:|---:|---:|---:|---:|
| 7d | 89 | 18 | 0 | 0 | 0 |
| 30d | 6 | 0 | 0 | 101 | 0 |

Books: 432 usable / 432 attempted / 452 selected distinct contracts across hours.
Quote sizes, source-to-book lag, spans, value differences and failure reasons: [JSON report](options_expiry_pilot.json).

Repeated horizons and contracts are dependent. A usability gain does not demonstrate predictive skill.
