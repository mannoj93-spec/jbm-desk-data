"""Content-addressed forecast archive. Repository permissions remain the trust boundary."""
import hashlib
import os
from pathlib import Path
from schema import validate
from storage import atomic_bytes, atomic_json, loads, read_json


def test_hash(base, path):
    """Include local root Python dependencies in the prospective registration clock."""
    base, path = Path(base), Path(path)
    files = sorted(set(base.glob("*.py")) | {path})
    h = hashlib.sha256()
    for item in files:
        h.update(str(item.relative_to(base)).encode() + b"\0" + item.read_bytes() + b"\0")
    return h.hexdigest()


def register(base, now):
    base = Path(base)
    state_path = base / "state/registered.json"
    stamps = read_json(state_path, {})
    manifest_path = base / "state/forecast_manifest.json"
    manifest = read_json(manifest_path, {})
    new, errors = [], []
    for path in sorted((base / "registry").glob("*.json")):
        if path.name.startswith("_"):
            continue
        rel = path.relative_to(base).as_posix()
        try:
            raw = path.read_bytes()
            fc = loads(raw)
            issues = validate(fc)
            if issues:
                raise ValueError("; ".join(issues))
            h = hashlib.sha256(raw).hexdigest()
            fid = fc["id"]
            if fid in manifest:
                if manifest[fid]["sha256"] != h or manifest[fid]["source"] != rel:
                    raise ValueError("registered ID changed or reused; original remains authoritative; use a new ID")
                continue
            # Retain a legacy exact-content stamp, if one exists, rather than inventing history.
            rat = stamps.get(f"{rel}@{h[:16]}", now)
            frozen = f"registry/frozen/{h}.json"
            target = base / frozen
            if target.exists() and target.read_bytes() != raw:
                raise ValueError("frozen content mismatch")
            if not target.exists():
                atomic_bytes(target, raw)
            manifest[fid] = {"id": fid, "source": rel, "sha256": h, "frozen": frozen,
                             "registered": rat, "registration_commit": os.environ.get("GITHUB_SHA", "local")}
            stamps[f"{rel}@{h}"] = rat
            new.append(rel)
        except (ValueError, TypeError, KeyError) as exc:
            errors.append(f"{rel}: {exc}")
    for path in sorted((base / "tests").glob("*.py")):
        if path.name.startswith("_"):
            continue
        key = path.relative_to(base).as_posix() + "@" + test_hash(base, path)
        if key not in stamps:
            stamps[key] = now
            new.append(key)
    # Frozen bytes are durable before the manifest that refers to them.
    atomic_json(manifest_path, manifest)
    atomic_json(state_path, stamps)
    return new, errors


class BatchError(ValueError):
    """A batch could not be registered; nothing it wrote is referenced by the manifest."""


def _hook(hooks, name):
    if hooks and name in hooks:
        hooks[name]()


def register_batch(base, items, frozen_at, meta, hooks=None):
    """Register several forecasts as one logical transaction (desk range stream, repo 2.15).

    items: [(relative source path, exact bytes)]. frozen_at: the single local freezing time (ms) used for
    validation and as `registered`; every window must start strictly after it. meta: fields added to each
    manifest entry (attempt, contract, code_commit). Order: validate all -> frozen bytes -> ONE atomic
    manifest write (the commit point) -> registration stamps -> source files (derivable from the frozen bytes,
    restored by `restore_sources`). Before the commit point every failure removes what this call created;
    after it the registration is complete and sources are rolled forward. Returns ("new"|"existing", entries).
    Durable publication (the remote commit) is separate and recorded by the caller."""
    base = Path(base)
    manifest_path, state_path = base / "state/forecast_manifest.json", base / "state/registered.json"
    manifest, stamps = read_json(manifest_path, {}), read_json(state_path, {})
    staged, existing = [], []
    for rel, raw in items:
        fc = loads(raw)
        issues = validate(fc, frozen_at)
        if issues:
            raise BatchError(f"{rel}: {'; '.join(issues)}")
        fid, h = fc["id"], hashlib.sha256(raw).hexdigest()
        if rel != f"registry/{fid}.json":
            raise BatchError(f"{rel}: source path must be registry/<id>.json")
        if fid in manifest:
            if manifest[fid]["sha256"] != h or manifest[fid]["source"] != rel:
                raise BatchError(f"{fid}: ID already registered with different content; the original stands")
            existing.append(fid)
            continue
        src = base / rel
        if src.exists() and src.read_bytes() != raw:
            raise BatchError(f"{rel}: an unregistered file with different bytes occupies this ID")
        staged.append((rel, raw, fid, h))
    if existing and staged:
        raise BatchError("batch partly registered already; refusing to mix records")
    if existing:
        return "existing", {fid: manifest[fid] for fid in existing}
    created = []
    try:
        for rel, raw, fid, h in staged:
            target = base / f"registry/frozen/{h}.json"
            if target.exists():
                if target.read_bytes() != raw:
                    raise BatchError("frozen content mismatch")
            else:
                atomic_bytes(target, raw)
                created.append(target)
        _hook(hooks, "after_frozen")
        new_entries = {}
        for rel, raw, fid, h in staged:
            new_entries[fid] = dict(meta, id=fid, source=rel, sha256=h, frozen=f"registry/frozen/{h}.json",
                                    registered=frozen_at)
        manifest.update(new_entries)
        _hook(hooks, "before_manifest")
        atomic_json(manifest_path, manifest)               # commit point
    except BaseException:
        for path in created:
            path.unlink(missing_ok=True)
        raise
    for rel, raw, fid, h in staged:
        stamps[f"{rel}@{h}"] = frozen_at
    atomic_json(state_path, stamps)
    _hook(hooks, "after_manifest")
    restore_sources(base, list(new_entries))
    return "new", new_entries


def restore_sources(base, ids=None):
    """Roll forward: rewrite missing or divergent source files of registered forecasts from frozen bytes."""
    base = Path(base)
    manifest = read_json(base / "state/forecast_manifest.json", {})
    fixed = []
    for fid in (ids if ids is not None else list(manifest)):
        entry = manifest[fid]
        raw = (base / entry["frozen"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise ValueError(f"frozen forecast {fid}: hash mismatch")
        src = base / entry["source"]
        if not src.exists() or src.read_bytes() != raw:
            atomic_bytes(src, raw)
            fixed.append(fid)
    return fixed


def forecasts(base, errors=None):
    """Verified (forecast, manifest entry) pairs. Without `errors` any integrity problem raises (fail closed);
    with a list, each failing record is reported there as (id, reason) and skipped - never yielded."""
    base = Path(base)
    manifest = read_json(base / "state/forecast_manifest.json", {})
    if not isinstance(manifest, dict):
        raise ValueError("forecast manifest is not an object")
    for fid, entry in sorted(manifest.items()):
        try:
            if not isinstance(entry, dict) or not isinstance(entry.get("frozen"), str):
                raise ValueError(f"frozen forecast {fid}: manifest entry malformed")
            path = base / entry["frozen"]
            if path.resolve().parent != (base / "registry/frozen").resolve():
                raise ValueError("invalid frozen path")
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != entry.get("sha256"):
                raise ValueError(f"frozen forecast {fid}: hash mismatch")
            fc = loads(raw)
            errs = validate(fc)
            if not isinstance(fc, dict) or fc.get("id") != fid or errs:
                raise ValueError(f"frozen forecast {fid}: invalid schema {errs}")
        except (ValueError, OSError, TypeError) as exc:
            if errors is None:
                raise
            errors.append((fid, str(exc)))
            continue
        yield fc, entry
