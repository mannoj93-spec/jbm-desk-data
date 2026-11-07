# Prospective 30-day options maturity pilot

State: active. Captures: 28/28 closed hours.

Control: nearest eligible expiries within 45 days. Alternate: within 90 days. Both capped at a 35-day span.
Identical frozen leg filters and source capture; no extrapolation. Later books do not alter quote eligibility.

| Horizon | Both usable | Gained | Lost | Neither | Missing capture |
|---|---:|---:|---:|---:|---:|
| 30d | 0 | 28 | 0 | 0 | 0 |

Books: 100 usable / 100 attempted / 112 selected distinct contracts across hours.
Quote sizes, source-to-book lag, spans, value differences and failure reasons: [JSON report](options_30d_pilot.json).

Separate prospective maturity experiment. Compare nearest eligible expiries within 45 versus 90 days, with identical leg filters and a 35-day maximum span in both arms. Repeated captures are dependent; usability is not predictive skill.
