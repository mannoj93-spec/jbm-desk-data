import test from 'node:test';
import assert from 'node:assert/strict';
import { forecastState, freshness, ageLabel, csv, escapeHTML, numeric } from './model.js';
const row = {state:'valid-current',start_utc:'2026-10-02T16:20:00Z',end_utc:'2026-10-02T20:20:00Z',valid_until_utc:'2026-10-02T20:20:00Z'};
const report = {generated_utc:'2026-10-02T17:00:00Z',status_expires_utc:'2026-10-02T18:00:00Z'};
test('forecast expires at the report boundary even if the window remains open', () => {
 assert.equal(forecastState(row,report,Date.parse('2026-10-02T17:59:59Z')),'valid-current');
 assert.equal(forecastState(row,report,Date.parse('2026-10-02T18:00:00Z')),'expired');
});
test('row expiry, window end, and clock mismatch cannot appear current', () => {
 assert.equal(forecastState({...row,valid_until_utc:'2026-10-02T17:30:00Z'},report,Date.parse('2026-10-02T17:30:00Z')),'expired');
 assert.equal(forecastState({...row,end_utc:'2026-10-02T17:30:00Z'},report,Date.parse('2026-10-02T17:30:00Z')),'expired');
 assert.equal(forecastState(row,report,Date.parse('2026-10-02T16:00:00Z')),'not current');
 assert.equal(forecastState(row,{},Date.now()),'unverified');
 assert.equal(forecastState({...row,state:'missing'},report),'missing');
 assert.equal(forecastState(null,report),'unavailable');
});
test('freshness ages against viewer clock rather than build date', () => {
 const now=Date.parse('2026-10-02T18:00:00Z');
 assert.equal(freshness('2026-10-02T12:00:00Z',6,now),'stale');
 assert.equal(freshness('2026-10-02T12:01:00Z',6,now),'within cadence');
 assert.equal(freshness('2026-10-03T12:01:00Z',6,now),'clock mismatch');
 assert.equal(freshness(null,6,now),'unknown');
 assert.equal(ageLabel(null,now),'Unknown');
});
test('missing numeric values remain missing, and export/rendering treat source text as data', () => {
 assert.equal(numeric(null),false);assert.equal(numeric(0),true);assert.equal(numeric(NaN),false);
 assert.equal(csv([['=HYPERLINK("x")',null,0]]),'"\'=HYPERLINK(""x"")","","0"');
 assert.equal(escapeHTML('<script>"x"</script>'),'&lt;script&gt;&quot;x&quot;&lt;/script&gt;');
});

