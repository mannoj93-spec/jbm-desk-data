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
