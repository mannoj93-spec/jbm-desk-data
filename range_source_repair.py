"""Controlled source repair and month readiness outside the frozen forecasting implementation.

Approved interior gaps are listed in research_tools/source_repairs.json. Each entry names one run of at
most six consecutive BTCUSDT 4h bars lying at least one day inside a single month, and pins the reviewed
evidence file by hash. A repair requires the checksum-matched monthly archive, all 12 neighbouring
API/archive bars matching exactly, retained raw responses, and the unchanged DVOL admission contract.
Adding an entry is an approval: it is made by a reviewed pull request, never by a workflow.
No forecast, decision timestamp, prior fit, or missed opportunity is rewritten.
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
from pathlib import Path
import urllib.request

from desk import range_job as J

A, C, UTC = J.A, J.C, dt.timezone.utc
ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / 'research_tools/source_repairs.json'
REGISTRY_SCHEMA = 'approved-range-source-repairs/1'
STEP = dt.timedelta(hours=4)
DAY = dt.timedelta(days=1)
MAX_GAP_BARS = 6          # the approved shape: at most one day of 4h bars
NEIGHBOURS = 6            # exact-match bars required on each side of the gap
MAX_TAIL_DAYS = 3          # trailing unpublished archive days the readiness check tolerates


class Spec:
    """One approved gap: its bars, month and the API window that must overlap the archive exactly."""

    def __init__(self, first_open_utc, bars, evidence=None, evidence_file_sha256=None, approved=None):
        first = J.R._t(first_open_utc)
        if not isinstance(bars, int) or isinstance(bars, bool) or not 1 <= bars <= MAX_GAP_BARS:
            raise ValueError(f'Repair refused: a gap of {bars!r} bars is outside the approved shape (1-{MAX_GAP_BARS})')
        if first != first.replace(minute=0, second=0, microsecond=0) or first.hour % 4:
            raise ValueError('Repair refused: gap does not start on a 4h open')
        self.start = first.replace(day=1, hour=0)
        self.end = self.start.replace(year=self.start.year + (self.start.month == 12), month=self.start.month % 12 + 1)
        self.gap = [J._iso(first + i * STEP) for i in range(bars)]
        self.api_start = first - NEIGHBOURS * STEP
        self.api_end = first + (bars + NEIGHBOURS) * STEP
        if self.api_start < self.start or self.api_end > self.end:
            raise ValueError('Repair refused: gap is within one day of a month edge')
        self.gap_month = f'{self.start:%Y-%m}'
        self.fit_month = f'{self.end:%Y-%m}'
        self.month_bars = int((self.end - self.start) / STEP)
        self.api_url = ('https://www.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=4h'
                        f'&startTime={J._ms(self.api_start)}&endTime={J._ms(self.api_end)-1}&limit=30')
        self.evidence = ROOT / evidence if evidence else None
        self.evidence_file_sha256 = evidence_file_sha256
        self.approved = approved


def approved(path=REGISTRY):
    """Approved repairs in month order. One gap per month; every entry pins its evidence file."""
    doc = json.loads(Path(path).read_text())
    if doc.get('schema') != REGISTRY_SCHEMA or not isinstance(doc.get('repairs'), list):
        raise ValueError('Unknown source-repair registry schema')
    specs = []
    for e in doc['repairs']:
        if not all(isinstance(e.get(k), str) and e[k] for k in ('gap_first_open_utc', 'evidence', 'evidence_file_sha256', 'approved')):
            raise ValueError('Source-repair registry entry is incomplete')
        specs.append(Spec(e['gap_first_open_utc'], e.get('gap_bars'), e['evidence'], e['evidence_file_sha256'], e['approved']))
    if len({s.gap_month for s in specs}) != len(specs):
        raise ValueError('Two approved repairs for one month')
    return sorted(specs, key=lambda s: s.start)


OCTOBER_2026 = approved()[0]
# Names kept from 2.30.7 for the first approved repair (BTCUSDT 4h, 2026-10-28).
EVIDENCE = OCTOBER_2026.evidence
START, END, GAP = OCTOBER_2026.start, OCTOBER_2026.end, OCTOBER_2026.gap
API_START, API_END, API_URL = OCTOBER_2026.api_start, OCTOBER_2026.api_end, OCTOBER_2026.api_url


def missing(rows, start, end):
    times = {b['open_utc'] for b in rows}
    return [J._iso(start + i * STEP) for i in range(int((end-start)/STEP))
            if J._iso(start + i * STEP) not in times]


def repaired_bars(state, archive, report, raw, spec=None):
    spec = spec or OCTOBER_2026
    if (state != 'incomplete' or report.get('malformed_rows') or report.get('conflicting_bars_excluded')
            or report.get('exact_duplicates_dropped') or report['prov'].get('checksum_status') != 'match'
            or missing(archive, spec.start, spec.end) != spec.gap or len(archive) != spec.month_bars - len(spec.gap)):
        raise ValueError('Repair refused: archive does not match the approved gap')
    values = json.loads(raw)
    if not isinstance(values, list) or any(not isinstance(r, list) or len(r) != len(A.KLINE_COLS) for r in values):
        raise ValueError('Repair API response is not a kline array')
    api_state, api, api_report = A.inspect_klines(
        [dict(zip(A.KLINE_COLS, map(str, row))) for row in values], spec.api_start, spec.api_end, '4h')
    if api_state != 'ok' or len(api) != len(spec.gap) + 2 * NEIGHBOURS or api_report['exact_duplicates_dropped']:
        raise ValueError('Repair API window is incomplete, duplicated or malformed')
    known = {r['open_utc']: r for r in archive}
    overlap = [r for r in api if r['open_utc'] in known]
    fields = ('open', 'high', 'low', 'close', 'volume', 'taker_buy_volume', 'close_utc', 'available_at_utc')
    if len(overlap) != 2 * NEIGHBOURS or any(any(r[k] != known[r['open_utc']][k] for k in fields) for r in overlap):
        raise ValueError('Repair API/archive overlap differs')
    sha = hashlib.sha256(raw).hexdigest()
    fill = [dict(r, source_sha256=sha, source_role='approved-interior-repair') for r in api if r['open_utc'] in spec.gap]
    rows = sorted(archive + fill, key=lambda r: r['open_utc'])
    if len(rows) != spec.month_bars or missing(rows, spec.start, spec.end):
        raise ValueError('Repaired month remains incomplete')
    return rows, {'overlap_checked': 2 * NEIGHBOURS, 'fields_checked': list(fields), 'filled': spec.gap,
                  'api_sha256': sha, 'archive_sha256': report['prov']['sha256']}


def capture_evidence(path=None, spec=None):
    """Explicit one-time preparation only. Normal workflows replay reviewed bytes offline."""
    spec = spec or OCTOBER_2026
    path = Path(path or spec.evidence)
    responses = {}
    def get(url):
        sent = J._iso(J._now())
        with urllib.request.urlopen(urllib.request.Request(url, headers=A.UA), timeout=60) as r:
            raw, headers = r.read(), dict(r.headers)
        responses[url] = {'raw_base64': base64.b64encode(raw).decode(), 'sha256': hashlib.sha256(raw).hexdigest(),
                          'headers': headers, 'sent_utc': sent, 'received_utc': J._iso(J._now())}
        return raw, headers
    state, archive, report = A.load_klines(spec.gap_month, '4h', opener=get)
    api, _ = get(spec.api_url)
    repaired_bars(state, archive, report, api, spec)
    dstate, dvol, drep = A.load_dvol(spec.start, spec.end, opener=get)
    C.admit_dvol(dstate, dvol, spec.end, drep, 'history')
    data = {'schema': 'reviewed-range-source-repair/1', 'captured_utc': J._iso(J._now()),
            'archive_report': report, 'dvol_report': drep, 'responses': responses}
    replay_evidence(data, spec)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')
    return data


def replay_evidence(data, spec=None):
    spec = spec or OCTOBER_2026
    if data['schema'] != 'reviewed-range-source-repair/1':
        raise ValueError('Unknown repair evidence schema')
    responses = data['responses']
    def get(url):
        r = responses[url]
        raw = base64.b64decode(r['raw_base64'], validate=True)
        if hashlib.sha256(raw).hexdigest() != r['sha256']:
            raise ValueError('Retained repair response hash mismatch')
        if not spec.end <= J.R._t(r['sent_utc']) <= J.R._t(r['received_utc']) <= J.R._t(data['captured_utc']):
            raise ValueError('Invalid retained repair retrieval clock')
        return raw, r['headers']
    state, archive, report = A.load_klines(spec.gap_month, '4h', opener=get)
    raw, _ = get(spec.api_url)
    bars, repair = repaired_bars(state, archive, report, raw, spec)
    dstate, dvol, drep = A.load_dvol(spec.start, spec.end, opener=get)
    admit = C.admit_dvol(dstate, dvol, spec.end, drep, 'history')
    # The parser's current replay clock is not the original retrieval clock.
    report['prov']['retrieved_at_utc'] = responses[A.kline_url('4h', spec.gap_month)]['received_utc']
    drep['retrieved_at_utc'] = data['captured_utc']
    return {'month': spec.fit_month, 'bars': bars, 'dvol': dvol,
            'manifest': [A.manifest_entry(state, report)], 'dvol_report': drep, 'dvol_admissibility': admit,
            'source_repair': dict(repair, retrieved_utc=data['captured_utc'],
                                 evidence_sha256=hashlib.sha256(C.canonical(data)).hexdigest()),
            'interpretation': 'Historical training input repair approved prospectively; not an on-time forecast or a backfill.'}


def prepare(base=ROOT, now=None, evidence=None, registry=REGISTRY):
    now = now or J._now()
    m0 = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if J.fit_path(m0.date(), base).exists():
        J.load_fit(base, m0)
        return {'state': 'fit-valid', 'month': f'{m0:%Y-%m}'}
    bars, _, _ = J.history_chain(base)
    last = J.R._t(bars[-1]['open_utc'])
    for spec in approved(registry):
        if last == spec.start - STEP and m0 >= spec.end:
            raw = Path(evidence or spec.evidence).read_bytes()
            if evidence is None and hashlib.sha256(raw).hexdigest() != spec.evidence_file_sha256:
                raise ValueError(f'Repair evidence for {spec.gap_month} does not match its approved hash')
            data = json.loads(raw)
            if J.R._t(data['captured_utc']) > now:
                raise ValueError('Repair evidence is from the future')
            delta = replay_evidence(data, spec)
            # Retain the complete raw-response evidence alongside the content-addressed training delta.
            J.write_blob(base, 'desk/inputs/source-repairs', data)
            J.write_blob(base, 'desk/inputs/refit', delta)
            last = spec.end - STEP
    if last < m0 - STEP:
        state, rows, manifest = A.load_klines_span((last+STEP).date(), (m0-dt.timedelta(days=1)).date(), '4h')
        holes = missing(rows, last+STEP, m0)
        print(json.dumps({'month': f'{m0:%Y-%m}', 'archive_state': state, 'missing_4h_opens': holes,
                          'manifest': manifest}, sort_keys=True))
        # Existing frozen refit still decides whether an unpublished trailing segment is admissible.
    return {'state': 'ready-for-frozen-refit', 'month': f'{m0:%Y-%m}'}


def readiness(now=None, span=None):
    """Read-only daily check of closed archive history; never substitutes API data or changes a fit.

    Days 1-3 check the whole previous month, which the refit at the month start needs. Every later day
    checks the current month through yesterday, so an interior gap is reported the day after it appears
    instead of in the last days of the month. Holes that are only the unpublished trailing days are
    'ready-unpublished-tail': the frozen refit fills an unpublished trailing segment from closed live bars.
    """
    now = now or J._now()
    span = span or A.load_klines_span
    month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.day <= 3:
        end = month
        start = (month-dt.timedelta(days=1)).replace(day=1)
    else:
        start, end = month, now.replace(hour=0, minute=0, second=0, microsecond=0)
    state, rows, manifest = span(start.date(), (end-dt.timedelta(days=1)).date(), '4h')
    holes = missing(rows, start, end)
    states = [(m or {}).get('state') for m in manifest]
    tail = []
    for i in range(1, len(holes) + 1):                      # holes running back from the end of the window
        if holes[-i] != J._iso(end - i * STEP):
            break
        tail.append(holes[-i])
    tail_days = sorted({t[:10] for t in tail})
    trailing_missing = 0                                    # unpublished files at the end of the manifest
    for st in reversed(states):
        if st != 'missing':
            break
        trailing_missing += 1
    unpublished = (bool(tail) and len(tail) == 6 * len(tail_days) and len(tail_days) <= MAX_TAIL_DAYS
                   and trailing_missing >= 1 and 'missing' not in states[:len(states) - trailing_missing])
    interior = [h for h in holes if not (unpublished and h in tail)]
    known = {t for s in approved() for t in s.gap}
    bad = sorted({x for x in states + [state] if x not in ('ok', 'missing', 'incomplete')})
    if bad or (interior and not set(interior) <= known) or (not holes and state != 'ok'):
        result = 'blocked'
    elif interior:
        result = 'ready-approved-repair'
    elif holes:
        result = 'ready-unpublished-tail'
    else:
        result = 'ready'
    return {'state': result,
            'checked_utc': J._iso(now), 'from_utc': J._iso(start), 'through_utc_exclusive': J._iso(end),
            'archive_state': state, 'missing_4h_opens': holes, 'manifest': manifest,
            'unapproved_interior_4h_opens': [h for h in interior if h not in known],
            'unpublished_tail_4h_opens': sorted(tail) if unpublished else [], 'inadmissible_states': bad,
            'interpretation': 'Closed archive history only; a final incomplete day is not assessed before it closes. '
                              'No automatic interior-gap repair: a new gap needs reviewed evidence and a registry entry.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=['capture-evidence', 'refit', 'readiness'])
    ap.add_argument('--as-of', help='readiness: assess as of this UTC time (YYYY-MM-DDTHH:MM:SSZ); a rehearsal, read-only')
    ap.add_argument('--gap-first-open', help='capture-evidence: first missing 4h open (UTC)')
    ap.add_argument('--gap-bars', type=int, help=f'capture-evidence: consecutive missing bars (1-{MAX_GAP_BARS})')
    ap.add_argument('--out', help='capture-evidence: evidence file to write')
    args = ap.parse_args()
    if args.command == 'capture-evidence':
        if not (args.gap_first_open and args.gap_bars and args.out):
            ap.error('capture-evidence needs --gap-first-open, --gap-bars and --out')
        path = Path(args.out).resolve()
        if path.exists():
            ap.error(f'{args.out} exists; reviewed evidence is never overwritten')
        data = capture_evidence(path, Spec(args.gap_first_open, args.gap_bars))
        print(json.dumps({'evidence': args.out, 'evidence_file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                          'captured_utc': data['captured_utc'],
                          'next': 'review the evidence, then add a registry entry by pull request'}, sort_keys=True))
    elif args.command == 'readiness':
        result = readiness(J.R._t(args.as_of) if args.as_of else None)
        print(json.dumps(result, indent=2, sort_keys=True))
        raise SystemExit(int(result['state'] == 'blocked'))
    else:
        print(json.dumps(prepare(), sort_keys=True))
        J.refit()


if __name__ == '__main__':
    main()
