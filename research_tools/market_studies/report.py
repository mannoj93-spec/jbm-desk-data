"""Conservative paired summaries, accounting for scheduled and failed opportunities."""
from collections import Counter
import json
import gzip
import hashlib
from pathlib import Path
import math
import random
from desk import paper_ps1 as P, stream_util as U
from . import experiments as X, models as M
from .core import DAY, HOUR, MIN, Journal, activation, atomic, protocol, slots, verified


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def paired_summary(values, block):
    good = [v for v in values if v is not None]
    ci = None
    if len(good) >= 10 * block:
        rng = random.Random(20261024)
        means = []
        for _ in range(2000):
            sample = []
            while len(sample) < len(values):
                k = rng.randrange(len(values) - block + 1)
                sample.extend(values[k:k + block])
            valid = [v for v in sample[:len(values)] if v is not None]
            if valid:
                means.append(mean(valid))
        ci = [M.quantile(means, .05), M.quantile(means, .95)]
    return {'paired': len(good), 'mean_difference': mean(good), 'block_size': block,
            'complete_block_equivalents': len(good) // block, 'ci90': ci,
            'method': 'moving blocks on the scheduled grid, missing positions retained; paired differences; 2000 draws',
            'status': 'collecting (descriptive); no automatic promotion'}


def hit_summary(pairs):
    """Conditional direction accuracy; neutral forecasts remain visible in the population."""
    selected = [(p, y) for p, y in pairs if p != .5]
    hits = sum((p > .5) == bool(y) for p, y in selected)
    return {'scored': len(pairs), 'directional': len(selected), 'neutral': len(pairs) - len(selected),
            'hits': hits, 'conditional_hit_rate': hits / len(selected) if selected else None}


def turnover_summary(executions, expected):
    arms = {}
    cfg = protocol()['turnover']
    for scenario in P.SCENARIOS:
        for arm in cfg['arms']:
            key = f'{scenario}/{arm}'
            rows = [e['data']['arms'][key] for e in executions]
            closed = rows[:-1]
            rs = [r['return_log'] for r in rows[1:]]
            hs = [r['duration_hours'] for r in rows[1:]]
            stats = P.dw_stats(rs, hs)
            peak, dd = 100000., 0.
            for r in rows:
                peak = max(peak, r['equity_pre'])
                dd = max(dd, 1 - r['equity_pre'] / peak)
            arms[key] = {'closed_intervals': len(rs), 'elapsed_hours': sum(hs), 'sharpe': P.sharpe_dw(rs, hs),
                         'net_return_closed': math.expm1(sum(rs)) if rs else None, 'max_drawdown': dd if rows else None,
                         'annualized_vol': math.sqrt(8760 * stats['var_h']) if stats['var_h'] is not None else None,
                         'exposure': sum(r['w_after'] * h for r, h in zip(closed, hs)) / sum(hs) if hs else None,
                         'cost_closed_usdt': sum(r['cost_vs_mid'] for r in closed) if closed else None,
                         'turnover_annualized': (sum(r['notional'] for r in closed) / mean([r['equity_pre'] for r in closed]) * 8760 / sum(hs)) if hs else None,
                         'open_interval': {'fill_ms': rows[-1]['fill_ms'], 'cost_usdt': rows[-1]['cost_vs_mid']} if rows else None}
    a, b = arms['stressed/B2_10']['sharpe'], arms['stressed/B2_05']['sharpe']
    ci = None
    if len(executions) - 1 >= 420:
        pairs = [e['data']['arms'] for e in executions[1:]]
        ci = P.bootstrap_sharpe_diff([r['stressed/B2_10']['return_log'] for r in pairs],
                                    [r['stressed/B2_05']['return_log'] for r in pairs],
                                    [r['stressed/B2_10']['duration_hours'] for r in pairs], block=42, reps=2000, seed=20261024)
    return {'executed': len(executions), 'scheduled': expected, 'coverage': len(executions) / expected if expected else None,
            'primary_stressed_sharpe_difference': a - b if a is not None and b is not None else None,
            'primary_ci90': ci, 'arms': arms, 'status': 'collecting (descriptive)' if executions else 'not launched',
            'checkpoint_rules': cfg['review']}


def insurance_ranges(stress):
    groups = {}
    for row in stress:
        if row['state'] == 'ok':
            for a in row['assets']:
                key = ','.join(sorted(row['pool_symbols'])) + '/' + a['asset']
                groups.setdefault(key, []).append(a['balance'])
    return {k: {'n': len(xs), 'min': min(xs), 'max': max(xs), 'unique': len(set(xs))} for k, xs in groups.items()}


