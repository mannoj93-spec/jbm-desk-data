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
// Report schemas whose clocks this view understands (repo 2.24). A legacy report keeps its own meanings: no new
// clock is read into it and an absent field is "not in this schema", never "none yet".
export const CLOCK_SCHEMAS = {companion: ['companion-report-3'], paper: ['ps1-report-4']};
const LEGACY = {companion: ['companion-report-2'], paper: ['ps1-report-3']};
export function schemaClass(kind, schema) {
  if (CLOCK_SCHEMAS[kind].includes(schema)) return 'current';
  if (LEGACY[kind].includes(schema)) return 'legacy';
  return 'unknown';
}
function legacyClocks(r, kind, now) {
  const cls = schemaClass(kind, r?.schema);
  const note = cls === 'legacy' ? `not in this schema (${r.schema})` : `unknown schema ${r?.schema ?? '(none)'}`;
  return [
    {label: 'Report generated', value: r?.generated_utc, state: clockState(r?.generated_utc, CLOCKS.stream_report_hours, now)},
    {label: 'Recorded source cutoff', value: r?.source_cutoff_utc,
     state: kind === 'companion' && cls === 'legacy' ? 'scoring time in this schema, not an observation cutoff' : note},
    {label: 'Observation cutoff', value: null, state: note},
  ];
}
export function companionClocks(c, now = Date.now()) {
  if (schemaClass('companion', c?.schema) !== 'current') return legacyClocks(c, 'companion', now);
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
  if (schemaClass('paper', p?.schema) !== 'current') return legacyClocks(p, 'paper', now);
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
  const time = (v, nullable = false) => (nullable && v == null) || (typeof v === 'string' && Number.isFinite(Date.parse(v)));
  need(list(s.health?.sources).every(x => obj(x) && typeof x.name === 'string' && numeric(x.ok) && numeric(x.observed)),
       'health.sources rows');
  need(obj(s.research) && Array.isArray(s.research.designs), 'research.designs must be a list');
  need(list(s.research?.designs).every(d => obj(d) && typeof d.design === 'string'), 'research.designs rows');
  need(obj(s.range) && obj(s.range.current) && obj(s.range.evaluation), 'range.current/evaluation');
  need(obj(s.market) && Array.isArray(s.market.bars), 'market.bars');
  need(list(s.market?.bars).every(validBar), 'market.bars rows must be [t, open, high, low, close, minutes] of finite numbers');
  need(s.market?.latest == null || (obj(s.market.latest) && numeric(s.market.latest.t) && numeric(s.market.latest.close)),
       'market.latest');
  need(time(s.market?.observed_utc, true), 'market.observed_utc');
  need(list(s.health?.datasets).every(r => obj(r) && typeof r.name === 'string' && time(r.observed_utc, true)), 'health.datasets rows');
  need(time(s.built_utc) && time(s.range?.generated_utc) && time(s.range?.status_expires_utc, true), 'snapshot and range timestamps');
  need(s.ops == null || (obj(s.ops) && time(s.ops.generated_utc) && obj(s.ops.source) && obj(s.ops.decisions)), 'ops (health report)');
  need(s.studyOps == null || validStudyOps(s.studyOps), 'market study operational report');
  need(obj(s.paper) && typeof s.paper.status === 'string' && obj(s.paper.integrity) && obj(s.paper.lifecycle),
       'paper.status/integrity/lifecycle');
  need(obj(s.companion) && obj(s.companion.evaluation) && obj(s.companion.evaluation.horizons) && obj(s.companion.integrity),
       'companion.evaluation.horizons/integrity');
  need(obj(s.feasibility), 'feasibility');
  need(obj(s.sources), 'sources');
  // Older snapshots predate this optional summary. When supplied, validate every container before a renderer
  // reads its fields; a prepared protocol or supplementary audit must retain its source's recorded status.
  if (s.developments !== undefined) {
    const d = s.developments;
    const text = value => typeof value === 'string' && value.trim().length > 0;
    const fields = (value, names) => obj(value) && names.every(name => text(value[name]));
    const window = value => Array.isArray(value) && value.length === 2 && value.every(v => time(v))
      && Date.parse(value[0]) < Date.parse(value[1]);
    const acceptance = value => fields(value, ['checker', 'verdict', 'service_verdict', 'reason', 'source'])
      && window(value.window) && time(value.evaluated_utc, true);
    need(obj(d), 'developments must be an object');
    if (obj(d)) {
      need(d.release === null || (fields(d.release, ['revision', 'title', 'source']) && time(d.release.date)),
           'developments.release');
      need(d.catalog === null || (fields(d.catalog, ['version', 'source']) && time(d.catalog.as_of_utc, true)
        && Number.isInteger(d.catalog.dataset_count) && d.catalog.dataset_count >= 0
        && Array.isArray(d.catalog.feature_families)
        && d.catalog.feature_families.every(f => fields(f, ['id', 'status']))), 'developments.catalog');
      need(Array.isArray(d.protocols)
        && d.protocols.every(p => fields(p, ['id', 'title', 'status', 'source']) && time(p.effective_utc, true)),
           'developments.protocols');
      // repo 2.30: component readiness records, optional (older snapshots predate them). A true state must carry
      // evidence; only the recorded vocabulary is accepted, so a renderer never shows an inferred state.
      const STATES = ['implemented', 'tested', 'pushed', 'merged', 'installed', 'deployed', 'observed', 'registered',
        'prepared', 'blocked', 'pending'];
      need(d.readiness === undefined || (Array.isArray(d.readiness) && d.readiness.every(r =>
        fields(r, ['id', 'title', 'version', 'code_path', 'source']) && time(r.as_of_utc, true) && obj(r.states)
        && Object.entries(r.states).every(([k, v]) => STATES.includes(k) && obj(v) && typeof v.value === 'boolean'
          && Array.isArray(v.evidence) && v.evidence.every(text) && (!v.value || v.evidence.length > 0))
        && Array.isArray(r.blockers) && r.blockers.every(text))), 'developments.readiness');
      need(d.acceptance === null || (acceptance(d.acceptance)
        && (d.acceptance.supplementary === null || (acceptance(d.acceptance.supplementary)
          && d.acceptance.supplementary.window.every((stamp, i) => Date.parse(stamp) === Date.parse(d.acceptance.window[i]))))),
           'developments.acceptance');
    }
  }
  return problems;
}

