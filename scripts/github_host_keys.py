#!/usr/bin/env python3
"""github_host_keys - write GitHub's SSH host keys to a known_hosts file for strict host checking (repo 2.26).

    python3 scripts/github_host_keys.py <known_hosts path> [--budget SECONDS]

The keys come from GET https://api.github.com/meta over HTTPS (ssh_keys). Repo 2.24.1-2.25.1 fetched it
unauthenticated, from the 60-requests-per-hour pool shared by every job on the runner's IP; four persistence steps
failed with "HTTP Error 403: rate limit exceeded" on Oct 4-5 2026 after their collection or scoring had succeeded.
Now:
  * authenticated with the job's own token when one is in the environment (DESK_META_TOKEN, GITHUB_TOKEN or
    GH_TOKEN; the endpoint needs no permission) - the GITHUB_TOKEN pool is 1,000 requests per hour per repository;
  * reused within the job: a validated copy in $RUNNER_TEMP serves later persistence steps of the same job;
  * bounded retries inside the caller's budget: rate limits wait for retry-after or x-ratelimit-reset only when that
    fits the budget (capped at 20 s), other failures back off 2, 4, 8 s;
  * validated: at least one line of a known key type with base64 key material, nothing else written.
It never falls back to an unverified source (no ssh-keyscan) and never prints the token. Exit 0 = keys written;
1 = no trustworthy keys within the budget (the caller pushes nothing). Stdlib only.
"""
from __future__ import annotations

import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

URL = "https://api.github.com/meta"
TYPES = ("ssh-ed25519", "ecdsa-sha2-nistp256", "ssh-rsa")
CACHE_NAME = "desk-github-known-hosts"
MAX_WAIT_S = 20
_sleep = time.sleep
_now = time.monotonic


def token(env=None):
    env = os.environ if env is None else env
    for name in ("DESK_META_TOKEN", "GITHUB_TOKEN", "GH_TOKEN"):
        if env.get(name):
            return env[name]
    return None


def lines_from(doc) -> list:
    """known_hosts lines for every well-formed key in a /meta document; [] when none is trustworthy."""
    keys = doc.get("ssh_keys") if isinstance(doc, dict) else None
    out = []
    for k in keys if isinstance(keys, list) else []:
        parts = k.split() if isinstance(k, str) else []
        if len(parts) != 2 or parts[0] not in TYPES or not re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", parts[1]):
            continue
        try:
            raw = base64.b64decode(parts[1], validate=True)
        except ValueError:
            continue
        # the blob starts with its own type name, length-prefixed (RFC 4253 6.6)
        n = int.from_bytes(raw[:4], "big") if len(raw) > 4 else 0
        if raw[4:4 + n].decode("ascii", "replace") != parts[0]:
            continue
        m = int.from_bytes(raw[4 + n:8 + n], "big") if len(raw) >= 8 + n else 0
        if m == 0 or len(raw) < 8 + n + m:           # the key material itself must be present
            continue
        out.append(f"github.com {parts[0]} {parts[1]}")
    return out


def wait_hint(err) -> float | None:
    """Seconds GitHub asks us to wait on a rate-limit response, or None when it is not one."""
    hdrs = getattr(err, "headers", None) or {}
    if err.code not in (403, 429):
        return None
    if hdrs.get("retry-after"):
        try:
            return float(hdrs["retry-after"])
        except ValueError:
            return 60.0
    if hdrs.get("x-ratelimit-remaining") == "0" and hdrs.get("x-ratelimit-reset"):
        try:
            return max(0.0, float(hdrs["x-ratelimit-reset"]) - time.time())
        except ValueError:
            return 60.0
    return 60.0 if err.code == 429 or "rate limit" in str(getattr(err, "reason", "")).lower() else None


def fetch(budget_s=60.0, env=None, opener=None, log=None) -> list:
    """Validated known_hosts lines, or [] when none could be obtained within budget_s seconds."""
    opener = opener or urllib.request.urlopen
    log = log or (lambda m: print(m, file=sys.stderr))
    tok = token(env)
    deadline = _now() + budget_s
    backoff = 2.0
    attempt = 0
    while True:
        attempt += 1
        left = deadline - _now()
        if left < 3:
            log(f"host keys: budget spent after {attempt - 1} attempt(s)")
            return []
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
                   "User-Agent": "jbm-desk-persistence"}
        if tok:
            headers["Authorization"] = f"Bearer {tok}"
        try:
            url = (env if env is not None else os.environ).get("DESK_META_URL") or URL   # tests only
            with opener(urllib.request.Request(url, headers=headers), timeout=min(20.0, left)) as r:
                lines = lines_from(json.loads(r.read()))
            if lines:
                log(f"host keys: {len(lines)} key(s) from api.github.com/meta "
                    f"({'authenticated' if tok else 'unauthenticated'}, attempt {attempt})")
                return lines
            log(f"host keys: response held no valid SSH host key (attempt {attempt})")
            wait = backoff
        except urllib.error.HTTPError as e:
            hint = wait_hint(e)
            log(f"host keys: HTTP {e.code} (attempt {attempt}{', rate limited' if hint is not None else ''})")
            if hint is not None and hint > min(MAX_WAIT_S, deadline - _now() - 3):
                log(f"host keys: GitHub asks for {hint:.0f} s, beyond the remaining budget; giving up")
                return []
            wait = hint if hint is not None else backoff
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
            log(f"host keys: {type(e).__name__} (attempt {attempt})")
            wait = backoff
        if wait > deadline - _now() - 3:
            log("host keys: no time left for another attempt")
            return []
        _sleep(wait)
        backoff = min(backoff * 2, 8.0)


def cached(env=None) -> Path | None:
    env = os.environ if env is None else env
    return Path(env["RUNNER_TEMP"]) / CACHE_NAME if env.get("RUNNER_TEMP") else None


def main(argv) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    out = Path(argv[1])
    budget = float(argv[argv.index("--budget") + 1]) if "--budget" in argv else 60.0
    cache = cached()
    if cache and cache.is_file():
        lines = [l for l in cache.read_text().splitlines() if l]
        if lines and lines == lines_from({"ssh_keys": [l.split(" ", 1)[1] for l in lines]}):
            out.write_text("\n".join(lines) + "\n")
            print(f"host keys: {len(lines)} key(s) reused from this job", file=sys.stderr)
            return 0
    lines = fetch(budget)
    if not lines:
        return 1
    out.write_text("\n".join(lines) + "\n")
    if cache:
        try:
            cache.write_text("\n".join(lines) + "\n")
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
