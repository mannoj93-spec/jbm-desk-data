"""Paired expiry selection on a shared prospective source capture; books are later diagnostics."""
from collections import Counter
from replay_precision import matches
import gzip
import hashlib
import json
import math
from pathlib import Path
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
        if K.protocol()['expiry_days'][0] <= days <= K.protocol()['expiry_days'][1]:
            state, pair = O.expiry_skew(cap, code, now)
            candidates[code] = {'days': days, 'state': state, 'pair': pair}
    arms = {}
    for name, maximum in [('eligible-45d', K.protocol()['control_expiry_days'][1]),
                          ('eligible-90d', K.protocol()['expiry_days'][1])]:
        eligible = sorted((v['days'], code) for code, v in candidates.items()
                          if v['state'] == 'ok' and v['days'] <= maximum)
        lo = max((e for e in eligible if e[0] <= 30), default=None)
        hi = min((e for e in eligible if e[0] >= 30), default=None)
        arm = {'state': 'no-eligible-bracket', 'value': None, 'instruments': []}
        if lo and hi:
            span = (O.expiry_ms(hi[1]) - O.expiry_ms(lo[1])) / K.DAY
            if span > K.protocol()['max_bracket_span_days']['30']:
                arm.update(state='bracket-too-wide', span_days=span)
            else:
                a, b = candidates[lo[1]]['pair'], candidates[hi[1]]['pair']
                target = 30 / 365.25
                values = []
                for side in ('call_iv', 'put_iv'):
                    if a['T'] == b['T']:
                        values.append(a[side])
                    else:
                        w = (target - a['T']) / (b['T'] - a['T'])
                        values.append(math.sqrt(((1-w)*a[side]**2*a['T'] + w*b[side]**2*b['T']) / target))
                arm.update(state='ok', value=round(100*(values[0]-values[1]), 4),
                           expiries=[lo[1], hi[1]], span_days=span)
                for code in dict.fromkeys(arm['expiries']):
                    pair = candidates[code]['pair']
                    for side, key in [('C', 'call_K'), ('P', 'put_K')]:
                        selected = [q['instrument'] for q in O._quotes(cap) if q['instrument'].split('-')[1] == code
                                    and q['instrument'].split('-')[3] == side
                                    and float(q['instrument'].split('-')[2]) == pair[key]]
                        if len(selected) != 1:
                            raise ValueError('Selected contract identity is not unique')
                        arm['instruments'].append(selected[0])
        arms[name] = arm
    return {'candidates': candidates, 'horizons': {'30': arms}, 'filters_sha': O.filters_sha256()}


from research_tools.options_pilot.study import books, verify_books


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
            if not (slot <= d['source_ms'] <= d['selected_ms'] < slot + K.HOUR and d['selected_ms'] <= d['recorded_ms']):
                raise ValueError('Invalid pilot observation clock')
            a = read_artifact(base, d['artifact'])
            if a['source']['observed_at'] != d['source_ms'] or not selection_matches(compare(a['source']), a['selection']):
                raise ValueError('Pilot selection failed reproduction')
            verify_books(a['books'], a['selection'], d['source_ms'], d['selected_ms'])
            if a['books'].get('ended_ms', a['books']['started_ms']) > d['recorded_ms']:
                raise ValueError('Pilot book batch ends after its observation record')
            data[slot] = a
        elif d['state'] != 'missed' or d['recorded_ms'] < slot + K.HOUR:
            raise ValueError('Invalid missed observation')
    closed = list(range(first, now // K.HOUR * K.HOUR, K.HOUR)) if first is not None else []
    captured = [data[t] for t in closed if t in data]
    horizons = {}
    for days in K.protocol()['targets_days']:
        counts, diffs, spans, reasons = Counter(), [], {'eligible-45d': [], 'eligible-90d': []}, Counter()
        for a in captured:
            arms = a['selection']['horizons'][str(days)]
            control, alternate = arms['eligible-45d'], arms['eligible-90d']
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
    return {'schema': 'options-30d-maturity/1', 'generated_ms': now, 'activation': activation,
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
    K.atomic(Path(base) / 'reports/options_30d_pilot.json', (json.dumps(out, indent=2, allow_nan=False)+'\n').encode())
    lines = ['# Prospective 30-day options maturity pilot', '', f"State: {out['state']}. Captures: {out['captured']}/{out['closed']} closed hours.",
             '', 'Control: nearest eligible expiries within 45 days. Alternate: within 90 days. Both capped at a 35-day span.',
             'Identical frozen leg filters and source capture; no extrapolation. Later books do not alter quote eligibility.',
             '', '| Horizon | Both usable | Gained | Lost | Neither | Missing capture |', '|---|---:|---:|---:|---:|---:|']
    for days, h in out['horizons'].items():
        c = h['paired']; lines.append(f"| {days}d | {c['both']} | {c['gained']} | {c['lost']} | {c['neither']} | {h['missing_capture']} |")
    b = out['books']
    lines += ['', f"Books: {b['usable']} usable / {b['attempted']} attempted / {b['expected']} selected distinct contracts across hours.",
              'Quote sizes, source-to-book lag, spans, value differences and failure reasons: [JSON report](options_30d_pilot.json).',
              '', out['interpretation']]
    K.atomic(Path(base) / 'reports/options_30d_pilot.md', ('\n'.join(lines)+'\n').encode())


def selection_matches(expected, actual):
    return matches(expected, actual, lambda p: len(p) == 4 and p[0] == 'candidates'
                   and p[2] == 'pair' and p[3] in ('call_iv', 'put_iv'))
