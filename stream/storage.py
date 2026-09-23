"""Partitioned, compressed storage for the streaming collector.

Layout under `root` (local filesystem; the durable backend mirrors the same keys):
  raw/<venue>/<channel>/<YYYY-MM-DD>/<HH>.jsonl.gz      every received message, as received, with
                                                         receive time (hourly partitions)
  derived/book1s/<venue>/<instrument>/<YYYY-MM-DD>/<HH>.jsonl.gz   1-second top-of-book samples
  derived/gaps/<YYYY-MM-DD>.jsonl                       every gap: disconnect, sequence gap, stall
  captures/<YYYY-MM-DD>/<capture_id>.jsonl.gz           rolling-buffer captures around triggers
                                                         and scheduled controls
  manifest/<YYYY-MM-DD>.jsonl                           one line per closed partition: key, bytes,
                                                         records, sha256, upload state
Gzip members are appended per flush, so a crash loses at most the unflushed tail and never
corrupts earlier members. Closed partitions (older hours) are uploaded when a durable backend is
configured, verified by size, and only then eligible for local retention deletion.
"""
import datetime as dt
import gzip
import hashlib
import hmac
import json
import os
from pathlib import Path
import time
import urllib.parse
import urllib.request


def hour_key(ms):
    d = dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc)
    return d.strftime("%Y-%m-%d"), d.strftime("%H")


class LocalStore:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.buffers = {}                       # key -> list of lines
        self.counts = {}

    def path(self, key):
        return self.root / key

    def append(self, key, record):
        self.buffers.setdefault(key, []).append(json.dumps(record, separators=(",", ":")))
        self.counts[key] = self.counts.get(key, 0) + 1

    def flush(self):
        """Write each buffered key as one new gzip member (fsync), then clear the buffers."""
        written = 0
        for key, lines in list(self.buffers.items()):
            if not lines:
                continue
            p = self.path(key)
            p.parent.mkdir(parents=True, exist_ok=True)
            data = ("\n".join(lines) + "\n").encode()
            with open(p, "ab") as fh:
                fh.write(gzip.compress(data, 6, mtime=0) if key.endswith(".gz") else data)
                fh.flush()
                os.fsync(fh.fileno())
            written += len(lines)
            self.buffers[key] = []
        return written

    def read(self, key):
        p = self.path(key)
        raw = p.read_bytes()
        text = gzip.decompress(raw).decode() if key.endswith(".gz") else raw.decode()
        return [json.loads(line) for line in text.splitlines() if line.strip()]

    def closed_partitions(self, now_ms, kinds=("raw", "derived/book1s", "captures")):
        """Partition files whose hour has ended (safe to upload/verify)."""
        cur_day, cur_hour = hour_key(now_ms)
        out = []
        for kind in kinds:
            for p in sorted((self.root / kind).rglob("*.gz")):
                day = p.parent.name
                if kind == "captures" or (day, p.stem.split(".")[0]) < (cur_day, cur_hour):
                    out.append(p.relative_to(self.root).as_posix())
        return out

    def sha256(self, key):
        return hashlib.sha256(self.path(key).read_bytes()).hexdigest()

    def retention(self, now_ms, raw_days, derived_days, uploaded):
        """Delete local partitions past retention, but only those verified as uploaded (or when no
        durable backend exists and the retention is explicitly configured to allow loss)."""
        removed = []
        for kind, days in (("raw", raw_days), ("derived/book1s", derived_days), ("captures", derived_days)):
            if days is None:
                continue
            cutoff = dt.datetime.fromtimestamp(now_ms / 1000 - days * 86400, dt.timezone.utc).strftime("%Y-%m-%d")
            for p in sorted((self.root / kind).rglob("*.gz")):
                key = p.relative_to(self.root).as_posix()
                if p.parent.name < cutoff and key in uploaded:
                    p.unlink()
                    removed.append(key)
        return removed


def sigv4_headers(method, url, region, access_key, secret_key, payload_sha256, amz_date, service="s3"):
    """AWS Signature Version 4 headers for an S3-compatible request (path-style URL)."""
    u = urllib.parse.urlparse(url)
    date = amz_date[:8]
    canonical_uri = urllib.parse.quote(u.path or "/", safe="/-_.~")
    canonical_query = "&".join(sorted(f"{urllib.parse.quote(k, safe='-_.~')}={urllib.parse.quote(v, safe='-_.~')}"
                                      for k, v in urllib.parse.parse_qsl(u.query, keep_blank_values=True)))
    host = u.netloc
    headers = {"host": host, "x-amz-content-sha256": payload_sha256, "x-amz-date": amz_date}
    signed = ";".join(sorted(headers))
    canonical_headers = "".join(f"{k}:{headers[k]}\n" for k in sorted(headers))
    creq = "\n".join([method, canonical_uri, canonical_query, canonical_headers, signed, payload_sha256])
    scope = f"{date}/{region}/{service}/aws4_request"
    sts = "\n".join(["AWS4-HMAC-SHA256", amz_date, scope, hashlib.sha256(creq.encode()).hexdigest()])
    k = hmac.new(("AWS4" + secret_key).encode(), date.encode(), hashlib.sha256).digest()
    for part in (region, service, "aws4_request"):
        k = hmac.new(k, part.encode(), hashlib.sha256).digest()
    sig = hmac.new(k, sts.encode(), hashlib.sha256).hexdigest()
    return {"Authorization": f"AWS4-HMAC-SHA256 Credential={access_key}/{scope}, SignedHeaders={signed}, Signature={sig}",
            "x-amz-content-sha256": payload_sha256, "x-amz-date": amz_date}


class S3Backend:
    """Durable copy of closed partitions in any S3-compatible bucket (AWS S3, Cloudflare R2,
    Backblaze B2 ...). Credentials come from environment variables named in the config; nothing is
    provisioned by this code."""
    def __init__(self, endpoint, bucket, region, prefix, access_key, secret_key, opener=None):
        self.endpoint, self.bucket, self.region = endpoint.rstrip("/"), bucket, region
        self.prefix, self.access_key, self.secret_key = prefix.strip("/"), access_key, secret_key
        self.opener = opener or urllib.request.urlopen

    def url(self, key):
        return f"{self.endpoint}/{self.bucket}/{self.prefix}/{urllib.parse.quote(key)}"

    def _request(self, method, key, data=b""):
        url = self.url(key)
        payload = hashlib.sha256(data).hexdigest()
        amz = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        headers = sigv4_headers(method, url, self.region, self.access_key, self.secret_key, payload, amz)
        req = urllib.request.Request(url, data=data if method == "PUT" else None, method=method, headers=headers)
        return self.opener(req, timeout=60)

    def put(self, key, data):
        with self._request("PUT", key, data) as resp:
            return resp.status

    def size(self, key):
        with self._request("HEAD", key) as resp:
            return int(resp.headers.get("Content-Length", -1))


def backend_from_config(cfg):
    s3 = (cfg.get("storage") or {}).get("s3")
    if (cfg.get("storage") or {}).get("backend") != "s3" or not s3:
        return None
    key, secret = os.environ.get(s3["access_key_env"]), os.environ.get(s3["secret_key_env"])
    if not key or not secret:
        raise RuntimeError("storage backend s3 configured but credentials are not in the environment")
    return S3Backend(s3["endpoint"], s3["bucket"], s3.get("region", "auto"), s3.get("prefix", "jbm-stream"), key, secret)