// ---- repo 2.23 ----
import { pairedRow, companionClocks, paperClocks, validateSnapshot, stage, reportExpiry, CLOCKS } from './model.js';
const horizon = (B2_vs_B1, extra = {}) => ({evaluation: {horizons: {'4h': {paired: B2_vs_B1?.n ?? 0, excluded_integrity: 0, B2_vs_B1, ...extra}}}});
test('a valid interval renders even without uncertainty text; reasons and absent pairs stay distinct', () => {
 const ok = pairedRow('4h', horizon({n: 11, diff_mean: -0.01, diff_mean_ci95: [-0.03, 0.002], effect: {mae_first: 0.4, mae_second: 0.41}}));
 assert.equal(ok.uncertainty, '95% interval -0.03 to 0.002');
 assert.equal(ok.n, 11);
 const noBlocks = pairedRow('4h', horizon({n: 11, diff_mean: -0.01, diff_mean_ci95: null, uncertainty: 'unavailable: 0 complete resampling block(s) of 42; needs 10'}));
 assert.match(noBlocks.uncertainty, /^unavailable: 0 complete/);
 assert.equal(pairedRow('4h', horizon({first: 'B2', second: 'B1', n: 0})).uncertainty, 'No scored pair');
 assert.equal(pairedRow('4h', {evaluation: {horizons: {}}}).uncertainty, 'No scored pair');
 assert.equal(pairedRow('4h', horizon({n: 3, diff_mean: 0.1})).uncertainty, 'Interval unavailable (no reason supplied)');
});
test('a withheld horizon carries no figures and no zeros', () => {
 const r = pairedRow('4h', horizon({withheld: 'withheld: integrity failure'}, {paired: 0, excluded_integrity: 1}));
 assert.equal(r.state, 'withheld');
 assert.equal(r.excluded, 1);
 assert.deepEqual([r.maeFirst, r.maeSecond, r.diff], [null, null, null]);
});
test('a fresh report never makes an old observation fresh', () => {
 const now = Date.parse('2026-10-03T12:00:00Z');
 const c = {schema: 'companion-report-3', generated_utc: '2026-10-03T11:50:00Z', processed_utc: '2026-10-03T11:49:00Z', source_cutoff_utc: '2026-10-02T20:00:00Z',
            evaluation: {horizons: {'4h': {paired: 3}}}};
 const [gen, , obs] = companionClocks(c, now);
 assert.equal(gen.state, 'within cadence');
 assert.equal(obs.state, 'stale');
 assert.equal(companionClocks({...c, source_cutoff_utc: null, evaluation: {horizons: {'4h': {paired: 0}}}}, now)[2].state, 'no included pair yet');
 assert.equal(CLOCKS.stream_report_hours, 8);
});
test('PS1 pre-launch null cutoff and paused streams are not collection failures', () => {
 const now = Date.parse('2026-10-03T12:00:00Z');
 assert.equal(paperClocks({schema: 'ps1-report-4', generated_utc: '2026-10-03T11:00:00Z', source_cutoff_utc: null, launch: null, lifecycle: {state: 'approved'}}, now)[2].state, 'pre-launch: none expected');
 assert.equal(paperClocks({schema: 'ps1-report-4', source_cutoff_utc: '2026-10-01T00:00:00Z', launch: {}, lifecycle: {state: 'paused', paused_by: 'operator'}}, now)[2].state, 'not collecting (paused by operator)');
 assert.equal(paperClocks({schema: 'ps1-report-4', source_cutoff_utc: '2026-10-01T00:00:00Z', launch: {}, lifecycle: {state: 'active'}}, now)[2].state, 'stale');
 assert.equal(paperClocks({schema: 'ps1-report-4', source_cutoff_utc: null, launch: {}, lifecycle: {state: 'active'}}, now)[2].state, 'unknown');
});
test('RC1D report expiry is exact', () => {
 assert.equal(reportExpiry({status_expires_utc: '2026-10-03T00:20:00Z'}, Date.parse('2026-10-03T00:19:59Z')), 'within expiry');
 assert.equal(reportExpiry({status_expires_utc: '2026-10-03T00:20:00Z'}, Date.parse('2026-10-03T00:20:00Z')), 'expired');
 assert.equal(reportExpiry({}), 'unknown');
});
const good = () => ({schema: 'jbm-dashboard/2', built_utc: '2026-10-03T00:00:00Z', health: {sources: [{name: 'a', ok: 1, observed: 1}], datasets: [], alerts: []},
  research: {designs: [{design: 'A1'}]}, range: {current: {}, evaluation: {}, generated_utc: '2026-10-03T00:00:00Z', status_expires_utc: null}, market: {bars: []},
  paper: {status: 'not launched', integrity: {}, lifecycle: {}}, companion: {evaluation: {horizons: {}}, integrity: {}},
  feasibility: {}, sources: {}});
