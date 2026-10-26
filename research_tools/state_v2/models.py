"""Frozen v1 models with one explicit depth-selection correction, shared by train and predict."""
from collections import Counter
from datetime import datetime
from desk import stream_util as U
from lab.data import Store
from research_tools import panel as P
from research_tools.market_studies import models as V1
from .core import DAY, HOUR, MIN, Journal, protocol

feature_sets = V1.feature_sets
predict = V1.predict
price_outcome = V1.price_outcome


def depth(row, snaps, t, start, end):
    candidates, eligible = [], []
    for _, available, snap in snaps.recent(t):
        book = snap.get('depth_binance_usdt') or {}
        if not book:
            continue
        measured = P._measured(snap, 'depth_binance_usdt')
        distance = max(start - measured, measured - end, 0)
        bid, bs = P.E.number(book.get('bid_btc_25'), 'nonneg')
        ask, ass = P.E.number(book.get('ask_btc_25'), 'nonneg')
        why = []
        total = bid + ask if bs == ass == 'ok' else None
        if book.get('st') != 'ok' or total is None:
            why.append('malformed')
        if measured > available or available > t:
            why.append('invalid-clock')
        if t - measured > P.DEPTH_MAX_AGE:
            why.append('stale')
        if distance > P.DEPTH_ALIGN:
            why.append('misaligned')
        if total is not None and total < P.MIN_DEPTH_BTC:
            why.append('insufficient-depth')
        item = {'measured_ms': measured, 'available_ms': available, 'distance_ms': distance,
                'age_ms': t - measured, 'depth_btc': total, 'snapshot_sha': U.sha(snap), 'rejections': why}
        candidates.append(item)
        if not why:
            eligible.append(item)
    rank = lambda x: (x['distance_ms'], -x['measured_ms'], -x['available_ms'], x['snapshot_sha'])
    candidates.sort(key=rank)
    chosen = min(eligible, key=rank) if eligible else None
    row['inputs']['depth_selection_v2'] = {'candidates': candidates, 'selected': chosen}
    if chosen is None:
        P._src(row, 'depth', None, None, t, 'no-eligible-depth')
        row['inputs'].pop('depth_snapshot_utc', None)
        counts = Counter(why for x in candidates for why in x['rejections'])
        return 'no-eligible-depth: ' + (', '.join(sorted(counts)) or 'source-missing'), None
    P._src(row, 'depth', chosen['measured_ms'], chosen['available_ms'], t, 'ok')
    row['inputs']['depth_snapshot_utc'] = P.iso(chosen['measured_ms'])
    return 'ok', chosen['depth_btc']


def state_panel(store, start, end):
    rows = V1.state_panel(store, start, end)
    snaps = P._Avail(P._snap_items(store))
    bars = store.bars('binance_klines_1m_BTCUSDT_perp')
    for row in rows:
        row['feature_version'] = 'market-state-2'
        if row['fstate'].get('flow_btc') != 'ok':
            continue                         # never repair an invalid underlying flow window
        end_ms = int(datetime.fromisoformat(row['inputs']['perp_window_end_utc'].replace('Z', '+00:00')).timestamp() * 1000)
        state, amount = depth(row, snaps, row['t'], end_ms - P.WINDOW * MIN, end_ms)
        for key in ('depth_25bp_btc', 'flow_per_depth'):
            row['features'].pop(key, None)
            row['fstate'][key] = state
        row['state']['flow_liquidity'] = state
        if state == 'ok':
            # Use the original unrounded flow, exactly as v1 does.
            flow = sum(2 * bars[t]['tbv'] - bars[t]['v'] for t in range(end_ms - P.WINDOW * MIN, end_ms, MIN))
            row['features'].update(depth_25bp_btc=round(amount, 3), flow_per_depth=round(flow / amount, 5))
    return rows


def state_fit(base, cutoff):
    cfg = protocol()['state']
    store = Store(base, cutoff - 1)
    bars = store.bars('binance_klines_1m_BTCUSDT_perp')
    members = []
    for row in state_panel(store, cutoff - cfg['training_days'] * DAY, cutoff - 4 * HOUR - 30 * MIN):
        label = price_outcome(bars, row['t'] + 30 * MIN, 240, cutoff)
        if label and P.eligible(row, feature_sets()['full'])[0]:
            members.append({'t': row['t'], 'features': {k: row['features'][k] for k in feature_sets()['full']},
                            'row_sha': U.sha(row), 'label': label})
    ready = len(members) >= cfg['minimum_training']
    return {'cutoff': cutoff, 'state': 'ready' if ready else 'warmup', 'training_use': 'discovery only',
            'members': members, 'models': {k: V1.logistic_fit(members, fs) for k, fs in feature_sets().items()} if ready else {}}


def daily_fit(base, now):
    cutoff = now // DAY * DAY
    journal = Journal(base, 'fits')
    key = f'state-{cutoff}'
    return journal.get(key) or journal.add(key, state_fit(base, cutoff))
