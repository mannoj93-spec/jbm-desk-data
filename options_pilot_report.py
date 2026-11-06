"""Operational replay/report adapter. Frozen pilot code and retained evidence stay byte-for-byte intact.

Only candidate call/put IV calculations allow <=1e-12 absolute roundoff. All keys,
selection decisions, rounded RR25 values, clocks, hashes and book evidence remain exact.
"""
from collections import Counter
import json
from pathlib import Path
from research_tools.options_pilot import core as K
from research_tools.options_pilot.study import compare, read_artifact, verify_books
from replay_precision import matches


def selection_matches(expected, actual):
    return matches(expected, actual, lambda p: len(p) == 4 and p[0] == 'candidates'
                   and p[2] == 'pair' and p[3] in ('call_iv', 'put_iv'))


def distribution(xs):
    import statistics
    xs = sorted(xs)
    return {**summary(xs), 'median': statistics.median(xs) if xs else None,
            'p90': xs[int(.9 * (len(xs)-1))] if xs else None}


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
                      'source_to_book_ms': distribution([q['source_to_book_ms'] for q in quotes if q['source_to_book_ms'] is not None]),
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


if __name__ == '__main__':
    from desk import stream_util as U
    K.production()
    now = U.clock_ms()
    try:
        write(K.ROOT, now)
    except Exception as exc:
        K.Journal(K.ROOT, 'runs').add(f'report-{now}', {'stage': 'report', 'started_ms': now,
            'ended_ms': U.clock_ms(), 'state': 'error', 'error': type(exc).__name__ + ': ' + str(exc)[:600],
            'run': U.run_meta(), 'adapter': 'operational-replay/1'})
        raise
    K.Journal(K.ROOT, 'runs').add(f'report-{now}', {'stage': 'report', 'started_ms': now,
        'ended_ms': U.clock_ms(), 'state': 'completed', 'run': U.run_meta(), 'adapter': 'operational-replay/1'})
