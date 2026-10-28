"""Options pilot publication journal with its own frozen identity and clock.

Keep v1 untouched: its recorded identity includes all files in its own package.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from desk import stream_util as U

ROOT = Path(__file__).resolve().parents[2]
STREAM = Path('streams/market-studies/options-v2')
MIN = 60_000
HOUR = 60 * MIN
DAY = 24 * HOUR


def protocol():
    return json.loads((ROOT / 'research_tools/options_pilot/protocol.json').read_text())


def identity():
    # Dependencies remain frozen by v1; this registration additionally binds every pilot file.
    from research_tools.market_studies.core import identity as original_identity
    ident = original_identity()
    paths = list((ROOT / 'research_tools/options_pilot').glob('*.py'))
    paths.append(ROOT / 'research_tools/options_pilot/protocol.json')
    ident.update({str(p.relative_to(ROOT)): U.file_sha(p) for p in sorted(paths)})
    return ident


def atomic(path, raw):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix='.study-')
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


class Journal:
    """Single writer (repo-write workflow lock); atomic replacement, immutable keys, checked hash chain."""
    def __init__(self, base, name):
        self.path = Path(base) / STREAM / (name + '.jsonl')
        self.rows = []
        self.index = {}
        prev = None
        for raw in self.path.read_text().splitlines() if self.path.exists() else []:
            r = json.loads(raw)
            body = {k: v for k, v in r.items() if k != 'sha256'}
            if r.get('prev') != prev or U.sha(body) != r.get('sha256'):
                raise ValueError(f'Corrupt study journal: {self.path}')
            if r['id'] in self.index:
                raise ValueError('Duplicate immutable record')
            self.rows.append(r)
            self.index[r['id']] = r
            prev = r['sha256']

    def get(self, key):
        return self.index.get(key)

    def add(self, key, data):
        old = self.get(key)
        if old:
            if old['data'] != data:
                raise ValueError(f'Attempt to rewrite immutable {key}')
            return old
        body = {'id': key, 'data': data, 'prev': self.rows[-1]['sha256'] if self.rows else None}
        row = dict(body, sha256=U.sha(body))
        rows = self.rows + [row]
        atomic(self.path, b''.join(U.canonical(x) + b'\n' for x in rows))
        self.rows = rows
        self.index[key] = row
        return row


def register(base, now):
    j = Journal(base, 'registration')
    old = j.get('options-v2')
    ident = identity()
    if old:
        if old['data']['identity'] != ident or old['data']['protocol'] != protocol():
            raise ValueError('Study identity drift: new version/clock required')
        return old
    return j.add('options-v2', {'created_ms': now, 'identity': ident, 'protocol': protocol(), 'run': U.run_meta()})


def remote(base, paths):
    subprocess.run(['git', 'fetch', '--quiet', 'origin', 'main'], cwd=base, check=True, timeout=60)
    commit = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=base, text=True).strip()
    out = {}
    for path in paths:
        r = subprocess.run(['git', 'show', f'origin/main:{path}'], cwd=base, capture_output=True, timeout=15)
        out[str(path)] = r.stdout if r.returncode == 0 else None
    return commit, out


def confirm(base, clock=U.clock_ms, fetch=remote):
    reg = register(base, clock())
    paths = [STREAM / 'registration.jsonl']
    # Verify the actual implementation and frozen protocol too, not only a record claiming their identity.
    paths += [Path(x) for x in reg['data']['identity']]
    commit, files = fetch(base, paths)
    t = clock()                         # first observed on remote; never a git author timestamp
    for p, sha in reg['data']['identity'].items():
        raw = files.get(p)
        if raw is None or hashlib.sha256(raw).hexdigest() != sha:
            raise ValueError(f'Implementation not on main: {p}')
    rawreg = files.get(str(paths[0])) or b''
    if U.canonical(reg) not in rawreg.splitlines():
        raise ValueError('Registration not on main')
    activations = Journal(base, 'activation')
    if not activations.get('options-v2'):
        activations.add('options-v2', {'registration_sha': reg['sha256'], 'confirmed_ms': t,
                               'first_slot': (t // HOUR + 1) * HOUR, 'commit': commit})


def activation(base):
    reg = register(base, U.clock_ms())
    a = Journal(base, 'activation').get('options-v2')
    if a:
        d = a['data']
        if d['registration_sha'] != reg['sha256']:
            raise ValueError('Activation does not bind registration')
        if d['confirmed_ms'] < reg['data']['created_ms'] or d['first_slot'] != (d['confirmed_ms'] // HOUR + 1) * HOUR:
            raise ValueError('Invalid prospective activation clock')
    return a['data'] if a else None


def slots(first, now, step):
    return range((first + step - 1) // step * step, now // step * step + 1, step)


def production():
    if not U.run_meta()['production']:
        raise RuntimeError('Production mutations require the main-branch GitHub Actions workflow')
