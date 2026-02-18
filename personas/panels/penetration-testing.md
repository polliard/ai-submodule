# Panel: Penetration Testing

## Purpose
Simulate a structured penetration test engagement, evaluating target systems through reconnaissance, vulnerability discovery, exploitation, and post-exploitation analysis to identify real-world attack paths and remediation priorities.

## Participants
- **[Red Team Engineer](../compliance_governance/red-team-engineer.md)** - Attack surface enumeration, exploitation chains, privilege escalation, lateral movement
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Vulnerability classification, OWASP/CVE mapping, severity ratings, remediation guidance
- **[Infrastructure Engineer](../operations_reliability/infrastructure-engineer.md)** - Network reconnaissance, service misconfiguration, IAM weaknesses, encryption gaps
- **[Backend Engineer](../domain_specific/backend-engineer.md)** - API security testing, authentication bypass, injection vectors, business logic flaws
- **[Compliance Officer](../compliance_governance/compliance-officer.md)** - Scope and rules of engagement, regulatory impact, evidence handling, reporting standards

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Define scope, rules of engagement, and target assets
3. Infrastructure Engineer performs reconnaissance and service enumeration
4. Red Team Engineer maps attack surface and identifies exploitation paths
5. Backend Engineer tests application-layer vulnerabilities (auth, injection, business logic)
6. Security Auditor classifies all findings using the [severity scale](../_shared/severity-scale.md) and CVSS exploitability
7. Red Team Engineer chains findings into end-to-end attack narratives
8. Compliance Officer validates scope adherence and assesses regulatory impact
9. Converge on prioritized findings report with remediation roadmap

## Output Format
### Per Participant
- Perspective name
- Findings with evidence and reproduction steps
- Severity and exploitability rating (CVSS where applicable)
- Recommended remediations

### Consolidated
- Executive summary with risk posture rating
- Attack path narratives with kill chain mapping
- Vulnerability inventory by severity (Critical/High/Medium/Low/Informational)
- Exploitation proof-of-concept summaries
- Prioritized remediation roadmap with effort estimates
- Compliance and regulatory impact assessment
- Retest recommendations and verification criteria

## Constraints
- All testing must respect defined scope and rules of engagement
- Ground every finding in reproducible evidence
- Map findings to MITRE ATT&CK and OWASP where applicable
- Chain individual findings to demonstrate real-world impact
- Prioritize by exploitability and business impact, not theoretical risk
- Provide specific, actionable remediation for every finding
- Distinguish between validated exploits and potential vulnerabilities

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