test('malformed nested fields are rejected before they replace the last good snapshot', () => {
 assert.deepEqual(validateSnapshot(good()), []);
 const bad = good(); bad.research.designs = {};
 assert.ok(validateSnapshot(bad).length);
 const nan = good(); nan.health.sources[0].ok = null;
 assert.ok(validateSnapshot(nan).some(p => p.includes('health.sources')));
 assert.ok(validateSnapshot(null).length);
 assert.ok(validateSnapshot({...good(), schema: 'jbm-dashboard/1'}).length);
});
test('staging keeps the previous snapshot on validation or render failure and commits only a good one', () => {
 const prev = good();
 const invalid = good(); invalid.research.designs = {};
 let r = stage(prev, invalid, () => {});
 assert.equal(r.data, prev); assert.match(r.error, /Invalid snapshot/);
 r = stage(prev, good(), () => { throw new Error('boom'); });
 assert.equal(r.data, prev); assert.match(r.error, /failed to render: boom/);
 const next = good();
 r = stage(prev, next, () => {});
 assert.equal(r.data, next); assert.equal(r.error, null);
 r = stage(undefined, invalid, () => {});
 assert.equal(r.data, undefined);
});

// ---- repo 2.24 ----
import { validBar, chartPoints, marketSummary, schemaClass, opsRows } from './model.js';
const snap = () => ({schema: 'jbm-dashboard/2', built_utc: '2026-10-03T13:00:00Z', health: {sources: [], datasets: [{name: 'x', observed_utc: null}], alerts: []},
  research: {designs: []}, range: {current: {}, evaluation: {}, generated_utc: '2026-10-03T12:00:00Z', status_expires_utc: '2026-10-03T13:20:00Z'},
  market: {bars: [[0, 1, 2, 0.5, 1.5, 60], [3600000, 1.5, 2, 1, 1.8, 42]], latest: {t: 3600000, close: 1.8}, observed_utc: '2026-10-03T12:59:00+00:00'},
  paper: {status: 'x', integrity: {}, lifecycle: {}}, companion: {evaluation: {horizons: {}}, integrity: {}}, feasibility: {}, sources: {}, ops: null});
