---
description: "Run a multi-perspective incident post-mortem panel for root cause analysis and systemic improvements"
argument-hint: "<target: incident description, timeline, or path to incident data>"
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

# Incident Post-Mortem Panel

Execute a comprehensive incident post-mortem following the panel
definition at `~/.ai/personas/panels/incident-post-mortem.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/incident-post-mortem.md` for participant roles
   and process.
2. Load each participant persona from `~/.ai/personas/` as referenced in
   the panel definition.
3. Read the shared policies:
   - `~/.ai/personas/_shared/severity-scale.md`
   - `~/.ai/personas/_shared/scope-constraints.md`
   - `~/.ai/personas/_shared/credential-policy.md`

## Target

Analyze: $ARGUMENTS

If no argument is provided, prompt the user to describe the incident.

## Execution

Follow the process from the panel definition:

1. **Bootstrap tooling** — Execute Tool Setup for each participant
   persona. Install and verify all required tools, deduplicating across
   participants.
2. **Reconstruct timeline** — Reconstruct the incident timeline with all
   available data.
3. **Independent analysis** — Each participant analyzes from their
   perspective (response, SLO impact, architecture, resilience,
   observability, code-level faults).
4. **Contributing factors** — Identify contributing factors (not blame).
5. **Root cause separation** — Distinguish symptoms from root causes.
6. **Present findings** — Use the severity scale for all findings.
7. **Prioritize** — Prioritize preventive actions by impact.

## Output

Write the final report to `.panels/incident-post-mortem/` in the target
repository root (or current working directory).

Include incident summary, root causes, contributing factors, what went
well, and actionable items with owners.
