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
 const c = {generated_utc: '2026-10-03T11:50:00Z', processed_utc: '2026-10-03T11:49:00Z', source_cutoff_utc: '2026-10-02T20:00:00Z',
            evaluation: {horizons: {'4h': {paired: 3}}}};
 const [gen, , obs] = companionClocks(c, now);
 assert.equal(gen.state, 'within cadence');
 assert.equal(obs.state, 'stale');
 assert.equal(companionClocks({...c, source_cutoff_utc: null, evaluation: {horizons: {'4h': {paired: 0}}}}, now)[2].state, 'no included pair yet');
 assert.equal(CLOCKS.stream_report_hours, 8);
});
test('PS1 pre-launch null cutoff and paused streams are not collection failures', () => {
 const now = Date.parse('2026-10-03T12:00:00Z');
 assert.equal(paperClocks({generated_utc: '2026-10-03T11:00:00Z', source_cutoff_utc: null, launch: null, lifecycle: {state: 'approved'}}, now)[2].state, 'pre-launch: none expected');
 assert.equal(paperClocks({source_cutoff_utc: '2026-10-01T00:00:00Z', launch: {}, lifecycle: {state: 'paused', paused_by: 'operator'}}, now)[2].state, 'not collecting (paused by operator)');
 assert.equal(paperClocks({source_cutoff_utc: '2026-10-01T00:00:00Z', launch: {}, lifecycle: {state: 'active'}}, now)[2].state, 'stale');
 assert.equal(paperClocks({source_cutoff_utc: null, launch: {}, lifecycle: {state: 'active'}}, now)[2].state, 'unknown');
});
test('RC1D report expiry is exact', () => {
 assert.equal(reportExpiry({status_expires_utc: '2026-10-03T00:20:00Z'}, Date.parse('2026-10-03T00:19:59Z')), 'within expiry');
 assert.equal(reportExpiry({status_expires_utc: '2026-10-03T00:20:00Z'}, Date.parse('2026-10-03T00:20:00Z')), 'expired');
 assert.equal(reportExpiry({}), 'unknown');
});
const good = () => ({schema: 'jbm-dashboard/2', health: {sources: [{name: 'a', ok: 1, observed: 1}], datasets: [], alerts: []},
  research: {designs: [{design: 'A1'}]}, range: {current: {}, evaluation: {}}, market: {bars: []},
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