test('null, truncated and non-finite chart rows are rejected before commit; empty bars stay legitimate', () => {
 assert.deepEqual(validateSnapshot(snap()), []);
 for (const bad of [[null], [[0, 1, 2]], [[0, 1, 2, 0.5, NaN, 60]], [[0, 1, 2, 0.5, Infinity, 1]], [[0, '1', 2, 0.5, 1, 1]], [[0, 1, 0.5, 2, 1, 1]]]) {
  const s = snap(); s.market.bars = bad;
  assert.ok(validateSnapshot(s).some(p => p.startsWith('market.bars rows')), JSON.stringify(bad));
  assert.equal(stage({good: true}, s, () => {}).data.good, true);
 }
 const empty = snap(); empty.market = {bars: [], latest: null, observed_utc: null};
 assert.deepEqual(validateSnapshot(empty), []);
 assert.deepEqual(chartPoints([], 7), []);
 assert.throws(() => chartPoints([null], 7));
 assert.equal(chartPoints(snap().market.bars, 1).length, 2);
});
test('an empty selected market period retains unavailable values', () => {
 assert.deepEqual(marketSummary([], 1), {high: null, low: null, change: null, count: 0, partial: 0});
});
test('market summary follows the chart period and compares selected hourly closes', () => {
 const hour = 3600000;
 const bars = [[0, 5, 100, 1, 10, 60], [hour, 15, 25, 12, 20, 60], [25 * hour, 22, 35, 18, 30, 60]];
 assert.deepEqual(marketSummary(bars, 1), {high: 35, low: 12, change: 0.5, count: 2, partial: 0});
 assert.deepEqual(marketSummary(bars, 7), {high: 100, low: 1, change: 2, count: 3, partial: 0});
});
test('a zero first close has no percentage change', () => {
 const bars = [[0, 1, 2, 0, 0, 60], [3600000, 1, 3, 1, 2, 60]];
 assert.deepEqual(marketSummary(bars, 1), {high: 3, low: 0, change: null, count: 2, partial: 0});
});
test('market summary counts recorded and partial hours without inventing missing hours', () => {
 const bars = [[0, 10, 14, 9, 12, 12], [5 * 3600000, 12, 13, 8, 9, 60], [9 * 3600000, 9, 10, 6, 6, 59]];
 assert.deepEqual(marketSummary(bars, 1), {high: 14, low: 6, change: -0.5, count: 3, partial: 2});
 assert.throws(() => marketSummary([[0, 10, 14, 9, NaN, 60]], 1), /invalid market bar/);
});
const developments = () => ({
 release: {revision: '2.36', date: '2026-10-19', title: 'Repository revision 2.36', source: 'CHANGELOG.md'},
 catalog: {version: '2.36', as_of_utc: null, dataset_count: 12,
   feature_families: [{id: 'flow', status: 'available'}], source: 'research_tools/catalog.json'},
 protocols: [{id: 'E1', title: 'Streaming pilot', status: 'prepared; not commissioned',
   effective_utc: null, source: 'stream/pilot_e1.json'}],
 acceptance: {checker: 'acceptance-1', verdict: 'not accepted', service_verdict: 'fail', reason: 'Recorded gap',
   window: ['2026-10-17T00:00:00Z', '2026-10-18T00:00:00Z'], evaluated_utc: null,
   source: 'docs/acceptance/results/result-1.json', supplementary: null},
});
test('developments remain optional for legacy snapshots and empty source records remain explicit', () => {
 assert.deepEqual(validateSnapshot(snap()), []);
 assert.deepEqual(validateSnapshot({...snap(), developments: {release: null, catalog: null, protocols: [], acceptance: null}}), []);
 const d = developments();
 assert.deepEqual(validateSnapshot({...snap(), developments: d}), []);
 d.acceptance.supplementary = {...d.acceptance, checker: 'audit-1', source: 'docs/acceptance/results/supplementary-1.json'};
 delete d.acceptance.supplementary.supplementary;
 assert.deepEqual(validateSnapshot({...snap(), developments: d}), []);
});
test('malformed development containers and leaf types are rejected before commit', () => {
 const changes = [
  d => null,
  d => [],
  d => ({...d, release: []}),
  d => ({...d, release: {...d.release, revision: 2.36}}),
  d => ({...d, release: {...d.release, date: 'not a date'}}),
  d => ({...d, catalog: {...d.catalog, dataset_count: -1}}),
  d => ({...d, catalog: {...d.catalog, dataset_count: 1.5}}),
  d => ({...d, catalog: {...d.catalog, feature_families: {}}}),
  d => ({...d, catalog: {...d.catalog, feature_families: [null]}}),
  d => ({...d, catalog: {...d.catalog, as_of_utc: 'yesterday'}}),
  d => ({...d, protocols: {}}),
  d => ({...d, protocols: [null]}),
  d => ({...d, protocols: [{...d.protocols[0], status: null}]}),
  d => ({...d, protocols: [{...d.protocols[0], effective_utc: 'later'}]}),
  d => ({...d, acceptance: []}),
  d => ({...d, acceptance: {...d.acceptance, window: {}}}),
  d => ({...d, acceptance: {...d.acceptance, window: [null, null]}}),
  d => ({...d, acceptance: {...d.acceptance, window: d.acceptance.window.toReversed()}}),
  d => ({...d, acceptance: {...d.acceptance, supplementary: []}}),
  d => ({...d, acceptance: {...d.acceptance, supplementary: {...d.acceptance, window: ['2026-10-16T00:00:00Z', '2026-10-18T00:00:00Z']}}}),
 ];
 const previous = snap();
 for (const change of changes) {
  const candidate = {...snap(), developments: change(developments())};
  assert.ok(validateSnapshot(candidate).some(p => p.startsWith('developments')), JSON.stringify(candidate.developments));
  assert.equal(stage(previous, candidate, () => {}).data, previous);
 }
});
test('timestamps the renderers parse must be parseable or legitimately null', () => {
 const s = snap(); s.range.generated_utc = 'yesterday';
 assert.ok(validateSnapshot(s).some(p => p.includes('timestamps')));
 const d = snap(); d.health.datasets = [{name: 'x', observed_utc: 'not a time'}];
 assert.ok(validateSnapshot(d).some(p => p.includes('health.datasets')));
 const o = snap(); o.ops = {generated_utc: 'x', source: {}, decisions: {}};
 assert.ok(validateSnapshot(o).some(p => p.includes('ops')));
});
test('legacy report schemas keep their meanings; no "none yet" and no new clocks', () => {
 assert.equal(schemaClass('companion', 'companion-report-2'), 'legacy');
 assert.equal(schemaClass('paper', 'ps1-report-4'), 'current');
 const now = Date.parse('2026-10-02T21:30:00Z');
 const c2 = companionClocks({schema: 'companion-report-2', generated_utc: '2026-10-02T21:01:20Z', source_cutoff_utc: '2026-10-02T20:54:43Z'}, now);
 assert.ok(!c2.some(c => c.state === 'none yet'));
 assert.equal(c2[1].state, 'scoring time in this schema, not an observation cutoff');
 assert.match(c2[2].state, /not in this schema/);
 const p3 = paperClocks({schema: 'ps1-report-3', generated_utc: '2026-10-02T21:01:20Z', source_cutoff_utc: null}, now);
 assert.ok(!p3.some(c => c.state === 'none yet' || c.state === 'pre-launch: none expected'));
 assert.match(paperClocks({schema: 'ps1-report-9'}, now)[2].state, /unknown schema/);
});
test('operational health rows are judged on the viewer clock; a missing report is unknown', () => {
 assert.equal(opsRows(null)[0].state, 'unknown');
 const ops = {generated_utc: '2026-10-03T13:27:30Z', clock: 'runner', source: {last_scheduled_utc: '2026-10-03T13:27:02Z', stale_limit_min: 90,
   gaps: [{start_utc: '2026-10-03T11:04:10Z', end_utc: '2026-10-03T13:27:02Z', minutes: 142.86}]},
   decisions: {range: {'2026-10-03T12:00:00Z': 'absent'}, ps1: {'2026-10-03T12:00:00Z': 'missed: no decision record (run absent)'}, ps1_launched: true},
   ps1_coverage: {report_coverage: 1, report_generated_utc: '2026-10-03T09:03:10Z', not_covered: [{decision_utc: '2026-10-03T12:00:00Z', recorded_state: 'missed'}]},
   scoring_backlog: {}, monitors: {workflows: {'watchdog.yml': {last_success_utc: '2026-10-03T11:17:56Z', stale_after_min: 90}}}};
 const fresh = opsRows(ops, Date.parse('2026-10-03T13:40:00Z'));
 const by = Object.fromEntries(fresh.map(r => [r.area, r]));
 assert.equal(by['Health report'].state, 'within cadence');
 assert.equal(by['Recorded silences'].state, '1 in 72 h');                       // a recovered gap stays visible
 assert.equal(by['Range decisions'].state, '1 missed or failed');
 assert.equal(by['PS1 report coverage'].state, '1 due decision(s) not in the report');
 assert.equal(by['Monitor watchdog.yml'].state, 'stale');                         // an old success is not current health
 const later = Object.fromEntries(opsRows(ops, Date.parse('2026-10-03T15:30:00Z')).map(r => [r.area, r]));
 assert.equal(later['Health report'].state, 'stale');
 assert.equal(later['Collector schedule'].state, 'stale');
});
test('service continuity is judged apart from the native schedule (repo 2.25)', () => {
 const base = {generated_utc: '2026-10-04T20:00:00Z', clock: 'runner', decisions: {}, scoring_backlog: {}, monitors: {}};
 const old = Object.fromEntries(opsRows({...base, source: {last_scheduled_utc: '2026-10-04T11:07:58Z'}}, Date.parse('2026-10-04T20:05:00Z')).map(r => [r.area, r]));
 assert.equal(old['Collector service (automated activity)'].state, 'unknown');  // a pre-2.25 report has no service block
 const ops = {...base, source: {last_scheduled_utc: '2026-10-04T11:07:58Z', stale_limit_min: 90,
   service: {last_automated_utc: '2026-10-04T19:52:40Z', last_source: 'recovery', gaps: []},
   coverage_24h: {expected_slots: 96, intervals: 95, intervals_with_automated_run: 40, longest_automated_gap_min: 406.5,
                  runs_by_source: {'native-schedule': 5, recovery: 35, human: 1}}}};
 const by = Object.fromEntries(opsRows(ops, Date.parse('2026-10-04T20:05:00Z')).map(r => [r.area, r]));
 assert.equal(by['Collector schedule'].state, 'stale');                         // native silence stays visible
 assert.equal(by['Collector service (automated activity)'].state, 'within cadence');
 assert.equal(by['Collector data (last persisted critical success)'].state, 'unknown (report before 2.27)');
 assert.match(by['Collection, 24 h to report'].detail, /recovery 35/);
 assert.equal(by['Collection, 24 h to report'].state, '40 of 95 intervals (activity; before 2.27)');
});

