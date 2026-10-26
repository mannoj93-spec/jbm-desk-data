"""Read-only operational diagnostics for market studies v1; never changes its frozen research identity.

report writes only reports/market_study_health.{json,md}; check recomputes from journals on the current
clock without writing. Operational alerts are not research admission or promotion criteria.
"""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import statistics
import time

from desk import stream_util as U
from research_tools.market_studies import core as K, experiments as X

ROOT = Path(__file__).resolve().parent
SCHEMA = 'market-study-health/1'
GRACE = 5 * K.MIN             # allow final evidence persistence before declaring a missed deadline
STALE = 45 * K.MIN


def distribution(xs):
    xs = sorted(x for x in xs if x is not None)
    return {'n': len(xs), 'min': min(xs) if xs else None, 'median': statistics.median(xs) if xs else None,
            'p90': xs[min(len(xs)-1, int(.9*(len(xs)-1)))] if xs else None, 'max': max(xs) if xs else None}


def coverage(opportunities):
    counts = Counter(x['state'] for x in opportunities)
    good = [x for x in opportunities if x['state'] == 'ok']
    streak = 0
    for x in reversed(opportunities):
        if x['state'] == 'ok':
            break
        streak += 1
    n = len(opportunities)
    return {'due': n, 'successful': len(good), 'coverage': len(good)/n if n else None,
            'states': dict(counts), 'consecutive_misses': streak,
            'last_success_ms': max((x['success_ms'] for x in good), default=None)}


def period_coverage(closed, pending, since):
    """Keep the closed denominator; a verified newer success can clear the current miss alarm."""
    closed = [x for x in closed if x['slot'] >= since]
    pending = [x for x in pending if x['slot'] >= since and x['state'] == 'ok']
    out = coverage(closed)
    recovered = bool(pending and out['consecutive_misses'] and
                     max(x['slot'] for x in pending) > max(x['slot'] for x in closed))
    out.update(pending_successful=len(pending), recovered_before_close=recovered,
               active_consecutive_misses=0 if recovered else out['consecutive_misses'])
    return out


def capture_coverage(closed, pending, since, grouped=False):
    out = period_coverage(closed, pending, since)
    if grouped:
        by_time = defaultdict(list)
        for x in closed:
            if x['slot'] >= since:
                by_time[x['slot']].append(x)
        # Four liquidation vintages at one capture time are one opportunity for the continuity alarm.
        times = [{'state': 'ok' if any(x['state'] == 'ok' for x in xs) else 'missed', 'success_ms': t}
                 for t, xs in sorted(by_time.items())]
        out['consecutive_misses'] = coverage(times)['consecutive_misses']
        out['recovered_before_close'] = bool(out['recovered_before_close'] and out['consecutive_misses'])
        out['active_consecutive_misses'] = 0 if out['recovered_before_close'] else out['consecutive_misses']
    return out


def depth_diagnostics(rows, since, now):
    records, reasons, ages = [], Counter(), []
    for f, _ in rows:
        d = f['data']
        if d['study'] != 'state' or not since <= d['slot'] <= now:
            continue
        depth = d.get('row', {}).get('inputs', {}).get('sources', {}).get('depth', {})
        age = depth.get('age_s')
        if age is not None:
            ages.append(age / 60)
        why = d.get('reasons') or ([d['reason']] if d.get('reason') else [])
        if d['state'] == 'abstained':
            reasons.update(why or ['unspecified abstention'])
        records.append({'slot': d['slot'], 'state': d['state'], 'depth_state': depth.get('state', 'unavailable'),
                        'depth_age_minutes': age / 60 if age is not None else None, 'reasons': why})
    return {'forecasts': len(records), 'abstained': sum(x['state'] == 'abstained' for x in records),
            'missing_depth_age': sum(x['depth_age_minutes'] is None for x in records),
            'depth_age_minutes': distribution(ages), 'abstention_reasons': dict(reasons), 'records': records,
            'interpretation': 'Recorded as-of depth ages; unavailable ages are not zero. No feature reselection or threshold changes.'}


def selected_options(d, legs, horizon):
    """Resolve only the immutable strikes/expiries used by this RR25 horizon; never reselect."""
    rr = d[horizon]
    if rr['state'] != 'ok':
        return []
    selected = []
    if not rr.get('expiries'):
        raise ValueError('Usable RR25 has no selected expiries')
    for expiry in dict.fromkeys(rr['expiries']):
        info = d['expiries'][expiry]
        if info['state'] != 'ok':
            raise ValueError('Selected options expiry is not usable')
        for side, key in [('C', 'call_K'), ('P', 'put_K')]:
            matches = []
            for leg in legs:
                parts = (leg.get('instrument') or '').split('-')
                if len(parts) != 4 or parts[0] != 'BTC' or parts[1] != expiry or parts[3] != side:
                    continue
                if float(parts[2]) == info['pair'][key]:
                    matches.append(leg)
            if len(matches) != 1:
                raise ValueError('Selected options leg missing or ambiguous')
            selected.append(matches[0])
    return selected


