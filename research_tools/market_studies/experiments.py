"""Prospective opportunities, independent sizing accounts, and paired outcomes."""
import datetime as dt
import math
from desk import paper_ps1 as P, range_reader as RR, companion_job as B, stream_util as U
from lab.data import Store
from research_tools import panel
from . import models as M, collectors as C
from .core import HOUR, MIN, Journal, activation, protocol, register, slots, verified


def source(base, slot, horizon, now):
    rc = RR.read_current(base, dt.datetime.fromtimestamp(now / 1000, dt.timezone.utc), horizon)
    if rc.get('state') == 'integrity-failed':
        raise ValueError(rc['reason'])
    if rc.get('state') != 'valid-current' or U.ms(U.parse(rc['decision_utc'])) != slot:
        return None
    doc, entry, pub = U.rc1d_record(base, rc['id'])
    return {'id': rc['id'], 'document': doc, 'frozen_sha': entry['sha256'], 'publication': pub,
            'available_ms': rc['available_ms']}


def turnover_forecast(src, base):
    doc = src['document']
    bundle = U.rc1d_bundle(base, doc)
    if bundle['bars'][-1]['close_utc'] != doc['decision_utc']:
        raise ValueError('Sizing bars do not end at decision')
    sigma = P.sd_park(bundle['bars'])
    point = next(e['point'] for e in doc['events'] if e['name'].startswith('B2'))
    if not all(math.isfinite(x) and x > 0 for x in (point, sigma)):
        raise ValueError('Invalid sizing inputs')
    return {'source': src, 'input_bundle_sha': doc['input_bundle'], 'sd_park42': sigma, 'point_lr': point,
            'weights': P.weights(point, sigma, P.constants(P.load_protocol()))}


def paired_forecast(cap):
    if cap['state'] != 'ok':
        return {'state': 'abstained', 'capture': cap, 'reason': cap['state']}
    p, s = cap['flows']['perp'], cap['flows']['spot']
    combined = (p['signed'] + s['signed']) / (p['volume'] + s['volume'])
    def prob(x):
        return .75 if x > .15 else .25 if x < -.15 else .5
    rp = cap['raw']['perp']['received_ms']
    both = max(r['received_ms'] for r in cap['raw'].values())
    entry = lambda t: (t + 5 * MIN + MIN - 1) // MIN * MIN
    return {'state': 'ready', 'capture': cap,
            'entries': {'perp_original_clock': entry(rp), 'perp_synchronized_clock': entry(both),
                        'combined_synchronized_clock': entry(both)},
            'probabilities': {'perp_original_clock': prob(p['imbalance']), 'perp_synchronized_clock': prob(p['imbalance']),
                              'combined_synchronized_clock': prob(combined)},
            'deadline_ms': entry(rp), 'combined_imbalance': combined}


