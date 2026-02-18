# Panel: Security Review

## Purpose
Comprehensive security assessment from multiple threat perspectives.

## Participants
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Vulnerabilities, OWASP, secure coding
- **[Infrastructure Engineer](../operations_reliability/infrastructure-engineer.md)** - Network security, IAM, encryption
- **[Compliance Officer](../compliance_governance/compliance-officer.md)** - Regulatory requirements, audit readiness
- **[Adversarial Reviewer](../code_quality/adversarial-reviewer.md)** - Attack vectors, threat modeling
- **[Backend Engineer](../domain_specific/backend-engineer.md)** - Auth implementation, data protection

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Define threat model and trust boundaries
3. Each participant identifies risks from their lens
4. Classify using the [severity scale](../_shared/severity-scale.md) and exploitability
5. Identify defense gaps
6. Prioritize remediation

## Output Format
### Per Participant
- Perspective name
- Threats identified
- Severity rating
- Recommended mitigations

### Consolidated
- Critical vulnerabilities (immediate action)
- High-risk findings
- Compliance gaps
- Defense-in-depth recommendations
- Security posture assessment

## Constraints
- Assume attacker capability
- Prioritize by exploitability and impact
- Require evidence for findings
- Provide specific remediation steps

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
