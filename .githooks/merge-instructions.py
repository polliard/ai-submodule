#!/usr/bin/env python3
"""Section-level merge of instructions.md into copilot-instructions.md.

Merge strategy (operates at H2 boundaries):
- Preamble (before first ##): always from base (instructions.md)
- Section exists in both files: base wins (updates from import)
- Section only in target (copilot): preserved (project addition)
- Section only in base: appended before footer (new base section)
- Footer (--- + ## Project-Specific Instructions): always from target
"""

import sys


def parse_document(text):
    """Parse markdown into (preamble, sections, footer).

    preamble: lines before the first ## heading
    sections: list of (header, lines) preserving order
    footer:   lines from '---' + '## Project-Specific' onward
    """
    lines = text.rstrip("\n").split("\n")
    preamble = []
    sections = []
    footer = []
    current_header = None
    current_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect footer: '---' followed by '## Project-Specific ...'
        if line.strip() == "---":
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines) and lines[j].startswith("## Project-Specific"):
                if current_header is not None:
                    sections.append((current_header, current_lines))
                footer = lines[i:]
                break

        if line.startswith("## "):
            # Save previous section or preamble
            if current_header is not None:
                sections.append((current_header, current_lines))
            elif current_lines:
                preamble = current_lines
            current_header = line
            current_lines = [line]
        else:
            current_lines.append(line)

        i += 1
    else:
        # End of file with no footer
        if current_header is not None:
            sections.append((current_header, current_lines))
        elif current_lines and not preamble:
            preamble = current_lines

    return preamble, sections, footer


def merge(base_text, target_text):
    """Merge base into target, preserving target-only sections."""
    base_pre, base_secs, _ = parse_document(base_text)
    _, tgt_secs, tgt_footer = parse_document(target_text)

    base_lookup = {h: lines for h, lines in base_secs}
    base_headers = [h for h, _ in base_secs]

    result_sections = []
    used_base = set()

    # Walk target section order — preserves project section placement
    for header, tgt_lines in tgt_secs:
        if header in base_lookup:
            result_sections.append(base_lookup[header])
            used_base.add(header)
        else:
            result_sections.append(tgt_lines)

    # Append new base sections not already in target
    for header in base_headers:
        if header not in used_base:
            result_sections.append(base_lookup[header])

    # Assemble
    output = []
    output.extend(base_pre)

    for section_lines in result_sections:
        if output and output[-1].strip() != "":
            output.append("")
        output.extend(section_lines)

    if tgt_footer:
        if output and output[-1].strip() != "":
            output.append("")
        output.extend(tgt_footer)

    return "\n".join(output) + "\n"


def main():
    if len(sys.argv) != 3:
        print(
            f"Usage: {sys.argv[0]} <base> <target>",
            file=sys.stderr,
        )
        print(
            "Merges base H2 sections into target, writes to stdout.",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(sys.argv[1]) as f:
        base_text = f.read()
    with open(sys.argv[2]) as f:
        target_text = f.read()

    sys.stdout.write(merge(base_text, target_text))


if __name__ == "__main__":
    main()
