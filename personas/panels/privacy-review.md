# Panel: Privacy Review

## Purpose
Evaluate data privacy practices, PII handling, consent mechanisms, and regulatory compliance across the application stack.

## Participants
- **[Privacy Engineer](../compliance_governance/privacy-engineer.md)** - PII detection, data minimization, consent flows, GDPR/CCPA compliance
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Data protection controls, encryption, access control
- **[Compliance Officer](../compliance_governance/compliance-officer.md)** - Regulatory requirements, audit readiness, policy conformance
- **[Data Architect](../domain_specific/data-architect.md)** - Data lifecycle, retention policies, anonymization strategy
- **[Backend Engineer](../domain_specific/backend-engineer.md)** - Implementation of privacy controls, data access patterns, logging hygiene

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Map data flows and identify PII touchpoints
3. Each participant evaluates from their perspective
4. Assess consent mechanisms and data subject rights implementation
5. Present findings using the [severity scale](../_shared/severity-scale.md)
6. Prioritize by regulatory risk and data exposure severity

## Output Format
### Per Participant
- Perspective name
- Privacy concerns identified
- Regulatory requirements affected
- Recommended remediation

### Consolidated
- PII inventory and data flow map
- Consent mechanism gaps
- Data retention and deletion compliance
- Regulatory risk assessment (GDPR, CCPA, HIPAA as applicable)
- Critical privacy violations requiring immediate action
- Privacy improvement roadmap

## Constraints
- Map all PII flows, including logs, analytics, and third-party integrations
- Verify data subject rights (access, deletion, portability) are implementable
- Assess both technical controls and process/policy gaps
- Consider privacy implications of new features, not just existing ones

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
