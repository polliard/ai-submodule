---
description: "Run a multi-perspective performance review panel for bottleneck identification and optimization"
argument-hint: "<target: path, repo, or description of system to profile>"
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

# Performance Review Panel

Execute a comprehensive performance analysis following the panel
definition at `~/.ai/personas/panels/performance-review.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/performance-review.md` for participant roles
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
2. **Review requirements** — Review performance requirements and SLOs.
3. **Analyze metrics** — Analyze current metrics and bottlenecks.
4. **Independent evaluation** — Each participant identifies issues from
   their perspective (algorithms, backend, frontend, infrastructure,
   production).
5. **Prioritize** — Prioritize by user impact.
6. **Present findings** — Use the severity scale for all findings.
7. **Measurement strategy** — Define measurement strategy for validating
   improvements.

## Output

Write the final report to `.panels/performance-review/` in the target
repository root (or current working directory).

Include critical performance issues, quick wins, longer-term
optimizations, capacity risks, and benchmarking recommendations.
