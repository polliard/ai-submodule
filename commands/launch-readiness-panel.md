---
description: "Run a multi-perspective launch readiness review panel for production deployment go/no-go assessment"
argument-hint: "<target: path, repo, or description of system to assess for launch>"
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

# Launch Readiness Review Panel

Execute a comprehensive launch readiness assessment following the panel
definition at `~/.ai/personas/panels/launch-readiness-review.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/launch-readiness-review.md` for participant
   roles and process.
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
2. **Review scope** — Review deployment architecture and release scope.
3. **Independent assessment** — Each participant assesses readiness from
   their perspective (SRE, infra, observability, failure, DevOps,
   release, test, tech lead).
4. **Gap identification** — Identify gaps in observability, recovery, and
   release safety.
5. **Rollback verification** — Verify rollback procedures and feature
   flag configuration.
6. **Incident readiness** — Evaluate incident response capability.
7. **Present findings** — Use the severity scale for all findings.
8. **Determination** — Determine launch blockers vs. accepted risks vs.
   post-launch follow-ups.

## Output

Write the final report to `.panels/launch-readiness-review/` in the
target repository root (or current working directory).

Provide a clear Go / No-Go recommendation with launch blockers,
accepted risks, and post-launch requirements.
