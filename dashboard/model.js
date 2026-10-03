// Pure presentation rules. Research calculations and evidence thresholds remain upstream.
export const numeric = value => typeof value === 'number' && Number.isFinite(value);
export function ageLabel(value, now = Date.now()) {
  const timestamp = Date.parse(value);
  if (!Number.isFinite(timestamp)) return 'Unknown';
  const minutes = Math.floor((now - timestamp) / 60000);
  if (minutes < 0) return 'Clock mismatch';
  if (minutes < 1) return '<1m ago';
  if (minutes < 60) return `${minutes}m ago`;
  if (minutes < 1440) return `${Math.floor(minutes / 60)}h ${minutes % 60}m ago`;
  return `${Math.floor(minutes / 1440)}d ago`;
}
export function freshness(value, hours, now = Date.now()) {
  const stamp = Date.parse(value);
  if (!Number.isFinite(stamp)) return 'unknown';
  if (stamp > now + 60000) return 'clock mismatch';
  return now - stamp >= hours * 3600000 ? 'stale' : 'within cadence';
}

// Report clock contract (repo 2.23; canonical text: skill runbook.md section D2). Every clock is aged on the
// viewer's clock and judged on its own: a fresh build or a rescore never makes an old observation fresh.
// Stale = older than twice the producer's interval (stream reports: 4h workflow; research lab: 6h). RC1D keeps
// its own exact report/row/window expiry (forecastState, reportExpiry), not these rules.
export const CLOCKS = {
  stream_report_hours: 8,          // companion, PS1, feasibility: generated_utc
  companion_observation_hours: 12, // latest included outcome-window end: 8h + one 4h decision spacing
  ps1_observation_hours: 8,        // latest decision close or quote receipt while the stream is collecting
  research_observation_hours: 12,  // evidence-card cutoff and the coverage report: two 6h lab runs
};
export function clockState(value, hours, now = Date.now(), whenNull = 'unknown') {
  if (value == null) return whenNull;
  return freshness(value, hours, now);
}
export function companionClocks(c, now = Date.now()) {
  const paired = Object.values(c?.evaluation?.horizons || {}).some(h => numeric(h?.paired) && h.paired > 0);
  return [
    {label: 'Report generated', value: c?.generated_utc, state: clockState(c?.generated_utc, CLOCKS.stream_report_hours, now)},
    {label: 'Last scored', value: c?.processed_utc, state: c?.processed_utc ? 'processing time' : 'none yet'},
    {label: 'Observation cutoff', value: c?.source_cutoff_utc,
     state: clockState(c?.source_cutoff_utc, CLOCKS.companion_observation_hours, now,
                       paired ? 'unknown' : 'no included pair yet')},
  ];
}
export function paperClocks(p, now = Date.now()) {
  const life = p?.lifecycle?.state;
  const collecting = life === 'active' || (life === 'paused' && p?.lifecycle?.paused_by === 'job');
  let observed;
  if (p?.source_cutoff_utc == null) observed = p?.launch ? 'unknown' : 'pre-launch: none expected';
  else if (!p?.launch || collecting) observed = clockState(p.source_cutoff_utc, CLOCKS.ps1_observation_hours, now);
  else observed = `not collecting (${life}${p?.lifecycle?.paused_by ? ' by ' + p.lifecycle.paused_by : ''})`;
  return [
    {label: 'Report generated', value: p?.generated_utc, state: clockState(p?.generated_utc, CLOCKS.stream_report_hours, now)},
    {label: 'Last processed', value: p?.processed_utc, state: p?.processed_utc ? 'processing time' : 'none yet'},
    {label: 'Observation cutoff', value: p?.source_cutoff_utc, state: observed},
  ];
}

