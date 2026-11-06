"""Controlled source repair and month readiness outside the frozen forecasting implementation.

The sole approved interior gap is BTCUSDT 4h, 2026-10-28. It requires the
checksum-matched October archive, all 12 neighbouring API/archive bars matching
exactly, retained raw responses, and the unchanged DVOL admission contract.
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
EVIDENCE = ROOT / 'research_tools/fixtures/november_2026_source_repair.json'
STEP = dt.timedelta(hours=4)
START = dt.datetime(2026, 10, 1, tzinfo=UTC)
END = dt.datetime(2026, 11, 1, tzinfo=UTC)
GAP = [J._iso(dt.datetime(2026, 10, 28, h, tzinfo=UTC)) for h in range(0, 24, 4)]
API_START = dt.datetime(2026, 10, 27, tzinfo=UTC)
API_END = dt.datetime(2026, 10, 30, tzinfo=UTC)
API_URL = ('https://www.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=4h'
           f'&startTime={J._ms(API_START)}&endTime={J._ms(API_END)-1}&limit=30')


def missing(rows, start, end):
    times = {b['open_utc'] for b in rows}
    return [J._iso(start + i * STEP) for i in range(int((end-start)/STEP))
            if J._iso(start + i * STEP) not in times]


def repaired_bars(state, archive, report, raw):
    if (state != 'incomplete' or report.get('malformed_rows') or report.get('conflicting_bars_excluded')
            or report.get('exact_duplicates_dropped') or report['prov'].get('checksum_status') != 'match'
            or missing(archive, START, END) != GAP or len(archive) != 180):
        raise ValueError('Repair refused: archive does not match the approved six-bar gap')
    values = json.loads(raw)
    if not isinstance(values, list) or any(not isinstance(r, list) or len(r) != len(A.KLINE_COLS) for r in values):
        raise ValueError('Repair API response is not a kline array')
    api_state, api, api_report = A.inspect_klines(
        [dict(zip(A.KLINE_COLS, map(str, row))) for row in values], API_START, API_END, '4h')
    if api_state != 'ok' or len(api) != 18 or api_report['exact_duplicates_dropped']:
        raise ValueError('Repair API window is incomplete, duplicated or malformed')
    known = {r['open_utc']: r for r in archive}
    overlap = [r for r in api if r['open_utc'] in known]
    fields = ('open', 'high', 'low', 'close', 'volume', 'taker_buy_volume', 'close_utc', 'available_at_utc')
    if len(overlap) != 12 or any(any(r[k] != known[r['open_utc']][k] for k in fields) for r in overlap):
        raise ValueError('Repair API/archive overlap differs')
    sha = hashlib.sha256(raw).hexdigest()
    fill = [dict(r, source_sha256=sha, source_role='approved-interior-repair') for r in api if r['open_utc'] in GAP]
    rows = sorted(archive + fill, key=lambda r: r['open_utc'])
    if len(rows) != 186 or missing(rows, START, END):
        raise ValueError('Repaired month remains incomplete')
    return rows, {'overlap_checked': 12, 'fields_checked': list(fields), 'filled': GAP,
                  'api_sha256': sha, 'archive_sha256': report['prov']['sha256']}


def capture_evidence(path=EVIDENCE):
    """Explicit one-time preparation only. Normal workflows replay reviewed bytes offline."""
    responses = {}
    def get(url):
        sent = J._iso(J._now())
        with urllib.request.urlopen(urllib.request.Request(url, headers=A.UA), timeout=60) as r:
            raw, headers = r.read(), dict(r.headers)
        responses[url] = {'raw_base64': base64.b64encode(raw).decode(), 'sha256': hashlib.sha256(raw).hexdigest(),
                          'headers': headers, 'sent_utc': sent, 'received_utc': J._iso(J._now())}
        return raw, headers
    state, archive, report = A.load_klines('2026-10', '4h', opener=get)
    api, _ = get(API_URL)
    repaired_bars(state, archive, report, api)
    dstate, dvol, drep = A.load_dvol(START, END, opener=get)
    C.admit_dvol(dstate, dvol, END, drep, 'history')
    data = {'schema': 'reviewed-range-source-repair/1', 'captured_utc': J._iso(J._now()),
            'archive_report': report, 'dvol_report': drep, 'responses': responses}
    replay_evidence(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')
    return data


def replay_evidence(data):
    if data['schema'] != 'reviewed-range-source-repair/1':
        raise ValueError('Unknown repair evidence schema')
    responses = data['responses']
    def get(url):
        r = responses[url]
        raw = base64.b64decode(r['raw_base64'], validate=True)
        if hashlib.sha256(raw).hexdigest() != r['sha256']:
            raise ValueError('Retained repair response hash mismatch')
        if not END <= J.R._t(r['sent_utc']) <= J.R._t(r['received_utc']) <= J.R._t(data['captured_utc']):
            raise ValueError('Invalid retained repair retrieval clock')
        return raw, r['headers']
    state, archive, report = A.load_klines('2026-10', '4h', opener=get)
    raw, _ = get(API_URL)
    bars, repair = repaired_bars(state, archive, report, raw)
    dstate, dvol, drep = A.load_dvol(START, END, opener=get)
    admit = C.admit_dvol(dstate, dvol, END, drep, 'history')
    # The parser's current replay clock is not the original retrieval clock.
    report['prov']['retrieved_at_utc'] = responses[A.kline_url('4h', '2026-10')]['received_utc']
    drep['retrieved_at_utc'] = data['captured_utc']
    return {'month': '2026-11', 'bars': bars, 'dvol': dvol,
            'manifest': [A.manifest_entry(state, report)], 'dvol_report': drep, 'dvol_admissibility': admit,
            'source_repair': dict(repair, retrieved_utc=data['captured_utc'],
                                 evidence_sha256=hashlib.sha256(C.canonical(data)).hexdigest()),
            'interpretation': 'Historical training input repair approved prospectively; not an on-time forecast or a backfill.'}


def prepare(base=ROOT, now=None, evidence=EVIDENCE):
    now = now or J._now()
    m0 = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if J.fit_path(m0.date(), base).exists():
        J.load_fit(base, m0)
        return {'state': 'fit-valid', 'month': f'{m0:%Y-%m}'}
    bars, _, _ = J.history_chain(base)
    last = J.R._t(bars[-1]['open_utc'])
    if last == START - STEP and m0 >= END:
        data = json.loads(Path(evidence).read_text())
        if J.R._t(data['captured_utc']) > now:
            raise ValueError('Repair evidence is from the future')
        delta = replay_evidence(data)
        # Retain the complete raw-response evidence alongside the content-addressed training delta.
        J.write_blob(base, 'desk/inputs/source-repairs', data)
        J.write_blob(base, 'desk/inputs/refit', delta)
        last = END - STEP
    if last < m0 - STEP:
        state, rows, manifest = A.load_klines_span((last+STEP).date(), (m0-dt.timedelta(days=1)).date(), '4h')
        holes = missing(rows, last+STEP, m0)
        print(json.dumps({'month': f'{m0:%Y-%m}', 'archive_state': state, 'missing_4h_opens': holes,
                          'manifest': manifest}, sort_keys=True))
        # Existing frozen refit still decides whether an unpublished trailing segment is admissible.
    return {'state': 'ready-for-frozen-refit', 'month': f'{m0:%Y-%m}'}



def readiness(now=None, span=None):
    """Read-only month-end check; never substitutes API data or changes a fit."""
    now = now or J._now()
    span = span or A.load_klines_span
    month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = month.replace(year=month.year + (month.month == 12), month=month.month % 12 + 1)
    if now.day <= 3:
        end = month
        start = (month-dt.timedelta(days=1)).replace(day=1)
    elif (next_month-now).total_seconds() <= 4*86400:
        start, end = month, now.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        return {'state': 'outside-month-boundary-window', 'checked_utc': J._iso(now)}
    state, rows, manifest = span(start.date(), (end-dt.timedelta(days=1)).date(), '4h')
    holes = missing(rows, start, end)
    return {'state': 'ready' if state == 'ok' and not holes else 'blocked',
            'checked_utc': J._iso(now), 'from_utc': J._iso(start), 'through_utc_exclusive': J._iso(end),
            'archive_state': state, 'missing_4h_opens': holes, 'manifest': manifest,
            'interpretation': 'Closed archive history only; a final incomplete day is not assessed before it closes. No automatic interior-gap repair.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=['capture-evidence', 'refit', 'readiness'])
    args = ap.parse_args()
    if args.command == 'capture-evidence':
        capture_evidence()
    elif args.command == 'readiness':
        result = readiness()
        print(json.dumps(result, indent=2, sort_keys=True))
        raise SystemExit(int(result['state'] == 'blocked'))
    else:
        print(json.dumps(prepare(), sort_keys=True))
        J.refit()


if __name__ == '__main__':
    main()
