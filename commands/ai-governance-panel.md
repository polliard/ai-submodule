---
description: "Run a multi-perspective AI governance review panel for instruction quality, MCP config, and agent safety"
argument-hint: "<target: path, repo, or description of AI integration to review>"
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

# AI Governance Review Panel

Execute a comprehensive AI governance review following the panel
definition at `~/.ai/personas/panels/ai-governance-review.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/ai-governance-review.md` for participant roles
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
2. **Inventory instructions** — Inventory all AI instruction surfaces
   (.github/copilot-instructions.md, CLAUDE.md, .cursorrules,
   .ai/instructions.md).
3. **Inventory MCP** — Inventory MCP server configurations and tool
   definitions.
4. **Independent evaluation** — Each participant evaluates from their
   perspective (instruction quality, MCP config, documentation, security,
   UX).
5. **Cross-reference** — Cross-reference instruction files for
   duplication and drift.
6. **Token budgets** — Estimate token budgets and identify bloat.
7. **Present findings** — Use the severity scale for all findings.
8. **Prioritize** — Prioritize improvements by impact on AI behavior
   accuracy.

## Output

Write the final report to `.panels/ai-governance-review/` in the target
repository root (or current working directory).

Include instruction quality summary, MCP audit results, drift report,
agent safety assessment, and prioritized improvement roadmap.
