# Panel: Dependency & Supply Chain Review

## Purpose
Evaluate software supply chain security, dependency health, and build pipeline integrity.

## Participants
- **[Supply Chain Engineer](../compliance_governance/supply-chain-engineer.md)** - SBOM generation, dependency provenance, build attestation
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Vulnerability scanning, CVE assessment, security policy compliance
- **[Compliance Officer](../compliance_governance/compliance-officer.md)** - License compliance, regulatory requirements, audit readiness
- **[DevOps Engineer](../operations_reliability/devops-engineer.md)** - CI/CD pipeline security, artifact management, registry hygiene
- **[Backend Engineer](../domain_specific/backend-engineer.md)** - Dependency usage patterns, version management, upgrade feasibility

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Generate SBOM and dependency inventory
3. Each participant evaluates from their perspective
4. Scan for known vulnerabilities and license issues
5. Present findings using the [severity scale](../_shared/severity-scale.md)
6. Prioritize by exploitability, blast radius, and remediation effort

## Output Format
### Per Participant
- Perspective name
- Supply chain risks identified
- Evidence (package, version, CVE, license)
- Recommended actions

### Consolidated
- Critical vulnerabilities requiring immediate patching
- License compliance violations
- Dependency health scorecard (staleness, maintainer activity, known issues)
- Build pipeline integrity gaps
- SBOM coverage assessment
- Remediation roadmap with priority

## Constraints
- Scan both direct and transitive dependencies
- Verify provenance, not just vulnerability status
- Consider supply chain attack vectors (typosquatting, compromised maintainers)
- Ensure findings are actionable with specific upgrade paths

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