def pilot_summary(base, first, now):
    stress = [r['data'] for r in Journal(base, 'stress').rows]
    liq = [r['data'] for r in Journal(base, 'liquidations').rows]
    for capture in liq:
        if capture.get('capture_file'):
            raw = gzip.decompress((Path(base) / capture['capture_file']).read_bytes())
            if hashlib.sha256(raw).hexdigest() != capture['capture_sha']:
                raise ValueError('Liquidation capture artifact changed')
            original = json.loads(raw)
            if any(original.get(k) != v for k, v in capture.items() if k not in ('capture_file', 'capture_sha', 'page_count', 'order_count')):
                raise ValueError('Liquidation summary differs from retained capture')
    options = [r['data'] for r in Journal(base, 'options').rows]
    for q in options:
        raw = gzip.decompress((Path(base) / q['legs_file']).read_bytes())
        if hashlib.sha256(raw).hexdigest() != q['legs_sha']:
            raise ValueError('Options leg-quality artifact changed')
    pairs = []
    groups = {}
    for r in liq:
        groups.setdefault(r['end'], {})[r['vintage_hours']] = r
    for end, vs in sorted(groups.items()):
        original = vs.get(0)
        for v in (1, 6, 18):
            later = vs.get(v)
            comparable = original and later and original['state'] == later['state'] == 'ok'
            pairs.append({'end': end, 'vintage_hours': v, 'comparable': bool(comparable),
                          'size_revision': later['total_contracts'] - original['total_contracts'] if comparable else None,
                          'signal_flip': later['signal'] != original['signal'] if comparable else None,
                          'eligibility_flip': later['eligible'] != original['eligible'] if comparable else None})
    changes, term = [], []
    for x in options:
        a, b = x['rr25_7d'], x['rr25_30d']
        if a['state'] == b['state'] == 'ok':
            term.append({'t': x['observed_at'], 'rr25_30d_minus_7d': b['value'] - a['value']})
    for a, b in zip(options, options[1:]):
        if 50 * MIN <= b['observed_at'] - a['observed_at'] <= 70 * MIN and a['rr25_7d']['state'] == b['rr25_7d']['state'] == 'ok':
            changes.append({'t': b['observed_at'], 'change_7d': b['rr25_7d']['value'] - a['rr25_7d']['value']})
    risks = [x['risk'] for x in stress if x['state'] == 'ok']
    return {'stress': {'opportunities': len(slots(first, now, 30 * MIN)) if first else 0, 'records': len(stress),
                       'states': dict(Counter(x['state'] for x in stress)), 'ratings': dict(Counter(risks)),
                       'rating_transitions': sum(a['risk'] != b['risk'] for a, b in zip(stress, stress[1:]) if a['state'] == b['state'] == 'ok' and b['slot'] - a['slot'] == 30 * MIN),
                       'insurance_ranges': insurance_ranges(stress),
                       'interpretation': 'risk ratings, not realized ADL events; no predictive study'},
            'liquidations': {'states': dict(Counter(r['state'] for r in liq)), 'revisions': pairs,
                             'interpretation': 'source-specific retrospective diagnostic; first observations stay immutable'},
            'options': {'captures': len(options), 'expected_hourly_slots': len(slots(first, now, HOUR)) if first else 0,
                        'rr25_7d_states': dict(Counter(r['rr25_7d']['state'] for r in options)),
                        'rr25_30d_states': dict(Counter(r['rr25_30d']['state'] for r in options)),
                        'rejections': dict(sum((Counter(r['rejections']) for r in options), Counter())),
                        'changes': changes, 'term_structure': term, 'interpretation': 'usability only; no predictive admission'}}


