"""State-v2 publication journal, forked from frozen v1 to isolate its identity and clock.

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
STREAM = Path('streams/market-studies/state-v2')
MIN = 60_000
HOUR = 60 * MIN
DAY = 24 * HOUR


def protocol():
    return json.loads((ROOT / 'research_tools/state_v2/protocol.json').read_text())


def identity():
    # Dependencies remain frozen by v1; this registration additionally binds every v2 file.
    from research_tools.market_studies.core import identity as original_identity
    ident = original_identity()
    paths = list((ROOT / 'research_tools/state_v2').glob('*.py'))
    paths.append(ROOT / 'research_tools/state_v2/protocol.json')
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
    old = j.get('state-v2')
    ident = identity()
    if old:
        if old['data']['identity'] != ident or old['data']['protocol'] != protocol():
            raise ValueError('Study identity drift: new version/clock required')
        return old
    return j.add('state-v2', {'created_ms': now, 'identity': ident, 'protocol': protocol(), 'run': U.run_meta()})


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
    forecasts = Journal(base, 'forecasts')
    paths = [STREAM / (x + '.jsonl') for x in ('registration', 'forecasts', 'fits')]
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
    if not activations.get('state-v2'):
        activations.add('state-v2', {'registration_sha': reg['sha256'], 'confirmed_ms': t,
                               'first_slot': (t // HOUR + 1) * HOUR, 'commit': commit})
    remote_rows = set((files.get(str(paths[1])) or b'').splitlines())
    remote_fits = set((files.get(str(paths[2])) or b'').splitlines())
    fits = Journal(base, 'fits')
    conf = Journal(base, 'confirmations')
    for r in forecasts.rows:
        if conf.get(r['id']) or U.canonical(r) not in remote_rows:
            continue
        d = r['data']
        if d.get('fit'):
            fit = fits.get(d['fit']['id'])
            if not fit or fit['sha256'] != d['fit']['sha256'] or U.canonical(fit) not in remote_fits:
                raise ValueError('Training artifact not on main')
        conf.add(r['id'], {'forecast_sha': r['sha256'], 'confirmed_ms': t, 'commit': commit,
                           'eligible': d['state'] == 'ready' and d['prepared_ms'] <= t < d['deadline_ms']})


def activation(base):
    reg = register(base, U.clock_ms())
    a = Journal(base, 'activation').get('state-v2')
    if a and a['data']['registration_sha'] != reg['sha256']:
        raise ValueError('Activation does not bind registration')
    return a['data'] if a else None


def verified(base):
    """One forecast/confirmation consumption path, used by execution, scoring and reporting."""
    a = activation(base)
    conf = Journal(base, 'confirmations')
    fits = Journal(base, 'fits')
    out = []
    for r in Journal(base, 'forecasts').rows:
        d, c = r['data'], conf.get(r['id'])
        if d.get('fit'):
            fit = fits.get(d['fit']['id'])
            if not fit or fit['sha256'] != d['fit']['sha256']:
                raise ValueError('Training artifact changed or missing')
            if fit['data']['cutoff'] > d['slot']:
                raise ValueError('Training cutoff after forecast')
        if not a or d['slot'] < a['first_slot']:
            raise ValueError('Forecast predates activation')
        if c:
            v = c['data']
            if v['forecast_sha'] != r['sha256']:
                raise ValueError('Forecast changed after publication')
            expected = d['state'] == 'ready' and d['prepared_ms'] <= v['confirmed_ms'] < d['deadline_ms']
            if expected != v['eligible']:
                raise ValueError('Invalid publication eligibility')
        out.append((r, c))
    return out


def slots(first, now, step):
    return range((first + step - 1) // step * step, now // step * step + 1, step)


def production():
    if not U.run_meta()['production']:
        raise RuntimeError('Production mutations require the main-branch GitHub Actions workflow')