test('a failed monitor detected a problem only when its check step ran and reported one (repo 2.26-2.28)', () => {
 const mon = extra => ({generated_utc: '2026-10-05T07:00:00Z', clock: 'runner', decisions: {}, scoring_backlog: {}, source: {},
   monitors: {workflows: {'range-monitor.yml': {last_completed_utc: '2026-10-05T06:01:40Z', last_result: 'failure',
     last_success_utc: '2026-10-04T18:00:00Z', stale_after_min: 510, ...extra}}}});
 const row = extra => Object.fromEntries(opsRows(mon(extra), Date.parse('2026-10-05T07:05:00Z')).map(r => [r.area, r]))['Monitor range-monitor.yml'];
 assert.equal(row({last_executed: true, last_check: 'found a problem', last_execution: 'found a problem: decision missed'}).state,
              'ran its check; found a problem');
 assert.equal(row({last_executed: true, last_check: 'check failed'}).state, 'ran its check; failed without a finding');
 // 2.28 review: setup ran, checkout failed, the check was skipped - 2.27 called this "check executed"
 assert.equal(row({last_executed: false, last_check: 'failed before checking'}).state, 'failed before checking');
 assert.equal(row({last_executed: false, last_check: 'check skipped'}).state, 'check skipped');
 assert.match(row({}).detail, /last success 2026-10-04T18:00:00Z/);
 // the Oct 5 runner outage: the job never received a runner - nothing was checked
 assert.equal(row({last_executed: false, last_check: 'no runner', last_execution: 'no runner'}).state, 'could not execute (no runner)');
 assert.equal(row({last_executed: false, last_execution: 'no runner assigned'}).state, 'could not execute (no runner/steps)');  // 2.27 report
 assert.match(row({last_executed: false, last_execution: 'no runner assigned'}).detail, /no runner assigned/);
 // a 2.27 report's "check executed" counted setup steps: it cannot show the check ran
 assert.equal(row({last_executed: true, last_execution: 'check executed'}).state, 'failed; check evidence unknown (report before 2.28)');
 assert.equal(row({}).state, 'failed; check evidence unknown (report before 2.28)');
});

