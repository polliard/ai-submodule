---
description: "Run a multi-perspective architecture review panel for system design, data, and operational readiness"
argument-hint: "<target: path, repo, or description of system to review>"
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

# Architecture Review Panel

Execute a comprehensive architecture review following the panel
definition at `~/.ai/personas/panels/architecture-review.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/architecture-review.md` for participant roles
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
2. **Present context** — Present design context and constraints.
3. **Independent evaluation** — Each participant evaluates from their
   lens (structural, data, security, resilience, infrastructure, API,
   performance).
4. **Cross-cutting concerns** — Surface issues spanning multiple
   perspectives, including data model alignment with system boundaries.
5. **Schema evolution** — Assess schema evolution risks and migration
   complexity.
6. **Debate tradeoffs** — Explicitly discuss and document tradeoffs.
7. **Present findings** — Use the severity scale for all findings.
8. **Converge** — Produce consolidated recommendations with Go/No-Go.

## Output

Write the final report to `.panels/architecture-review/` in the target
repository root (or current working directory).

Provide a clear Go / No-Go recommendation with documented tradeoffs.
