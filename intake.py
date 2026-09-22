#!/usr/bin/env python3
"""Validate public market forecasts. Free text is public; this is not a privacy filter."""
import datetime as dt
import os
from pathlib import Path
import re
import secrets
import sys
from schema import INSTRUMENT, iso, ms, num, prepare, validate
from storage import atomic_json, loads

BASE = Path(os.environ.get("OUT_DIR", Path(__file__).resolve().parent))


def extract(body):
    if len(body.encode()) > 65_000:
        raise ValueError("forecast issue exceeds 65 KB")
    match = re.fullmatch(r"\s*```(?:json)?\s*(\{.*\})\s*```\s*", body, re.S)
    return loads(match.group(1) if match else body.strip())


def emit(result, message, path=""):
    print(message)
    target = os.environ.get("GITHUB_OUTPUT")
    if target:
        delimiter = "MSG_" + secrets.token_hex(24)
        with open(target, "a") as fh:
            fh.write(f"result={result}\npath={path}\nmessage<<{delimiter}\n{message}\n{delimiter}\n")


def main():
    now = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
    try:
        body = Path(sys.argv[sys.argv.index("--check") + 1]).read_text() if "--check" in sys.argv else os.environ.get("ISSUE_BODY", "")
        fc = prepare(extract(body), now)
        errors = validate(fc, now)
    except Exception as exc:
        errors = [f"could not parse forecast: {exc}"]
    if "--check" in sys.argv:
        print("\n".join(errors) if errors else "valid")
        return 1 if errors else 0
    if errors:
        emit("invalid", "Not registered:\n- " + "\n- ".join(errors))
        return 0
    rel = f"registry/{fc['id']}.json"
    if (BASE / rel).exists():
        emit("invalid", "Forecast ID already exists. Use a new ID; forecasts are write-once.")
        return 0
    atomic_json(BASE / rel, fc)
    emit("ok", f"Validated `{rel}`. Start {fc['start_utc']}; horizon {fc['horizon_utc']}.", rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