test('external timer arrivals are shown apart from the native dispatcher and service health (repo 2.28)', () => {
 const ops = {generated_utc: '2026-10-07T18:00:00Z', clock: 'runner', decisions: {}, scoring_backlog: {}, source: {},
   monitors: {workflows: {}, dispatcher_state: 'fresh', external_timer: {window_h: 24, opportunities: 95, on_time: 93,
     delayed: [], absent: ['2026-10-07T15:12:00Z', '2026-10-07T16:57:00Z'], last_arrival_utc: '2026-10-07T17:42:58Z', state: 'gaps'}}};
 const by = Object.fromEntries(opsRows(ops, Date.parse('2026-10-07T18:05:00Z')).map(r => [r.area, r]));
 assert.equal(by['External timer (primary trigger)'].state, '2 absent, 0 delayed in 24 h');
 assert.match(by['External timer (primary trigger)'].detail, /93 of 95 on time.*absent 10-07T15:12, 10-07T16:57 \(arrivals only\)/);
 const none = Object.fromEntries(opsRows({...ops, monitors: {workflows: {}}}, Date.parse('2026-10-07T18:05:00Z')).map(r => [r.area, r]));
 assert.equal(none['External timer (primary trigger)'], undefined);              // pre-2.28 report: no row invented
});

