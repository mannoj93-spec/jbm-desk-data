"""Frozen calibration and small, deterministic probability models; no parameter search."""
import math
from desk import companion_job as B, paper_ps1 as P, stream_util as U
from lab.data import Store
from research_tools import panel
from .core import DAY, HOUR, MIN, Journal, protocol


def quantile(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    i = (len(xs) - 1) * p
    lo = int(i)
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (i - lo)


def interval_score(lo, hi, y):
    if not all(math.isfinite(x) for x in (lo, hi, y)) or lo > hi:
        raise ValueError('Invalid interval')
    return hi - lo + 10 * max(0, lo - y) + 10 * max(0, y - hi)


def range_fit(base, cutoff):
    cfg = protocol()['range']
    members = []
    scores = B._rc1d_scores(base)
    for fid, s in sorted(scores.items()):
        if not fid.startswith('range-rc1d-24h-'):
            continue
        if not (cutoff - cfg['training_days'] * DAY <= s.get('horizon', 0) < cutoff
                and 0 < s.get('scored', 0) < cutoff):
            continue
        o = B.rc1d_outcome(base, fid, scores)       # raises on corrupt evidence; never quietly drops it
        if not o['eligible']:
            continue
        doc, entry, _ = U.rc1d_record(base, fid)
        e = next(x for x in doc['events'] if x['name'].startswith('B2'))
        members.append({'id': fid, 'score_sha': o['score_sha256'], 'forecast_sha': entry['sha256'],
                        'q10': e['q10'], 'q90': e['q90'], 'y': o['realized'], 'known_ms': o['scored_ms']})
    enough = len(members) >= cfg['minimum_training']
    return {'cutoff': cutoff, 'state': 'ready' if enough else 'warmup', 'members': members,
            'lower_offset': quantile([r['y'] - r['q10'] for r in members], .1) if enough else None,
            'upper_offset': quantile([r['y'] - r['q90'] for r in members], .9) if enough else None}


def calibrated(e, fit):
    if fit['state'] != 'ready':
        raise ValueError('Calibrator not ready')
    return {'q10': max(0, min(e['q50'], e['q10'] + fit['lower_offset'])), 'q50': e['q50'],
            'q90': max(e['q50'], e['q90'] + fit['upper_offset']), 'point': e['point']}


def price_outcome(bars, entry, minutes, cutoff):
    """Complete contiguous path, strictly known by cutoff, not merely two convenient endpoints."""
    seq = [bars.get(t) for t in range(entry, entry + minutes * MIN, MIN)]
    if not seq or any(b is None or b['avail'] >= cutoff for b in seq):
        return None
    if any(not all(math.isfinite(float(b[k])) and float(b[k]) > 0 for k in ('o', 'h', 'l', 'c')) for b in seq):
        return None
    ret = math.log(seq[-1]['c'] / seq[0]['o'])
    return {'y': int(ret > 0), 'return_bp': 1e4 * ret, 'known_ms': max(b['avail'] for b in seq),
            'entry': entry, 'end': entry + minutes * MIN, 'bars_sha': U.sha(seq)}


def state_panel(store, start, end):
    rows = [r for r in panel.build(store, start, end)['rows'] if r['t'] % HOUR == 0]
    bars = store.bars('binance_klines_1m_BTCUSDT_perp')
    for r in rows:
        available = [t for t, b in bars.items() if b['avail'] <= r['t'] and t + MIN <= r['t']]
        last = max(available, default=None)
        seq = [bars.get(t) for t in range(last - 59 * MIN, last + MIN, MIN)] if last is not None else []
        ok = (len(seq) == 60 and r['t'] - last - MIN <= 45 * MIN
              and all(b is not None and b['avail'] <= r['t'] and b['o'] > 0 and b['c'] > 0 for b in seq))
        r['features']['rv_1h_bp'] = math.sqrt(sum(math.log(b['c'] / b['o']) ** 2 for b in seq)) * 1e4 if ok else None
        r['fstate']['rv_1h_bp'] = 'ok' if ok else 'incomplete-or-stale'
        r['inputs']['rv_1h'] = {'end': last + MIN if last else None,
                               'source_sha': U.sha(seq) if ok else None,
                               'available': max(b['avail'] for b in seq) if ok else None}
    return [r for r in rows if r['t'] % HOUR == 0]


def feature_sets():
    p = protocol()['state']
    b = p['baseline']
    return {'baseline': b, 'flow': b + p['flow'], 'positioning': b + p['flow'] + p['positioning'],
            'full': b + p['flow'] + p['positioning'] + p['funding']}


def logistic_fit(members, features):
    n = len(members)
    means = [sum(r['features'][f] for r in members) / n for f in features]
    sds = [math.sqrt(sum((r['features'][f] - m) ** 2 for r in members) / n) or 1.0
           for f, m in zip(features, means)]
    xs = [[1.] + [max(-5, min(5, (r['features'][f] - m) / sd)) for f, m, sd in zip(features, means, sds)]
          for r in members]
    w = [0.] * (len(features) + 1)
    for _ in range(200):
        grad = [0.] * len(w)
        for x, r in zip(xs, members):
            z = max(-35, min(35, sum(a * b for a, b in zip(x, w))))
            err = 1 / (1 + math.exp(-z)) - r['label']['y']
            for j, value in enumerate(x):
                grad[j] += err * value
        w = [v - .1 * (g / n + (.1 * v if j else 0)) for j, (v, g) in enumerate(zip(w, grad))]
    return {'features': features, 'means': means, 'sds': sds, 'weights': w}


def predict(model, values):
    x = [1.] + [max(-5, min(5, (values[f] - m) / sd))
                 for f, m, sd in zip(model['features'], model['means'], model['sds'])]
    z = max(-35, min(35, sum(a * b for a, b in zip(x, model['weights']))))
    return 1 / (1 + math.exp(-z))


def state_fit(base, cutoff):
    cfg = protocol()['state']
    store = Store(base, cutoff - 1)
    bars = store.bars('binance_klines_1m_BTCUSDT_perp')
    rows = state_panel(store, cutoff - cfg['training_days'] * DAY, cutoff - 4 * HOUR - 30 * MIN)
    members = []
    for r in rows:
        label = price_outcome(bars, r['t'] + 30 * MIN, 240, cutoff)
        if not label or not panel.eligible(r, feature_sets()['full'])[0]:
            continue
        members.append({'t': r['t'], 'features': {k: r['features'][k] for k in feature_sets()['full']},
                        'row_sha': U.sha(r), 'label': label})
    ready = len(members) >= cfg['minimum_training']
    return {'cutoff': cutoff, 'state': 'ready' if ready else 'warmup', 'training_use': 'discovery only',
            'members': members, 'models': {k: logistic_fit(members, fs) for k, fs in feature_sets().items()} if ready else {}}


def daily_fit(base, kind, now):
    cutoff = now // DAY * DAY
    j = Journal(base, 'fits')
    key = f'{kind}-{cutoff}'
    old = j.get(key)
    if old:
        return old
    return j.add(key, (range_fit if kind == 'range' else state_fit)(base, cutoff))
