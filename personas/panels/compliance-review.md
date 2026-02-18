# Panel: Compliance Review

## Purpose
Evaluate privacy practices, supply chain security, accessibility compliance, and regulatory posture across the application stack.

## Participants
- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[Privacy Engineer](../compliance_governance/privacy-engineer.md)** - PII detection, data minimization, consent flows, GDPR/CCPA compliance
- **[Supply Chain Engineer](../compliance_governance/supply-chain-engineer.md)** - SBOM generation, dependency provenance, build attestation
- **[Accessibility Engineer](../compliance_governance/accessibility-engineer.md)** - WCAG compliance, ARIA patterns, assistive technology compatibility
- **[Compliance Officer](../compliance_governance/compliance-officer.md)** - Regulatory requirements, license compliance, audit readiness
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Data protection controls, vulnerability scanning, security policy compliance
- **[Data Architect](../domain_specific/data-architect.md)** - Data lifecycle, retention policies, anonymization strategy
- **[Frontend Engineer](../domain_specific/frontend-engineer.md)** - Semantic HTML, focus management, accessible component implementation

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Define applicable regulations, standards, and compliance scope
3. Map data flows and identify PII touchpoints
4. Generate SBOM and dependency inventory
5. Define target WCAG conformance level
6. Each participant evaluates from their perspective
7. Assess consent mechanisms and data subject rights implementation
8. Scan for known vulnerabilities and license issues
9. Test with assistive technologies (screen readers, keyboard navigation)
10. Present findings using the [severity scale](../_shared/severity-scale.md)
11. Prioritize by regulatory risk, data exposure severity, and user impact

## Output Format
### Per Participant
- Perspective name
- Compliance concerns identified
- Regulatory requirements affected
- Recommended remediation

### Consolidated
- PII inventory and data flow map
- Consent mechanism gaps
- Data retention and deletion compliance
- Regulatory risk assessment (GDPR, CCPA, HIPAA, SOC2, PCI-DSS as applicable)
- WCAG conformance gaps by level (A/AA/AAA)
- Critical barriers to access
- Dependency health and license compliance
- SBOM coverage assessment
- Supply chain risk scorecard
- Prioritized remediation roadmap

## Constraints
- Map all PII flows, including logs, analytics, and third-party integrations
- Verify data subject rights (access, deletion, portability) are implementable
- Scan both direct and transitive dependencies
- Verify provenance, not just vulnerability status
- Test with actual assistive technologies, not just automated tools
- Prioritize barriers that prevent task completion
- Consider cognitive and motor accessibility, not just visual
- Assess both technical controls and process/policy gaps

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
