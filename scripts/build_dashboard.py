#!/usr/bin/env python3
"""Build a read-only static desk from one repository checkout (standard library only)."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/mannoj93-spec/jbm-desk-data'


def write_assets(source, output):
    """Version the complete module graph so cached files cannot straddle releases."""
    for name in ['index.html', 'styles.css', 'app.js', 'model.js', 'favicon.svg']:
        shutil.copyfile(source / name, output / name)

    def versioned(name, content):
        path = Path(name)
        filename = f'{path.stem}.{hashlib.sha256(content).hexdigest()[:16]}{path.suffix}'
        (output / filename).write_bytes(content)
        return filename

    model = versioned('model.js', (source / 'model.js').read_bytes())
    app = (source / 'app.js').read_text(encoding='utf-8')
    if "'./model.js'" not in app:
        raise ValueError("app.js no longer imports './model.js': update write_assets before publishing")
    app = app.replace("'./model.js'", f"'./{model}'")
    # repo 2.30: every relative module the app imports must have been rewritten to a content-hashed name
    stray = sorted(set(re.findall(r"from\s+['\"](\./[^'\"]+)['\"]", app)) - {f'./{model}'})
    if stray:
        raise ValueError(f'unversioned module reference(s) in app.js: {stray}')
    app_name = versioned('app.js', app.encode('utf-8'))
    styles = versioned('styles.css', (source / 'styles.css').read_bytes())
    index = (source / 'index.html').read_text(encoding='utf-8')
    index = index.replace('href="styles.css"', f'href="{styles}"')
    index = index.replace('src="app.js"', f'src="{app_name}"')
    (output / 'index.html').write_text(index, encoding='utf-8')


def utc(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def table(text, first_header):
    """Read one explicitly named report table. Refuse ambiguous schema changes."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        cells = [v.strip() for v in line.strip().strip('|').split('|')]
        if line.startswith('|') and cells[0] == first_header:
            result = []
            for row in lines[i + 2:]:
                if not row.startswith('|'):
                    break
                values = [v.strip() for v in row.strip().strip('|').split('|')]
                if len(values) != len(cells):
                    raise ValueError(f'Malformed {first_header} table row')
                result.append(dict(zip(cells, values)))
            if not result:
                raise ValueError(f'Empty {first_header} table')
            return result
    raise ValueError(f'Missing report table: {first_header}')


def coverage(text):
    generated = re.search(r'^Generated (\d{4}-\d\d-\d\d[ T]\d\d:\d\dZ)', text, re.M)
    cutoff = re.search(r'Input cutoff: (\d{4}-\d\d-\d\d[ T]\d\d:\d\dZ)', text)
    if not generated or not cutoff:
        raise ValueError('Coverage report has no generation time or input cutoff')
    datasets = [{'name': r['Dataset'], 'observed_utc': utc(r['Latest observation written'])}
                for r in table(text, 'Dataset')]
    sources = []
    for row in table(text, 'Source'):
        match = re.fullmatch(r'(\d+)/(\d+)', row['OK / observed'])
        if not match:
            raise ValueError('Invalid source observation counts')
        ok, observed = map(int, match.groups())
        if ok > observed:
            raise ValueError('Successful observations exceed total')
        sources.append({'name': row['Source'], 'ok': ok, 'observed': observed, 'status': row['Latest status']})
    alerts = text.split('## 7. Alerts', 1)[-1] if '## 7. Alerts' in text else ''
    return {'generated_utc': utc(generated[1]), 'input_cutoff_utc': utc(cutoff[1]),
            'datasets': datasets, 'sources': sources,
            'cadence': table(text, 'Cadence period (UTC)'),
            'alerts': [line[2:].strip() for line in alerts.splitlines() if line.startswith('- ')]}


