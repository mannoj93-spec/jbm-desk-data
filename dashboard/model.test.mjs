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
import { validBar, chartPoints, schemaClass, opsRows } from './model.js';
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
 assert.equal(old['Collector service (automated)'].state, 'unknown');           // a pre-2.25 report has no service block
 const ops = {...base, source: {last_scheduled_utc: '2026-10-04T11:07:58Z', stale_limit_min: 90,
   service: {last_automated_utc: '2026-10-04T19:52:40Z', last_source: 'recovery', gaps: []},
   coverage_24h: {expected_slots: 96, intervals: 95, intervals_with_automated_run: 40, longest_automated_gap_min: 406.5,
                  runs_by_source: {'native-schedule': 5, recovery: 35, human: 1}}}};
 const by = Object.fromEntries(opsRows(ops, Date.parse('2026-10-04T20:05:00Z')).map(r => [r.area, r]));
 assert.equal(by['Collector schedule'].state, 'stale');                         // native silence stays visible
 assert.equal(by['Collector service (automated)'].state, 'within cadence');
 assert.match(by['Collection, 24 h to report'].detail, /recovery 35/);
 assert.equal(by['Collection, 24 h to report'].state, '40 of 95 intervals');
});

test('a monitor that ran on time and failed is a heartbeat with a detected problem (repo 2.26)', () => {
 const ops = {generated_utc: '2026-10-05T07:00:00Z', clock: 'runner', decisions: {}, scoring_backlog: {}, source: {},
   monitors: {workflows: {'range-monitor.yml': {last_completed_utc: '2026-10-05T06:01:40Z', last_result: 'failure',
     last_success_utc: '2026-10-04T18:00:00Z', stale_after_min: 510}}}};
 const by = Object.fromEntries(opsRows(ops, Date.parse('2026-10-05T07:05:00Z')).map(r => [r.area, r]));
 assert.equal(by['Monitor range-monitor.yml'].state, 'ran; detected a problem');
 assert.match(by['Monitor range-monitor.yml'].detail, /last success 2026-10-04T18:00:00Z/);
});
