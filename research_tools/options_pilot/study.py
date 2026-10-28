"""Paired expiry selection on a shared prospective source capture; books are later diagnostics."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urlencode
from desk import stream_util as U
from lab.data import Store
from research_tools import options_skew as O
from research_tools.market_studies import collectors as C
from research_tools.market_studies.network import fetch
from . import core as K


def compare(cap):
    now, candidates = cap['observed_at'], {}
    for code in cap.get('underlying_v2', {}):
        days = (O.expiry_ms(code) - now) / K.DAY
        if 1 <= days <= 45:
            state, pair = O.expiry_skew(cap, code, now)
            candidates[code] = {'days': days, 'state': state, 'pair': pair}
    results = {}
    for days in K.protocol()['targets_days']:
        control = C.rr25(cap, days)
        eligible = sorted((v['days'], code) for code, v in candidates.items() if v['state'] == 'ok')
        lo = max((e for e in eligible if e[0] <= days), default=None)
        hi = min((e for e in eligible if e[0] >= days), default=None)
        alternate = {'state': 'no-eligible-bracket', 'value': None}
        if lo and hi:
            span = hi[0] - lo[0]
            if span > K.protocol()['max_bracket_span_days'][str(days)]:
                alternate = {'state': 'bracket-too-wide', 'value': None, 'span_days': span}
            else:
                # Restrict only the expiry universe; use the exact frozen interpolation and leg selection.
                selected = dict(cap, underlying_v2={code: cap['underlying_v2'][code] for code in {lo[1], hi[1]}})
                alternate = C.rr25(selected, days)
        for result in (control, alternate):
            result['instruments'] = []
            if result['state'] == 'ok':
                a, b = result['expiries']
                result['span_days'] = candidates[b]['days'] - candidates[a]['days']
                for code in dict.fromkeys(result['expiries']):
                    pair = candidates[code]['pair']
                    for side, key in [('C', 'call_K'), ('P', 'put_K')]:
                        matches = [q['instrument'] for q in O._quotes(cap) if q['instrument'].split('-')[1] == code
                                   and q['instrument'].split('-')[3] == side
                                   and float(q['instrument'].split('-')[2]) == pair[key]]
                        if len(matches) != 1:
                            raise ValueError('Selected contract identity is not unique')
                        result['instruments'].append(matches[0])
        results[str(days)] = {'nearest-listed': control, 'nearest-eligible': alternate}
    return {'candidates': candidates, 'horizons': results, 'filters_sha': O.filters_sha256()}


def book_result(instrument, response, source_ms):
    result = {'instrument': instrument, 'state': 'unavailable', 'bid_size': None, 'ask_size': None,
              'sent_ms': response.get('sent_ms'), 'received_ms': response.get('received_ms'),
              'source_to_book_ms': None, 'amount_units': 'venue option contracts', 'price_units': 'BTC'}
    try:
        sent, received = response['sent_ms'], response['received_ms']
        data = C.payload(response)['result']
        result['source_to_book_ms'] = received - source_ms
        if not source_ms <= sent <= received or received - sent > 12_000:
            raise ValueError('request-clock')
        if data['instrument_name'] != instrument or data.get('state') != 'open':
            raise ValueError('wrong-instrument-or-closed')
        skew = K.protocol()['max_book_clock_skew_ms']
        if not sent - skew <= data['timestamp'] <= received + skew:
            raise ValueError('stale-or-future-book')
        bid, ask = C.finite(data['best_bid_price'], True), C.finite(data['best_ask_price'], True)
        if not 0 < bid < ask:
            raise ValueError('not-two-sided')
        bs, az = C.finite(data['best_bid_amount'], True), C.finite(data['best_ask_amount'], True)
        result.update(state='ok', bid_size=bs, ask_size=az, bid_price=bid, ask_price=ask,
                      event_ms=data['timestamp'])
    except (KeyError, TypeError, ValueError) as exc:
        result['reason'] = str(exc)
    return result


def books(selection, source_ms, get=fetch, clock=U.clock_ms):
    instruments = sorted({i for arms in selection['horizons'].values() for a in arms.values() for i in a['instruments']})
    p, start = K.protocol(), clock()
    if len(instruments) > p['max_book_contracts']:
        raise ValueError('Contract budget exceeded')
    if not 0 <= start - source_ms <= p['max_book_source_age_ms']:
        return {'state': 'source-too-old', 'expected': len(instruments), 'started_ms': start, 'raw': [], 'quotes': []}
    def capture(instrument):
        url = 'https://www.deribit.com/api/v2/public/get_order_book?' + urlencode({'instrument_name': instrument, 'depth': 1})
        return instrument, get(url)
    with ThreadPoolExecutor(max_workers=p['book_concurrency']) as pool:
        responses = list(pool.map(capture, instruments))
    end = clock()
    quotes = [book_result(i, r, source_ms) for i, r in responses]
    state = 'completed' if 0 <= end - start <= p['max_book_batch_ms'] else 'late-batch'
    if state != 'completed':
        for q in quotes:
            q.update(state='late-batch', bid_size=None, ask_size=None)
    return {'state': state, 'expected': len(instruments), 'started_ms': start, 'ended_ms': end,
            'raw': [r for _, r in responses], 'quotes': quotes}


def verify_books(book, selection, source_ms, selected_ms):
    expected = sorted({i for arms in selection['horizons'].values() for arm in arms.values() for i in arm['instruments']})
    if book['expected'] != len(expected):
        raise ValueError('Pilot book denominator changed')
    if book['state'] == 'source-too-old':
        if book['started_ms'] < selected_ms or book['started_ms'] - source_ms <= K.protocol()['max_book_source_age_ms'] or book['raw'] or book['quotes']:
            raise ValueError('Invalid skipped book batch')
        return
    if book['state'] not in ('completed', 'late-batch'):
        raise ValueError('Unknown book batch state')
    start, end = book['started_ms'], book['ended_ms']
    if not selected_ms <= start <= end or start - source_ms > K.protocol()['max_book_source_age_ms']:
        raise ValueError('Invalid book batch clock')
    late = end - start > K.protocol()['max_book_batch_ms']
    if late != (book['state'] == 'late-batch') or len(book['raw']) != len(expected):
        raise ValueError('Invalid book batch completion')
    if any(not start <= r['sent_ms'] <= r['received_ms'] <= end for r in book['raw']):
        raise ValueError('Book response outside batch clock')
    reproduced = [book_result(i, r, source_ms) for i, r in zip(expected, book['raw'])]
    if late:
        for q in reproduced:
            q.update(state='late-batch', bid_size=None, ask_size=None)
    if reproduced != book['quotes']:
        raise ValueError('Pilot books failed reproduction')


def artifact(base, value):
    raw = U.canonical(value)
    sha = hashlib.sha256(raw).hexdigest()
    path = K.STREAM / 'captures' / (sha + '.json.gz')
    K.atomic(Path(base) / path, gzip.compress(raw, mtime=0))
    return {'path': str(path), 'sha256': sha}


def read_artifact(base, ref):
    expected = K.STREAM / 'captures' / (ref['sha256'] + '.json.gz')
    if ref['path'] != str(expected):
        raise ValueError('Invalid pilot artifact path')
    raw = gzip.decompress((Path(base) / expected).read_bytes())
    if hashlib.sha256(raw).hexdigest() != ref['sha256']:
        raise ValueError('Pilot artifact changed')
    return json.loads(raw)


def collect(base, now, get=fetch, clock=U.clock_ms):
    activation = K.activation(base)
    if not activation:
        return
    journal = K.Journal(base, 'observations')
    caps = {}
    for cap in sorted(Store(base, now).option_quotes(), key=lambda c: c['observed_at']):
        slot = cap['observed_at'] // K.HOUR * K.HOUR
        if slot >= activation['first_slot']:
            caps.setdefault(slot, cap)
    for slot in K.slots(activation['first_slot'], now, K.HOUR):
        if journal.get(str(slot)):
            continue
        if now >= slot + K.HOUR:
            journal.add(str(slot), {'slot': slot, 'state': 'missed', 'recorded_ms': now})
            continue
        cap = caps.get(slot)
        if cap is None:
            continue                  # open opportunity: later source capture may still arrive
        selection = compare(cap)
        selected_ms = clock()
        if selected_ms >= slot + K.HOUR or selected_ms < cap['observed_at']:
            continue                  # cannot backfill a prospective comparison after its deadline
        book = books(selection, cap['observed_at'], get, clock)
        ref = artifact(base, {'source': cap, 'selection': selection, 'books': book})
        journal.add(str(slot), {'slot': slot, 'state': 'captured', 'source_ms': cap['observed_at'],
                               'selected_ms': selected_ms, 'recorded_ms': clock(), 'artifact': ref})


def report(base, now):
    activation = K.activation(base)
    rows = K.Journal(base, 'observations').rows
    first = activation['first_slot'] if activation else None
    data = {}
    for row in rows:
        d = row['data']; slot = d['slot']
        if d['recorded_ms'] > now:
            raise ValueError('Pilot observation from a future clock')
        if first is None or slot < first or slot % K.HOUR or row['id'] != str(slot):
            raise ValueError('Pilot observation outside registered clock')
        if d['state'] == 'captured':
            if not slot <= d['source_ms'] <= d['selected_ms'] < slot + K.HOUR:
                raise ValueError('Invalid pilot observation clock')
            a = read_artifact(base, d['artifact'])
            if a['source']['observed_at'] != d['source_ms'] or compare(a['source']) != a['selection']:
                raise ValueError('Pilot selection failed reproduction')
            verify_books(a['books'], a['selection'], d['source_ms'], d['selected_ms'])
            data[slot] = a
        elif d['state'] != 'missed' or d['recorded_ms'] < slot + K.HOUR:
            raise ValueError('Invalid missed observation')
    closed = list(range(first, now // K.HOUR * K.HOUR, K.HOUR)) if first is not None else []
    captured = [data[t] for t in closed if t in data]
    horizons = {}
    for days in K.protocol()['targets_days']:
        counts, diffs, spans, reasons = Counter(), [], {'nearest-listed': [], 'nearest-eligible': []}, Counter()
        for a in captured:
            arms = a['selection']['horizons'][str(days)]
            control, alternate = arms['nearest-listed'], arms['nearest-eligible']
            ca, aa = control['state'] == 'ok', alternate['state'] == 'ok'
            counts['both' if ca and aa else 'gained' if aa else 'lost' if ca else 'neither'] += 1
            if ca and aa:
                diffs.append(alternate['value'] - control['value'])
            for name, arm in arms.items():
                reasons[name + ':' + arm['state']] += 1
                if arm['state'] == 'ok':
                    spans[name].append(arm['span_days'])
        horizons[str(days)] = {'paired': {k: counts[k] for k in ('both', 'gained', 'lost', 'neither')},
                              'missing_capture': len(closed) - len(captured), 'states': dict(reasons),
                              'joint_value_difference': summary(diffs),
                              'span_days': {k: summary(v) for k, v in spans.items()}}
    quotes = [q for a in captured for q in a['books']['quotes']]
    return {'schema': 'options-expiry-pilot/1', 'generated_ms': now, 'activation': activation,
            'state': 'active' if activation else 'awaiting-activation', 'closed': len(closed),
            'captured': len(captured), 'pending_captured': len(data) - len(captured), 'horizons': horizons,
            'books': {'expected': sum(a['books']['expected'] for a in captured),
                      'attempted': sum(len(a['books']['raw']) for a in captured),
                      'usable': sum(q['state'] == 'ok' for q in quotes),
                      'states': dict(Counter(a['books']['state'] for a in captured)),
                      'quote_states': dict(Counter(q['state'] for q in quotes)),
                      'source_to_book_ms': summary([q['source_to_book_ms'] for q in quotes if q['source_to_book_ms'] is not None]),
                      'bid_size': summary([q['bid_size'] for q in quotes if q['bid_size'] is not None]),
                      'ask_size': summary([q['ask_size'] for q in quotes if q['ask_size'] is not None])},
            'interpretation': K.protocol()['interpretation']}


def summary(xs):
    return {'n': len(xs), 'min': min(xs) if xs else None, 'max': max(xs) if xs else None,
            'mean': sum(xs) / len(xs) if xs else None}


def write(base, now):
    out = report(base, now)
    K.atomic(Path(base) / 'reports/options_expiry_pilot.json', (json.dumps(out, indent=2, allow_nan=False)+'\n').encode())
    lines = ['# Prospective options expiry pilot', '', f"State: {out['state']}. Captures: {out['captured']}/{out['closed']} closed hours.",
             '', 'Control: nearest listed expiries. Alternate: nearest eligible expiries, capped at 14/35-day spans for 7d/30d.',
             'Identical frozen leg filters and source capture; no extrapolation. Later books do not alter quote eligibility.',
             '', '| Horizon | Both usable | Gained | Lost | Neither | Missing capture |', '|---|---:|---:|---:|---:|---:|']
    for days, h in out['horizons'].items():
        c = h['paired']; lines.append(f"| {days}d | {c['both']} | {c['gained']} | {c['lost']} | {c['neither']} | {h['missing_capture']} |")
    b = out['books']
    lines += ['', f"Books: {b['usable']} usable / {b['attempted']} attempted / {b['expected']} selected distinct contracts across hours.",
              'Quote sizes, source-to-book lag, spans, value differences and failure reasons: [JSON report](options_expiry_pilot.json).',
              '', out['interpretation']]
    K.atomic(Path(base) / 'reports/options_expiry_pilot.md', ('\n'.join(lines)+'\n').encode())
