# Backtest spec — written before results (Oct 5 2026, ~00:50Z Oct 6)

Class: retrospective exploration (E-01 "exploratory"). Not a registered prospective test.

Question: do the desk's lean rules (S-04 deferral + structure-break conversion + OI/funding
confirmation) produce directional calls that beat a no-skill baseline, and how often do they fire?

Data: Binance BTCUSDT perp 4H klines 2020-01-01 → 2026-10-04 (data.binance.vision via jbm_archive);
Binance BTCUSDT OI (archive metrics, 5-min, ok days only) 2024-10-01 → 2026-10-04; Binance funding
history 2020 →. Cross-venue OI has no history before Sep 2026, so Binance OI stands in (labelled).

Mechanical proxy for a lean (the live process is partly judgmental; this tests the rules, not me):
- Structure break: long if close_t > max(high, prior N bars); short if close_t < min(low, prior N).
- S-04 gate: bar move m_t = close_t − open_t. If m_t in the lean direction exceeds T, defer to the
  next close: convert if that close is still beyond the level and its bar move ≤ T in that
  direction; carry once more if it is again > T; withdraw after two carries; cancel if back inside.
- OI confirmation: Binance OI change over the decision bar > 0 (new positions, not covering).
- Funding not crowded: long needs last settled funding ≤ +1 bp; short needs ≥ −1 bp.

Variants: V0 raw break; V1 + S-04 (desk rule); V2 = V1 + OI; V3 = V2 + funding.

PRIMARY (declared now): N = 24 bars, T = 0.353% of price (300 pts at 85,000), horizon 24h
(6 bars), cost 10 bp round trip (taker both sides), metric = mean signed log return net of cost,
drift-adjusted (minus direction × the sample's mean 24h return), 95% CI by weekly block bootstrap.
Samples: full 2020-01→2026-10 (V0, V1), last 24 months (V0–V3).

Secondary (multiplicity noted, not used to pick a winner): N ∈ {24, 42}; T ∈ {0.353% of price,
0.5 × trailing 42-bar 4H σ}; horizons 4h and 24h; last 6 months.

Also measured: S-04 directly — after a bar moving more than T, the next-4h and next-24h return in
the move's direction (continuation) vs. all bars.

Baselines: zero (no skill, before drift), and the drift adjustment above. Hit rate vs 50%.
