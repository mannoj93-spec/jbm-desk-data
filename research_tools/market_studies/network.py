"""Bounded read-only public HTTP capture. Parent kills a hung request after 12 seconds."""
import hashlib
import json
import subprocess
import sys
import time
import urllib.request
import urllib.error

LIMIT = 4 * 1024 * 1024


def clock():
    return int(time.time() * 1000)


def fetch(url):
    sent = clock()
    try:
        p = subprocess.run([sys.executable, '-m', 'research_tools.market_studies.network', url],
                           capture_output=True, timeout=12, check=True)
        result = json.loads(p.stdout)
        return result
    except (subprocess.SubprocessError, ValueError) as exc:
        return {'url': url, 'sent_ms': sent, 'received_ms': clock(), 'state': 'request-error',
                'error': type(exc).__name__, 'raw': None}


def worker(url):
    out = {'url': url, 'sent_ms': clock()}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'jbm-market-studies/1 (public research)'})
        try:
            response = urllib.request.urlopen(req, timeout=8)
        except urllib.error.HTTPError as exc:
            response = exc
        with response as r:
            out['http_status'] = r.status
            raw = r.read(LIMIT + 1)
            if len(raw) > LIMIT:
                raise ValueError('Response exceeds 4 MiB')
        out.update(received_ms=clock(), raw=raw.decode(), raw_sha=hashlib.sha256(raw).hexdigest(), state='ok' if out['http_status'] == 200 else 'http-error')
        if out['state'] == 'ok':
            json.loads(out['raw'])
    except Exception as exc:
        out.update(received_ms=clock(), state='request-error', error=type(exc).__name__ + ': ' + str(exc)[:300])
    return out


if __name__ == '__main__':
    print(json.dumps(worker(sys.argv[1]), allow_nan=False))
