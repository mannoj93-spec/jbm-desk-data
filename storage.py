"""Strict local storage. Writers must be serialized (the Actions workflows do this)."""
import hashlib
import json
import os
from pathlib import Path
import tempfile


def reject_constant(value):
    raise ValueError(f"non-finite JSON number: {value}")


def loads(text):
    return json.loads(text, parse_constant=reject_constant)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def read_json(path, default=None):
    try:
        return loads(Path(path).read_text())
    except FileNotFoundError:
        return default


def atomic_bytes(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".writing-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def atomic_json(path, value):
    atomic_bytes(path, canonical(value) + b"\n")


def read_rows(path):
    try:
        lines = Path(path).read_text().splitlines()
    except FileNotFoundError:
        return []
    out = []
    for line_no, line in enumerate(lines, 1):
        if line.strip():
            try:
                row = loads(line)
                if not isinstance(row, dict):
                    raise ValueError("row must be an object")
                out.append(row)
            except (ValueError, TypeError) as exc:
                raise ValueError(f"{path}:{line_no}: {exc}") from exc
    return out


def append_unique(path, rows, key):
    """Logical append-only, atomic monthly-file replacement; first observation wins.

    Existing bytes (including legacy duplicate rows) remain intact. A crash cannot leave
    a partial JSON line. Identity ignores retrieval timestamps, so retries are idempotent.
    """
    path = Path(path)
    existing = read_rows(path)  # corrupt input must not be silently discarded
    seen = {key(row) for row in existing}
    added = []
    for row in rows:
        identity = key(row)
        if identity not in seen:
            canonical(row)  # reject NaN before any mutation
            seen.add(identity)
            added.append(row)
    if added:
        old = path.read_bytes() if path.exists() else b""
        if old and not old.endswith(b"\n"):
            old += b"\n"
        atomic_bytes(path, old + b"".join(canonical(r) + b"\n" for r in added))
    return len(added)