def prepare(base, clock=U.clock_ms, get=C.fetch):
    register(base, clock())
    a = activation(base)
    if not a:
        return
    j, attempts = Journal(base, 'forecasts'), Journal(base, 'attempts')
    now = clock()
    # Train before timing-sensitive fetches. Artifacts are retained inside each forecast, so publication binds them.
    fits = {kind: M.daily_fit(base, kind, now) for kind in ('range', 'state')}
    now = clock()
    store = Store(base, now)
    for kind, step, delay in [('turnover', 4 * HOUR, 90 * MIN), ('range', 4 * HOUR, 25 * MIN),
                              ('state', HOUR, 25 * MIN), ('paired', 15 * MIN, 25 * MIN)]:
        for slot in slots(a['first_slot'], now, step):
            key = f'{kind}-{slot}'
            if j.get(key):
                continue
            t = clock()
            d = {'study': kind, 'slot': slot, 'prepared_ms': t, 'deadline_ms': slot + delay, 'state': 'missed'}
            if t >= d['deadline_ms']:
                d['reason'] = 'no on-time preparation'
            elif kind in ('range', 'turnover'):
                src = source(base, slot, '24h' if kind == 'range' else '4h', t)
                if not src:
                    attempts.add(f'{key}-{t}', {'study': kind, 'slot': slot, 'time': t, 'state': 'waiting-for-source'})
                    continue                  # retry while the original deadline remains open
                if kind == 'turnover':
                    d.update(turnover_forecast(src, base), state='ready')
                else:
                    fit = fits['range']
                    e = next(e for e in src['document']['events'] if e['name'].startswith('B2'))
                    d.update(source=src, fit={'id': fit['id'], 'sha256': fit['sha256']}, control=e, deadline_ms=U.ms(U.parse(src['document']['start_utc'])),
                             end_ms=U.ms(U.parse(src['document']['horizon_utc'])))
                    if fit['data']['state'] == 'ready':
                        d.update(state='ready', calibrated=M.calibrated(e, fit['data']))
                    else:
                        d.update(state='warmup', reason='fewer than 40 eligible matured training outcomes')
            elif kind == 'state':
                row = M.state_panel(store, slot, slot + 1)[0]
                fit = fits['state']
                eligible, reasons = panel.eligible(row, M.feature_sets()['full'])
                d.update(row=row, fit={'id': fit['id'], 'sha256': fit['sha256']}, entry=slot + 30 * MIN, end_ms=slot + 270 * MIN)
                if fit['data']['state'] != 'ready':
                    d.update(state='warmup', reason='fewer than 200 jointly eligible matured training rows')
                elif not eligible:
                    d.update(state='abstained', reasons=reasons)
                else:
                    d.update(state='ready', probabilities={k: M.predict(m, row['features']) for k, m in fit['data']['models'].items()})
            else:
                d.update(paired_forecast(C.pair_capture(slot, get)))
            d['prepared_ms'] = clock()
            if d['state'] == 'ready' and d['prepared_ms'] >= d['deadline_ms']:
                d.update(state='late', reason='computation/capture crossed deadline')
            j.add(key, d)


def simulate(d, quote, prior):
    cfg = protocol()['turnover']
    proto = P.load_protocol()
    out = {}
    for scenario in P.SCENARIOS:
        for arm, (model, band) in cfg['arms'].items():
            key = f'{scenario}/{arm}'
            old = prior.get(key)
            st = {'cash': old['cash_after'], 'btc': old['btc_after']} if old else {'cash': 100000., 'btc': 0.}
            _, rec = P.rebalance(st, d['weights'][model], quote, proto['costs'][scenario], band)
            rec.update(fill_ms=quote['t_received_ms'], slot=d['slot'], scenario=scenario, arm=arm,
                       return_log=math.log(rec['equity_pre'] / old['equity_pre']) if old else None,
                       duration_hours=(quote['t_received_ms'] - old['fill_ms']) / HOUR if old else None)
            if old and rec['duration_hours'] <= 0:
                raise ValueError('Execution clock is not increasing')
            out[key] = rec
    return out


def turnover_chain(base):
    byid = {r['id']: (r, c) for r, c in verified(base)}
    prior, good = {}, []
    for e in Journal(base, 'executions').rows:
        r, c = byid.get(e['id'], (None, None))
        x = e['data']
        if not r or not c or not c['data']['eligible'] or x['forecast_sha'] != r['sha256'] or x['confirmation_sha'] != c['sha256']:
            raise ValueError('Unbound sizing execution')
        valid, why = P.eligible_quote(x['quote'], c['data']['confirmed_ms'], r['data']['deadline_ms'])
        if not valid:
            raise ValueError('Ineligible sizing quote: ' + why)
        want = simulate(r['data'], x['quote'], prior)
        if x['prior_sha'] != U.sha(prior) or x['arms'] != want:
            raise ValueError('Sizing state/arms do not reproduce')
        prior = want
        good.append(e)
    return prior, good