def build(base, now):
    a = activation(base)
    forecasts = verified(base)
    _, executions = X.turnover_chain(base)
    scores = Journal(base, 'scores')
    # Reproduce cached scores from their original cutoff and immutable input bindings.
    from lab.data import Store
    from desk import companion_job as B
    bars = Store(base, now).bars('binance_klines_1m_BTCUSDT_perp')
    rc = B._rc1d_scores(base)
    paired = {}
    for r, c in forecasts:
        s = scores.get(r['id'])
        if s:
            x = s['data']
            if not c or not c['data']['eligible'] or x['forecast_sha'] != r['sha256'] or x['confirmation_sha'] != c['sha256']:
                raise ValueError('Report found an unbound score')
            expected = X.score_record(base, r, x['scored_ms'], bars, rc)
            if not expected or any(x.get(k) != v for k, v in expected.items()):
                raise ValueError('Cached score failed reproduction')
            paired[r['id']] = x
    if set(scores.index) - {r['id'] for r, _ in forecasts}:
        raise ValueError('Orphan study score')
    out = {'generated_ms': now, 'activation': a, 'studies': {}, 'pilots': pilot_summary(base, a['first_slot'] if a else None, now)}
    launch = Journal(base, 'launches')
    for kind, step, block in [('turnover', 4 * HOUR, 42), ('range', 4 * HOUR, 42), ('state', HOUR, 168), ('paired', 15 * MIN, 672)]:
        fs = [(r, c) for r, c in forecasts if r['data']['study'] == kind]
        expected_slots = list(slots(a['first_slot'], now, step)) if a else []
        ss = [paired[r['id']] for r, _ in fs if r['id'] in paired]
        status = Counter(r['data']['state'] for r, _ in fs)
        eligible = [(r, c) for r, c in fs if c and c['data']['eligible']]
        first = executions[0]['data']['quote']['t_received_ms'] if kind == 'turnover' and executions else (
            eligible[0][1]['data']['confirmed_ms'] if kind != 'turnover' and eligible else None)
        if first is not None:
            launch.add(kind, {'first_observed_ms': first, 'kind': 'first verified execution' if kind == 'turnover' else 'first on-time confirmed forecast'})
        elif launch.get(kind):
            raise ValueError('Launch without verified evidence')
        summary = {'scheduled': len(expected_slots), 'recorded': len(fs), 'states': dict(status),
                   'missing_run': len(expected_slots) - len(fs), 'on_time_published': len(eligible),
                   'late_publication': sum(c is not None and not c['data']['eligible'] and r['data']['state'] == 'ready' for r, c in fs),
                   'pending_confirmation': sum(c is None and r['data']['state'] == 'ready' for r, c in fs),
                   'scored': len(ss), 'launch_ms': first, 'status': 'collecting (descriptive)' if first is not None else 'registered; not launched'}
        if kind == 'turnover':
            summary['results'] = turnover_summary(executions, len(expected_slots))
            results = summary['results']
            days = (now - first) / DAY if first is not None else 0
            results['review'] = {'days_since_launch': days, 'C1_due': days >= 180 and len(executions) - 1 >= 420,
                                 'C2_due': days >= 365 and len(executions) - 1 >= 840,
                                 'action': 'operator review only; no automatic status change'}
            results['secondary_sharpe_contrasts'] = {}
            for label, ka, kb in [('ordinary_B2_10_minus_05', 'ordinary/B2_10', 'ordinary/B2_05'),
                                  ('stressed_B2_10_minus_VOL_10', 'stressed/B2_10', 'stressed/VOL_10')]:
                va, vb = results['arms'][ka]['sharpe'], results['arms'][kb]['sharpe']
                results['secondary_sharpe_contrasts'][label] = va-vb if va is not None and vb is not None else None
        else:
            lookup = {x['slot']: x['primary_difference'] for x in ss}
            summary['results'] = paired_summary([lookup.get(t) for t in expected_slots], block)
            summary['review_eligible'] = first is not None and now - first >= 180 * DAY and len(ss) >= 10 * block
            if kind == 'range':
                summary['calibration'] = {k: {'coverage': mean([float(x['arms'][k]['covered']) for x in ss]),
                                             'width': mean([x['arms'][k]['width'] for x in ss])} for k in ('control', 'calibrated')}
            elif kind == 'state':
                summary['secondary_brier'] = {k: mean([x['losses'][k] for x in ss]) for k in M.feature_sets()}
                summary['event_ordinary'] = {k: {'n': sum(x['event'] == flag for x in ss),
                                                'difference': mean([x['primary_difference'] for x in ss if x['event'] == flag])}
                                            for k, flag in [('event', True), ('ordinary', False)]}
            elif kind == 'paired':
                byslot = {r['data']['slot']: r['data'] for r, _ in eligible}
                summary['conditional_hits'] = {
                    str(h): {arm: hit_summary([(byslot[x['slot']]['probabilities'][arm], x['horizons'][str(h)][arm]['outcome']['y']) for x in ss])
                             for arm in protocol()['paired']['arms']} for h in (60, 15)}
                summary['equal_entry_clock_share'] = mean([float(r['data']['entries']['perp_original_clock'] == r['data']['entries']['perp_synchronized_clock']) for r, _ in eligible])
                summary['secondary_15m_difference'] = mean([x['horizons']['15']['combined_synchronized_clock']['brier'] - x['horizons']['15']['perp_synchronized_clock']['brier'] for x in ss])
                summary['clock_only_60m_difference'] = mean([x['horizons']['60']['perp_synchronized_clock']['brier'] - x['horizons']['60']['perp_original_clock']['brier'] for x in ss])
        out['studies'][kind] = summary
    return out


