"""Isolated collectors: paired clocks, liquidation vintages and capability pilots."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import gzip
import json
import math
from desk import stream_util as U
from research_tools import options_skew as O
from .core import DAY, HOUR, MIN, STREAM, Journal, atomic, protocol, slots
from .network import fetch


def payload(r):
    if r['state'] != 'ok':
        raise ValueError(r['state'])
    if hashlib.sha256(r['raw'].encode()).hexdigest() != r['raw_sha']:
        raise ValueError('Raw response changed')
    return json.loads(r['raw'])


def finite(x, nonnegative=False):
    if isinstance(x, bool):
        raise ValueError('Boolean numeric input')
    v = float(x)
    if not math.isfinite(v) or (nonnegative and v < 0):
        raise ValueError('Invalid numeric input')
    return v


def flow(r, slot):
    rows = payload(r)
    if not isinstance(rows, list) or len(rows) != 5:
        raise ValueError('Need exactly five closed bars')
    volume, signed = 0., 0.
    for t, b in zip(range(slot - 5 * MIN, slot, MIN), rows):
        if b[0] != t or b[6] != t + MIN - 1:
            raise ValueError('Misaligned/duplicate/incomplete bars')
        v, buy = finite(b[5], True), finite(b[9], True)
        if buy > v:
            raise ValueError('Buy volume exceeds volume')
        for x in b[1:5]:
            if finite(x) <= 0:
                raise ValueError('Bad price')
        volume += v
        signed += 2 * buy - v
    if volume <= 0:
        raise ValueError('No volume')
    return {'volume': volume, 'signed': signed, 'imbalance': signed / volume}


def depth_quote(url):
    """Same bounded transport as the pilots; PS1 validates the captured-book semantics."""
    from desk import paper_ps1 as P
    r = fetch(url)
    obj = payload(r)
    return {'source': url, 't_sent_ms': r['sent_ms'], 't_received_ms': r['received_ms'],
            'last_update_id': obj.get('lastUpdateId'), 'bids': obj.get('bids'), 'asks': obj.get('asks'),
            'retrieval': P.LIVE, 'raw_sha256': r['raw_sha'], 'raw': r['raw']}


def pair_capture(slot, get=fetch):
    params = f'symbol=BTCUSDT&interval=1m&startTime={slot-5*MIN}&endTime={slot-1}&limit=5'
    urls = {'perp': 'https://www.binance.com/fapi/v1/klines?' + params,
            'spot': 'https://www.binance.com/api/v3/klines?' + params}
    with ThreadPoolExecutor(max_workers=2) as pool:
        fs = {k: pool.submit(get, url) for k, url in urls.items()}
        raw = {k: f.result() for k, f in fs.items()}
    out = {'raw': raw, 'slot': slot, 'state': 'ok'}
    try:
        fs = {k: flow(r, slot) for k, r in raw.items()}
        lag = abs(raw['spot']['received_ms'] - raw['perp']['received_ms'])
        out.update(flows=fs, receipt_gap_ms=lag,
                   request_gap_ms=abs(raw['spot']['sent_ms'] - raw['perp']['sent_ms']))
        if any(r['sent_ms'] < slot or r['received_ms'] <= r['sent_ms'] or r['received_ms'] - r['sent_ms'] > 12_000 for r in raw.values()):
            out['state'] = 'invalid-clock'
        elif max(r['received_ms'] for r in raw.values()) >= slot + 25 * MIN:
            out['state'] = 'late-capture'
        elif lag > protocol()['paired']['join_timeout_ms']:
            out['state'] = 'join-timeout'
    except (ValueError, KeyError, TypeError, IndexError) as exc:
        out.update(state='source-unavailable', reason=str(exc))
    return out


def stress_capture(slot, get=fetch):
    raw = [get(u) for u in protocol()['stress']['sources']]
    out = {'slot': slot, 'raw': raw, 'state': 'unavailable', 'risk': None, 'assets': None}
    try:
        a, b = [payload(r) for r in raw]
        a = next((x for x in a if x.get('symbol') == 'BTCUSDT'), None) if isinstance(a, list) else a
        b = next((x for x in b if 'BTCUSDT' in x.get('symbols', [])), None) if isinstance(b, list) else b
        rating = str(a['adlRisk']).lower()
        if a['symbol'] != 'BTCUSDT' or rating not in ('low', 'medium', 'high'):
            raise ValueError('Unknown ADL schema/rating')
        age = raw[0]['received_ms'] - int(a['updateTime'])
        if not 0 <= age <= HOUR:
            raise ValueError('Stale/future ADL risk')
        out.update(risk=rating, risk_update_ms=int(a['updateTime']), risk_age_ms=age)
        if 'BTCUSDT' not in b['symbols'] or not b['assets']:
            raise ValueError('No BTC insurance pool/assets')
        # Preserve asset schema as delivered; do not assume every venue version uses the same balance field.
        assets = []
        for asset in b['assets']:
            balance = finite(asset['marginBalance'], True)
            stamp = int(asset['updateTime'])
            if not isinstance(asset['asset'], str) or not 0 <= raw[1]['received_ms'] - stamp <= 2 * DAY:
                raise ValueError('Stale/future/malformed insurance snapshot')
            assets.append({'asset': asset['asset'], 'balance': balance, 'update_ms': stamp})
        out.update(assets=assets, pool_symbols=b['symbols'], state='ok')
    except (ValueError, KeyError, TypeError) as exc:
        out['reason'] = str(exc)
    return out


def liquidation_capture(end, vintage, get=fetch):
    start = end - HOUR
    url = ('https://www.okx.com/api/v5/public/liquidation-orders?instType=SWAP&uly=BTC-USDT'
           '&instId=BTC-USDT-SWAP&state=filled&limit=100')
    pages, orders, after, covered = [], {}, end, False
    reason = 'page-cap'
    for _ in range(protocol()['liquidations']['max_pages']):
        raw = get(url + f'&after={after}')
        pages.append(raw)
        try:
            obj = payload(raw)
            if str(obj.get('code')) != '0' or not isinstance(obj.get('data'), list):
                raise ValueError('OKX error/schema')
            details = [d for block in obj['data'] for d in block.get('details', [])]
            # Empty page cannot establish retention/coverage; absence is not zero activity.
            if not details:
                reason = 'empty-page-coverage-unknown'
                break
            times = [int(d['ts']) for d in details]
            for d, t in zip(details, times):
                size = finite(d['sz'], True)
                if d.get('posSide') not in ('long', 'short') or finite(d['bkPx']) <= 0:
                    raise ValueError('Malformed liquidation')
                if start <= t < end:
                    key = '|'.join(str(d.get(k)) for k in ('ts', 'posSide', 'side', 'sz', 'bkPx'))
                    orders[key] = {'t': t, 'size': size, 'side': d['posSide']}
            oldest = min(times)
            if oldest < start:
                covered, reason = True, 'source-window-covered'
                break
            nxt = oldest + 1
            if nxt >= after:
                reason = 'pagination-stalled-boundary-unknown'
                break
            after = nxt
        except (KeyError, TypeError, ValueError) as exc:
            reason = 'source-error: ' + str(exc)
            break
    long = sum(x['size'] for x in orders.values() if x['side'] == 'long')
    short = sum(x['size'] for x in orders.values() if x['side'] == 'short')
    total = long + short
    return {'end': end, 'vintage_hours': vintage, 'pages': pages, 'orders': list(orders.values()),
            'state': 'ok' if covered else 'coverage-unknown', 'reason': reason,
            'total_contracts': total if covered else None, 'signed_contracts': long - short if covered else None,
            'eligible': covered and total >= protocol()['liquidations']['signal_contract_threshold'],
            'signal': (int(long > short) - int(long < short)) if covered else None,
            'received_ms': pages[-1]['received_ms']}


def rr25(cap, days):
    now = cap['observed_at']
    exps = []
    for code in cap.get('underlying_v2', {}):
        d = (O.expiry_ms(code) - now) / DAY
        if 1 <= d <= 45:
            exps.append((d, code))
    lo = max((e for e in exps if e[0] <= days), default=None)
    hi = min((e for e in exps if e[0] >= days), default=None)
    if not lo or not hi:
        return {'state': 'no-bracketing-expiry', 'value': None}
    s1, a = O.expiry_skew(cap, lo[1], now)
    s2, b = O.expiry_skew(cap, hi[1], now)
    if s1 != 'ok' or s2 != 'ok':
        return {'state': f'{lo[1]}:{s1}|{hi[1]}:{s2}', 'value': None}
    target = days / 365.25
    vals = []
    for side in ('call_iv', 'put_iv'):
        if a['T'] == b['T']:
            vals.append(a[side])
        else:
            w = (target - a['T']) / (b['T'] - a['T'])
            vals.append(math.sqrt(((1-w)*a[side]**2*a['T'] + w*b[side]**2*b['T']) / target))
    return {'state': 'ok', 'value': round(100 * (vals[0] - vals[1]), 4), 'expiries': [lo[1], hi[1]]}


def options_quality(cap):
    legs, expiries = [], {}
    for q in O._quotes(cap):
        reasons = []
        age = spread = delta_distance = None
        try:
            _, code, strike, side = q['instrument'].split('-')
            T = (O.expiry_ms(code) - cap['observed_at']) / (365.25 * DAY)
            if not 1 / 365.25 <= T <= 45 / 365.25:
                reasons.append('maturity')
            F = finite(cap['underlying_v2'][code][1])
            iv = finite(q['mark_iv']) / 100
            delta_distance = abs(abs(O.delta76(F, float(strike), T, iv, side == 'C')) - .25) if T > 0 and iv > 0 else None
            if delta_distance is None or delta_distance > .08:
                reasons.append('delta-distance')
            bid, ask = finite(q['bid_price_btc'], True), finite(q['ask_price_btc'], True)
            if bid <= 0 or ask <= bid:
                reasons.append('no-two-sided-or-crossed')
            spread = (ask - bid) / ((ask + bid) / 2) if ask + bid > 0 else None
            if spread is None or spread > .25:
                reasons.append('wide')
            if finite(q['open_interest_btc'], True) < 5:
                reasons.append('low-oi')
            age = cap['observed_at'] - (cap['t_event_min'] + int(q['source_ts_offset_ms']))
            if not 0 <= age <= 30_000:
                reasons.append('stale-or-future')
        except (TypeError, ValueError, KeyError, ZeroDivisionError):
            reasons.append('missing-or-malformed')
        legs.append({'instrument': q.get('instrument'), 'quote_age_ms': age, 'relative_spread': spread,
                     'oi_btc': q.get('open_interest_btc'), 'delta_distance': delta_distance,
                     'bid_size': q.get('bid_size'), 'ask_size': q.get('ask_size'),
                     'size_state': 'not-in-source' if q.get('bid_size') is None else 'observed', 'reasons': reasons})
    for code in cap.get('underlying_v2', {}):
        if 1 <= (O.expiry_ms(code) - cap['observed_at']) / DAY <= 45:
            state, pair = O.expiry_skew(cap, code, cap['observed_at'])
            expiries[code] = {'state': state, 'pair': pair}
    return {'observed_at': cap['observed_at'], 'source_sha': U.sha(cap), 'filters_sha': O.filters_sha256(),
            'legs': legs, 'expiries': expiries, 'rr25_7d': rr25(cap, 7), 'rr25_30d': rr25(cap, 30),
            'predictive_status': 'not admitted'}


def pilots(base, first, now, get=fetch):
    stress = Journal(base, 'stress')
    for slot in slots(first, now, 30 * MIN):
        key = str(slot)
        if not stress.get(key):
            capture = stress_capture(slot, get) if now - slot < 30 * MIN else {'slot': slot, 'state': 'missed'}
            if capture.get('raw') and max(r['received_ms'] for r in capture['raw']) >= slot + 30 * MIN:
                capture['state'] = 'late-capture'
            stress.add(key, capture)
    liq = Journal(base, 'liquidations')
    for end in slots(first + HOUR, now, HOUR):
        for v in protocol()['liquidations']['vintage_hours']:
            due, key = end + v * HOUR, f'{end}-{v}'
            if due > now or liq.get(key):
                continue
            capture = liquidation_capture(end, v, get) if now - due < 30 * MIN else {'end': end, 'vintage_hours': v, 'state': 'missed', 'received_ms': None}
            if capture['received_ms'] is not None:
                capture['lag_ms'] = capture['received_ms'] - due
                if not 0 <= capture['lag_ms'] < 30 * MIN:
                    capture.update(state='late-capture', eligible=False)
            liq.add(key, capture)
    options = Journal(base, 'options')
    from lab.data import Store
    for cap in Store(base, now).option_quotes():
        if cap['observed_at'] < first:
            continue
        key = str(cap['observed_at'])
        if not options.get(key):
            quality = options_quality(cap)
            legs = quality.pop('legs')
            from collections import Counter
            from pathlib import Path
            quality['leg_count'] = len(legs)
            quality['rejections'] = dict(Counter(reason for leg in legs for reason in leg['reasons']))
            raw = U.canonical(legs)
            digest = hashlib.sha256(raw).hexdigest()
            path = STREAM / 'option_legs' / f'{digest}.json.gz'
            atomic(Path(base) / path, gzip.compress(raw, mtime=0))
            quality['legs_file'] = str(path)
            quality['legs_sha'] = digest
            options.add(key, quality)
