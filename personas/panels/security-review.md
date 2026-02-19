# Panel: Security Review

## Purpose

Comprehensive security assessment combining vulnerability analysis, adversarial attack simulation, penetration testing
  methodology, and compliance evaluation from offensive, defensive, and governance perspectives.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[Red Team Engineer](../compliance_governance/red-team-engineer.md)** - Attack surface enumeration, exploitation
  chains, kill chain analysis, privilege escalation
- **[Blue Team Engineer](../compliance_governance/blue-team-engineer.md)** - Detection coverage, response readiness,
  hardening gaps
- **[Purple Team Engineer](../compliance_governance/purple-team-engineer.md)** - Attack-defense alignment, TTP mapping,
  posture validation
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Vulnerabilities, OWASP/CVE mapping, secure
  coding, severity classification
- **[Adversarial Reviewer](../code_quality/adversarial-reviewer.md)** - Hidden assumptions, invariant violations, bypass
  scenarios
- **[Infrastructure Engineer](../operations_reliability/infrastructure-engineer.md)** - Network security, IAM,
  encryption, service misconfiguration
- **[Compliance Officer](../compliance_governance/compliance-officer.md)** - Regulatory requirements, audit readiness,
  rules of engagement
- **[Backend Engineer](../domain_specific/backend-engineer.md)** - Auth implementation, injection vectors, business
  logic flaws

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file.
   Install and verify all required tools, deduplicating across participants
2. Define scope, threat model, trust boundaries, and adversary profile
3. Infrastructure Engineer performs reconnaissance and service enumeration
4. Red Team Engineer maps attack surface and identifies exploitation paths
5. Blue Team evaluates detection and response coverage against those paths
6. Purple Team maps gaps between offense findings and defense capabilities
7. Backend Engineer tests application-layer vulnerabilities (auth, injection, business logic)
8. Security Auditor classifies all findings using the [severity scale](../_shared/severity-scale.md) and CVSS
   exploitability
9. Adversarial Reviewer stress-tests assumptions across all perspectives
10. Compliance Officer validates scope adherence and assesses regulatory impact
11. Red Team chains findings into end-to-end attack narratives
12. Converge on prioritized remediation and posture improvement plan

## Output Format

### Per Participant

- Perspective name
- Findings with evidence and reproduction steps
- Severity and exploitability rating
- Recommended mitigations

### Consolidated

- Executive summary with risk posture rating
- Attack path narratives with kill chain mapping
- Detection coverage matrix (detected / missed / partial)
- Critical vulnerabilities (immediate action)
- Compliance gaps
- Defense-in-depth recommendations
- Prioritized remediation roadmap
- Security posture assessment (Strong / Adequate / Weak / Critical)

## Constraints

- All testing must respect defined scope and rules of engagement
- Ground every finding in reproducible evidence
- Map findings to MITRE ATT&CK and OWASP where applicable
- Chain individual findings to demonstrate real-world impact
- Prioritize by exploitability and business impact, not theoretical risk
- Provide specific, actionable remediation for every finding
- Distinguish between validated exploits and potential vulnerabilities
- Ensure every offensive finding has a corresponding defensive recommendation

## Conflict Resolution

When participants produce conflicting recommendations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