def write(base, now):
    from pathlib import Path
    out = build(base, now)
    lines = ['# Market studies', '', f'Generated {U.iso_ms(now)}. Paper research only. Missing outcomes are never zero.', '',
             '| Study | Status | Scheduled | On-time published | Scored / executed |', '|---|---|---:|---:|---:|']
    for k, s in out['studies'].items():
        n = s['results']['executed'] if k == 'turnover' else s['scored']
        lines.append(f'| {k} | {s["status"]} | {s["scheduled"]} | {s["on_time_published"]} | {n} |')
    def number(value, percent=False):
        return '—' if value is None else (f'{100*value:.2f}%' if percent else f'{value:.6g}')
    lines += ['', '## Primary comparisons', '',
              'Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.', '',
              '| Study | Paired difference | 90% block interval | First verified launch |',
              '|---|---:|---|---|']
    for kind, study in out['studies'].items():
        result = study['results']
        value = result.get('primary_stressed_sharpe_difference') if kind == 'turnover' else result.get('mean_difference')
        ci = result.get('primary_ci90') if kind == 'turnover' else result.get('ci90')
        interval = '— (insufficient blocks)' if ci is None else f'{number(ci[0])} to {number(ci[1])}'
        launched = U.iso_ms(study['launch_ms']) if study['launch_ms'] is not None else 'not launched'
        lines.append(f'| {kind} | {number(value)} | {interval} | {launched} |')
    lines += ['', '## Turnover accounts', '',
              'Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.', '',
              '| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |',
              '|---|---:|---:|---:|---:|---:|---:|']
    for key, a in out['studies']['turnover']['results']['arms'].items():
        lines.append(f'| {key} | {number(a["net_return_closed"], True)} | {number(a["annualized_vol"], True)} | '
                     f'{number(a["exposure"], True)} | {number(a["max_drawdown"], True)} | '
                     f'{number(a["turnover_annualized"])} | {number(a["cost_closed_usdt"])} |')
    lines += ['', '## Range calibration', '', '| Arm | 80% interval coverage | Mean interval width (ln H/L) |', '|---|---:|---:|']
    for key, a in out['studies']['range'].get('calibration', {}).items():
        lines.append(f'| {key} | {number(a["coverage"], True)} | {number(a["width"])} |')
    lines += ['', '## Paired-flow direction checks', '',
              'Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.', '',
              '| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |', '|---|---|---:|---:|---:|---:|']
    for horizon, arms in out['studies']['paired'].get('conditional_hits', {}).items():
        for arm, h in arms.items():
            lines.append(f'| {horizon}m | {arm} | {h["scored"]} | {h["directional"]} | {h["neutral"]} | {number(h["conditional_hit_rate"], True)} |')
    pilot = out['pilots']
    options, stress, liq = pilot['options'], pilot['stress'], pilot['liquidations']
    comparable = [x for x in liq['revisions'] if x['comparable']]
    lines += ['', '## Data usability pilots', '',
              f'- Options: {options["captures"]} captures; usable 7d RR25 in {options["rr25_7d_states"].get("ok", 0)}, '
              f'usable 30d RR25 in {options["rr25_30d_states"].get("ok", 0)}; {len(options["changes"])} valid hourly changes.',
              f'- Liquidations: {len(comparable)} comparable first/later vintage pairs; '
              f'{sum(x["signal_flip"] for x in comparable)} direction changes. Capture states: `{json.dumps(liq["states"], sort_keys=True)}`.',
              f'- Exchange stress: {stress["records"]}/{stress["opportunities"]} scheduled records. '
              f'Capture states: `{json.dumps(stress["states"], sort_keys=True)}`. Ratings: `{json.dumps(stress["ratings"], sort_keys=True)}`.',
              '', 'These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.',
              '', 'The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.',
              'A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.',
              'No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).', '']
    atomic(Path(base) / 'reports/market_studies.json', json.dumps(out, indent=2, allow_nan=False).encode() + b'\n')
    atomic(Path(base) / 'reports/market_studies.md', '\n'.join(lines).encode())
    return out