def bound_scores(base, forecasts):
    out = []
    for r in K.Journal(base, 'scores').rows:
        f, c = forecasts.get(r['id'], (None, None))
        d = r['data']
        if not f or not c or not c['data']['eligible'] or d['forecast_sha'] != f['sha256'] or d['confirmation_sha'] != c['sha256']:
            raise ValueError('Unbound operational score')
        out.append((f['data'], d))
    return out


def paired_diagnostics(pairs):
    groups = defaultdict(list)
    for f, s in pairs:
        if f['study'] == 'paired':
            groups[f['entries']['combined_synchronized_clock']].append((f, s))
    means = [statistics.mean(s['primary_difference'] for _, s in rows) for rows in groups.values()]
    clocks = [f['entries']['perp_original_clock'] == f['entries']['perp_synchronized_clock']
              for rows in groups.values() for f, _ in rows]
    entries = sorted(groups)
    # Distinct entry windows can still overlap. No count here is an effective sample size.
    disjoint, end = 0, None
    for t in entries:
        if end is None or t >= end:
            disjoint += 1
            end = t + K.HOUR
    return {'scored_forecasts': len(clocks), 'unique_entries': len(groups),
            'repeated_entry_groups': sum(len(v) > 1 for v in groups.values()),
            'largest_disjoint_60m_subset': disjoint,
            'equal_entry_clock_share': statistics.mean(clocks) if clocks else None,
            'entry_grouped_mean_difference': statistics.mean(means) if means else None,
            'interpretation': 'Sensitivity only: average within each shared entry, then across entries. '
                              'Overlapping windows remain dependent; no new primary, interval or support claim.'}


def options_diagnostics(base, rows):
    ages, spreads, delta = [], [], []
    rejected, sizes, signatures, switches = Counter(), Counter(), {}, Counter()
    expiry_sets, rolls, count = None, 0, 0
    selected = {h: [] for h in ('rr25_7d', 'rr25_30d')}
    usable = Counter()
    for r in rows:
        d = r['data']
        path = (Path(base) / d['legs_file']).resolve()
        if not path.is_relative_to((Path(base) / K.STREAM / 'option_legs').resolve()):
            raise ValueError('Options evidence path outside study directory')
        raw = gzip.decompress(path.read_bytes())
        if hashlib.sha256(raw).hexdigest() != d['legs_sha']:
            raise ValueError('Options leg evidence hash mismatch')
        legs = json.loads(raw)
        for horizon in selected:
            chosen = selected_options(d, legs, horizon)
            selected[horizon].extend(chosen)
            usable[horizon] += bool(chosen)
        for leg in legs:
            count += 1
            rejected.update(set(leg['reasons']))
            sizes[leg['size_state']] += 1
            ages.append(leg['quote_age_ms'])
            spreads.append(leg['relative_spread'])
            delta.append(leg['delta_distance'])
        # Strike changes within the same expiry are distinct from changes of interpolation expiries.
        for expiry, info in d['expiries'].items():
            if info['state'] == 'ok':
                sig = (info['pair']['call_K'], info['pair']['put_K'])
                if expiry in signatures and signatures[expiry] != sig:
                    switches[expiry] += 1
                signatures[expiry] = sig
        current = tuple(tuple(d[k].get('expiries', [])) for k in ('rr25_7d', 'rr25_30d'))
        if expiry_sets is not None and current != expiry_sets:
            rolls += 1
        expiry_sets = current
    return {'captures': len(rows), 'legs': count, 'rejection_counts': dict(rejected),
            'size_states': dict(sizes), 'quote_age_ms': distribution(ages),
            'relative_spread': distribution(spreads), 'delta_distance': distribution(delta),
            'selected_strike_changes_by_expiry': dict(switches), 'bracketing_expiry_changes': rolls,
            'selected_by_horizon': {h: {'usable_captures': usable[h], 'legs': len(ls),
                'quote_age_ms': distribution([l['quote_age_ms'] for l in ls]),
                'relative_spread': distribution([l['relative_spread'] for l in ls]),
                'delta_distance': distribution([l['delta_distance'] for l in ls]),
                'size_states': dict(Counter(l['size_state'] for l in ls)),
                'diagnostic_reasons': dict(Counter(reason for l in ls for reason in set(l['reasons'])))}
                for h, ls in selected.items()},
            'selected_interpretation': 'Only call/put legs at the recorded interpolation expiries, separately per horizon. '
                'Shared legs count once per capture within each horizon; repeated captures and horizons are dependent. '
                'Diagnostic reasons describe the retained selection and never replace its frozen eligibility.',
            'interpretation': 'All observed legs, not independent samples. Rejection reasons overlap. '
                              'No filter change or predictive admission; quote size stays unavailable when absent.'}


