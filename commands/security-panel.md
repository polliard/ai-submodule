---
description: "Run a multi-perspective security review panel combining offensive, defensive, and compliance evaluation"
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

# Security Review Panel

Execute a comprehensive security assessment following the panel
definition at `~/.ai/personas/panels/security-review.md`.

## Setup

1. Read the panel definition at
   `~/.ai/personas/panels/security-review.md` for participant roles and
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
2. **Scope definition** — Define scope, threat model, trust boundaries,
   and adversary profile.
3. **Reconnaissance** — Infrastructure Engineer performs service
   enumeration.
4. **Attack surface mapping** — Red Team maps attack surface and
   exploitation paths.
5. **Detection assessment** — Blue Team evaluates detection and response
   coverage.
6. **Gap analysis** — Purple Team maps offense-defense gaps.
7. **Application testing** — Backend Engineer tests application-layer
   vulnerabilities.
8. **Classification** — Security Auditor classifies findings with
   severity scale and CVSS.
9. **Stress test** — Adversarial Reviewer challenges assumptions across
   all perspectives.
10. **Compliance check** — Compliance Officer validates scope adherence
    and regulatory impact.
11. **Attack narratives** — Red Team chains findings into end-to-end
    attack stories.
12. **Converge** — Produce prioritized remediation and posture
    improvement plan.

## Output

Write the final report to `.panels/security-review/` in the target
repository root (or current working directory).

Provide a security posture assessment (Strong / Adequate / Weak /
Critical) with prioritized remediation roadmap.
