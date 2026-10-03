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
               'workflow': {'status': 'unverified', 'url': REPO + '/actions'}, 'sources': sources}
    serialized = json.dumps(payload, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
    output.mkdir(parents=True, exist_ok=True)
    for name in ['index.html', 'styles.css', 'app.js', 'model.js', 'favicon.svg']:
        shutil.copyfile(base / 'dashboard' / name, output / name)
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
