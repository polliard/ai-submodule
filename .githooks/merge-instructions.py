#!/usr/bin/env python3
"""Sync instructions.md into copilot-instructions.md between SYNC markers.

The target file (copilot-instructions.md) contains two zones:
  1. Project-specific content above the SYNC:INSTRUCTIONS START marker
  2. Auto-synced content from instructions.md between the markers

The base file's H1 heading is stripped; everything from the first
non-blank line after the H1 onward is injected between the markers.

Usage:
    python3 merge-instructions.py <base> <target>

Writes merged output to stdout.
"""

import sys

SYNC_START = "<!-- SYNC:INSTRUCTIONS START"
SYNC_END = "<!-- SYNC:INSTRUCTIONS END -->"


def strip_h1_preamble(text):
    """Remove the H1 heading line and leading blanks after it."""
    lines = text.split("\n")
    result = []
    skipped_h1 = False
    for line in lines:
        if not skipped_h1 and line.startswith("# "):
            skipped_h1 = True
            continue
        result.append(line)
    # Strip leading blank lines after H1 removal
    while result and result[0].strip() == "":
        result.pop(0)
    return "\n".join(result)


def sync(base_text, target_text):
    """Replace content between SYNC markers with base instructions."""
    lines = target_text.split("\n")

    start_line = None
    end_line = None
    for i, line in enumerate(lines):
        if SYNC_START in line and start_line is None:
            start_line = i
        if SYNC_END in line:
            end_line = i

    if start_line is None or end_line is None:
        print(
            "Error: SYNC markers not found in target file.",
            file=sys.stderr,
        )
        print(f"  Expected start containing: {SYNC_START}", file=sys.stderr)
        print(f"  Expected end: {SYNC_END}", file=sys.stderr)
        sys.exit(1)

    if start_line >= end_line:
        print(
            "Error: START marker must appear before END marker.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build output
    before = lines[: start_line + 1]
    after = lines[end_line:]

    content = strip_h1_preamble(base_text).rstrip("\n")

    output = before + [""] + content.split("\n") + [""] + after
    return "\n".join(output) + "\n"


def main():
    if len(sys.argv) != 3:
        print(
            f"Usage: {sys.argv[0]} <base> <target>",
            file=sys.stderr,
        )
        print(
            "Syncs base content into target between SYNC markers, "
            "writes to stdout.",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(sys.argv[1]) as f:
        base_text = f.read()
    with open(sys.argv[2]) as f:
        target_text = f.read()

    sys.stdout.write(sync(base_text, target_text))


if __name__ == "__main__":
    main()
