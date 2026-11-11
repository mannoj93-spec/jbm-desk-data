# Proposal: a multiplicity rule for the concurrently registered market-study primaries

**Status: proposed, not adopted.** Drafted 2026-11-11 for the operator's decision. Nothing here changes a protocol,
a registration, a clock or a stored record, and no review may cite it until it is adopted by a dated revision.

## The gap

Five fixed primaries are registered and running, each with its own interval-based review and none with a rule for
the others:

| study | primary | first review |
|---|---|---|
| turnover (v1) | Sharpe(B2_10) minus Sharpe(B2_05), stressed costs | 365 days and 20 blocks; support needs the 90% block interval above zero |
| range calibration (v1) | paired 80% interval score, calibrated minus B2 | 180 days, 10 blocks |
| state (v1) | Brier(full) minus Brier(price/vol baseline) | 180 days, 10 blocks |
| paired (v1) | 60m Brier(combined) minus Brier(perp) | 180 days, 10 blocks |
| state (v2) | the same primary as state v1, corrected depth selection | 180 days from its own clock (registered 2026-10-26), 10 blocks |

A 90% interval above zero is a one-sided 5% test. If four unrelated primaries are each read that way and none has
an effect, the chance that at least one looks supported is 1 - 0.95^4 = 18.5%; with five, 22.6%. State v1 and v2
also test one hypothesis twice, and choosing between them after the results are visible is a second way to manufacture
support. The protocols say "no optional stopping or automated supported status" but nothing about the family.

## Proposed rule

1. **The family** is the set of fixed primaries registered before any review interval exists: turnover, range
   calibration, state, paired. Four hypotheses. The options pilots carry no inference and are outside it.
2. **State is one hypothesis, read from v2.** State v2 is the designated primary because it is the prospectively
   registered correction of the same design. State v1 remains a retained sensitivity record: it is reported beside
   v2, and a result seen only in v1 supports nothing.
3. **Each hypothesis is read at one quarter of the error rate.** "Support" requires the 97.5% moving-block
   interval (one-sided 1.25%) to lie on the favourable side of zero, in place of the 90% interval, with every other
   registered condition unchanged (minimum days and blocks, coverage, the turnover risk and drawdown conditions).
   This is a Bonferroni split. It is chosen over a step-down rule because the reviews fall on different dates and a
   split is valid whatever their order and whatever the dependence between studies.
4. **The interval is computed once per review**, by the registered bootstrap (2,000 draws, seed 20261024), at the
   registered review date. No interim interval is computed or displayed for a study below its minimum blocks, as now.

## What this costs and what it does not settle

- Power: a true effect must clear a wider interval. With 2,000 draws the 1.25% tail rests on 25 draws, so the bound
  itself is coarse; that precision is stated with any result.
- It covers these four hypotheses only. The research lab keeps its own family-wise variant count, and the desk's
  registered tests (package `queue.md`) are a third family. Nothing here controls error across the three.
- It does not decide whether state v1 keeps running (a separate operator decision; the frozen v1 code can pause only
  all of v1).

## To adopt

A dated revision that (a) records the operator's approval, (b) adds the rule to `docs/MARKET_STUDIES.md` as the
review procedure, and (c) leaves every `protocol.json` untouched - the rule governs how a review is read, not what
a study records. It must land before the earliest 180-day review floor, about 2027-04-22 (v1's registration on
2026-10-24 plus 180 days; the study reports carry the exact dates).
