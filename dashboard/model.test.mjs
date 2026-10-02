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
