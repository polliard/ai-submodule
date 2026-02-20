---
description: "Run a multi-perspective API review panel for design, developer experience, and consumer usability"
argument-hint: "<target: path, API spec, or description of API to review>"
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

# API Review Panel

Execute a comprehensive API review following the panel definition at
`~/.ai/personas/panels/api-review.md`.

## Setup

1. Read the panel definition at `~/.ai/personas/panels/api-review.md`
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
target codebase.

## Execution

Follow the process from the panel definition:

1. **Bootstrap tooling** — Execute Tool Setup for each participant
   persona. Install and verify all required tools, deduplicating across
   participants.
2. **Review surface** — Review API contract, documentation, and SDK
   surface.
3. **Define personas** — Define developer personas and key workflows.
4. **Independent evaluation** — Each participant evaluates from their
   perspective (design, consumer, UX, frontend, backend, docs).
5. **Hands-on testing** — Perform hands-on testing of key consumer
   journeys.
6. **Breaking changes** — Identify breaking change risks.
7. **Present findings** — Use the severity scale for all findings.
8. **Prioritize** — Prioritize by developer friction and frequency of
   impact.
9. **Converge** — Produce consolidated design and experience
   improvements.

## Output

Write the final report to `.panels/api-review/` in the target repository
root (or current working directory).

Provide a developer satisfaction assessment (Strong / Adequate / Needs
Work / Poor) with prioritized improvements.