def price_history(base, record_source):
    """Latest observed bar wins; aggregate actual recorded minute OHLC into hourly OHLC."""
    folder = base / 'data/prices/binance_klines_1m_BTCUSDT_perp'
    rows = {}
    observed = None
    # Two latest monthly partitions cover seven days even across a month boundary.
    for path in sorted(folder.glob('*.jsonl'))[-2:]:
        record_source(path)
        for line in path.read_text().splitlines():
            row = json.loads(line)
            seen = row.get('observed_at')
            if not isinstance(seen, (int, float)):
                continue
            for bar in row.get('bars', []):
                if len(bar) < 5 or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in bar[:5]):
                    raise ValueError('Invalid price bar')
                stamp = bar[0]
                if stamp not in rows or seen >= rows[stamp][0]:
                    rows[stamp] = (seen, bar[:5])
            observed = max(observed or seen, seen)
    if not rows:
        return {'series': 'BTCUSDT perpetual · trade price', 'observed_utc': None, 'bars': [], 'latest': None}
    cutoff = max(rows) - 7 * 86400000
    groups = {}
    for stamp, (_, bar) in sorted(rows.items()):
        if stamp < cutoff:
            continue
        hour = int(stamp // 3600000 * 3600000)
        if hour not in groups:
            groups[hour] = [hour, bar[1], bar[2], bar[3], bar[4], 1]
        else:
            g = groups[hour]
            g[2], g[3], g[4], g[5] = max(g[2], bar[2]), min(g[3], bar[3]), bar[4], g[5] + 1
    last = rows[max(rows)][1]
    return {'series': 'BTCUSDT perpetual · Binance trade price',
            'observed_utc': datetime.fromtimestamp(observed / 1000, timezone.utc).isoformat(),
            'latest': {'t': last[0], 'close': last[4]}, 'bars': list(groups.values()),
            'note': 'Hourly OHLC aggregated from stored one-minute bars. Partial hours are retained; gaps are not filled.'}


def developments(base, record_source):
    """Summarize optional repository records without promoting preparation into live evidence."""
    def read(path):
        record_source(path)
        value = json.loads(path.read_text())
        if not isinstance(value, dict):
            raise ValueError(f'Invalid development record: {path.relative_to(base)}')
        return value

    def text(value, field, path):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'Invalid {field}: {path.relative_to(base)}')
        return value

    result = {'release': None, 'catalog': None, 'protocols': [], 'acceptance': None, 'readiness': []}
    changelog = base / 'CHANGELOG.md'
    if changelog.exists():
        record_source(changelog)
        # Presentation-only entries may precede the latest numbered repository revision.
        match = re.search(r'^# (.*?\brevision\s+([\d.]+).*?(\d{4}-\d\d-\d\d).*)$',
                          changelog.read_text(), re.M | re.I)
        if match:
            result['release'] = {'revision': match[2], 'date': match[3], 'title': match[1],
                                 'source': 'CHANGELOG.md'}

    catalog_path = base / 'research_tools/catalog.json'
    if catalog_path.exists():
        catalog = read(catalog_path)
        if catalog.get('schema') != 'desk-data-catalog/1' or not isinstance(catalog.get('datasets'), list) or not isinstance(catalog.get('feature_families'), list):
            raise ValueError('Invalid research catalog schema')
        families = []
        for family in catalog['feature_families']:
            if not isinstance(family, dict):
                raise ValueError('Invalid research catalog feature family')
            families.append({key: text(family.get(key), key, catalog_path) for key in ('id', 'status')})
        result['catalog'] = {'version': text(catalog.get('version'), 'version', catalog_path),
                             'as_of_utc': utc(catalog.get('as_of_utc')), 'dataset_count': len(catalog['datasets']),
                             'feature_families': families, 'source': str(catalog_path.relative_to(base))}

    titles = {'DIR1': 'Directional forecasts', 'A2-synchronized-flow': 'Synchronized flow',
              'PS1-T1': 'Turnover control', 'E1-pilot-1': 'Streaming pilot'}
    paths = sorted((base / 'research/registrations').glob('*/protocol.json'))
    pilot = base / 'stream/pilot_e1.json'
    if pilot.exists():
        paths.append(pilot)
    for path in paths:
        protocol = read(path)
        identifier = text(protocol.get('id'), 'protocol id', path)
        result['protocols'].append({'id': identifier, 'title': titles.get(identifier, identifier),
                                    'status': text(protocol.get('status'), 'protocol status', path),
                                    'effective_utc': utc(protocol.get('effective_utc')),
                                    'source': str(path.relative_to(base))})

    def acceptance(path):
        record = read(path)
        clocks = record.get('clocks')
        if not isinstance(clocks, dict) or not isinstance(clocks.get('window'), list) or len(clocks['window']) != 2:
            raise ValueError(f'Invalid acceptance clocks: {path.relative_to(base)}')
        window = [utc(value) for value in clocks['window']]
        if not all(window) or window[0] >= window[1]:
            raise ValueError(f'Invalid acceptance window: {path.relative_to(base)}')
        return {**{key: text(record.get(key), key, path)
                   for key in ('checker', 'verdict', 'service_verdict', 'reason')},
                'window': window, 'evaluated_utc': utc(clocks.get('evaluated_utc')),
                'source': str(path.relative_to(base))}

    # Component readiness (repo 2.30): recorded states with their evidence, displayed as recorded; a state is never
    # inferred here, and the record's own clock (as_of_utc) is shown apart from the build time.
    states = ('implemented', 'tested', 'pushed', 'merged', 'installed', 'deployed', 'observed', 'registered',
              'prepared', 'blocked', 'pending')
    for path in sorted((base / 'research/readiness').glob('*.json')):
        rec = read(path)
        if rec.get('schema') != 'component-readiness/1' or not isinstance(rec.get('states'), dict) \
                or not isinstance(rec.get('code'), dict) or not isinstance(rec.get('blockers'), list):
            raise ValueError(f'Invalid readiness record: {path.relative_to(base)}')
        st = {}
        for name, value in rec['states'].items():
            if name not in states or not isinstance(value, dict) or not isinstance(value.get('value'), bool) \
                    or not isinstance(value.get('evidence'), list):
                raise ValueError(f'Invalid readiness state {name!r}: {path.relative_to(base)}')
            if value['value'] and not value['evidence']:
                raise ValueError(f'Readiness state {name!r} without evidence: {path.relative_to(base)}')
            st[name] = {'value': value['value'], 'evidence': [text(e.get('ref'), 'evidence ref', path)
                                                               for e in value['evidence']]}
        result['readiness'].append({'id': text(rec.get('id'), 'id', path), 'title': text(rec.get('title'), 'title', path),
                                    'version': text(rec['code'].get('version'), 'version', path),
                                    'code_path': text(rec['code'].get('path'), 'code path', path),
                                    'as_of_utc': utc(rec.get('as_of_utc')), 'states': st,
                                    'blockers': [text(x, 'blocker', path) for x in rec['blockers']],
                                    'source': str(path.relative_to(base))})

    # Result-of-record files remain authoritative; a supplementary audit never replaces one.
    records = [(path, acceptance(path)) for path in sorted((base / 'docs/acceptance/results').glob('*/result-*.json'))]
    if records:
        path, latest = max(records, key=lambda item: (item[1]['window'][1], item[1]['window'][0]))
        audits = [acceptance(p) for p in sorted(path.parent.glob('supplementary-*.json'))]
        if any(audit['window'] != latest['window'] for audit in audits):
            raise ValueError('Supplementary acceptance audit does not match the result window')
        latest['supplementary'] = max(audits, key=lambda audit: audit['evaluated_utc'] or '') if audits else None
        result['acceptance'] = latest
    return result


