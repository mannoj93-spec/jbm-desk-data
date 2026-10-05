"""SSH host-key acquisition for deploy-key persistence (repo 2.26). Reproduces the Oct 4-5 2026 failure (an
unauthenticated api.github.com/meta request answered "HTTP Error 403: rate limit exceeded", so nothing was pushed) and
covers the real acquisition path: success, rate limiting, timeout, malformed and empty keys, an exhausted budget,
job-level reuse, token redaction, credential cleanup, no false persistence success and the push guard still enforced.
Every network call goes to a local mock server or an injected opener."""
import base64
import http.server
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import github_host_keys as K   # noqa: E402

SCRIPT = ROOT / "scripts/commit_push.sh"
ID = ["-c", "user.name=t", "-c", "user.email=t@t"]


def key(kind="ssh-ed25519", body=b"x" * 32):
    blob = len(kind).to_bytes(4, "big") + kind.encode() + len(body).to_bytes(4, "big") + body
    return f"{kind} {base64.b64encode(blob).decode()}"


GOOD = {"ssh_keys": [key(), key("ecdsa-sha2-nistp256"), key("ssh-rsa")]}


class Resp(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def http_error(code, headers=None, reason="rate limit exceeded"):
    return urllib.error.HTTPError(K.URL, code, reason, headers or {}, None)


class Opener:
    def __init__(self, *responses):
        self.responses, self.requests = list(responses), []

    def __call__(self, req, timeout=None):
        self.requests.append(req)
        r = self.responses.pop(0) if self.responses else GOOD
        if isinstance(r, Exception):
            raise r
        return Resp(json.dumps(r).encode() if not isinstance(r, bytes) else r)


class AcquisitionTests(unittest.TestCase):
    def setUp(self):
        self.slept = []
        self._s, K._sleep = K._sleep, self.slept.append
        self.logs = []

    def tearDown(self):
        K._sleep = self._s

    def fetch(self, opener, env=None, budget=60):
        return K.fetch(budget, env=env if env is not None else {"GITHUB_TOKEN": "t0k"}, opener=opener, log=self.logs.append)

    def test_success_is_authenticated_with_the_job_token_and_validated(self):
        o = Opener(GOOD)
        lines = self.fetch(o)
        self.assertEqual(len(lines), 3)
        self.assertTrue(all(l.startswith("github.com ") for l in lines))
        self.assertEqual(o.requests[0].get_header("Authorization"), "Bearer t0k")
        self.assertFalse(any("t0k" in m for m in self.logs))

    def test_reproduced_rate_limit_then_retry_succeeds_inside_the_budget(self):
        limited = http_error(403, {"x-ratelimit-remaining": "0", "x-ratelimit-reset": "0"})
        o = Opener(limited, GOOD)
        self.assertEqual(len(self.fetch(o)), 3)
        self.assertEqual(len(o.requests), 2)
        self.assertTrue(any("rate limited" in m for m in self.logs))

    def test_rate_limit_longer_than_the_budget_fails_closed(self):
        o = Opener(http_error(429, {"retry-after": "120"}))
        self.assertEqual(self.fetch(o), [])
        self.assertEqual(len(o.requests), 1)            # no hammering past the requested wait
        self.assertEqual(self.slept, [])

    def test_timeouts_back_off_and_stop(self):
        o = Opener(*[urllib.error.URLError(TimeoutError("timed out"))] * 10)
        t = [0.0]
        _n, K._now = K._now, (lambda: t[0])
        def sleep(s):
            self.slept.append(s)
            t[0] += s
        K._sleep = sleep
        try:
            self.assertEqual(self.fetch(o, budget=20), [])
        finally:
            K._now = _n
        self.assertEqual(self.slept, [2.0, 4.0, 8.0])
        self.assertLessEqual(sum(self.slept), 20)

    def test_malformed_and_empty_key_material_is_rejected(self):
        bad = {"ssh_keys": ["ssh-ed25519", "ssh-dss AAAA", "ssh-ed25519 not*base64", key("ssh-ed25519", b"")[:-4] + "AAAA",
                            "ssh-ed25519 " + base64.b64encode(b"\x00\x00\x00\x07ssh-rsaXXXX").decode(), 42]}
        self.assertEqual(K.lines_from(bad), [])
        self.assertEqual(K.lines_from({"ssh_keys": []}), [])
        self.assertEqual(K.lines_from({}), [])
        o = Opener(bad, {"ssh_keys": []}, b"not json", GOOD)
        self.assertEqual(len(self.fetch(o)), 3)
        self.assertEqual(len(o.requests), 4)

    def test_githubs_published_keys_validate(self):
        published = ["ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl",
                     "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEmKSENjQEezOmxkZMy7opKgwFB9nkt5"
                     "YRrYMjNuG5N87uRgg6CLrbo5wAdT/y6v0mKV0U2w0WZ2YB/++Tpockg="]   # docs.github.com, read Oct 5 2026
        self.assertEqual(len(K.lines_from({"ssh_keys": published})), 2)

    def test_exhausted_budget_makes_no_request(self):
        o = Opener(GOOD)
        self.assertEqual(self.fetch(o, budget=2), [])
        self.assertEqual(o.requests, [])

    def test_without_a_token_it_still_works_unauthenticated(self):
        o = Opener(GOOD)
        self.assertEqual(len(self.fetch(o, env={})), 3)
        self.assertIsNone(o.requests[0].get_header("Authorization"))


class MetaServer:
    """A local stand-in for api.github.com/meta answering a scripted sequence."""
    def __init__(self, script):
        self.script, self.seen = list(script), []
        outer = self

        class H(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                outer.seen.append(self.headers.get("Authorization"))
                code, body, hdrs = outer.script.pop(0) if outer.script else (200, GOOD, {})
                self.send_response(code)
                for k, v in hdrs.items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(json.dumps(body).encode() if not isinstance(body, bytes) else body)

            def log_message(self, *a):
                pass

        self.httpd = http.server.HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.httpd.server_port}/meta"

    def close(self):
        self.httpd.shutdown()


class CommitPushPathTests(unittest.TestCase):
    """commit_push.sh with a deploy key goes through the real acquisition (DESK_META_URL points it at the mock)."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.origin, self.work, self.keytmp, self.runner = d / "origin.git", d / "work", d / "tmp", d / "runner"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(self.origin)], check=True)
        subprocess.run(["git", "clone", "-q", str(self.origin), str(self.work)], check=True, capture_output=True)
        g = lambda *a: subprocess.run(["git", "-C", str(self.work), *a], check=True, capture_output=True)  # noqa: E731
        g("checkout", "-q", "-b", "main")
        (self.work / "data").mkdir()
        (self.work / "data/a.jsonl").write_text("{}\n")
        (self.work / "collector.py").write_text("print(1)\n")
        g(*ID, "add", ".")
        g(*ID, "commit", "-qm", "init")
        g("push", "-q", "origin", "main")
        self.keytmp.mkdir()
        self.runner.mkdir()
        self.before = self.tip()

    def tearDown(self):
        self.tmp.cleanup()

    def tip(self):
        return subprocess.run(["git", "-C", str(self.origin), "rev-parse", "main"], capture_output=True, text=True).stdout.strip()

    def push(self, server, budget="60", **extra):
        env = {k: v for k, v in os.environ.items() if k not in ("DESK_DEPLOY_KEY", "DESK_PUSH_URL", "GITHUB_TOKEN", "GH_TOKEN")}
        env.update(TMPDIR=str(self.keytmp), RUNNER_TEMP=str(self.runner), PERSIST_BUDGET_S=budget, DESK_WRITER="collector",
                   DESK_DEPLOY_KEY="-----BEGIN OPENSSH PRIVATE KEY-----\nsecret\n-----END OPENSSH PRIVATE KEY-----",
                   DESK_PUSH_URL=str(self.origin), DESK_META_URL=server.url, DESK_META_TOKEN="ghs_tok3n", **extra)
        return subprocess.run(["bash", str(SCRIPT), "data"], cwd=self.work, env=env, capture_output=True, text=True, timeout=120)

    def test_rate_limited_lookup_recovers_and_persists(self):
        s = MetaServer([(403, {"message": "API rate limit exceeded"}, {"x-ratelimit-remaining": "0", "x-ratelimit-reset": "0"}),
                        (200, GOOD, {})])
        try:
            (self.work / "data/a.jsonl").write_text('{"x": 1}\n')
            r = self.push(s)
        finally:
            s.close()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotEqual(self.tip(), self.before)
        self.assertEqual(s.seen, ["Bearer ghs_tok3n", "Bearer ghs_tok3n"])
        self.assertNotIn("ghs_tok3n", r.stdout + r.stderr)
        self.assertNotIn("secret", r.stdout + r.stderr)
        self.assertEqual(list(self.keytmp.iterdir()), [])                     # key directory removed

    def test_persistent_rate_limit_pushes_nothing_and_says_so(self):
        s = MetaServer([(429, {}, {"retry-after": "300"})] * 5)
        try:
            (self.work / "data/a.jsonl").write_text('{"x": 2}\n')
            r = self.push(s)
        finally:
            s.close()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("nothing pushed; remote persistence not confirmed", r.stderr)
        self.assertEqual(self.tip(), self.before)
        self.assertEqual(list(self.keytmp.iterdir()), [])

    def test_empty_keys_fail_closed_within_the_budget(self):
        s = MetaServer([(200, {"ssh_keys": []}, {})] * 20)
        try:
            (self.work / "data/a.jsonl").write_text('{"x": 3}\n')
            r = self.push(s, budget="12")
        finally:
            s.close()
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.tip(), self.before)

    def test_second_step_of_a_job_reuses_validated_keys(self):
        s = MetaServer([(200, GOOD, {})])
        try:
            (self.work / "data/a.jsonl").write_text('{"x": 4}\n')
            self.assertEqual(self.push(s).returncode, 0)
            (self.work / "data/b.jsonl").write_text('{}\n')
            r = self.push(s)
        finally:
            s.close()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(len(s.seen), 1)
        self.assertIn("reused from this job", r.stderr)

    def test_push_guard_still_enforced_after_keys(self):
        s = MetaServer([(200, GOOD, {})])
        try:
            (self.work / "collector.py").write_text("print(2)\n")
            subprocess.run(["git", "-C", str(self.work), "add", "collector.py"], check=True)
            r = self.push(s)
        finally:
            s.close()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("maintained by a revision", r.stderr)
        self.assertEqual(self.tip(), self.before)


class WiringTests(unittest.TestCase):
    def test_every_persistence_step_passes_the_job_token_for_the_lookup(self):
        import re
        n = 0
        for wf in sorted((ROOT / ".github/workflows").glob("*.yml")):
            for step in re.split(r"\n {6}- ", wf.read_text())[1:]:
                if "DESK_WRITER:" in step:
                    self.assertIn("DESK_META_TOKEN: ${{ github.token }}", step, wf.name)
                    n += 1
        self.assertEqual(n, 10)        # 2.27: + the collector's yield-receipt persistence step


if __name__ == "__main__":
    unittest.main()