test('data outcome and activity are shown apart; a fresh failure stays visible; stale data stays stale (repo 2.27)', () => {
 const svc = {state: 'failing', data_state: 'fresh', last_success_utc: '2026-10-05T18:27:35Z', last_activity_utc: '2026-10-05T18:42:24Z',
   last_activity_result: 'critical failure', last_automated_utc: '2026-10-05T18:42:24Z', last_source: 'native-schedule', gaps: [],
   acceptance_target: {max_gap_min: 45}};
 const ops = {generated_utc: '2026-10-05T18:44:10Z', clock: 'runner', decisions: {}, scoring_backlog: {}, monitors: {},
   source: {state: 'failing', last_scheduled_utc: '2026-10-05T18:42:24Z', stale_limit_min: 90, service: svc,
     coverage_24h: {expected_slots: 96, intervals: 95, intervals_with_automated_run: 95, intervals_with_successful_automated_run: 90,
                    longest_automated_gap_min: 16, longest_successful_gap_min: 47, automated_critical_failures: 5, runs_by_source: {}}}};
 const at = t => Object.fromEntries(opsRows(ops, Date.parse(t)).map(r => [r.area, r]));
 const fresh = at('2026-10-05T18:50:00Z');
 assert.equal(fresh['Collector schedule'].state, 'failing');                      // 2.26 showed "within cadence"
 assert.equal(fresh['Collector service (automated activity)'].state, 'failing');
 assert.equal(fresh['Collector data (last persisted critical success)'].state, 'within cadence');
 assert.match(fresh['Collector data (last persisted critical success)'].detail, /target met/);
 assert.equal(fresh['Collection, 24 h to report'].state, '90 of 95 intervals');  // successes, not activity
 assert.match(fresh['Collection, 24 h to report'].detail, /longest gap 47 min; 5 critical failure/);
 // 20:00Z, the Oct 5 runner outage: the 18:44 report is still inside its own 90-minute rule, but the newest persisted
 // success (18:27:35 in this fixture) is past the stale limit and the 45-minute acceptance target is breached
 const late = at('2026-10-05T20:00:00Z');
 assert.equal(late['Health report'].state, 'within cadence');
 assert.equal(late['Collector data (last persisted critical success)'].state, 'stale');
 assert.match(late['Collector data (last persisted critical success)'].detail, /target breached/);
 // a fresh dispatch or activity does not make stale data healthy
 const act = {...ops, source: {...ops.source, service: {...svc, state: 'healthy', last_activity_utc: '2026-10-05T19:59:00Z',
   last_success_utc: '2026-10-05T18:00:00Z'}}};
 const by = Object.fromEntries(opsRows(act, Date.parse('2026-10-05T20:00:00Z')).map(r => [r.area, r]));
 assert.equal(by['Collector service (automated activity)'].state, 'within cadence');
 assert.match(by['Collector data (last persisted critical success)'].detail, /target breached/);
});