// The B2/B1 paired row for one horizon. Withheld and unavailable states are carried, never turned into zeros.
export function pairedRow(horizon, companion) {
  const e = companion?.evaluation?.horizons?.[horizon];
  const r = e?.B2_vs_B1;
  const excluded = numeric(e?.excluded_integrity) ? e.excluded_integrity : null;
  if (!e || !r) return {horizon, n: null, maeFirst: null, maeSecond: null, diff: null, excluded,
                        uncertainty: 'No scored pair', state: 'unavailable'};
  if (r.withheld) return {horizon, n: numeric(e.paired) ? e.paired : null, maeFirst: null, maeSecond: null, diff: null,
                          excluded, uncertainty: 'Withheld: integrity failure in this horizon', state: 'withheld'};
  const n = numeric(r.n) ? r.n : null;
  let uncertainty;
  if (!n) uncertainty = 'No scored pair';
  else if (Array.isArray(r.diff_mean_ci95) && r.diff_mean_ci95.length === 2 && r.diff_mean_ci95.every(numeric))
    uncertainty = `95% interval ${r.diff_mean_ci95[0]} to ${r.diff_mean_ci95[1]}`;
  else uncertainty = r.uncertainty || 'Interval unavailable (no reason supplied)';
  return {horizon, n, maeFirst: r.effect?.mae_first ?? null, maeSecond: r.effect?.mae_second ?? null,
          diff: numeric(r.diff_mean) ? r.diff_mean : null, excluded, uncertainty, state: n ? 'reported' : 'no pair'};
}

// Structural validation of every field the renderers consume, before a candidate replaces the last good snapshot.
export function validateSnapshot(s) {
  const problems = [];
  const need = (ok, what) => { if (!ok) problems.push(what); };
  const obj = v => v !== null && typeof v === 'object' && !Array.isArray(v);
  need(obj(s), 'snapshot is not an object');
  if (!obj(s)) return problems;
  need(s.schema === 'jbm-dashboard/2', `unsupported schema ${s.schema}`);
  need(obj(s.health) && Array.isArray(s.health.sources) && Array.isArray(s.health.datasets) && Array.isArray(s.health.alerts),
       'health.sources/datasets/alerts');
  const list = v => Array.isArray(v) ? v : [];
  need(list(s.health?.sources).every(x => obj(x) && typeof x.name === 'string' && numeric(x.ok) && numeric(x.observed)),
       'health.sources rows');
  need(obj(s.research) && Array.isArray(s.research.designs), 'research.designs must be a list');
  need(list(s.research?.designs).every(d => obj(d) && typeof d.design === 'string'), 'research.designs rows');
  need(obj(s.range) && obj(s.range.current) && obj(s.range.evaluation), 'range.current/evaluation');
  need(obj(s.market) && Array.isArray(s.market.bars), 'market.bars');
  need(obj(s.paper) && typeof s.paper.status === 'string' && obj(s.paper.integrity) && obj(s.paper.lifecycle),
       'paper.status/integrity/lifecycle');
  need(obj(s.companion) && obj(s.companion.evaluation) && obj(s.companion.evaluation.horizons) && obj(s.companion.integrity),
       'companion.evaluation.horizons/integrity');
  need(obj(s.feasibility), 'feasibility');
  need(obj(s.sources), 'sources');
  return problems;
}

// Stage a candidate: validate, then render every view with it; only a candidate that passes both is committed.
// renderAll(candidate) must throw on any failure and must not mutate the current state.
export function stage(current, candidate, renderAll) {
  const problems = validateSnapshot(candidate);
  if (problems.length) return {data: current, error: `Invalid snapshot: ${problems.slice(0, 3).join('; ')}`};
  try { renderAll(candidate); } catch (err) { return {data: current, error: `Snapshot failed to render: ${err.message}`}; }
  return {data: candidate, error: null};
}

export function forecastState(row, report, now = Date.now()) {
  if (!row) return 'unavailable';
  if (row.state !== 'valid-current') return row.state || 'unavailable';
  const expiry = Date.parse(report?.status_expires_utc);
  const until = Date.parse(row.valid_until_utc);
  const start = Date.parse(row.start_utc);
  const end = Date.parse(row.end_utc);
  const generated = Date.parse(report?.generated_utc);
  if (![expiry, until, start, end, generated].every(Number.isFinite)) return 'unverified';
  if (now < generated || now < start) return 'not current';
  return now >= Math.min(expiry, until, end) ? 'expired' : 'valid-current';
}
export function reportExpiry(report, now = Date.now()) {
  const expiry = Date.parse(report?.status_expires_utc);
  if (!Number.isFinite(expiry)) return 'unknown';
  return now >= expiry ? 'expired' : 'within expiry';
}
export function csv(rows) {
  return rows.map(row => row.map(value => {
    let text = value == null ? '' : String(value);
    if (/^[=+@\-\t\r]/.test(text)) text = "'" + text;
    return '"' + text.replaceAll('"', '""') + '"';
  }).join(',')).join('\r\n');
}
export function escapeHTML(value) {
  return String(value ?? '—').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
