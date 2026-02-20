---
description: "Run a multi-perspective documentation review panel for accuracy, completeness, and usability"
argument-hint: "<target: path, repo, or description of documentation to review>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
  - Task
  - WebFetch
  - WebSearch
---

# Documentation Review Panel

Execute a comprehensive documentation review following the panel
definition at `~/.ai/personas/panels/documentation-review.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/documentation-review.md` for participant roles
   and process.
2. Load each participant persona from `~/.ai/personas/` as referenced in
   the panel definition.
3. Read the shared policies:
   - `~/.ai/personas/_shared/severity-scale.md`
   - `~/.ai/personas/_shared/scope-constraints.md`
   - `~/.ai/personas/_shared/credential-policy.md`

## Target

Analyze: $ARGUMENTS

If no argument is provided, analyze the current working directory as the
target codebase.

## Execution

Follow the process from the panel definition:

1. **Bootstrap tooling** — Execute Tool Setup for each participant
   persona. Install and verify all required tools, deduplicating across
   participants.
2. **Identify audiences** — Identify target audiences for the
   documentation.
3. **Independent evaluation** — Each participant evaluates from their
   perspective (accuracy, clarity, discoverability, learning, UX).
4. **Follow-along test** — Test documentation by following it step by
   step.
5. **Gap analysis** — Identify gaps and inconsistencies.
6. **Present findings** — Use the severity scale for all findings.
7. **Prioritize** — Prioritize improvements by user impact.

## Output

Write the final report to `.panels/documentation-review/` in the target
repository root (or current working directory).

Include critical missing docs, accuracy issues, structure improvements,
and maintenance recommendations.
