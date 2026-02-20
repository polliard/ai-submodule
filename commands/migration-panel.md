---
description: "Run a multi-perspective migration review panel for data integrity, rollback, and operational safety"
argument-hint: "<target: migration plan, path, or description of migration>"
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

# Migration Review Panel

Execute a comprehensive migration review following the panel definition
at `~/.ai/personas/panels/migration-review.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/migration-review.md` for participant roles and
   process.
2. Load each participant persona from `~/.ai/personas/` as referenced in
   the panel definition.
3. Read the shared policies:
   - `~/.ai/personas/_shared/severity-scale.md`
   - `~/.ai/personas/_shared/scope-constraints.md`
   - `~/.ai/personas/_shared/credential-policy.md`

## Target

Analyze: $ARGUMENTS

If no argument is provided, analyze the current working directory for
migration-related files and plans.

## Execution

Follow the process from the panel definition:

1. **Bootstrap tooling** — Execute Tool Setup for each participant
   persona. Install and verify all required tools, deduplicating across
   participants.
2. **Review plan** — Review migration plan and timeline.
3. **Independent assessment** — Each participant assesses from their
   perspective (plan completeness, data integrity, operations, failure
   scenarios, resources).
4. **Rollback gaps** — Identify rollback gaps at every step.
5. **Failure stress test** — Stress-test failure scenarios.
6. **Present findings** — Use the severity scale for all findings.
7. **Communication plan** — Validate communication plan.

## Output

Write the final report to `.panels/migration-review/` in the target
repository root (or current working directory).

Provide a Go / No-Go recommendation with migration blockers, risk
mitigations, and rollback verification checklist.
