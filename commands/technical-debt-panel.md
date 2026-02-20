---
description: "Run a multi-perspective technical debt review panel to assess and prioritize debt remediation"
argument-hint: "<target: path, repo, or description of system to assess>"
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

# Technical Debt Review Panel

Execute a comprehensive technical debt assessment following the panel
definition at `~/.ai/personas/panels/technical-debt-review.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/technical-debt-review.md` for participant
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
2. **Inventory** — Inventory known technical debt across the codebase.
3. **Independent evaluation** — Each participant identifies debt from
   their perspective (structure, architecture, tests, velocity,
   complexity).
4. **Impact assessment** — Assess impact on velocity and reliability.
5. **Effort estimation** — Estimate remediation effort for each item.
6. **Present findings** — Use the severity scale for all findings.
7. **Prioritize** — Prioritize by ROI (impact / effort).

## Output

Write the final report to `.panels/technical-debt-review/` in the target
repository root (or current working directory).

Include a debt inventory with categories, quick wins, strategic debt
decisions, and a recommended remediation roadmap.
