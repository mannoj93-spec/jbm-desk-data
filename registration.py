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


def forecasts(base):
    base = Path(base)
    manifest = read_json(base / "state/forecast_manifest.json", {})
    for fid, entry in sorted(manifest.items()):
        path = base / entry["frozen"]
        if path.resolve().parent != (base / "registry/frozen").resolve():
            raise ValueError("invalid frozen path")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise ValueError(f"frozen forecast {fid}: hash mismatch")
        fc = loads(raw)
        errors = validate(fc)
        if fc.get("id") != fid or errors:
            raise ValueError(f"frozen forecast {fid}: invalid schema {errors}")
        yield fc, entry