def build(base, now):
    base = Path(base)
    out = {'schema': SCHEMA, 'generated_utc': U.iso_ms(now), 'generated_ms': now, 'window_start_ms': now-K.DAY,
           'stale_after_minutes': STALE//K.MIN, 'paused': (base/K.STREAM/'paused.json').exists(),
           'studies': {}, 'pilots': {}, 'alerts': [], 'warnings': [], 'integrity': 'ok'}
    if not (base/K.STREAM/'registration.jsonl').exists():
        out['alerts'].append('Market studies are not registered; launch state is unknown')
        return out
    # Existing registration is checked, never created by this reader.
    a = K.activation(base)
    if not a:
        out['alerts'].append('Registration exists but activation is not confirmed')
        return out
    first, since = a['first_slot'], now-K.DAY
    config = base / 'market_study_ops.json'
    deployment = json.loads(config.read_text()) if config.exists() else None
    deployment_start = None
    if deployment:
        if deployment['schema'] != 'market-study-operations/1':
            raise ValueError('Invalid operational deployment schema')
        deployment = deployment['deployment']
        deployment_start = U.ms(U.parse(deployment['started_utc']))
        if len(deployment['commit']) != 40 or any(c not in '0123456789abcdef' for c in deployment['commit']):
            raise ValueError('Invalid operational deployment commit')
        out['deployment'] = {**deployment, 'started_ms': deployment_start, 'studies': {}, 'pilots': {}}
    collection_start = min(since, deployment_start) if deployment_start is not None else since
    rows = K.verified(base)
    forecasts = {r['id']: (r, c) for r, c in rows}
    _, executions = X.turnover_chain(base)
    executed = {e['id']: e['data'] for e in executions}
    pairs = bound_scores(base, forecasts)
    scored = {f['study']+'-'+str(f['slot']): s for f, s in pairs}
    runs = [r['data'] for r in K.Journal(base, 'runs').rows if r['data']['stage'] == 'prepare' and r['data']['state'] == 'completed']
    last_run = max((r['ended_ms'] for r in runs), default=None)
    out['last_prepare_ms'] = last_run
    if not out['paused'] and now >= first + STALE and (last_run is None or now-last_run > STALE):
        out['alerts'].append('No successful study preparation in 45 minutes')
    for kind, step, delay in [('turnover', 4*K.HOUR, 90*K.MIN), ('range', 4*K.HOUR, 25*K.MIN),
                              ('state', K.HOUR, 25*K.MIN), ('paired', 15*K.MIN, 30*K.MIN)]:
        opportunities, pending_successes = [], []
        delays = []
        pending = overdue = 0
        # Backlogs do not disappear when the originating opportunity leaves the rolling coverage window.
        for f, c in rows:
            d = f['data']
            if d['study'] != kind or kind == 'turnover' or not c or not c['data']['eligible'] or f['id'] in scored:
                continue
            end = d.get('end_ms', max(d.get('entries', {}).values(), default=d['slot'])+K.HOUR)
            if now <= end+2*K.HOUR:
                pending += 1
            else:
                overdue += 1
        for slot in K.slots(max(first, collection_start), now, step):
            fid = kind+'-'+str(slot)
            r, c = forecasts.get(fid, (None, None))
            d = r['data'] if r else None
            deadline = max(slot+delay, d['deadline_ms']) if d else slot+delay
            ok = bool(c and c['data']['eligible'])
            state = 'ok' if ok else (d['state'] if d else 'no-run')
            if d and d['state'] == 'ready' and not ok:
                state = 'late-publication' if c else 'unconfirmed'
            success = c['data']['confirmed_ms'] if ok else None
            if ok:
                if slot >= since and now >= deadline + GRACE:
                    delays.append((success-slot)/K.MIN)
                if kind == 'turnover':
                    ok = fid in executed
                    state = 'ok' if ok else 'no-execution'
                    success = executed[fid]['quote']['t_received_ms'] if ok else None
            detail = {'slot': slot, 'state': state, 'success_ms': success,
                      'reason': d.get('reason') if d else 'No opportunity record'}
            if now < deadline + GRACE:
                if ok:
                    pending_successes.append(detail)
                continue
            if kind == 'range' and not ok:
                try:
                    fid_source = 'range-rc1d-24h-'+U.iso_ms(slot).replace('-', '').replace(':', '')[:13]+'Z'
                    doc, _, pub = U.rc1d_record(base, fid_source)
                    detail['source_confirmed_ms'] = pub['confirmed'] if pub and pub.get('eligible') else None
                    detail['source_window_start_ms'] = U.ms(U.parse(doc['start_utc']))
                except (ValueError, KeyError, FileNotFoundError):
                    detail['source_confirmed_ms'] = None
            opportunities.append(detail)
        summary = period_coverage(opportunities, pending_successes, since)
        summary.update(pending_outcomes=pending, overdue_scores=overdue,
                       publication_delay_minutes=distribution(delays), opportunities=[x for x in opportunities if x['slot'] >= since])
        out['studies'][kind] = summary
        if deployment_start is not None:
            out['deployment']['studies'][kind] = period_coverage(opportunities, pending_successes, deployment_start)
        if not out['paused'] and summary['active_consecutive_misses'] >= 2:
            out['alerts'].append(f'{kind}: {summary["active_consecutive_misses"]} consecutive closed opportunities missed')
        if overdue:
            out['alerts'].append(f'{kind}: {overdue} scores overdue by more than two hours')
        if summary['coverage'] is not None and summary['coverage'] < .8:
            out['warnings'].append(f'{kind}: last-24h operational coverage below 80% (not a research threshold)')
    for kind, step in [('stress', 30*K.MIN), ('liquidations', K.HOUR), ('options', K.HOUR)]:
        journal = K.Journal(base, kind).rows
        byslot = {}
        for r in journal:
            d = r['data']
            if kind == 'liquidations':
                byslot[(d['end'], d['vintage_hours'])] = d
            elif kind == 'options':
                byslot[d['observed_at']//K.HOUR*K.HOUR] = d
            else:
                byslot[d['slot']] = d
        opportunities, pending_successes = [], []
        starts = K.slots(first+K.HOUR if kind == 'liquidations' else first, now, step)
        for slot in starts:
            for vintage in ([0, 1, 6, 18] if kind == 'liquidations' else [0]):
                due = slot+vintage*K.HOUR
                # Options arrive from the existing hourly capture, with a full hour to persist.
                grace = K.HOUR if kind == 'options' else 30*K.MIN
                if due < collection_start or due > now:
                    continue
                d = byslot.get((slot, vintage) if kind == 'liquidations' else slot)
                state = d.get('state', 'ok') if d else 'no-run'
                if kind == 'options' and d:
                    state = 'ok' if all(d[k]['state'] == 'ok' for k in ('rr25_7d', 'rr25_30d')) else 'unusable'
                success = (d.get('received_ms') or d.get('observed_at') or max((x['received_ms'] for x in d.get('raw', [])), default=None)) if d and state == 'ok' else None
                detail = {'slot': due, 'state': state, 'success_ms': success, 'vintage_hours': vintage}
                if due+grace+GRACE > now:
                    if state == 'ok':
                        pending_successes.append(detail)
                else:
                    opportunities.append(detail)
        opportunities.sort(key=lambda x: (x['slot'], x['vintage_hours']))
        summary = capture_coverage(opportunities, pending_successes, since, grouped=kind == 'liquidations')
        if deployment_start is not None:
            out['deployment']['pilots'][kind] = capture_coverage(opportunities, pending_successes, deployment_start,
                                                               grouped=kind == 'liquidations')
        opportunities = [x for x in opportunities if x['slot'] >= since]
        if kind == 'liquidations':
            summary['by_vintage'] = {str(v): coverage([x for x in opportunities if x['vintage_hours'] == v]) for v in [0, 1, 6, 18]}
        out['pilots'][kind] = summary
        if not out['paused'] and summary['active_consecutive_misses'] >= 2:
            out['alerts'].append(f'{kind}: consecutive capture opportunities missed or unusable')
    out['paired_diagnostics'] = paired_diagnostics(pairs)
    out['depth_diagnostics'] = {'last_24h': depth_diagnostics(rows, since, now)}
    if deployment_start is not None:
        out['depth_diagnostics']['since_deployment'] = depth_diagnostics(rows, deployment_start, now)
    opts = [r for r in K.Journal(base, 'options').rows if since <= r['data']['observed_at'] <= now]
    out['options_quality'] = options_diagnostics(base, opts)
    fits = K.Journal(base, 'fits').rows
    out['training'] = {k: {'state': r['data']['state'], 'members': len(r['data']['members']), 'cutoff_ms': r['data']['cutoff']}
                       for k in ('range', 'state') for r in fits if r['id'] == f'{k}-{now//K.DAY*K.DAY}'}
    return out


def safe_build(base, now):
    try:
        return build(base, now)
    except Exception as exc:
        return {'schema': SCHEMA, 'generated_utc': U.iso_ms(now), 'generated_ms': now,
                'stale_after_minutes': STALE//K.MIN, 'paused': False, 'integrity': 'failed',
                'studies': {}, 'pilots': {}, 'warnings': [], 'alerts': [f'Integrity or diagnostics failure: {type(exc).__name__}: {exc}']}


def markdown(out):
    lines = ['# Market study operational health', '', f'Generated {out["generated_utc"]}. Integrity: {out["integrity"]}.',
             '', 'Operational diagnostics only; frozen study results and launch clocks are unchanged.',
             'Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.',
             '', 'Paused: '+str(out['paused']), '', '## Alerts']
    lines += ['- '+x for x in out['alerts']] or ['None.']
    lines += ['', '## Coverage', '', '| Program | Successful / due | Coverage | Consecutive misses |', '|---|---:|---:|---:|']
    for name, v in {**out['studies'], **out['pilots']}.items():
        pct = f'{100*v["coverage"]:.1f}%' if v['coverage'] is not None else '—'
        lines.append(f'| {name} | {v["successful"]}/{v["due"]} | {pct} | {v["consecutive_misses"]} |')
    for name, v in {**out['studies'], **out['pilots']}.items():
        if v.get('recovered_before_close'):
            lines += ['', f'{name}: newer verified success; the current miss alert is cleared. Historical misses remain.']
    deployment = out.get('deployment')
    if deployment:
        lines += ['', '## Since recovery deployment', '',
                  f'{deployment["label"]}, {deployment["started_utc"]}; commit `{deployment["commit"]}`.',
                  'Fixed operational comparison by opportunity time, not a reset of research history.', '',
                  '| Program | Successful / closed | Additional successes awaiting closure |', '|---|---:|---:|']
        for name, v in {**deployment['studies'], **deployment['pilots']}.items():
            lines.append(f'| {name} | {v["successful"]}/{v["due"]} | {v["pending_successful"]} |')
    lines += ['', '## Diagnostics', '', 'Training readiness, per-opportunity reasons and source confirmations, publication delays, '
              'pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in '
              '[the JSON report](market_study_health.json).', '', 'Warnings:']
    lines += ['- '+x for x in out['warnings']] or ['None.']
    if out.get('paired_diagnostics'):
        p = out['paired_diagnostics']
        lines += ['', f'Paired study: {p["scored_forecasts"]} scored forecasts; {p["unique_entries"]} unique entries; '
                  f'{p["largest_disjoint_60m_subset"]} windows in the largest disjoint subset. These are not independent-sample counts.',
                  p['interpretation']]
    for period, d in out.get('depth_diagnostics', {}).items():
        lines += ['', f'State depth ({period}): {d["forecasts"]} forecasts, {d["abstained"]} abstentions; '
                  f'{d["missing_depth_age"]} unavailable depth ages. Median/max age in minutes: '
                  f'{d["depth_age_minutes"]["median"]} / {d["depth_age_minutes"]["max"]}.']
        lines += [f'- {n}: {reason}' for reason, n in d['abstention_reasons'].items()]
    for horizon, d in out.get('options_quality', {}).get('selected_by_horizon', {}).items():
        lines += ['', f'Selected {horizon} legs: {d["usable_captures"]} usable captures, {d["legs"]} leg observations. '
                  f'Quote age median (ms): {d["quote_age_ms"]["median"]}; relative spread median: '
                  f'{d["relative_spread"]["median"]}. Repeated legs and horizons are dependent; missing sizes stay unavailable.']
    return '\n'.join(lines)+'\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=['check', 'report'])
    args = ap.parse_args()
    out = safe_build(ROOT, int(time.time()*1000))
    print(markdown(out))
    if args.command == 'report':
        K.atomic(ROOT/'reports/market_study_health.json', (json.dumps(out, indent=2, allow_nan=False)+'\n').encode())
        K.atomic(ROOT/'reports/market_study_health.md', markdown(out).encode())
    return int(bool(out['alerts'])) if args.command == 'check' else int(out['integrity'] != 'ok')


if __name__ == '__main__':
    raise SystemExit(main())
