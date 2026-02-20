---
description: "Run a 5-track parallel threat modeling panel review using STRIDE + MITRE ATT&CK + Attack Trees"
argument-hint: "<target: path, repo, or description of system to analyze>"
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

# Threat Modeling Panel

Execute a comprehensive threat model following the methodology defined in
`~/.ai/prompts/threat-model.md` and output the report using the template at
`~/.ai/templates/threat-model.md`.

## Setup

1. Read `~/.ai/prompts/threat-model.md` for the full methodology, panel
   composition, 5-phase process, 19 agentic-specific patterns, compliance
   frameworks, and output requirements.
2. Read `~/.ai/templates/threat-model.md` for the report structure. Use it as
   the structural foundation for the final output.
3. Read the panel definition at `~/.ai/personas/panels/threat-modeling-review.md`
   for participant roles and process.
4. Load each participant persona from `~/.ai/personas/` as referenced in the
   panel definition.
5. Read the shared policies:
   - `~/.ai/personas/_shared/severity-scale.md`
   - `~/.ai/personas/_shared/scope-constraints.md`
   - `~/.ai/personas/_shared/credential-policy.md`

## Target

Analyze: $ARGUMENTS

If no argument is provided, analyze the current working directory as the target
codebase.

## Execution

Follow the 5-phase parallel process from the prompt:

1. **Phase 1 — Parallel Analysis**: Launch all 5 review tracks simultaneously.
   Each sub-moderator coordinates their specialist reviewers to analyze the
   actual source code with file and line references.
2. **Phase 2 — Per-Track Aggregation**: Each sub-moderator deduplicates,
   ranks, and flags cross-domain findings.
3. **Phase 3 — Overall Moderator Integration**: Cross-reference all tracks,
   identify convergent findings, construct compound attack chains, arbitrate
   severity.
4. **Phase 4 — 5 Hardening Rounds**: Sub-moderators challenge each other's
   findings iteratively. Overall Moderator validates mitigations.
5. **Phase 5 — Final Report Assembly**: Produce the integrated report using
   the template structure with all required Mermaid diagrams.

## Output

Write the final report to `.panels/threat-modeling-review/` in the target
repository root (or current working directory).

All diagrams MUST use Mermaid syntax. No ASCII art.
