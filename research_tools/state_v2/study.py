"""Separate prospective evidence for the corrected state feature; never re-score v1."""
import json
from desk import stream_util as U
from lab.data import Store
from research_tools import panel
from research_tools.market_studies.report import paired_summary
from . import core as K, models as M


def prepare(base, clock=U.clock_ms):
    K.register(base, clock())
    activation = K.activation(base)
    if not activation:
        return
    fit = M.daily_fit(base, clock())
    now = clock()
    store, journal = Store(base, now), K.Journal(base, 'forecasts')
    for slot in K.slots(activation['first_slot'], now, K.HOUR):
        key = f'state-{slot}'
        if journal.get(key):
            continue
        d = {'study': 'state', 'version': 'market-state-2', 'slot': slot, 'state': 'missed',
             'prepared_ms': clock(), 'deadline_ms': slot + 25 * K.MIN}
        if d['prepared_ms'] >= d['deadline_ms']:
            d['reason'] = 'no on-time preparation'
        else:
            row = M.state_panel(store, slot, slot + 1)[0]
            eligible, reasons = panel.eligible(row, M.feature_sets()['full'])
            d.update(row=row, fit={'id': fit['id'], 'sha256': fit['sha256']},
                     entry=slot + 30 * K.MIN, end_ms=slot + 270 * K.MIN)
            if fit['data']['state'] != 'ready':
                d.update(state='warmup', reason='fewer than 200 jointly eligible matured training rows')
            elif not eligible:
                d.update(state='abstained', reasons=reasons)
            else:
                d.update(state='ready', probabilities={k: M.predict(m, row['features']) for k, m in fit['data']['models'].items()})
        d['prepared_ms'] = clock()
        if d['state'] == 'ready' and d['prepared_ms'] >= d['deadline_ms']:
            d.update(state='late', reason='computation crossed deadline')
        journal.add(key, d)


def bound_scores(base, rows):
    forecasts = {r['id']: (r, c) for r, c in rows}
    out = {}
    for score in K.Journal(base, 'scores').rows:
        f, c = forecasts.get(score['id'], (None, None))
        d = score['data']
        if not f or not c or not c['data']['eligible'] or d['forecast_sha'] != f['sha256'] or d['confirmation_sha'] != c['sha256']:
            raise ValueError('Unbound state-v2 score')
        out[score['id']] = d
    return out


def score(base, now):
    rows = K.verified(base)
    existing = bound_scores(base, rows)
    journal = K.Journal(base, 'scores')
    bars = Store(base, now).bars('binance_klines_1m_BTCUSDT_perp')
    for f, c in rows:
        if f['id'] in existing or not c or not c['data']['eligible']:
            continue
        d = f['data']
        outcome = M.price_outcome(bars, d['entry'], 240, now)
        if outcome:
            losses = {k: (p - outcome['y']) ** 2 for k, p in d['probabilities'].items()}
            journal.add(f['id'], {'study': 'state', 'slot': d['slot'], 'scored_ms': now,
                'forecast_sha': f['sha256'], 'confirmation_sha': c['sha256'], 'outcome': outcome,
                'losses': losses, 'primary_difference': losses['full'] - losses['baseline'],
                'event': d['row'].get('event', False)})


def build(base, now):
    a = K.activation(base)
    rows = K.verified(base)
    scores = bound_scores(base, rows)
    byslot = {f['data']['slot']: (f, c) for f, c in rows}
    opportunities = []
    for slot in K.slots(a['first_slot'], now, K.HOUR) if a else []:
        f, c = byslot.get(slot, (None, None))
        d = f['data'] if f else {}
        eligible = bool(c and c['data']['eligible'])
        s = scores.get(f['id']) if f else None
        opportunities.append({'slot': slot, 'recorded': f is not None, 'state': d.get('state', 'no-run'),
                              'eligible': eligible, 'scored': s is not None,
                              'difference': s['primary_difference'] if s else None})
    values = [r['difference'] for r in opportunities]
    secondary = {name: paired_summary([scores[f'state-{r["slot"]}']['losses'][name] -
                    scores[f'state-{r["slot"]}']['losses']['baseline'] if r['scored'] else None
                    for r in opportunities], 168) for name in ('flow', 'positioning')}
    strata = {name: paired_summary([scores[f'state-{r["slot"]}']['primary_difference']
                    if r['scored'] and scores[f'state-{r["slot"]}']['event'] == event else None
                    for r in opportunities], 168) for name, event in [('event', True), ('ordinary', False)]}
    return {'version': 'market-state-2', 'generated_utc': U.iso_ms(now), 'activation': a,
            'scheduled': len(opportunities), 'recorded': len(rows),
            'eligible': sum(r['eligible'] for r in opportunities), 'scored': len(scores),
            'abstained': sum(r['state'] == 'abstained' for r in opportunities),
            'primary': paired_summary(values, 168), 'secondary': secondary, 'strata': strata,
            'opportunities': opportunities,
            'interpretation': 'Separate v2 prospective clock. No v1 pooling or retroactive repair; descriptive only.'}


def write(base, now):
    out = build(base, now)
    K.atomic(base / 'reports/market_state_v2.json', (json.dumps(out, indent=2, allow_nan=False) + '\n').encode())
    text = ('# Market state v2\n\n' + out['interpretation'] + '\n\nGenerated ' + out['generated_utc'] +
            f'. Scheduled: {out["scheduled"]}; recorded: {out["recorded"]}; eligible: {out["eligible"]}; '
            f'abstained: {out["abstained"]}; scored: {out["scored"]}.\n\n' +
            f'Primary paired Brier difference: {out["primary"]["mean_difference"]}. '
            f'90% block interval: {out["primary"]["ci90"]} (null means insufficient evidence).\n\n' +
            '[Full report, clock, secondary contrasts and scheduled opportunities](market_state_v2.json)\n')
    text += ('\nFirst scheduled opportunity: ' + U.iso_ms(out['activation']['first_slot']) + '.\n'
             if out['activation'] else '\nNot activated; registration alone is not launch.\n')
    K.atomic(base / 'reports/market_state_v2.md', text.encode())