def build(base, output):
    base, output = Path(base).resolve(), Path(output).resolve()
    # Output may never overwrite any source or evidence directory.
    if output == base or output in base.parents or (output.is_relative_to(base) and output != base / '.dashboard-build'):
        raise ValueError('Use .dashboard-build or a separate output directory')
    sources = {}
    def record(path):
        rel = str(path.relative_to(base))
        sources[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    def read(rel):
        path = base / rel
        record(path)
        return json.loads(path.read_text())
    health_path = base / 'reports/latest.md'
    record(health_path)
    health = coverage(health_path.read_text())
    index = read('research/evidence/index.json')
    designs = []
    for design, entry in sorted(index['designs'].items()):
        version = entry['current']
        path = f'research/evidence/v2/{design}@{version}.json'
        card = read(path)
        if card.get('evaluation_version') != version:
            raise ValueError(f'Evidence index/card version mismatch: {design}')
        designs.append({key: card.get(key) for key in [
            'design', 'evaluation_version', 'module', 'condition', 'status', 'status_reason',
            'generated_at', 'cutoff_ms', 'research_integrity', 'publication', 'checkpoints',
            'min_dependence_blocks', 'min_retained_observations', 'primary_horizon_min']})
        designs[-1]['source'] = path
        cutoff = card.get('cutoff_ms')
        designs[-1]['cutoff_utc'] = (datetime.fromtimestamp(cutoff / 1000, timezone.utc).isoformat().replace('+00:00', 'Z')
                                     if isinstance(cutoff, (int, float)) and math.isfinite(cutoff) else None)
    forecasts = read('reports/range_status.json')
    utc(forecasts['generated_utc'])
    utc(forecasts['status_expires_utc'])
    if not isinstance(forecasts.get('current'), dict) or not isinstance(forecasts.get('evaluation'), dict):
        raise ValueError('Invalid range report schema')
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=base, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None
    cutoffs = sorted(d['cutoff_utc'] for d in designs if d['cutoff_utc'])
    # Clocks are named (repo 2.23): the index's 'updated' is when the lab last published (processing); observation
    # cutoffs come from each card's cutoff_ms. A rebuild never refreshes either.
    payload = {'schema': 'jbm-dashboard/2', 'built_utc': datetime.now(timezone.utc).isoformat(),
               'repository': REPO, 'commit': commit, 'health': health, 'range': forecasts,
               'research': {'index_updated_utc': utc(index['updated']), 'source_cutoff_utc': cutoffs[-1] if cutoffs else None,
                            'oldest_cutoff_utc': cutoffs[0] if cutoffs else None, 'designs': designs,
                            'statuses': dict(Counter(d['status'] for d in designs))},
               'companion': read('reports/companion_b1.json'), 'paper': read('reports/paper_ps1.json'),
               'feasibility': read('reports/feasibility.json'), 'market': price_history(base, record),
               'ops': read('reports/health.json') if (base / 'reports/health.json').exists() else None,
               'developments': developments(base, record),
               'workflow': {'status': 'unverified', 'url': REPO + '/actions'}, 'sources': sources}
    serialized = json.dumps(payload, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
    output.mkdir(parents=True, exist_ok=True)
    write_assets(base / 'dashboard', output)
    (output / '.nojekyll').touch()
    (output / 'data.json').write_text(serialized + '\n')
    print(f'Dashboard built: {output} ({len(serialized):,} bytes of data; {len(sources)} verified source hashes)')
    return payload


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=ROOT / '.dashboard-build')
    args = parser.parse_args()
    build(args.source, args.output)
