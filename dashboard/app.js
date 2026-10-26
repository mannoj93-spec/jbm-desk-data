import { numeric, ageLabel, freshness, forecastState, reportExpiry, csv, escapeHTML as esc, CLOCKS, companionClocks, paperClocks, pairedRow, stage, chartPoints, marketSummary, opsRows, studyRows } from './model.js';

const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const HORIZONS = ['4h', '24h', '72h'];
const pageCodes = {overview: 'OVRV', forecasts: 'RNG', research: 'LAB', health: 'DATA', paper: 'PAPR', reports: 'AUDIT'};
const pages = {
  overview: ['Desk overview', 'The market, the models, and the evidence behind them.'],
  forecasts: ['Range forecasts', 'Registered full-window ranges. Every estimate has an expiry.'],
  research: ['Research lab', 'Pre-registered questions. Prospective observations. Reviewable evidence.'],
  health: ['Data health', 'Collection coverage, source availability, and the age of each observation.'],
  paper: ['Paper desk', 'Simulated sizing experiments and paired model comparisons.'],
  reports: ['Reports & audit', 'Trace every displayed result to the source snapshot.'],
};
const stored = (key, fallback) => { try { return localStorage.getItem('jbm-' + key) || fallback; } catch { return fallback; } };
const save = (key, value) => { try { localStorage.setItem('jbm-' + key, value); } catch { /* Storage is optional. */ } };
let data, refreshError = null, page = 'overview', period = stored('period', '7D'), query = '', filter = 'all', sort = 'name', ascending = true, chartObserver;
if (!['1D', '3D', '7D'].includes(period)) period = '7D';
let theme = stored('theme', 'dark');
if (!['dark', 'light'].includes(theme)) theme = 'dark';
let exported = [];
const format = (v, digits = 0) => numeric(v) ? v.toLocaleString('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits }) : '—';
const percent = (v, digits = 0) => numeric(v) ? `${format(v * 100, digits)}%` : '—';
const stamp = v => {
  const d = new Date(v);
  return v != null && Number.isFinite(d.getTime()) ? d.toISOString().slice(0, 16).replace('T', ' ') + ' UTC' : 'Unknown';
};
const currentAge = v => `<span data-age="${esc(v || '')}">${esc(ageLabel(v))}</span>`;
const flag = (text, type = '') => `<span class="chip ${type}">${esc(text)}</span>`;
const tone = s => /failed|blocked|unavailable|expired|stale|withheld|unaccounted|missed opportunities|^attention$/i.test(s) ? 'bad' : /passed|valid-current|supported|^ok$|^verified$|within cadence|within expiry/.test(s) ? 'good' : 'warn';
const sourceURL = path => `${data.repository}/blob/${data.commit || 'main'}/${path.split('/').map(encodeURIComponent).join('/')}`;
const source = (path, label = 'Source report ↗') => `<a href="${esc(sourceURL(path))}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>`;
const panel = (number, title, body, extra = '', footer = '') => `<section class="panel"><div class="panel-header"><div class="panel-title"><span class="panel-number">${number}</span><h2>${title}</h2></div>${extra}</div>${body}${footer ? `<div class="panel-foot">${footer}</div>` : ''}</section>`;
const metric = (title, value, note, color = '') => `<div class="stat"><div class="stat-label">${title}</div><div class="stat-value ${color}">${value}</div><div class="stat-note">${note}</div></div>`;
const table = (headers, rows) => `<div class="table-wrap"><table><thead><tr>${headers.map(h => `<th scope="col">${h}</th>`).join('')}</tr></thead><tbody>${rows.length ? rows.join('') : `<tr><td colspan="${headers.length}" class="empty">No matching records.</td></tr>`}</tbody></table></div>`;
const reportTime = (value, hours) => `<span data-freshness="${esc(value || '')}" data-hours="${hours}">${flag(freshness(value, hours), tone(freshness(value, hours)))}</span>`;

function applyTheme() {
  document.documentElement.dataset.theme = theme;
  $('#theme-toggle').textContent = theme === 'dark' ? 'LIGHT' : 'DARK';
  $('#theme-toggle').setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
}
applyTheme();
$('#theme-toggle').addEventListener('click', () => { theme = theme === 'dark' ? 'light' : 'dark'; save('theme', theme); applyTheme(); });

function overview() {
  const research = data.research.designs;
  const passed = research.filter(d => d.research_integrity?.required && d.research_integrity?.status === 'passed').length;
  const required = research.filter(d => d.research_integrity?.required).length;
  const supported = research.filter(d => d.status === 'supported' && d.publication?.evaluation_valid).length;
  const stats = `<div class="stats">${metric('Market observation', currentAge(data.market.observed_utc), 'Stored BTC price · not a live feed', 'amber')}${metric('Workflow result', 'Unverified', '<a href="' + data.workflow.url + '" target="_blank" rel="noopener noreferrer">Inspect GitHub Actions ↗</a>')}${metric('Required integrity checks', `${passed}<span class="muted"> / ${required}</span>`, 'Latest research attempt', required ? (passed === required ? 'positive' : 'negative') : '')}${metric('Supported designs', `${supported}<span class="muted"> / ${research.length}</span>`, 'Support requires the registered criteria')}</div>`;
  const market = panel('01', 'BTC / USDT', marketChart(), '<span class="chip">PERPETUAL · STORED DATA</span>', `<span>¹ First to last recorded close in selection · gaps unfilled</span><span>Last captured ${currentAge(data.market.observed_utc)}</span>`);
  const compare = panel('04', 'Model vs. persistence', comparisons(), flag('Descriptive', 'warn'), `<span>MAE of ln range · lower is better</span>${source('reports/range.md')}`);
  const signals = panel('02', 'Forecast monitor', table(['Window', 'Point range¹', 'Availability'], HORIZONS.map(h => {
    const row = data.range.current[h];
    return `<tr><td class="mono">${h.toUpperCase()}</td><td class="numeric">${format(row?.points_at_decision_close?.point, 1)}</td><td data-forecast="${h}">${flag(forecastState(row, data.range), tone(forecastState(row, data.range)))}</td></tr>`;
  })) + `<div class="forecast-note"><strong>REGISTERED RANGES</strong><br>Full-window estimates, frozen before the window opens. Availability is checked against your clock.</div>`, `<a href="#forecasts" class="mini-text amber">OPEN →</a>`, '<span>¹ USD-equivalent range at decision close; not a target.</span>');
  const lab = panel('03', 'Research watchlist', researchTable(research.slice(0, 5), true), `<a href="#research" class="mini-text amber">ALL ${research.length} DESIGNS →</a>`, `<span>Oldest evidence cutoff ${esc(stamp(data.research.oldest_cutoff_utc))}</span>${reportTime(data.research.oldest_cutoff_utc, CLOCKS.research_observation_hours)}`);
  const review = panel('05', 'Desk review', alertsHTML(), `<a href="#health" class="mini-text amber">DETAILS →</a>`);
  exported = [['Signal', 'Value', 'As of'], ['Market observation', data.market.observed_utc, data.market.observed_utc], ['Required integrity passed', passed, data.research.oldest_cutoff_utc], ['Supported designs', supported, data.research.oldest_cutoff_utc], ['Workflow', 'unverified', 'Not queried']];
  return stats + `<div class="overview-primary">${market}<div class="stack" style="grid-template-columns:1fr">${signals}${review}</div></div><div class="overview-secondary section-gap">${lab}${compare}</div>${developmentsBrief()}`;
}

function developmentsBrief() {
  const d = data.developments;
  if (!d) return '';
  const prepared = d.protocols.filter(p => /^prepared\b/i.test(p.status)).length;
  const a = d.acceptance;
  const body = `<div class="brief-grid"><div class="brief-item"><span class="eyebrow">REPOSITORY UPDATE</span><h3>${d.release ? `Revision ${esc(d.release.revision)}` : 'Revision not reported'}</h3><p class="definition">${d.release ? esc(d.release.title) : 'No release summary is available in this snapshot.'}</p>${d.release ? `<span class="brief-link">${source(d.release.source, 'READ CHANGELOG ↗')}</span>` : ''}</div><div class="brief-item"><span class="eyebrow">RESEARCH PIPELINE</span><h3>${prepared} prepared / ${d.protocols.length} protocols</h3><p class="definition">Preparation does not establish registration, commissioning, or research support.</p><p class="mini-text section-gap">${esc(d.protocols.map(p => p.id).join(' · ') || 'No protocol records available.')}</p><a href="#research" class="brief-link">INSPECT READINESS →</a></div><div class="brief-item"><span class="eyebrow">LATEST ACCEPTANCE WINDOW</span><h3>${a ? esc(a.window[0].slice(0, 10)) + ' / UTC' : 'No result of record'}</h3>${a ? `${flag(a.verdict, tone(a.verdict))}<p class="definition section-gap">Service: ${esc(a.service_verdict)} · ${esc(a.checker)}<br>Service and acceptance are separate verdicts.</p><span class="brief-link">${source(a.source, 'OPEN RESULT OF RECORD ↗')}</span>` : '<p class="definition">An absent acceptance result remains unknown.</p>'}</div></div>`;
  return `<div class="section-gap">${panel('06', 'Repository developments', body, flag('Commit-pinned'), '<span>Recorded source states · a repository update does not activate a research protocol.</span>')}</div>`;
}
function researchReadiness() {
  const d = data.developments;
  if (!d) return '';
  const protocols = table(['Protocol / question', 'Recorded state', 'Effective UTC', 'Source'], d.protocols.map(p => `<tr><td><span class="mono">${esc(p.id)}</span><span class="sub">${esc(p.title)}</span></td><td class="protocol-state">${esc(p.status)}</td><td class="mono">${p.effective_utc ? esc(stamp(p.effective_utc)) : 'Not recorded'}</td><td>${source(p.source, 'PROTOCOL ↗')}</td></tr>`));
  const catalog = d.catalog ? `<div class="panel-body"><p class="definition"><strong class="amber">${format(d.catalog.dataset_count)} cataloged datasets</strong> · ${esc(d.catalog.version)} · recorded as of ${esc(stamp(d.catalog.as_of_utc))}</p><p class="definition">These states describe feature implementation and data access. They do not describe evidence maturity.</p></div>${table(['Feature family', 'Implementation state'], d.catalog.feature_families.map(f => `<tr><td class="mono">${esc(f.id)}</td><td>${esc(f.status)}</td></tr>`))}` : '<div class="empty">No research catalog in this snapshot.</div>';
  const cols = ['implemented', 'tested', 'merged', 'deployed', 'observed', 'registered'];
  const cell = (r, k) => { const v = r.states[k]; if (!v) return '<td class="mini-text">—</td>'; return `<td title="${esc(v.evidence.join('; '))}">${v.value ? 'yes' : 'no'}</td>`; };
  const rd = d.readiness || [];
  const asOf = rd.map(r => r.as_of_utc).filter(Boolean).sort().at(-1);
  const comps = rd.length ? `<div class="panel-body"><p class="definition">Recorded as of ${asOf ? esc(stamp(asOf)) : 'an unrecorded time'} (snapshot built ${esc(stamp(data.built_utc))}). A state appears only with its evidence; a test establishes "tested" and nothing more.</p></div>${table(['Component', ...cols.map(c => c[0].toUpperCase() + c.slice(1)), 'Blockers', 'Source'], rd.map(r => `<tr><td><span class="mono">${esc(r.id)}</span><span class="sub">${esc(r.title)} · ${esc(r.version)}</span></td>${cols.map(c => cell(r, c)).join('')}<td class="mini-text">${esc(r.blockers.join(' · ') || '—')}</td><td>${source(r.source, 'RECORD ↗')}</td></tr>`))}` : '<div class="empty">No component readiness records in this snapshot.</div>';
  return `<div class="section-gap">${panel('03', 'Protocol readiness', protocols, flag('Recorded states'), '<span>Prepared ≠ registered · pilot criteria ≠ commissioned recorder · no effective date is inferred.</span>')}</div><div class="section-gap">${panel('03b', 'Component readiness', comps, flag('Recorded states'), '<span>Implemented ≠ merged ≠ deployed ≠ observed · persistence recovery is operations, not a research result.</span>')}</div><div class="section-gap">${panel('04', 'Research data catalog', catalog, '', d.catalog ? source(d.catalog.source, 'OPEN CATALOG ↗') : '')}</div>`;
}
function acceptanceDetail() {
  const a = data.developments?.acceptance;
  if (!a) return '';
  const records = [['Result of record', a], ...(a.supplementary ? [['Supplementary audit', a.supplementary]] : [])];
  return `<div class="section-gap">${panel('A1', 'Acceptance audit', `<div class="panel-body"><p class="definition">Window ${esc(stamp(a.window[0]))} → ${esc(stamp(a.window[1]))}. A supplementary audit does not replace the result of record.</p></div>${table(['Record', 'Checker', 'Acceptance', 'Service', 'Source'], records.map(([label, r]) => `<tr><td>${label}</td><td class="mono">${esc(r.checker)}</td><td>${flag(r.verdict, tone(r.verdict))}</td><td>${esc(r.service_verdict)}</td><td>${source(r.source, 'RESULT ↗')}</td></tr>`))}<details><summary>Assessment and evaluation clocks</summary>${records.map(([label, r]) => `<p><strong>${label}</strong> · evaluated ${esc(stamp(r.evaluated_utc))}<br>${esc(r.reason)}</p>`).join('')}</details>`, flag('Historical window'))}</div>`;
}

function marketChart() {
  const latest = data.market.latest;
  if (!latest || !data.market.bars.length) return '<div class="empty">No stored market prices available.</div>';
  return `<div class="quote-row"><div><div class="quote-label">LAST STORED PRICE / USD</div><div class="quote">${format(latest.close, 2)}<span class="quote-unit">USD</span></div><div class="quote-sub">${esc(stamp(latest.t))}</div></div><div class="segmented" aria-label="Price history period">${['1D', '3D', '7D'].map(v => `<button data-period="${v}" aria-pressed="${period === v}">${v}</button>`).join('')}</div></div><div id="market-chart" class="chart"><svg role="img" aria-label="Recorded BTCUSDT hourly closing prices in USD over the selected period"></svg><div class="chart-tooltip" hidden></div></div><div id="chart-summary" class="chart-summary">${chartSummaryHTML()}</div>`;
}
function chartSummaryHTML() {
  const s = marketSummary(data.market.bars, parseInt(period, 10));
  const change = numeric(s.change) ? `${s.change > 0 ? '+' : ''}${percent(s.change, 2)}` : '—';
  return `<div><span>${period} OBSERVED MOVE¹</span><strong class="${s.change > 0 ? 'positive' : s.change < 0 ? 'negative' : ''}">${change}</strong></div><div><span>RECORDED HIGH</span><strong>${format(s.high, 2)}</strong></div><div><span>RECORDED LOW</span><strong>${format(s.low, 2)}</strong></div><div><span>HOURS / PARTIAL</span><strong>${format(s.count)} / ${format(s.partial)}</strong></div>`;
}
function drawMarket() {
  const box = $('#market-chart');
  if (!box) return;
  const svg = box.querySelector('svg'), tooltip = box.querySelector('.chart-tooltip');
  if ($('#chart-summary')) $('#chart-summary').innerHTML = chartSummaryHTML();
  const days = parseInt(period, 10);
  const points = chartPoints(data.market.bars, days);
  if (!points.length) return;
  const width = Math.max(240, box.clientWidth - 20), height = Math.max(window.innerWidth < 521 ? 230 : window.innerWidth >= 1600 ? 290 : 250, box.clientHeight || 0);
  const left = 12, right = 63, top = 28, bottom = 35;
  const min = Math.min(...points.map(p => p[4])), max = Math.max(...points.map(p => p[4]));
  const pad = Math.max((max - min) * .18, max * .0005), lo = min - pad, hi = max + pad;
  const first = points[0][0], last = points.at(-1)[0];
  const x = t => left + (t - first) / Math.max(1, last - first) * (width - left - right);
  const y = v => top + (hi - v) / (hi - lo) * (height - top - bottom);
  const ticks = [0, 1, 2, 3, 4].map(i => lo + (hi - lo) * i / 4);
  const grid = ticks.map(v => `<line class="grid" x1="${left}" x2="${width - right}" y1="${y(v)}" y2="${y(v)}"/><text x="${width - right + 9}" y="${y(v) + 4}">${format(v)}</text>`).join('');
  const xTicks = [0, .5, 1].map(f => {
    const t = first + f * (last - first), d = new Date(t);
    return `<line class="grid vertical-grid" x1="${x(t)}" x2="${x(t)}" y1="${top}" y2="${height - bottom}"/><text x="${x(t)}" y="${height - 10}" text-anchor="${f === 0 ? 'start' : f === 1 ? 'end' : 'middle'}">${days === 1 ? d.toISOString().slice(11, 16) : d.toISOString().slice(5, 10)} UTC</text>`;
  }).join('');
  const segments = [];
  for (const p of points) {
    if (!segments.length || p[0] - segments.at(-1).at(-1)[0] > 3600000) segments.push([]);
    segments.at(-1).push(p);
  }
  const paths = segments.map(segment => {
    const line = segment.map((p, i) => `${i ? 'L' : 'M'}${x(p[0]).toFixed(2)},${y(p[4]).toFixed(2)}`).join(' ');
    return `<path class="area" d="${line} L${x(segment.at(-1)[0])},${height - bottom} L${x(segment[0][0])},${height - bottom}Z"/><path class="price-line" d="${line}"/>`;
  }).join('');
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  svg.innerHTML = `<title>BTCUSDT hourly closing price, ${days} day view</title><desc>Stored prices in USD. UTC timestamps. Missing hours are not interpolated.</desc>${grid}${xTicks}<text x="${width - right + 9}" y="14">USD</text>${paths}<line class="last-line" x1="${left}" x2="${width - right}" y1="${y(points.at(-1)[4])}" y2="${y(points.at(-1)[4])}"/><circle class="point" cx="${x(last)}" cy="${y(points.at(-1)[4])}" r="3"/><line id="hover-guide" class="chart-guide" x1="0" x2="0" y1="${top}" y2="${height - bottom}" visibility="hidden"/>`;
  const hide = () => { tooltip.hidden = true; box.querySelector('#hover-guide')?.setAttribute('visibility', 'hidden'); };
  svg.onpointermove = e => {
    const rect = svg.getBoundingClientRect(), px = (e.clientX - rect.left) * width / rect.width;
    const target = first + (px - left) / (width - left - right) * (last - first);
    const p = points.reduce((a, b) => Math.abs(b[0] - target) < Math.abs(a[0] - target) ? b : a);
    tooltip.innerHTML = `${esc(stamp(p[0]))}<br>Close <strong>${format(p[4], 2)} USD</strong><br>${p[5]} / 60 recorded minutes`;
    tooltip.hidden = false;
    tooltip.style.left = `${Math.max(4, Math.min(box.clientWidth - tooltip.offsetWidth - 4, px - 50))}px`;
    tooltip.style.top = '4px';
    const guide = box.querySelector('#hover-guide');guide.setAttribute('x1', x(p[0]));guide.setAttribute('x2', x(p[0]));guide.setAttribute('visibility', 'visible');
  };
  svg.onpointerleave = hide;
}

function comparisons() {
  const rows = data.range.evaluation?.horizons || {};
  const max = Math.max(.00001, ...Object.values(rows).flatMap(r => [r.mae_b2, r.mae_b0]).filter(numeric));
  return `<div class="panel-body"><div class="legend"><span><i></i>B2 range model</span><span><i class="baseline"></i>B0 persistence</span></div>${HORIZONS.map(h => {
    const r = rows[h];
    if (!r || !numeric(r.mae_b2)) return `<div class="empty">${h}: no scored evidence</div>`;
    return `<div class="comparison-row"><div class="comparison-head"><span>${h.toUpperCase()} <span class="muted">· n=${r.n}</span></span><span class="${numeric(r.reduction_vs_b0) && r.reduction_vs_b0 < 0 ? 'negative' : 'amber'}">${numeric(r.reduction_vs_b0) ? percent(Math.abs(r.reduction_vs_b0), 1) + (r.reduction_vs_b0 < 0 ? ' higher MAE' : ' lower MAE') : '—'}</span></div><div class="comparison-track" aria-label="B2 MAE ${r.mae_b2}"><span style="width:${r.mae_b2 / max * 100}%"></span></div><div class="comparison-track baseline" aria-label="B0 MAE ${r.mae_b0}"><span style="width:${r.mae_b0 / max * 100}%"></span></div><div class="mini-text">B2 ${format(r.mae_b2, 4)} <span class="divider">/</span> B0 ${format(r.mae_b0, 4)}</div></div>`;
  }).join('')}<div class="mini-text">Overlapping windows are dependent. Descriptive comparisons do not establish a trading edge.</div></div>`;
}
function alertsHTML() {
  const entries = [];
  const expired = HORIZONS.filter(h => forecastState(data.range.current[h], data.range) !== 'valid-current');
  if (expired.length) entries.push(['Forecast availability', `${expired.join(', ')}: check expiry and source status in Range forecasts.`]);
  for (const alert of data.health.alerts.slice(0, 2)) {
    const colon = alert.indexOf(':');
    entries.push([colon > 0 ? alert.slice(0, colon) : 'Collection observation', colon > 0 ? alert.slice(colon + 1) : alert]);
  }
  if (!data.research.designs.some(d => d.status === 'supported')) entries.push(['Evidence developing', 'No research design is currently reported as supported.']);
  return entries.slice(0, 3).map(([title, description]) => `<div class="alert-row"><span class="alert-dot"></span><div>${esc(title)}<p>${esc(description)}</p></div></div>`).join('') || '<div class="empty">No review items in this snapshot.</div>';
}

function forecasts() {
  const report = data.range;
  exported = [['Horizon', 'State on export', 'Point range (USD equivalent at decision close)', 'Q10', 'Q50', 'Q90', 'Window start UTC', 'Window end UTC', 'Valid until UTC']];
  const cards = HORIZONS.map(h => {
    const r = report.current[h], state = forecastState(r, report), points = r?.points_at_decision_close;
    exported.push([h, state, points?.point, points?.q10, points?.q50, points?.q90, r?.start_utc, r?.end_utc, r?.valid_until_utc]);
    if (!r || !points) return panel(h.toUpperCase(), 'Full-window range', `<div class="empty">${esc(r?.reason || 'No available forecast')}</div>`, flag(state, tone(state)));
    const upper = numeric(points.q90) ? points.q90 * 1.12 : 1;
    const band = [points.q10, points.q50, points.q90].every(numeric) ? `<div class="range-scale" role="img" aria-label="Range quantiles Q10 ${points.q10}, Q50 ${points.q50}, Q90 ${points.q90} USD equivalent"><span class="range-band" style="left:${points.q10 / upper * 100}%;width:${(points.q90 - points.q10) / upper * 100}%"></span><span class="range-median" style="left:${points.q50 / upper * 100}%"></span></div><div class="range-labels"><span>Q10 ${format(points.q10)}</span><span>Q50 ${format(points.q50)}</span><span>Q90 ${format(points.q90)}</span></div>` : '<div class="empty">Quantiles unavailable</div>';
    return panel(h.toUpperCase(), 'Full-window range', `<div class="panel-body"><div><div class="forecast-value">${format(points.point, 1)} <span class="mini-text">USD</span></div><div class="definition">Equivalent range at decision close</div>${band}</div><dl class="detail-grid"><div class="detail-item"><dt>REFERENCE PRICE</dt><dd>${format(r.reference_price, 2)}</dd></div><div class="detail-item"><dt>VALID UNTIL</dt><dd>${esc(stamp(r.valid_until_utc))}</dd></div><div class="detail-item"><dt>WINDOW START</dt><dd>${esc(stamp(r.start_utc))}</dd></div><div class="detail-item"><dt>WINDOW END</dt><dd>${esc(stamp(r.end_utc))}</dd></div></dl></div>`, `<span data-forecast="${h}">${flag(state, tone(state))}</span>`, source(`registry/${r.id}.json`, 'Frozen registration ↗'));
  }).join('');
  const scoring = table(['Horizon', 'Waiting maturity', 'Ready', 'Overdue', 'Failed', 'Scored'], HORIZONS.map(h => {
    const r = report.scoring?.[h] || {};
    return `<tr><td class="mono">${h}</td>${['waiting-maturity', 'ready', 'overdue', 'scoring-failed', 'scored'].map(k => `<td class="numeric">${format(r[k])}</td>`).join('')}</tr>`;
  }));
  const rows = report.evaluation?.horizons || {};
  const evidence = table(['Window', 'Pairs', 'MAE B2', 'MAE B0', 'B2 coverage', '95% interval of mean difference'], HORIZONS.map(h => {
    const r = rows[h] || {};
    return `<tr><td>${h}</td><td class="numeric">${format(r.n)}</td><td class="numeric">${format(r.mae_b2, 5)}</td><td class="numeric">${format(r.mae_b0, 5)}</td><td class="numeric">${percent(r.coverage_b2)}</td><td>${Array.isArray(r.diff_mean_ci95) ? esc(r.diff_mean_ci95.join(' to ')) : esc(r.uncertainty || 'Unavailable')}</td></tr>`;
  }));
  return `<div class="notice"><strong>Interpretation:</strong> these estimate full-window high-to-low range, not direction, price targets, or remaining range. Quantiles describe range magnitude. Expired forecasts remain visible as historical records.</div><div class="forecast-cards">${cards}</div><div class="workspace-grid section-gap">${panel('04', 'Scoring pipeline', scoring, '', `<span>Report ${esc(stamp(report.generated_utc))}</span>${source('reports/range.md')}`)}${panel('05', 'Model comparison', comparisons())}</div><div class="section-gap">${panel('06', 'Descriptive evidence', evidence, flag('Dependent windows', 'warn'), esc(report.evaluation.note))}</div>`;
}

function researchTable(designs, compact = false) {
  return table(compact ? ['Design', 'Evidence status', 'Checkpoint'] : ['Design / version', 'Evidence status', 'Integrity', 'Publication', 'Checkpoint'], designs.map(d => {
    const pending = d.checkpoints?.pending;
    const retained = pending?.retained, need = pending?.need;
    const progress = numeric(retained) && numeric(need) && need > 0 ? Math.min(100, retained / need * 100) : 0;
    return `<tr><td><button class="text-button" data-design="${esc(d.design)}">${esc(d.design)}</button><span class="sub">${esc(compact ? d.module?.replaceAll('_', ' ') : d.evaluation_version)}</span></td><td>${flag(d.status, d.status === 'supported' ? 'good' : 'warn')}</td>${compact ? '' : `<td>${flag(d.research_integrity?.status?.replaceAll('_', ' ') || 'unknown', tone(d.research_integrity?.status || ''))}</td><td>${d.publication?.evaluation_valid === true ? flag('Valid', 'good') : flag('Blocked / unknown', 'bad')}</td>`}<td class="mono">${format(retained)} / ${format(need)}<div class="small-progress" role="img" aria-label="${format(retained)} of ${format(need)} retained observations"><span style="width:${progress}%"></span></div></td></tr>`;
  }));
}
function research() {
  const all = data.research.designs;
  const visible = all.filter(d => (filter === 'all' || d.status === filter) && `${d.design} ${d.module} ${d.condition}`.toLowerCase().includes(query.toLowerCase()));
  const statuses = [...new Set(all.map(d => d.status))];
  exported = [['Design', 'Version', 'Status', 'Integrity', 'Publication valid', 'Retained', 'Checkpoint requirement', 'Card generated UTC', 'Observation cutoff UTC'], ...visible.map(d => [d.design, d.evaluation_version, d.status, d.research_integrity?.status, d.publication?.evaluation_valid, d.checkpoints?.pending?.retained, d.checkpoints?.pending?.need, d.generated_at, d.cutoff_utc])];
  return `<div class="toolbar"><div class="filter-group"><label class="filter-label" for="research-search">FIND</label><input class="input" id="research-search" placeholder="Search designs or questions…" value="${esc(query)}"><label class="filter-label" for="research-filter">STATUS</label><select class="select" id="research-filter"><option value="all">All evidence states</option>${statuses.map(s => `<option value="${esc(s)}" ${filter === s ? 'selected' : ''}>${esc(s)}</option>`).join('')}</select></div><span class="mini-text">${visible.length} / ${all.length} designs</span></div>${panel('01', 'Evidence register', researchTable(visible), reportTime(data.research.oldest_cutoff_utc, CLOCKS.research_observation_hours), `<span>Observation cutoff ${esc(stamp(data.research.oldest_cutoff_utc))} · index updated ${esc(stamp(data.research.index_updated_utc))}</span>${source('reports/research.md')}`)}<div class="notice section-gap">Checkpoint progress counts retained test observations. Meeting a count alone does not establish support: dependence blocks and the pre-registered decision rules also apply. Open any design to inspect its question and publication status.</div>${panel('02', 'What the signals mean', '<div class="panel-body"><div class="detail-grid" style="margin-top:0"><div><h3>Integrity</h3><p class="definition">Whether required inputs validated for this attempt. “Not required” is an explicit result for bar-based designs.</p></div><div><h3>Evidence maturity</h3><p class="definition">The research engine’s status, preserved as reported. A workflow pass, fresh data, or a small sample does not imply support.</p></div></div></div>')}${researchReadiness()}`;
}
function openDesign(id) {
  const d = data.research.designs.find(row => row.design === id);
  if (!d) return;
  const feasibility = data.feasibility.lab?.find(r => r.id === id && r.version === d.evaluation_version);
  $('#detail-body').innerHTML = `<h2>${esc(d.design)}</h2><p>${esc(d.condition)}</p><div class="section-gap">${flag(d.status, 'warn')} ${flag(d.research_integrity?.status?.replaceAll('_', ' ') || 'unknown')}</div><dl class="detail-grid">${[['VERSION', d.evaluation_version], ['PRIMARY HORIZON', `${d.primary_horizon_min} minutes`], ['CHECKPOINT', `${format(d.checkpoints?.pending?.retained)} / ${format(d.checkpoints?.pending?.need)} retained`], ['PUBLICATION', d.publication?.evaluation_valid ? 'Valid' : 'Blocked / unknown'], ['MIN. DEPENDENCE BLOCKS', d.min_dependence_blocks], ['GENERATED', stamp(d.generated_at)], ['OBSERVATION CUTOFF', stamp(d.cutoff_utc)]].map(([label, value]) => `<div class="detail-item"><dt>${label}</dt><dd>${esc(value)}</dd></div>`).join('')}</dl><h3 class="section-gap">Current assessment</h3><p>${esc(d.status_reason)}</p>${feasibility ? `<h3 class="section-gap">Limiting factor</h3><p>${esc(feasibility.limiting_factor)}. ${esc(feasibility.time_to_checkpoint_note)}</p>` : ''}<div class="section-gap">${source(d.source, 'Open full evidence card ↗')}</div>`;
  $('#detail').showModal();
}
$('#close-detail').addEventListener('click', () => $('#detail').close());

function health() {
  const h = data.health, all = h.sources;
  const visible = all.filter(s => s.name.toLowerCase().includes(query.toLowerCase()) && (filter !== 'issues' || s.ok !== s.observed || s.status !== 'ok'));
  visible.sort((a, b) => {const av = sort === 'coverage' ? (a.observed ? a.ok / a.observed : -1) : a.name;const bv = sort === 'coverage' ? (b.observed ? b.ok / b.observed : -1) : b.name; return (typeof av === 'string' ? av.localeCompare(bv) : av - bv) * (ascending ? 1 : -1);});
  const stats = `<div class="stats">${metric('Coverage report', currentAge(h.generated_utc), 'Refreshed by the six-hourly research lab', 'amber')}${metric('Sources observed', format(all.length), 'From the coverage report')}${metric('Latest status OK', `${all.filter(s => s.status === 'ok').length} / ${all.length}`, 'At report cutoff · not a live probe', 'positive')}${metric('Sources with failed calls', format(all.filter(s => s.ok < s.observed).length), 'Within this report window')}</div>`;
  const sources = table(['<button class="sort-button" data-sort="name">Source ↕</button>', 'OK / observed', '<button class="sort-button" data-sort="coverage">Availability ↕</button>', 'Latest reported status'], visible.map(s => `<tr><td class="mono">${esc(s.name)}</td><td class="numeric">${s.ok} / ${s.observed}</td><td class="numeric ${s.ok === s.observed ? 'source-good' : 'source-issue'}">${s.observed ? percent(s.ok / s.observed, 1) : '—'}</td><td>${esc(s.status)}</td></tr>`));
  const datasets = table(['Dataset', 'Latest observation written', 'Age now'], h.datasets.map(r => `<tr><td>${esc(r.name)}</td><td class="mono">${esc(stamp(r.observed_utc))}</td><td class="mono">${currentAge(r.observed_utc)}</td></tr>`));
  exported = [['Source', 'OK observations', 'Total observations', 'Availability', 'Status at cutoff', 'Report generated UTC'], ...visible.map(s => [s.name, s.ok, s.observed, s.observed ? s.ok / s.observed : null, s.status, h.generated_utc]), [], ['Health area', 'State on export clock', 'Detail'], ...opsRows(data.ops).map(r => [r.area, r.state, r.detail]), [], ['Market study area', 'State on export clock', 'Detail'], ...studyRows(data.studyOps).map(r => [r.area, r.state, r.detail])];
  const ops = opsRows(data.ops);
  const opsPanel = panel('00', 'Operational health', table(['Area', 'State on your clock', 'Detail'], ops.map(r => `<tr><td>${esc(r.area)}</td><td>${flag(r.state, tone(r.state))}</td><td class="mono">${esc(r.detail)}</td></tr>`)), '', `<span>Each row is judged separately; a green row says nothing about the others.</span>${source('reports/health.md')}`);
  const studies = studyRows(data.studyOps);
  const studiesPanel = panel('00B', 'Market study health', table(['Program', 'State on your clock', 'Coverage and diagnostics'], studies.map(r => `<tr><td>${esc(r.area)}</td><td>${flag(r.state, tone(r.state))}</td><td>${esc(r.detail)}</td></tr>`)), '', `<span>Operational targets do not change research thresholds. Pending outcomes are not missed forecasts.</span>${source('reports/market_study_health.md')}`);
  return opsPanel + `<div class="section-gap">${studiesPanel}</div>` + stats + `<div class="notice">Collection figures describe the report cutoff, ${esc(stamp(h.input_cutoff_utc))}. Ages below use your current clock; they do not prove the collector has stopped since that cutoff.</div><div class="toolbar"><div class="filter-group"><label class="filter-label" for="health-search">SOURCE</label><input id="health-search" class="input" placeholder="Filter sources…" value="${esc(query)}"><label class="filter-label" for="health-filter">SHOW</label><select id="health-filter" class="select"><option value="all">All sources</option><option value="issues" ${filter === 'issues' ? 'selected' : ''}>Sources with issues</option></select></div><span class="mini-text">${visible.length} sources</span></div><div class="workspace-grid">${panel('01', 'Source availability', sources, reportTime(h.input_cutoff_utc, CLOCKS.research_observation_hours), source('reports/latest.md'))}<div class="stack" style="grid-template-columns:1fr">${panel('02', 'Dataset freshness', datasets)}${panel('03', 'Recorded observations', h.alerts.length ? h.alerts.map(a => `<div class="alert-row"><span class="alert-dot"></span><p>${esc(a)}</p></div>`).join('') : '<div class="empty">No recorded alerts.</div>')}</div></div>`;
}

const clockRows = (kind, clocks) => table(['Clock', 'UTC', 'Age now', 'State'], clocks.map((c, i) => `<tr><td>${esc(c.label)}</td><td class="mono">${esc(stamp(c.value))}</td><td class="mono">${currentAge(c.value)}</td><td data-clock="${kind}:${i}">${flag(c.state, tone(c.state))}</td></tr>`));
function paper() {
  const p = data.paper, c = data.companion, pi = p.integrity || {}, ci = c.integrity || {};
  const rows = HORIZONS.map(h => pairedRow(h, c));
  exported = [['Horizon', 'State', 'Paired n', 'Excluded (integrity)', 'MAE B2', 'MAE B1', 'Mean B2 minus B1', 'Uncertainty', 'Companion integrity', 'Companion observation cutoff UTC'],
    ...rows.map(r => [r.horizon, r.state, r.n, r.excluded, r.maeFirst, r.maeSecond, r.diff, r.uncertainty, ci.ok === true ? 'ok' : 'FAILED', c.source_cutoff_utc])];
  const lr = pi.ledger_rows || {};
  const ledger = numeric(lr.physical) ? `${format(lr.physical)} physical · ${format(lr.verified)} verified · ${format(lr.quarantined)} quarantined · ${format(lr.excluded)} excluded · ${format(lr.in_progress)} in progress${numeric(lr.unaccounted) && lr.unaccounted ? ` · ${format(lr.unaccounted)} unaccounted` : ''}` : 'Not reported';
  const exclusions = (pi.excluded_decisions || []).map(x => `<div class="alert-row"><span class="alert-dot"></span><div>${esc(x.decision_id)} · ${x.integrity ? 'integrity' : 'lifecycle'}<p>${esc(x.reason)} — ${esc(x.disposition)}</p></div></div>`).join('');
  const failures = (list, title) => list?.length ? `<h3 class="section-gap negative">${title}</h3>${list.slice(0, 5).map(f => `<p class="definition">${esc(typeof f === 'string' ? f : `${f.id}: ${f.reason}`)}</p>`).join('')}` : '';
  const nc = data.ops?.ps1_coverage?.not_covered;
  const coverage = `<p class="definition">Coverage ${p.coverage == null ? '—' : esc(percent(p.coverage, 0))} as of this report (${esc(stamp(p.generated_utc))}). ${!data.ops ? 'Due decisions after it: unknown (no health report).' : nc?.length ? `Due since and not in it: ${esc(nc.map(x => `${x.decision_utc.slice(5, 16)} ${x.recorded_state}`).join('; '))}.` : 'No due decision since it.'}</p>`;
  const ps1 = `<div class="panel-body"><h3>${esc(p.reason || p.status)}</h3>${coverage}<p class="definition">${esc(p.label)}</p><dl class="detail-grid"><div class="detail-item"><dt>LIFECYCLE</dt><dd>${esc(p.lifecycle?.state)}${p.lifecycle?.paused_by ? ' · by ' + esc(p.lifecycle.paused_by) : ''}</dd></div><div class="detail-item"><dt>INTEGRITY</dt><dd>${flag(pi.state || (pi.ok === true ? 'verified' : 'failed / unknown'), tone(pi.state || (pi.ok === true ? 'verified' : 'failed')))}</dd></div><div class="detail-item"><dt>LEDGER ROWS</dt><dd>${esc(ledger)}</dd></div><div class="detail-item"><dt>RECORDED FAILURE ROWS</dt><dd>${format(pi.recorded_failures)} <span class="muted">(append-only history)</span></dd></div></dl>${failures(pi.failures, 'Unresolved — performance withheld')}${exclusions ? `<h3 class="section-gap">Excluded decisions</h3>${exclusions}` : ''}</div>${clockRows('paper', paperClocks(p))}`;
  const b1 = `<div class="panel-body"><h3>Does DVOL add to the forecast?</h3><p class="definition">B2 compared with B1 (HAR/calendar without DVOL), on the same eligible windows.</p><dl class="detail-grid"><div class="detail-item"><dt>REGISTERED</dt><dd>${format(c.registered)}</dd></div><div class="detail-item"><dt>CONFIRMED</dt><dd>${format(c.confirmed)}</dd></div><div class="detail-item"><dt>EVIDENCE CLASS</dt><dd>${esc(c.evidence_class)}</dd></div><div class="detail-item"><dt>INTEGRITY</dt><dd>${flag(ci.ok === true ? 'ok' : 'failed / unknown', ci.ok === true ? 'good' : 'bad')}</dd></div></dl>${failures(ci.failures_now, 'Integrity exclusions now — affected horizons withheld')}</div>${clockRows('companion', companionClocks(c))}`;
  const paired = table(['Window', 'State', 'Pairs', 'Excluded (integrity)', 'MAE B2', 'MAE B1', 'Mean difference', 'Uncertainty'], rows.map(r => `<tr><td>${r.horizon}</td><td>${flag(r.state, tone(r.state))}</td><td class="numeric">${format(r.n)}</td><td class="numeric">${format(r.excluded)}</td><td class="numeric">${format(r.maeFirst, 5)}</td><td class="numeric">${format(r.maeSecond, 5)}</td><td class="numeric">${format(r.diff, 5)}</td><td>${esc(r.uncertainty)}</td></tr>`));
  return `<div class="notice"><strong>PAPER RESEARCH ONLY.</strong> ${esc(p.label)} Range-forecast accuracy (B1), simulated sizing (PS1) and live trading are different evidence; none is a trading edge.</div><div class="stats">${metric('PS1 status', esc(p.status), esc(p.protocol), 'amber')}${metric('Decisions', format(p.scheduled_decisions ?? p.decisions_recorded), p.launch ? 'Scheduled since launch' : 'Recorded before launch')}${metric('Verified executions', format(pi.verified_executions), 'Verified only; see ledger rows for completeness')}${metric('Evidence class', esc(p.evidence_class), 'Preserved from the experiment report')}</div><div class="workspace-grid">${panel('01', 'PS1 sizing experiment', ps1, '', source('reports/paper_ps1.md'))}${panel('02', 'Companion B1', b1, '', source('reports/companion_b1.md'))}</div><div class="section-gap">${panel('03', 'Paired B2 / B1 evidence', paired, flag('Descriptive', 'warn'), '<span>MAE of ln range · negative difference favors B2 · overlapping windows are dependent · withheld horizons show no figures.</span>')}</div>`;
}

function reports() {
  const reports = [
    ['COLLECTION', 'Collection health', 'Data age, source coverage, cadence, and collection observations.', 'reports/latest.md'],
    ['RESEARCH', 'Research evidence', 'Design status, integrity, publication checks, and evidence cards.', 'reports/research.md'],
    ['FORECASTS', 'Range model', 'Registered ranges, availability, scoring, and baseline comparisons.', 'reports/range.md'],
    ['COMPANION', 'B1 comparison', 'Paired comparisons with and without the DVOL feature.', 'reports/companion_b1.md'],
    ['PAPER DESK', 'PS1 sizing experiment', 'Simulated execution, lifecycle, and protocol evidence.', 'reports/paper_ps1.md'],
    ['MARKET STUDIES', 'Experiments and pilots', 'Independent prospective experiments and data usability pilots.', 'reports/market_studies.md'],
    ['STUDY HEALTH', 'Coverage and deadlines', 'Rolling coverage, missed opportunities, unique entries, and options quality.', 'reports/market_study_health.md'],
    ['FEASIBILITY', 'Evidence readiness', 'Warm-up, observation counts, and limiting factors.', 'reports/feasibility.md'],
    ['GOVERNANCE', 'Skill proposals', 'Proposed changes and reasons that no proposal is eligible.', 'reports/skill_proposals.md'],
    ['OPERATIONS', 'Operations guide', 'Collection, deployment, scoring, and operating procedures.', 'docs/OPERATIONS.md'],
    ['VALIDATION', 'Validation record', 'How the research system was tested and deployed.', 'VALIDATION.md'],
  ];
  if (data.developments) reports.push(
    ['RESEARCH TOOLS', 'Research interface', 'Shared evidence contract, research queries, and prepared experiment tools.', 'docs/RESEARCH_INTERFACE.md'],
    ['RELEASE NOTES', 'Repository changes', 'Recent revisions, causes, implementation changes, and validation records.', 'CHANGELOG.md']
  );
  exported = [['Source file', 'SHA-256', 'Snapshot commit'], ...Object.entries(data.sources).map(([path, hash]) => [path, hash, data.commit])];
  return `<div class="notice">Every report link is pinned to the dashboard’s source commit. Data generation times may differ by pipeline; a new dashboard build does not make old research fresh.</div><div class="report-grid">${reports.map(([category, title, description, path]) => `<a class="report-card" href="${esc(sourceURL(path))}" target="_blank" rel="noopener noreferrer"><span class="eyebrow">${category}</span><h3>${title}</h3><p>${description}</p><span class="report-link">OPEN SOURCE REPORT ↗</span></a>`).join('')}</div>${acceptanceDetail()}<div class="section-gap">${panel('A2', 'Snapshot provenance', `<div class="panel-body"><dl class="detail-grid" style="margin-top:0"><div class="detail-item"><dt>SOURCE COMMIT</dt><dd>${esc(data.commit)}</dd></div><div class="detail-item"><dt>DASHBOARD BUILT</dt><dd>${esc(stamp(data.built_utc))}</dd></div><div class="detail-item"><dt>SOURCE FILE HASHES</dt><dd>${Object.keys(data.sources).length} SHA-256 records · export above</dd></div><div class="detail-item"><dt>DATA FORMAT</dt><dd>${esc(data.schema)} · <a href="data.json" download>Download snapshot JSON ↓</a></dd></div></dl></div>`)}</div>`;
}

const renderers = { overview, forecasts, research, health, paper, reports };
function render() {
  if (!data) return;
  chartObserver?.disconnect();
  $('#page-title').textContent = pages[page][0];
  $('#page-code').textContent = pageCodes[page];
  document.title = `JBM | ${pages[page][0]}`;
  $('#page-description').textContent = pages[page][1];
  $$('[data-page]').forEach(a => { if (a.dataset.page === page) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
  $('#view').innerHTML = renderers[page]();
  $('#view').setAttribute('aria-busy', 'false');
  $('#export').disabled = false;
  $('#export').textContent = page === 'reports' ? 'Export audit CSV ↓' : page === 'paper' ? 'Export B1 comparison ↓' : 'Export CSV ↓';
  $('#snapshot-bar').innerHTML = (refreshError ? `<span role="alert" class="negative">Refresh failed (${esc(refreshError)}). Showing the previous snapshot; its original timestamps still apply.</span>` : '') + `<span><strong>REPOSITORY SNAPSHOT</strong> <span class="divider">/</span> Built ${esc(stamp(data.built_utc))}</span><span>Research evidence ${reportTime(data.research.oldest_cutoff_utc, CLOCKS.research_observation_hours)} <span class="divider">/</span> Range report ${flag(reportExpiry(data.range), tone(reportExpiry(data.range)))}</span>`;
  $('#build-meta').textContent = `${data.commit?.slice(0, 8) || 'Unversioned'} · Read-only · UTC`;
  $$('[data-design]').forEach(b => b.addEventListener('click', () => openDesign(b.dataset.design)));
  $$('[data-period]').forEach(b => b.addEventListener('click', () => {period = b.dataset.period;save('period', period);$$('[data-period]').forEach(v => v.setAttribute('aria-pressed', String(v.dataset.period === period)));safeDraw();}));
  for (const id of ['research-search', 'health-search']) {
    const input = $('#' + id);
    input?.addEventListener('input', () => {const pos = input.selectionStart;query = input.value;render();const next = $('#' + id);next.focus();next.setSelectionRange(pos, pos);});
  }
  for (const id of ['research-filter', 'health-filter']) $('#' + id)?.addEventListener('change', e => {filter = e.target.value;render();$('#' + id)?.focus();});
  $$('[data-sort]').forEach(b => b.addEventListener('click', () => {ascending = sort === b.dataset.sort ? !ascending : true;sort = b.dataset.sort;render();}));
  let drawError = null;
  if ($('#market-chart')) {drawError = safeDraw();chartObserver = new ResizeObserver(() => safeDraw());chartObserver.observe($('#market-chart'));}
  tick();
  return drawError;
}
// A chart failure stays inside the chart box: the snapshot, navigation and every other view remain usable.
function safeDraw() {
  try { drawMarket(); return null; }
  catch (err) {
    const box = $('#market-chart');
    if (box) box.innerHTML = `<div class="empty" role="alert">Chart unavailable: ${esc(err.message)}. Prices are not substituted.</div>`;
    return err;
  }
}
function route() {
  const next = location.hash.slice(1);
  page = pages[next] ? next : 'overview';
  query = ''; filter = 'all'; save('page', page);render();
}
window.addEventListener('hashchange', route);
window.addEventListener('keydown', event => {
  if (!event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || event.repeat
      || event.target?.closest?.('input, select, textarea, [contenteditable="true"]') || $('#detail').open) return;
  const number = /^Digit[1-6]$/.test(event.code) ? Number(event.code.slice(-1)) : 0;
  if (number) { event.preventDefault(); location.hash = Object.keys(pages)[number - 1]; }
});
$('#export').addEventListener('click', () => {
  if (page === 'forecasts') forecasts(); // Revalidate availability at export time.
  const blob = new Blob(['\uFEFF' + csv(exported)], {type: 'text/csv;charset=utf-8'});
  const link = document.createElement('a');link.href = URL.createObjectURL(blob);link.download = `jbm-${page}-${new Date().toISOString().slice(0, 10)}.csv`;link.click();setTimeout(() => URL.revokeObjectURL(link.href), 1000);
});
function tick() {
  $('#utc-clock').textContent = new Date().toISOString().slice(11, 19) + ' UTC';
  $$('[data-age]').forEach(el => el.textContent = ageLabel(el.dataset.age));
  $$('[data-freshness]').forEach(el => {const state = freshness(el.dataset.freshness, Number(el.dataset.hours));el.innerHTML = flag(state, tone(state));});
  if (data) $$('[data-clock]').forEach(el => {const [kind, i] = el.dataset.clock.split(':');const c = (kind === 'paper' ? paperClocks(data.paper) : companionClocks(data.companion))[Number(i)];if (c) el.innerHTML = flag(c.state, tone(c.state));});
  if (data) $$('[data-forecast]').forEach(el => {const state = forecastState(data.range.current[el.dataset.forecast], data.range);el.innerHTML = flag(state, tone(state));});
}
setInterval(tick, 1000);
function renderAllWith(candidate) {
  // Render every view against the candidate without touching the live state; restore it whatever happens.
  const saved = {data, exported, page};
  try {
    data = candidate;
    for (const name of Object.keys(renderers)) { page = name; renderers[name](); }
    for (const p of ['1D', '3D', '7D']) chartPoints(candidate.market.bars, parseInt(p, 10));
  } finally {
    ({data, exported, page} = saved);
  }
}
async function load() {
  $('#refresh').disabled = true;$('#refresh').textContent = 'Loading…';
  const previous = {data, page};
  try {
    let candidate, failure = null;
    try {
      const response = await fetch('./data.json', {cache: 'no-store'});
      if (!response.ok) throw new Error(`Snapshot request failed (${response.status})`);
      candidate = await response.json();
    } catch (err) { failure = err.message || String(err); }
    const result = failure ? {data, error: failure} : stage(data, candidate, renderAllWith);
    refreshError = result.error;
    if (result.data !== data) {
      data = result.data;
      if (!location.hash) {const remembered = stored('page', 'overview');history.replaceState(null, '', '#' + (pages[remembered] ? remembered : 'overview'));}
      page = pages[location.hash.slice(1)] ? location.hash.slice(1) : 'overview';
    }
    if (data) {
      let failed = null;
      try { failed = render(); } catch (err) { failed = err; }
      if (failed && data !== previous.data) {
        // The committed snapshot failed in the live DOM: return to the last good one (its own timestamps and
        // provenance) and keep the failure on screen. If that one cannot draw its chart either, the chart box says so.
        ({data, page} = previous);
        refreshError = `Snapshot failed to render: ${failed.message}`;
        if (data) render(); else throw failed;
      } else if (failed instanceof Error && !$('#market-chart')) throw failed;
    } else {
      $('#view').innerHTML = `<div class="panel empty" role="alert"><h3>Snapshot unavailable</h3><p>${esc(refreshError)}</p><p class="section-gap">Use Refresh to retry, or <a class="amber" href="https://github.com/mannoj93-spec/jbm-desk-data/tree/main/reports">open the source reports ↗</a>.</p></div>`;
      $('#snapshot-bar').textContent = 'DATA UNAVAILABLE · No values have been substituted.';$('#view').setAttribute('aria-busy', 'false');
    }
  } catch (err) {
    $('#view').innerHTML = `<div class="panel empty" role="alert"><h3>Snapshot unavailable</h3><p>${esc(err.message || String(err))}</p></div>`;
    $('#snapshot-bar').textContent = 'DATA UNAVAILABLE · No values have been substituted.';
  } finally {
    $('#refresh').disabled = false;$('#refresh').textContent = '↻ Refresh';
  }
}
$('#refresh').addEventListener('click', load);
load();
