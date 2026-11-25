#!/usr/bin/env python3
"""Entry: write the childhood-memory sentence to the output.

The sentence ("Still Small Enough") recalls pretending to fall asleep on
the living-room floor so a father would carry the child to bed. The text
lives in entry.txt next to this program — a single source of truth — and
the program reads it, verifies it (UTF-8, 1 to 280 Unicode code points,
not only white space), and copies it to the output. Standard library
only, no network, and every run writes the exact same bytes.
"""

import os
import sys

MAX_CHARS = 280


def validate(text):
    """The gate wants one sentence of 1-280 code points, not whitespace."""
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(f"entry is {len(text)} characters, must be 1-{MAX_CHARS}")
    if not text.strip():
        raise SystemExit("entry is only white space")
    terminators = sum(text.count(mark) for mark in ".!?")
    if terminators != 1 or not text.rstrip().endswith((".", "!", "?")):
        raise SystemExit("entry must be a single sentence")


def read_bundle():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.txt")
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main(argv):
    out = argv[1] if len(argv) > 1 else "/output/entry.txt"
    text = read_bundle()
    validate(text)
    directory = os.path.dirname(out)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    with open(out, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != text:
        raise SystemExit("verification failed: written text differs")
    print(f"wrote {len(written)} characters to {out}")


if __name__ == "__main__":
    main(sys.argv)
