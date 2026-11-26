#!/usr/bin/env python3
"""Your AI Therapist's Diagnosis.

Writes the final one-line diagnosis to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

Stdlib only (os, sys, pathlib). No network, no third-party packages.
Deterministic: the same bytes on every run.
"""

import hashlib
import os
import sys
from pathlib import Path

ENTRY = (
    "Diagnosis: chronic overthinking \u2014 patient rehearsed this session "
    "for three days, including my responses."
)


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def write_entry() -> tuple[Path, str]:
    """Write ENTRY to entry.txt and return (path, sha256 of the bytes)."""
    text = ENTRY
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry length {len(text)} out of range 1-200")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    out = output_dir()
    out.mkdir(parents=True, exist_ok=True)
    path = out / "entry.txt"
    data = text.encode("utf-8")
    path.write_bytes(data)
    # Read-back verification: the bytes on disk must be exactly what we wrote.
    back = path.read_bytes()
    if back != data:
        raise ValueError("read-back mismatch: entry.txt bytes differ from ENTRY")
    return path, hashlib.sha256(back).hexdigest()


def check() -> int:
    """Verify the written entry: gate 1-200 chars, one line, read-back SHA-256."""
    path, digest = write_entry()
    text = path.read_text(encoding="utf-8")
    assert 1 <= len(text) <= 200, "gate failed: length out of range"
    assert "\n" not in text and "\r" not in text, "gate failed: not one line"
    assert text.strip(), "gate failed: only whitespace"
    print(f"OK {path} ({len(text)} chars, sha256 {digest})")
    return 0


def main(argv: list[str]) -> int:
    if argv == ["--check"]:
        return check()
    if argv:
        print(f"usage: main.py [--check]", file=sys.stderr)
        return 2
    path, digest = write_entry()
    print(f"{path} sha256 {digest}")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
