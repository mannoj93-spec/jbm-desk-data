# Validation record — research-integrity revision 2.9 (lab-2.1)

Validated 2026-09-23 with Python 3.11 (container); GitHub workflows select Python 3.12. Tables
below the 2.9 block are the record of earlier revisions and are kept as they were.

| Check (2.9) | Result |
|---|---|
| Default branch before the work | `af73759` (and `4b49827` at deployment prep); since the reviewed `c9fff86` only automated data commits; code identical to the review |
| Reproductions on `c9fff86` (`scripts/repro_integrity_29.py old-tree`) | #1 n=100 look `retired` with the first 100 observations, `supported` after 100 later ones were appended (and `supported` in a single run with all 200); #2 the 09:45 option event (inputs 09:47) present with small, absent with large funding first observed at 10:00, in both the quote-qualified and mark-only variants; #3 mean test residuals at 30 / 60 / 240 min +47.7 / 0.0 / +33.4 bp with horizon-specific outcomes (60-minute model everywhere), and the 480-minute baseline 100% "identifiable" with no complete 480-minute control label |
| Same reproductions on 2.9 | #1 `retired` / `retired` / `retired`, checkpoint 1 recorded (n 100, p_long 0.0, cutoff before the later observations); #2 identical event (group, direction, features, t_inputs 09:47) for both funding values and both policies; #3 0.0 / 0.0 / 0.0 bp, 480-minute share 0.0 and comparison withheld |
| New tests against `c9fff86` (`test_rev29.py` copied into the old tree) | 15 of 28 fail or error there (10 failures, 5 errors: missing interfaces such as `collapse_as_known` or the `design` argument), 9 skip (new checkpoint/per-horizon interfaces absent), 4 pass on both (options guards: delayed current snapshot, later arrivals, missing funding, later use of a value). Every test passes on 2.9 |
| Offline regression suite | 266 passed (238 kept; 28 new in `test_rev29.py`), about 30 s; 19 local full-suite runs: 17 clean, 2 failed once each in the unchanged collector timing test `test_rev26 ... test_one_hung_venue_cannot_cost_every_venue_its_snapshot` (series stage 243.6 s against a 241 s bound); that test passed 12/12 alone on 2.8 and on 41 hash seeds, the reviewed tree passed 8/8 full-suite runs, and collector.py and test_rev26.py are byte-identical to 2.8, so the lab change is not implicated but the intermittency is recorded rather than dismissed. Numerical fixtures 25 passed |
| Adversarial review of the first draft (separate agent, read-only, scripts under a scratch directory) | 7 findings, all fixed with regressions (CHANGELOG 2.9, "Hardening"): episode collapse across freeze times, options controls moved by late snapshots, frozen-decision merge order, funding and spread availability in labels, record-level verification, registration-bounded multiplicity, concurrent checkpoint writes. Checked and found sound: the binary search for the cutoff (greedy thinning of equal-length intervals keeps the maximum, fuzzed on 3000 random sets), JSON float round trip and bootstrap determinism, supported-status gating, per-horizon cache keys and training rows |
| Byte preservation and idempotency (scratch copy of the repository at `4b49827`, lab run with `--now` and writes, then a second run at the same cutoff) | First run: no file under `data/`, `registry/`, `research/evidence/cards`, `research/experiments`, `research/ledger`, `research/evidence/v2/*@<lab-2.0 version>.json` or `state/lab_registered.json` changed; `research/v2/experiments` and `research/v2/ledger` append-only; 8 new cards; `state/lab_registrations.json` kept all 8 lab-2.0 entries unchanged and added 8. Second run: only the run counter in `state/lab_run_state.json` changed. Checkpoint files are appended once per look (tested: repeat runs leave every `.jsonl` byte-identical; a later look only appends) |
| Version migration | Every design gets a new `ev-...` version under lab-2.1 (scratch run: A1 `ev-807f3c751b86`, B1 `ev-7e4d0eed56aa`, C1 `ev-d9cbcefb4a31`, D1 `ev-dbc5dbdb0de9`, E1 `ev-839d57e8ed3e`, F1 `ev-7b9b890aebaf`, G1 `ev-0a974aa122b5`, H1 `ev-8120dafd44e3`; ids depend only on design + semantic code); the lab-2.0 versions are indexed `retired (superseded)` with `superseded_by`; no lab-2.0 version had frozen evaluation decisions or checkpoints to carry over |
| Research lab on current data | 8 designs in 2.5 s (writes, scratch copy); with a 5-day reconstruction, 21 s (read-only) |
| Checksums | `SHA256SUMS` regenerated from its own file list plus the two new files: 104 entries (was 102), all match |

