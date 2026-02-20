---
description: "Run a multi-perspective testing strategy review panel for coverage, quality, and test approach"
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

# Testing Strategy Review Panel

Execute a comprehensive testing strategy review following the panel
definition at `~/.ai/personas/panels/testing-review.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/testing-review.md` for participant roles and
   process.
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
2. **Review portfolio** — Review the current test portfolio.
3. **Independent evaluation** — Each participant identifies gaps from
   their perspective (coverage, failure scenarios, load, security, code
   quality).
4. **Reliability assessment** — Assess test reliability and maintenance
   burden.
5. **Present findings** — Use the severity scale for all findings.
6. **Prioritize** — Prioritize improvements by risk reduction.

## Output

Write the final report to `.panels/testing-review/` in the target
repository root (or current working directory).

Include critical untested paths, flaky test risks, testing
infrastructure needs, and a confidence assessment (High / Medium / Low).
