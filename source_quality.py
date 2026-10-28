"""Operational no-trade diagnostics; never rewrites bars, forecasts or frozen eligibility."""
import json
from pathlib import Path
from desk import stream_util as U
from lab.data import Store
from research_tools.market_studies import core as K

PATH = Path('streams/market-studies/source-quality/events.jsonl')
MIN_RUN = 5
SERIES = ['binance_klines_1m_' + s + '_perp' for s in ('BTCUSDT', 'ETHUSDT', 'SOLUSDT')]


def flat_runs(bars, minimum=MIN_RUN):
    runs, current = [], []
    def finish():
        if len(current) >= minimum:
            start, end = current[0], current[-1] + K.MIN
            recovery = next((t for t in sorted(bars) if t >= end and bars[t].get('n', 0) > 0
                             and bars[t].get('v', 0) > 0), None)
            runs.append({'start_ms': start, 'end_ms': end, 'minutes': len(current),
                         'price': bars[start]['c'], 'state': 'recovered' if recovery is not None else 'unresolved',
                         'recovery_ms': recovery, 'known_ms': max(bars[t]['avail'] for t in current),
                         'bars_sha': U.sha([bars[t] for t in current])})
    for t, b in sorted(bars.items()):
        flat = b.get('n') == 0 and b.get('v') == 0 and b.get('c', 0) > 0 and all(b.get(k) == b['c'] for k in ('o','h','l'))
        if current and (not flat or t != current[-1] + K.MIN or b['c'] != bars[current[-1]]['c']):
            finish(); current = []
        if flat:
            current.append(t)
    finish()
    return runs


def impacts(base, incident):
    from research_tools.state_v2 import core as V
    out = []
    if incident['series'] != SERIES[0]:
        return out                         # these study outcomes use BTC perpetuals only
    for version, core in [('v1', K), ('state-v2', V)]:
        for score in core.Journal(base, 'scores').rows:
            d = score['data']
            windows = [('state', d['outcome'])] if d.get('study') == 'state' else []
            if d.get('study') == 'paired':
                windows = [(h + 'm/' + arm, value['outcome']) for h, arms in d['horizons'].items() for arm, value in arms.items()]
            for name, w in windows:
                if w['entry'] < incident['end_ms'] and w['end'] > incident['start_ms']:
                    out.append({'version': version, 'forecast_id': score['id'], 'window': name,
                                'score_sha': score['sha256'], 'entry_ms': w['entry'], 'end_ms': w['end']})
    return out


def build(base, now):
    journal(base)  # validate persisted history even during read-only health checks
    store, incidents = Store(base, now), []
    comparisons = {name: store.bars(series) for name, series in [
        ('spot', 'binance_klines_1m_BTCUSDT_spot'), ('mark', 'binance_markklines_1m_BTCUSDT_perp')]}
    for series in SERIES:
        for item in flat_runs(store.bars(series)):
            item.update(id=series + '-' + str(item['start_ms']), series=series, cause='unknown')
            item['cross_feed_bp'] = {}
            if series == SERIES[0]:
                for name, bars in comparisons.items():
                    b = bars.get(item['end_ms'] - K.MIN)
                    item['cross_feed_bp'][name] = 1e4 * (b['c'] / item['price'] - 1) if b else None
            item['affected_score_windows'] = impacts(base, item)
            incidents.append(item)
    return {'schema': 'source-quality/1', 'generated_ms': now, 'minimum_consecutive_minutes': MIN_RUN,
            'incidents': incidents, 'unresolved': sum(x['state'] == 'unresolved' for x in incidents),
            'interpretation': 'Zero trades and a flat last price are a source-quality anomaly, not proof of an exchange outage. '
                              'Overlapping windows are not independent. Frozen scores and input eligibility remain unchanged.'}


def journal(base):
    path = Path(base) / PATH
    rows = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    prev, latest = None, {}
    for row in rows:
        body = {k:v for k,v in row.items() if k != 'sha256'}
        if row['prev'] != prev or U.sha(body) != row['sha256']:
            raise ValueError('Source-quality incident journal corruption')
        prev = row['sha256']; latest[row['incident']['id']] = row
    return rows, prev, latest


def persist(base, report):
    """Append a hash-chained diagnostic event only when an incident grows or recovers."""
    path = Path(base) / PATH
    rows, prev, latest = journal(base)
    for incident in report['incidents']:
        core = {k:v for k,v in incident.items() if k != 'affected_score_windows'}
        old = latest.get(incident['id'])
        if old and old['incident'] == core:
            continue
        body = {'incident': core, 'detected_ms': report['generated_ms'],
                'first_detected_ms': old['first_detected_ms'] if old else report['generated_ms'], 'prev': prev}
        row = dict(body, sha256=U.sha(body)); rows.append(row); prev = row['sha256']
    if rows:
        K.atomic(path, b''.join(U.canonical(r) + b'\n' for r in rows))
