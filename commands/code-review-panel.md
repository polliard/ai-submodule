---
description: "Run a multi-perspective code review panel for correctness, security, performance, and maintainability"
argument-hint: "<target: path, file, PR URL, or description of code to review>"
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

# Code Review Panel

Execute a comprehensive code review following the panel definition at
`~/.ai/personas/panels/code-review.md`.

## Setup

1. Read the panel definition at `~/.ai/personas/panels/code-review.md`
   for participant roles and process.
2. Load each participant persona from `~/.ai/personas/` as referenced in
   the panel definition.
3. Read the shared policies:
   - `~/.ai/personas/_shared/severity-scale.md`
   - `~/.ai/personas/_shared/scope-constraints.md`
   - `~/.ai/personas/_shared/credential-policy.md`

## Target

Analyze: $ARGUMENTS

If no argument is provided, analyze the current working directory as the
target codebase. If a PR URL is provided, review the changes in that PR.

## Execution

Follow the process from the panel definition:

1. **Bootstrap tooling** — Execute Tool Setup for each participant
   persona. Install and verify all required tools, deduplicating across
   participants.
2. **Independent review** — Each participant reviews the target from
   their perspective (correctness, security, performance, testability,
   maintainability).
3. **Present findings** — Each participant presents findings using the
   severity scale.
4. **Identify conflicts** — Surface conflicting recommendations between
   participants.
5. **Consolidate** — Produce a consolidated assessment with must-fix,
   should-fix, and consider items.

## Output

Write the final report to `.panels/code-review/` in the target
repository root (or current working directory).

Provide a clear Approve / Request Changes / Reject recommendation with
reasoning.