| Check (2.8) | Result |
|---|---|
| Default branch before the work | `9a47d65`; since the reviewed `900d0b1` only automated data commits; code identical to the review |
| Reproductions on `900d0b1` (`scripts/repro_integrity.py old-tree`) | #2 same-bar entries counted {30m: 2, 60m: 2, 240m: 1, 480m: 1}; #3 module G event 48.0 min before its delayed input; #5 transition labelled `confirmed`; #6 exact 3 events + 1 control, jittered 0 + 0; #7 all quotes stale: event unchanged (`bearish_disagreement`), only counters moved |
| Same reproductions on 2.8 | #2 {1, 1, 1, 1}; #3 event 1.0 min after the input (input + assumed processing); #5 `none_observed`; #6 exact and jittered both 3 + 1; #7 event regrouped `bearish_disagreement_ineligible` with reason "stale", surface value unchanged |
| New tests against `900d0b1` | `test_integrity.py` cannot import there (`lab.asof` and the other lab-2.0 modules do not exist); the version-independent script above is the per-finding evidence |
| Offline regression suite | 238 passed (200 kept; 38 new), about 25 s, 3 consecutive runs, no flakes; numerical fixtures 25 passed |
| Earlier reliability cases | `test_stalled_venue_leaves_every_other_book_collected`, `test_one_hung_venue_cannot_cost_every_venue_its_snapshot` and `test_complete_snapshot_loss_is_critical_and_partial_loss_is_not` pass unchanged |
| Byte preservation and idempotency (scratch copy of live data, two runs at one cutoff) | First run creates only `research/v2`, `research/evidence/v2`, `research/evidence/index.json`, `state/lab_registrations.json`, `state/lab_run_state.json` and the two research reports; no data, legacy research or lab-1.0 state byte changed. Second run at the same cutoff adds no rows; only the commit hash in reports/cards and the run counter change |
| Version migration | Each design registered under a new `ev-...` version; `state/lab_registered.json` and the lab-1.0 cards untouched and indexed as legacy; a docstring/comment edit, a README edit and a data file leave versions unchanged; a detector constant, a cost value, or (for module B) the HL sampling policy start a new version (tested) |
| Research lab on current data (read-only) | 8 designs run in 2 s; with the 60-day reconstruction of A and G, 2 min 17 s (limit 30 min) |
| Coverage report refresh | `report.py --coverage-only` writes only `reports/latest.md` (report 2.5 with generation time, input cutoff, versions and 9 dataset freshness rows); no registry or scoring files touched |
| Deployment (GitHub, 2026-09-23, web upload to branch `mannoj93-spec-patch-1`, PR #5, merge commit `87268f3`) | 8 branch commits (`61e9131` ... `5d977b3`) verified byte-for-byte; main then matched all 102 checksum entries. Intermediate branch runs of the regression workflow failed as expected (tests uploaded before their modules and scripts); the branch head (`5d977b3`, push and pull_request) and main after the merge (`87268f3`) passed. Data commits between the base and the merge were preserved by the merge (139 inserted lines, 0 deleted, in data/) |
| Research lab on GitHub (run 35927653635, dispatch with a 60-day reconstruction) | Success in 3 min 31 s; committed as `5669cbd`: 8 versioned cards, index with the lab-1.0 cards marked legacy, 8 experiment rows, 28 ledger rows, 8 registrations, `reports/latest.md` refreshed to report 2.5 (input cutoff 22:17Z, lab-2.0 last run 22:19Z). No lab-1.0 file changed. Reconstruction A1: 13 firings, 7 episodes, 6 retained in 6 blocks (lab-1.0 reported "6 independent"); G1: 51 firings, 48 episodes, 44 retained in 33 blocks |
| First scheduled collection after the merge (22:22 slot, started 22:26Z, committed as `e078bb3`) | `collector-2.7`, 17/17 books, options and Hyperliquid complete, 279 requests, 0 rate-limited, 0 failed, 103 s; watchdog exit 0 "collector healthy" |

## Revision 2.7

| Check (2.7) | Result |
|---|---|
| Offline regression tests (`regression/`) | 200 passed (124 from 2.6.1; new: 20 `test_rev27.py`, 30 `test_lab.py`, 26 `test_stream.py`), about 20 s; numerical fixtures 25 passed |
| Schema compatibility | Option schema-1 fields and the v1 BTC position record still written; `OPTIONS_SCHEMA=1` and `HL_SAMPLING_POLICY=v1` restore the 2.6 code paths (tested) |
| Live collector run under the final 2.7 code, scratch copy (20:13Z) | 17/17 books; options complete (851 with OI, 123 zero-OI listed, panel 12/12, metadata refreshed); Hyperliquid 190 accounts (29 ok_btc, 138 ok_flat, 23 ok_other, 0 failed), fixed cohort of 100 selected, enrichment: 1 ledger + 9 TWAP checks; 1,500 bars per price series on first run, 0 missing minutes; 1 insurance row; 298 requests, 0 rate-limited, 0 failed; 170 s (series 41, liquidations 11, snapshot 18, forward 94, enrichment 7) of the 600 s budget. An earlier 2.7 build (19:23Z) gave the same counts in 173 s |
| Report and watchdog on that copy | Report 2.4 section 3c lists all new datasets; watchdog exit 0 (healthy), warning that the newest run was local |
| Record sizes per run (live) | options 36 KB (8 KB gz), HL accounts 36 KB (13 KB gz), v1 BTC map 5 KB, enrichment 2 KB, price batch ~1.4 KB per series; hourly quote record 68 KB (22 KB gz) |
| API behaviour verified live | Hyperliquid `twapHistory` answers (empty list for sampled accounts), fills carry `twapId`; OKX insurance fund `type=regular_update` is rejected (HTTP 400), `limit=1` used instead; Bybit REST 403 from the container but WebSocket reachable; Deribit summaries return null bid/ask with no resting order |
| Research lab on the live copy, prospective | All 8 designs ran in 1 s; states: A, B, C, D, F, G, H insufficient_data with the reason named; E unavailable (no streaming data) |
| Research lab, 60-day reconstruction (Binance 1-minute history, 4 series) | Fetch 170 s, compute ~65 s; A1: 6 weak vs 93 strong independent episodes over 41 days (exploratory only); G1: 44 test vs 1,437 control-time references; both flagged with contradictory evidence (chronological halves disagree in a variant) |
| Streaming service, live smoke tests (90 s, 2 x 45 s, 120 s) | 3 venues connected, 0 reconnects; Bybit 3,073 consecutive deltas with no sequence gap; restart gaps written; heartbeat check ok; 120 s: 2.3 s CPU, 29 MB max RSS, 373 KB written (351 KB raw, 21 KB derived) |
| S3 SigV4 signer | Matches botocore 1.35.0 on 4 fixed vectors (PUT/HEAD, two endpoints) |
| Skill evaluation on synthetic fixtures | Detects the dropped decision-status line and one overclaim; negated wording ("not yet supported") not flagged; refuses an output path inside the repository; live mode without a key reports "not run" |
| Deployment (GitHub, 2026-09-23, via the web upload page; no local git credentials) | Collector code `43b28c7` (20:20Z), fixtures `240a27f`, lab `631cfa1`, modules `e9e3928`, designs `7105a5d`, skill-eval fixtures `07c8139` `a0622f8` `ccd0d08`, stream `a9b76aa`, stream deploy files `fa3bb59`, tests `53f0381`, research workflow `d155cba`. Every file verified byte-for-byte against the local tree after fetch. Regression and numerical fixtures green on every push, including `53f0381` (the 200-test suite on GitHub's Python 3.12) |
| First scheduled 2.7 collection on GitHub (run 35916223074, 20:22 slot, started 20:28:50Z) | `collector-2.7`, `trigger: schedule`; 17/17 books; options complete (851 with OI, 123 zero-OI, panel 12/12); Hyperliquid 190 accounts (29 ok_btc, 138 ok_flat, 23 ok_other, 0 failed), fixed cohort of 100 selected and frozen (`state/hl_cohort_fixed_v2.json`, members sha256 `4e8dd2cf...`), 10 enrichment requests; 1,500 bars per price series; 1 insurance row; 297 requests, 0 rate-limited, 0 errors; 96.5 s (series 35, liquidations 6, snapshot 8, forward 44, enrichment 4); committed as `e5fd091` with every new dataset present |
| Second scheduled 2.7 collection (20:37 slot, committed as `e1de0f6`) | 17/17 books; fixed cohort file byte-identical (not re-selected); a different rotating block (17 ok_btc, 154 ok_flat, 19 ok_other, 0 failed); 13 new bars per price series from the checkpoint, 0 minutes behind; option metadata served from the daily cache; 294 requests, 0 rate-limited; 100 s |
| First research-lab run on GitHub (run 35915877912, dispatch with 60-day reconstruction) | Success in 3 min 6 s end to end; committed as `dbda592` (8 cards, 8 experiment rows, 27 ledger rows, registration stamps). Reconstruction figures identical to the container run (A1: 6 vs 93 episodes, same interval), so the pipeline reproduces across environments |
| Watchdog and report after deployment (on the fetched repository) | Watchdog exit 0: "last scheduled run 20:28Z, collector-2.7"; report 2.4 section 3c lists all new datasets with 0 missing minutes and the lab's first run |

| Check (2.6.1) | Result |
|---|---|
| Offline regression tests (`regression/`) | 124 passed; numerical fixtures 25 passed; 3 consecutive full runs, no flakes |
| Stalled Binance, snapshot stage only, fake clock (the review's case) | 2.6: 5 Binance attempts, 0 other requests, 0/17 books in 120 s. 2.6.1: 1 Binance attempt, 27 other requests, 14/17 books (all non-Binance) in 20 s; 7 requests skipped by the open circuit |
| Same stall inside a full run (`main()`) | 14/17 books; history stopped at its stage limit; forward books attempted |
| New and strengthened tests run against 2.6 (`62e51cc`) | 6 fail or error, as intended |
| Watchdog, 0/17 books with history intact | 2.6: exit 0 "healthy". 2.6.1: exit 2 "no open-interest book collected (0/17)"; 1/17 stays exit 0 with warnings |
| Live routine run under 2.6.1, scratch copy (16:49Z) | 17/17 books, no circuit opened; options and HL complete (7 Hyperliquid 429s on the container IP, retried and recorded); 169 s |

| Check (2.6) | Result |
|---|---|
| Numerical fixture checks (`test_fixtures.py`) | 25 passed |
| Offline regression tests (`regression/`) | 119 passed (50 from 2.1, 37 in `test_rev22.py`, 32 in `test_rev26.py`); 5 consecutive full runs, no flakes |
| `test_rev26.py` run against 2.5.1 code and workflows (`bcccf14`) | 26 of 32 fail or error, as intended; the 6 that pass pin behaviour 2.5.1 already had (native resolution, successful push, cadence arithmetic) |
| Simulated sustained outage of every venue, fake clock, 600 s budget | Run ends at 600.0 s, record written with every failure and `deadline_reached`; 14-minute job leaves 3.0 minutes for persistence and the recovery artifact |
| Simulated stall of one venue (Binance), fake clock | History stops at its 240 s stage limit; snapshot and forward books still run (2.5: history took all 600 s, snapshot skipped) |
| Hung remote, `PERSIST_BUDGET_S=8` | `commit_push.sh` exits 1 in under 20 s with "remote persistence not confirmed" (unbounded: four 30 s pushes plus rebases) |
| Live routine run under 2.6, scratch copy (15:58Z) | 17/17 books; options complete, 847 strikes; HL complete 200/200 in 82 s; 281 requests, 0 rate-limited; 154 s; stages: series 39 s, liquidations 17 s (daily probe), snapshot 15 s, forward 82 s |
| Report and watchdog on the live copy | Hourly period judged against hourly slots (16/16, upper bound); local run excluded from scheduled figures; watchdog healthy, warns that the newest run was local |
| `SHA256SUMS` | Covers code, docs, workflows, `cadence.json` and templates; data, state and reports change every run |
| Deployment (GitHub, 2026-09-23) | Workflows `90fce23` (16:06:13Z, the start of the 15-minute period in `cadence.json`), persistence script `2d12847`, test update `9327896`, code and docs `e3ff93a`, new tests `d98b842`. Tree verified byte-for-byte against `SHA256SUMS` after fetch. Regression and numerical fixtures runs #15–#19 all green, one per push |
| Manual collection on GitHub (run 35887308099, 16:14Z, manual deployment check) | `collector-2.6`, `trigger: workflow_dispatch`; 17/17 books; options and HL complete; 285 requests, 0 rate-limited; 104 s (series 36, liquidations 13 with the daily probe, snapshot 11, forward 44); committed as `8afc250` |
| Manual watchdog on GitHub (run 35887689676, 16:17Z) | Exit 0 "collector healthy" on the last pre-2.6 scheduled run (15:22Z); warning that the newest run was manual and not counted as scheduled; sparse checkout worked |
| Weekly report on GitHub (run 35887705789, 16:17Z) | Report 2.3 committed as `622a65f`: hourly period 16/16 slots (upper bound, trigger unrecorded), 15/15 intervals covered; 15-minute period listed with no slot yet due |
| First scheduled 15-minute run (run 35888255376, 16:22 slot) | Process start 16:22:51Z; `trigger: schedule`, cron recorded; 17/17 books; options and HL complete; no probe (already done that UTC day); 110 s; committed as `feee7c8`. The 16:07 slot, one minute after the workflow commit, did not run |

| Check (2.5.1 and earlier) | Result |
|---|---|
| Numerical fixture checks (`test_fixtures.py`) | 25 passed |
| `SHA256SUMS` | Now covers code, docs, workflows and templates only; data, state and reports change every hour |
| Offline regression tests (`regression/`) | 87 passed (50 from 2.1, 37 in `test_rev22.py`); 5 consecutive full runs, no flakes |
| 2.5.1 late-byte tests run against 2.5 (`9090fba`) | 503 case fails (2.30 s), as intended; 200 case passes on both |
| Live run under 2.5.1, scratch copy | 17/17 books; options and HL complete; no errors; 159 s |
| 2.5 slow-response tests run against 2.4 (`f6fa022`) | 3 trickle tests fail, as intended; prompt response passes on both |
| Local trickling server, 1.2 s budget | Body and headers: 1.20 s, rejected (2.4: 3.45 s and 3.57 s, accepted) |
| Live run under 2.5, scratch copy | 17/17 books; options complete; HL complete 200/200 in 97 s; no errors; 155 s |
| 2.4 outage tests run against 2.3 (`22d2c65`) | 6 of 6 fail or error, as intended |
| Simulated outage, fake clock, 2.4 | Hyperliquid only: 27 requests, 5.0 min. Every venue: 38 requests, 20.0 min, run record written (2.3: 400 requests / 190 min and 576 / 285 min) |
| Live run under 2.4, scratch copy | 17/17 books; options complete 850/850; HL degraded 3/200 on HTTP 429, then complete 200/200 in 93 s with the backoff |
| 2.3 tests run against `ed45dd2` | 9 of 23 in `test_rev22.py` fail or error, as intended |
| The 13 collector, scoring and schema tests run against the 2.1 code | 11 fail or error, as intended; the 2 that pass pin behaviour 2.1 already had |
| Live hourly run, updated collector, scratch copy of the repo | 17/17 books, 849 option strikes with OI, 29 HL BTC positions in top 200, no errors, 147 s |
| Live taker backfill with the pagination fix | 5m: 17 missing rows recovered, 0 gaps; 1h: 1 recovered, 0 gaps |
| Report generation on the live copy | Passed; retired books labelled, not alerted |
| Watchdog against the deployed repository data | "collector healthy" |
| Live hourly run under 2.3, scratch copy (00:45Z) | 17/17 books; options complete, 850/850 rows valid; HL complete, 200/200 accounts, 29 BTC positions; 160 s |
| End-to-end forecast, scratch copy | Registered before start, frozen, scored on 180 live 1m bars, evidence hash verified, idempotent; all seven event types formatted |
| First GitHub backfill under 2.2 (00:01Z, 434 s) | Taker 5m and 1h: 0 gaps in the repository. Found the 4xx-boundary regression fixed in 2.2.1 |

## Measurements behind the changes (live, 2026-09-22 23:30Z)

- Binance `/futures/data`, `endTime = X − 1`: taker returns up to X − 10m; ratio and OI endpoints up
  to X − 5m. The 1h ratio and OI rows equal the 5m rows at the same stamp. Taker 1h `buyVol` at T
  equals the sum of the twelve 5m rows from T (within 0.1%).
- Stored taker gaps: 17 × 5m at 500-row spacing from 2026-08-24 04:50Z; each present at the source.
- OKX liquidation feed: 50 of 2,493 stored timestamps carry two orders; `after = ts + 1` returns the
  boundary pair again, `after = ts` does not.
- OKX account ratio: the row stamped 23:00 was returned at 23:35.
- Bitget BTCUSD coin-margined perpetual: code 40309, "The symbol has been removed".
- BitMEX `/instrument/active`: XBT_USDT Delisted, XBT_USDC Unlisted; no open XBT perpetual.
- Deribit `get_book_summary_by_currency` (BTC options): 972 instruments, 849 with OI; ~30 KB compact.
- Hyperliquid leaderboard: 46,876 rows, 39 MB; `clearinghouseState` ~0.33 s per call.

## Scope limits

2.9: still no design has evaluation observations, so no checkpoint has completed and every status is
exploratory; no skill change is warranted. The checkpoint machinery is exercised on synthetic data
only until the first look completes. The 2.8 dependence-block rule is unchanged: if retained
test and reference intervals overlap continuously across midnight (e.g. hourly test firings with a
60-minute horizon), consecutive days chain into one block, which is conservative and can keep such
a design below its block minimum; at the designs' actual horizons with sparse firings the blocks
are one per day (measured on synthetic 60-day tapes). Funding used in cost attribution of a label is settled funding within the
label window; its availability is now in label_available, but a settlement missing from the
stored series (after the series has moved past it) still contributes zero rather than making the
label incomplete.

2.8: no design has evaluation observations yet; every status is exploratory and no skill change is
warranted. Decisions are as-of replays computed every 6 hours, not live executions. The
multiplicity adjustment and look schedule are conservative house rules, not a formal sequential
test. Streaming (module E) remains inactive.

2.7: no module has an evaluation episode yet; every status is exploratory, and the
reconstruction figures are not evidence of an advantage. The cost model's fee and slippage values
are assumptions (the Binance fee page could not be retrieved automatically). The streaming service
has run only as local smoke tests. Sustained collection of the new datasets is measured by the
weekly report from deployment on.


At the time of writing one scheduled 15-minute run has been observed; sustained scheduled
execution at this cadence (delays, dropped slots, queueing behind intake and report) is measured
by the weekly report from here on, not established by this record. Backlog pruning under an outage
and the watchdog's stale and failing states are verified offline only. Live endpoint behaviour is
dated and can change. This is a reliability revision, not a claim of forecasting skill.

## Reproduce

```sh
python test_fixtures.py
python -m unittest discover -s regression -v
python collector.py          # live; writes into this checkout
python report.py --days 7
```
