# Prospective options expiry pilot

State: active. Captures: 544/545 closed hours.

Control: nearest listed expiries. Alternate: nearest eligible expiries, capped at 14/35-day spans for 7d/30d.
Identical frozen leg filters and source capture; no extrapolation. Later books do not alter quote eligibility.

| Horizon | Both usable | Gained | Lost | Neither | Missing capture |
|---|---:|---:|---:|---:|---:|
| 7d | 454 | 87 | 0 | 3 | 1 |
| 30d | 213 | 19 | 0 | 312 | 1 |

Books: 2912 usable / 2916 attempted / 3084 selected distinct contracts across hours.
Quote sizes, source-to-book lag, spans, value differences and failure reasons: [JSON report](options_expiry_pilot.json).

Repeated horizons and contracts are dependent. A usability gain does not demonstrate predictive skill.
