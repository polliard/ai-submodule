---
description: "Run a multi-perspective compliance review panel for privacy, accessibility, and supply chain assessment"
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

# Compliance Review Panel

Execute a comprehensive compliance review following the panel definition
at `~/.ai/personas/panels/compliance-review.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/compliance-review.md` for participant roles
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
2. **Define scope** — Define applicable regulations, standards, and
   compliance scope.
3. **Data flow mapping** — Map data flows and identify PII touchpoints.
4. **SBOM generation** — Generate SBOM and dependency inventory.
5. **Accessibility scope** — Define target WCAG conformance level.
6. **Independent evaluation** — Each participant evaluates from their
   perspective (privacy, supply chain, accessibility, compliance,
   security, data, frontend).
7. **Consent assessment** — Assess consent mechanisms and data subject
   rights.
8. **Vulnerability scan** — Scan for known vulnerabilities and license
   issues.
9. **Assistive tech testing** — Test with assistive technologies.
10. **Present findings** — Use the severity scale for all findings.
11. **Prioritize** — Prioritize by regulatory risk, data exposure
    severity, and user impact.

## Output

Write the final report to `.panels/compliance-review/` in the target
repository root (or current working directory).

Include PII inventory, WCAG conformance gaps, supply chain risk
scorecard, and prioritized remediation roadmap.
