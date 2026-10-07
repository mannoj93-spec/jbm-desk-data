# Lean-rule backtest: S-04 and the conversion conditions (Oct 5–6 2026), corrected Oct 6

**Status.** This replaces the Oct 6 00:44Z version of this note, which over-stated three findings: that deferral "made breakout leans worse", that large moves are "not followed by more reversal", and the 48-cell count. It is retrospective exploration (E-01 exploratory), not a registered prospective test. It tests a mechanical proxy of the lean rules, not the analyst's judgment. The specification, scripts, printed outputs and input hashes are in the appendix, `claude/backtest-lean-rules-2026-10-05-appendix.md`. Package home: crypto-desk 12.4.11 `baserates.md` F11–F12 and U5–U7, and `methods.md` S-04.

## What was fixed in advance and what came after
- **Primary specification:** the file was written at 00:42:10Z Oct 6, before the first script (00:42:32Z) and before any result. Its own header says "~00:50Z"; that is wrong.
- **Data:**
  - Binance BTCUSDT perp 4H klines, 14,814 bars, Jan 2020 – Oct 4 2026, from `jbm_archive`.
  - Binance OI archive metrics: 727 `ok` days, Oct 2024 – Oct 2026; 7 `incomplete` days excluded.
  - Binance funding history.
- **Lean proxy:** a close beyond the prior 24 bars' high or low.
- **S-04 gate:** defer if that bar moved more than T in the lean direction. Convert at the next close if price is still beyond the level and that bar moved ≤ T. Carry once more; withdraw after two carries; cancel if back inside.
- **Variants:**
  - V0: raw break.
  - V1: plus S-04.
  - V2: plus Binance OI rising over the bar.
  - V3: plus funding not crowded.
- **Primary parameters:** T = 0.353% of price (300 points at 85,000); 24h horizon; 10 bp round trip; drift-adjusted mean; 95% interval by weekly block bootstrap.
- **Secondary, declared in advance:** N 24/42; T fixed or 0.5 × trailing 42-bar σ; 4h/24h; last 6 months. That gives 36 distinct cells (48 printed, because V0 does not depend on T). Multiplicity applies.
- **Post hoc (run after the results):**
  - continuation after bars above T compared with bars at or below T;
  - the paired deferral test;
  - the Parkinson, 1σ and 2σ thresholds;
  - the breakout-bar binding share;
  - the naive band rates (U5, U6);
  - the funding distribution (U7).

## Results

**Primary (24h, after 10 bp, drift-adjusted, 95% interval)**

| sample | variant | leans | hit | drift-adj bp |
|---|---|---|---|---|
| Mar 2020 – Oct 2026 | V0 | 1,089 | 48.6% | +5.6 [−23, +32] |
| Mar 2020 – Oct 2026 | V1 | 514 | 44.0% | −23.1 [−50, +4] |
| last 24 months | V0 | 363 | 49.6% | −19.3 [−52, +14] |
| last 24 months | V1 | 170 | 45.9% | −26.1 [−65, +13] |
| last 24 months | V2 = V3 | 84 | 41.7% | −23.3 [−71, +28] |

- No variant beats zero after costs.
- The funding clause never bound, so V3 = V2.
- In the secondary grid, no cell is positive with an interval that excludes zero. Every interval that excludes zero is negative; these are the 4h cells over the last 24 months, where costs dominate.
- The six-month V1 24h cells are positive (+27 to +75 bp drift-adjusted) on 26–37 non-overlapping leans. Their intervals run from about −64 to +216: noise.

**Deferral against entering at once** (post hoc, paired on the same breakout signals, 24h, after 10 bp; deferral minus immediate)
- 0.353% threshold:
  - full sample: −13.8 bp [−35, +7]
  - last 24 months: +2.3 [−22, +26]
- 1σ and 2σ thresholds: all intervals include zero.
- At those larger thresholds the dropped signals had been losers when entered at once (−36 bp, n=234; −110 bp, n=65; full sample). The later entry of the rest gave the saving back.
- **Reading:** no measured difference either way. The earlier "deferral made it worse" compared different signal sets and is withdrawn.

**S-04's premise: reversal after outsized bars** (post hoc, against bars at or below T; 40 intervals, so multiplicity applies)
- At 0.353%, full sample, next 4h:
  - continuation −2.3 points [−3.7, −0.7]
  - mean +0.6 bp [−3.1, +4.5]
  - nothing at 24h
- Last 24 months: nothing detected at any threshold. The intervals still include the full-sample effect.
- After bars beyond 2σ, full sample, 4h: more continuation, not less (+4.1 points [+0.8, +7.1]). Over 24 months the same figure is +0.5 [−5.8, +6.6].

**How often the threshold binds**
- 0.353% of price is exceeded by 59% of 4H bars over the full sample and 55% over the last 24 months.
- It is exceeded by 97% and 94% of breakout bars in those samples.
- A literal 300 points binds on 39% and 56% of bars.

**Naive bands** (next 4H close within the band)
- ±0.90% band: 71.3% full sample, 78.2% last 24 months, 83.4% last 6 months.
- ±1σ band (Parkinson 6-bar through the issue bar): 76.4%, 74.7%, 74.8%.
- The thread's containment calls went 21 of 27 (78%; Wilson 59–89%, treating overlapping calls as independent). They were unregistered. That is indistinguishable from the naive rate.

**Funding** (Binance BTCUSDT, 2,196 settlements, Oct 2024 – Oct 2026)
- 97.4% were at or below +1 bp: exactly +1.000 on 18.4%, between −1 and +1 on 78.6%.
- 2.6% were above +1 bp; 0.4% were below −1 bp.

## Reading
1. No mechanical version of the lean rules forecasts direction after costs.
2. S-04's deferral showed no measured benefit. Its premise is weak at the threshold in use, and the threshold binds on most bars. That is the basis for making it a disclosure (12.4.11), not a measured harm.
3. The OI confirmation did not improve results, and the funding confirmation was inert.
4. The rule's original cases were leans within minutes of an intrabar move, which 4H bars cannot see. Package test O33 tags and scores those going forward.

## Limits
- This is a proxy, not the live judgmental process.
- Binance-only OI stands in for cross-venue OI, which has no history before Sep 2026.
- The 10 bp cost assumes taker on both sides.
- Overlapping 24h windows are handled by weekly blocks.
- No parameter was tuned to these results.
- The scripts are unversioned thread code.