export function validBar(b) {
  return Array.isArray(b) && b.length >= 6 && b.slice(0, 6).every(numeric) && b[2] >= b[3];
}
// The market chart's geometry inputs (pure; app.js draws them). Throws on any row a validator should have caught.
export function chartPoints(bars, days) {
  if (!Array.isArray(bars) || !bars.length) return [];
  if (!bars.every(validBar)) throw new Error('invalid market bar');
  const end = bars.at(-1)[0];
  return bars.filter(p => p[0] >= end - days * 86400000);
}

// Summarize only the recorded hours in the chart's selected period. The change compares hourly closes;
// missing hours stay missing and incomplete hours are counted explicitly rather than filled in.
export function marketSummary(bars, days) {
  const points = chartPoints(bars, days);
  if (!points.length) return {high: null, low: null, change: null, count: 0, partial: 0};
  const firstClose = points[0][4];
  return {
    high: Math.max(...points.map(p => p[2])),
    low: Math.min(...points.map(p => p[3])),
    change: firstClose === 0 ? null : (points.at(-1)[4] - firstClose) / firstClose,
    count: points.length,
    partial: points.filter(p => p[5] < 60).length,
  };
}

// Operational health rows (reports/health.json), each judged on the viewer's clock. A missing report is unknown.
export const HEALTH_STALE_MIN = 90;
export function opsRows(ops, now = Date.now()) {
  if (!ops) return [{area: 'Health report', state: 'unknown', detail: 'reports/health.json not in this snapshot'}];
  const age = (now - Date.parse(ops.generated_utc)) / 60000;
  const reportState = !Number.isFinite(age) ? 'unknown' : age < -1 ? 'clock mismatch' : age > HEALTH_STALE_MIN ? 'stale' : 'within cadence';
  const src = ops.source || {};
  const limit = src.stale_limit_min || HEALTH_STALE_MIN;
  // Repo 2.27: the age of a timestamp is judged on the viewer's clock; a failure state the report recorded stays
  // visible while the evidence is fresh (a fresh failure is never shown as "within cadence"), and stale evidence is
  // stale whatever the report said. Reports before 2.27 carry no data/activity split: their states are shown as such.
  const judged = (stamp, recorded) => {
    const a = (now - Date.parse(stamp)) / 60000;
    if (!Number.isFinite(a)) return 'unknown';
    if (a > limit) return 'stale';
    return recorded && !['healthy', 'fresh'].includes(recorded) ? recorded : 'within cadence';
  };
  const srcState = judged(src.last_scheduled_utc, src.state);
  const gaps = (src.gaps || []).map(g => `${g.start_utc} → ${g.end_utc || 'ongoing at report'} (${Math.round(g.minutes)} min)`);
  const last = obj => Object.entries(obj || {}).slice(-6).map(([k, v]) => `${k.slice(5, 16)} ${v}`).join(' · ') || 'none';
  const problems = obj => Object.values(obj || {}).filter(v => /^(absent|failed|missed|invalid)/.test(v)).length;
  const mon = ops.monitors || {};
  const monRows = Object.entries(mon.workflows || {}).filter(([, v]) => v.stale_after_min).map(([k, v]) => {
    // Repo 2.26: heartbeat = last completed run, whatever it found; reports before 2.26 carry only last_success_utc.
    // Repo 2.27: a failed run is "detected a problem" only when its check executed (job/step evidence); a run whose
    // job never received a runner could not execute; without that evidence the failure's cause is unknown.
    const beat = v.last_completed_utc || v.last_success_utc;
    const a = (now - Date.parse(beat)) / 60000;
    const failed = v.last_result && v.last_result !== 'success';
    // Repo 2.28: the check step itself is read (last_check); setup running is not the check running.
    const CHECK = {'found a problem': 'ran its check; found a problem', 'check failed': 'ran its check; failed without a finding',
                   'failed before checking': 'failed before checking', 'check skipped': 'check skipped',
                   'no runner': 'could not execute (no runner)', 'running': 'check running', unknown: 'failed; check evidence unknown'};
    const st = !Number.isFinite(a) ? 'unknown' : a > v.stale_after_min ? 'stale'
      : !failed ? 'within cadence'
      : v.last_check ? (CHECK[v.last_check] || `failed; ${v.last_check}`)
      : v.last_executed === false ? 'could not execute (no runner/steps)'
      : 'failed; check evidence unknown (report before 2.28)';
    return {area: `Monitor ${k}`, state: st,
            detail: v.last_completed_utc ? `last run ${v.last_completed_utc} (${v.last_result || '—'}${v.last_execution ? '; ' + v.last_execution : ''}); last success ${v.last_success_utc || 'none'}`
                                         : `last success ${v.last_success_utc || 'unknown'}`};
  });
  // Repo 2.28: arrivals of the designated primary trigger (external timer), apart from the native dispatcher and from
  // overall service health - fallback keeping service healthy never hides missing primary arrivals.
  const tm = mon.external_timer;
  const timerRows = tm && 'opportunities' in tm ? [{area: 'External timer (primary trigger)',
    state: tm.absent?.length || tm.delayed?.length ? `${tm.absent.length} absent, ${tm.delayed.length} delayed in ${tm.window_h} h` : tm.state,
    detail: `${tm.on_time} of ${tm.opportunities} on time; last arrival ${tm.last_arrival_utc || 'none'}` +
            (tm.absent?.length ? `; absent ${tm.absent.slice(-4).map(x => x.slice(5, 16)).join(', ')}` : '') + ' (arrivals only)'}] : [];
  const cov = ops.ps1_coverage || {};
  // Repo 2.25: service continuity (native or recovery-dispatcher runs) is judged apart from the native schedule;
  // a person's dispatch counts as neither. Reports written before 2.25 carry no service block: unknown.
  // Repo 2.27: data (last persisted critical success) and activity (last automated run, any result) are separate rows.
  const svc = src.service || null;
  const hasSplit = svc && 'last_success_utc' in svc;
  const dataState = !svc ? 'unknown' : hasSplit ? judged(svc.last_success_utc, null) : 'unknown (report before 2.27)';
  const actState = !svc ? 'unknown' : judged(svc.last_activity_utc || svc.last_automated_utc, svc.state);
  const tgt = svc?.acceptance_target;
  const dataAge = hasSplit ? (now - Date.parse(svc.last_success_utc)) / 60000 : NaN;
  const c24 = src.coverage_24h;
  const svcRows = [
    {area: 'Collector data (last persisted critical success)', state: dataState,
     detail: hasSplit ? `${svc.last_success_utc || 'none'}; 45-min acceptance target ${Number.isFinite(dataAge) && dataAge <= (tgt?.max_gap_min || 45) ? 'met' : 'breached'} on this clock (watchdog limit ${limit} min is separate)` : 'not in this report'},
    {area: 'Collector service (automated activity)', state: actState,
     detail: svc ? `last automated run ${svc.last_activity_utc || svc.last_automated_utc || 'unknown'} (${svc.last_activity_result || svc.last_source || '—'}); ${(svc.gaps || []).length} silence(s) in 72 h` : 'not in this report (before repo 2.25)'},
    ...(c24 ? [{area: 'Collection, 24 h to report',
               state: `${c24.intervals_with_successful_automated_run ?? c24.intervals_with_automated_run} of ${c24.intervals} intervals${c24.intervals_with_successful_automated_run == null ? ' (activity; before 2.27)' : ''}`,
               detail: `${c24.expected_slots} slots; runs ${Object.entries(c24.runs_by_source || {}).map(([k, v]) => `${k} ${v}`).join(', ') || 'none'}; longest gap ${c24.longest_successful_gap_min ?? c24.longest_automated_gap_min} min${c24.automated_critical_failures ? `; ${c24.automated_critical_failures} critical failure(s)` : ''}`}] : []),
  ];
  return [
    {area: 'Health report', state: reportState, detail: `generated ${ops.generated_utc}; ${ops.clock}`},
    {area: 'Collector schedule', state: srcState, detail: `native: last scheduled run ${src.last_scheduled_utc || 'unknown'}`},
    ...svcRows,
    {area: 'Recorded silences', state: gaps.length ? `${gaps.length} in ${72} h` : 'none', detail: gaps.join('; ') || '—'},
    {area: 'Range decisions', state: problems(ops.decisions?.range) ? `${problems(ops.decisions.range)} missed or failed` : 'none missed', detail: last(ops.decisions?.range)},
    {area: 'PS1 decisions', state: ops.decisions?.ps1_launched ? (problems(ops.decisions.ps1) ? `${problems(ops.decisions.ps1)} missed` : 'none missed') : 'not launched', detail: last(ops.decisions?.ps1)},
    {area: 'PS1 report coverage', state: cov.not_covered?.length ? `${cov.not_covered.length} due decision(s) not in the report` : 'report covers all due decisions',
     detail: `coverage ${cov.report_coverage ?? '—'} as of ${cov.report_generated_utc || '—'}`},
    {area: 'Scoring backlog', state: Object.keys(ops.scoring_backlog || {}).length ? 'backlog' : 'none', detail: Object.entries(ops.scoring_backlog || {}).map(([h, v]) => `${h} ${v.length}`).join(' · ') || '—'},
    ...(monRows.length ? monRows : [{area: 'Monitors', state: 'unknown', detail: mon.source || 'not reported'}]),
    ...timerRows,
  ];
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

// Operational status has its own expiry. Rebuilding the dashboard never refreshes a study report.
export function validStudyOps(s) {
  const obj = x => x !== null && typeof x === 'object' && !Array.isArray(x);
  const count = x => Number.isInteger(x) && x >= 0;
  if (!obj(s) || s.schema !== 'market-study-health/1' || !Number.isFinite(Date.parse(s.generated_utc)) ||
      s.stale_after_minutes !== 45 || !['ok', 'failed'].includes(s.integrity) || typeof s.paused !== 'boolean' ||
      !obj(s.studies) || !obj(s.pilots) || !Array.isArray(s.alerts) || !Array.isArray(s.warnings) ||
      ![...s.alerts, ...s.warnings].every(x => typeof x === 'string')) return false;
  const deployment = s.deployment;
  if (deployment != null && (!obj(deployment) || !Number.isFinite(Date.parse(deployment.started_utc)) ||
      !/^[0-9a-f]{40}$/.test(deployment.commit) || typeof deployment.label !== 'string' ||
      !obj(deployment.studies) || !obj(deployment.pilots))) return false;
  for (const row of [...Object.values(s.studies), ...Object.values(s.pilots),
      ...Object.values(deployment?.studies || {}), ...Object.values(deployment?.pilots || {})]) {
    if (!obj(row) || !count(row.due) || !count(row.successful) || row.successful > row.due ||
        !count(row.consecutive_misses) || row.consecutive_misses > row.due ||
        (row.due === 0 ? row.coverage !== null : !numeric(row.coverage) || Math.abs(row.coverage-row.successful/row.due) > 1e-9)) return false;
    if (row.pending_successful != null && !count(row.pending_successful) ||
        row.active_consecutive_misses != null && (!count(row.active_consecutive_misses) || row.active_consecutive_misses > row.consecutive_misses) ||
        row.recovered_before_close != null && typeof row.recovered_before_close !== 'boolean') return false;
  }
  const dist = d => obj(d) && count(d.n) && ['min','median','p90','max'].every(k => d[k] === null || numeric(d[k]));
  if (s.depth_diagnostics != null) {
    if (!obj(s.depth_diagnostics)) return false;
    for (const d of Object.values(s.depth_diagnostics)) {
      if (!obj(d) || !count(d.forecasts) || !count(d.abstained) || d.abstained > d.forecasts ||
          !count(d.missing_depth_age) || d.missing_depth_age > d.forecasts || !dist(d.depth_age_minutes) ||
          !obj(d.abstention_reasons) || !Object.values(d.abstention_reasons).every(count)) return false;
    }
  }
  if (s.options_quality?.selected_by_horizon != null) {
    if (!obj(s.options_quality.selected_by_horizon)) return false;
    for (const d of Object.values(s.options_quality.selected_by_horizon)) {
      if (!obj(d) || !count(d.usable_captures) || !count(d.legs) ||
          !['quote_age_ms','relative_spread','delta_distance'].every(k => dist(d[k])) ||
          !obj(d.size_states) || !Object.values(d.size_states).every(count)) return false;
    }
  }
  if (s.paired_diagnostics != null) {
    const p = s.paired_diagnostics;
    if (!obj(p) || !['scored_forecasts','unique_entries','largest_disjoint_60m_subset'].every(k => count(p[k])) ||
        p.unique_entries > p.scored_forecasts || p.largest_disjoint_60m_subset > p.unique_entries ||
        !(p.equal_entry_clock_share === null || numeric(p.equal_entry_clock_share) && p.equal_entry_clock_share >= 0 && p.equal_entry_clock_share <= 1)) return false;
  }
  return true;
}

export function studyRows(s, now = Date.now()) {
  if (!s) return [{area: 'Market studies', state: 'unknown', detail: 'Operational study report not in this snapshot'}];
  if (!validStudyOps(s)) return [{area: 'Market studies', state: 'invalid', detail: 'Invalid study report; results withheld'}];
  const age = (now - Date.parse(s.generated_utc)) / 60000;
  const clock = age < -1 ? 'clock mismatch' : age > s.stale_after_minutes ? 'stale' : 'within cadence';
  const rows = [{area: 'Study report', state: s.integrity === 'failed' ? 'integrity failed' : clock,
    detail: `Generated ${s.generated_utc}; counts cover closed opportunities in the 24 hours to this report`}];
  const label = name => ({turnover:'Turnover control', range:'Range calibration', state:'Continuous market state', paired:'Paired spot/perpetual', stress:'Exchange stress', liquidations:'Liquidation revisions', options:'Options usability'})[name] || name;
  const status = r => clock !== 'within cadence' ? clock : s.paused ? 'paused' :
    r.recovered_before_close ? 'recovered; history retained' : r.due === 0 ? 'none due' :
    (r.active_consecutive_misses ?? r.consecutive_misses) >= 2 ? 'missed opportunities' :
    r.coverage < .8 ? 'historical coverage below 80%' : 'within target';
  const detail = r => `${r.successful}/${r.due} closed opportunities successful; ${r.consecutive_misses} trailing closed misses` +
    (r.pending_successful ? `; ${r.pending_successful} additional successes awaiting deadline/grace closure` : '') +
    (r.recovered_before_close ? '; a newer verified success cleared the current miss alert' : '');
  for (const [name, r] of Object.entries({...s.studies, ...s.pilots})) {
    rows.push({area: `${label(name)} (24h)`, state: status(r), detail: detail(r)});
  }
  if (s.deployment) {
    rows.push({area: 'Recovery deployment', state: clock === 'within cadence' ? 'operational comparison' : clock,
      detail: `${s.deployment.label}; opportunity times from ${s.deployment.started_utc}. Fixed baseline; research clocks unchanged.`});
    for (const [name, r] of Object.entries({...s.deployment.studies, ...s.deployment.pilots})) {
      rows.push({area: `${label(name)} (since deployment)`, state: status(r), detail: detail(r)});
    }
  }
  for (const detail of s.alerts) rows.push({area: 'Recorded alert', state: clock === 'within cadence' ? 'attention' : clock, detail});
  const p = s.paired_diagnostics;
  if (p) rows.push({area: 'Paired sample (since launch)', state: 'descriptive', detail:
    `${p.scored_forecasts} scored forecasts; ${p.unique_entries} distinct entries; ${p.largest_disjoint_60m_subset} disjoint 60m windows. ` +
    `Equal entry clocks: ${p.equal_entry_clock_share == null ? 'unknown' : (100*p.equal_entry_clock_share).toFixed(1)+'%'}. Counts do not establish independence.`});
  const fmt = (x, scale = 1) => x == null ? 'unavailable' : (x * scale).toFixed(2);
  for (const [period, d] of Object.entries(s.depth_diagnostics || {})) {
    rows.push({area: `State depth (${period === 'last_24h' ? '24h' : 'since deployment'})`, state: clock === 'within cadence' ? 'descriptive' : clock,
      detail: `${d.forecasts} forecasts; ${d.abstained} abstentions; depth age median ${fmt(d.depth_age_minutes.median)} min, max ${fmt(d.depth_age_minutes.max)} min; ${d.missing_depth_age} unavailable ages. ` +
        Object.entries(d.abstention_reasons).map(([why, n]) => `${n}: ${why}`).join('; ')});
  }
  for (const [horizon, d] of Object.entries(s.options_quality?.selected_by_horizon || {})) {
    rows.push({area: `Selected options (${horizon === 'rr25_7d' ? '7d' : '30d'}, 24h)`, state: clock === 'within cadence' ? 'descriptive' : clock,
      detail: `${d.usable_captures} usable captures; ${d.legs} selected leg observations; quote age median ${fmt(d.quote_age_ms.median, .001)} s; spread median ${fmt(d.relative_spread.median, 100)}%, p90 ${fmt(d.relative_spread.p90, 100)}%; delta distance median ${fmt(d.delta_distance.median)}. ` +
        `${d.size_states['not-in-source'] || 0} legs lack quote size. Repeated legs are not independent observations.`});
  }
  return rows;
}