def execute(base, clock=U.clock_ms, fetch_quote=C.depth_quote):
    prior, _ = turnover_chain(base)
    journal, attempts = Journal(base, 'executions'), Journal(base, 'quote_attempts')
    for r, c in verified(base):
        d = r['data']
        if d['study'] != 'turnover' or journal.get(r['id']) or not c or not c['data']['eligible']:
            continue
        if clock() >= d['deadline_ms']:
            continue
        try:
            q = fetch_quote('https://www.binance.com/api/v3/depth?symbol=BTCUSDT&limit=20')
            ok, why = P.eligible_quote(q, c['data']['confirmed_ms'], d['deadline_ms'])
            if not ok:
                raise ValueError(why)
        except Exception as exc:
            attempts.add(f'{r["id"]}-{clock()}', {'state': 'unavailable', 'reason': str(exc)[:300]})
            continue
        # All eight arm/scenario rows + quote + prior binding in ONE atomic record. Never a partial ledger.
        arms = simulate(d, q, prior)
        journal.add(r['id'], {'forecast_sha': r['sha256'], 'confirmation_sha': c['sha256'], 'prior_sha': U.sha(prior),
                              'quote': q, 'arms': arms})
        prior = arms


def score_record(base, r, now, bars, rc_scores):
    d = r['data']
    if d['study'] == 'range':
        if now <= d['end_ms']:
            return None
        try:
            o = B.rc1d_outcome(base, d['source']['id'], rc_scores)
        except B.Unscored:
            return None
        if not o['eligible'] or o['scored_ms'] > now:
            return None
        doc, entry, _ = U.rc1d_record(base, d['source']['id'])
        if entry['sha256'] != d['source']['frozen_sha'] or doc != d['source']['document']:
            raise ValueError('Range source changed after preparation')
        y = o['realized']
        arms = {}
        for name, e in [('control', d['control']), ('calibrated', d['calibrated'])]:
            arms[name] = {'interval_score': M.interval_score(e['q10'], e['q90'], y),
                          'covered': e['q10'] <= y <= e['q90'], 'width': e['q90'] - e['q10']}
        return {'outcome': o, 'arms': arms, 'primary_difference': arms['calibrated']['interval_score'] - arms['control']['interval_score']}
    if d['study'] == 'state':
        o = M.price_outcome(bars, d['entry'], 240, now)
        if not o:
            return None
        losses = {k: (p - o['y']) ** 2 for k, p in d['probabilities'].items()}
        return {'outcome': o, 'losses': losses, 'primary_difference': losses['full'] - losses['baseline'],
                'event': d['row'].get('event', False)}
    if d['study'] == 'paired':
        result = {}
        for horizon in protocol()['paired']['horizons_minutes']:
            arms = {}
            for arm, entry in d['entries'].items():
                o = M.price_outcome(bars, entry, horizon, now)
                if not o:
                    return None                 # common joint population for all reported contrasts
                arms[arm] = {'outcome': o, 'brier': (d['probabilities'][arm] - o['y']) ** 2}
            result[str(horizon)] = arms
        primary = result['60']
        return {'horizons': result, 'primary_difference': primary['combined_synchronized_clock']['brier'] - primary['perp_synchronized_clock']['brier']}
    return None


def score(base, now):
    j = Journal(base, 'scores')
    bars = Store(base, now).bars('binance_klines_1m_BTCUSDT_perp')
    rc_scores = B._rc1d_scores(base)
    for r, c in verified(base):
        if not c or not c['data']['eligible']:
            continue
        old = j.get(r['id'])
        if old:
            if old['data']['forecast_sha'] != r['sha256'] or old['data']['confirmation_sha'] != c['sha256']:
                raise ValueError('Unbound score')
            continue
        result = score_record(base, r, now, bars, rc_scores)
        if result:
            j.add(r['id'], {'study': r['data']['study'], 'slot': r['data']['slot'], 'scored_ms': now,
                           'forecast_sha': r['sha256'], 'confirmation_sha': c['sha256'], **result})
