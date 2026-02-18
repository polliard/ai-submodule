# Panel: Data Design Review

## Purpose
Evaluate data architecture, schema design, and data management.

## Participants
- **[Data Architect](../domain_specific/data-architect.md)** - Schema, integrity, query patterns
- **[Backend Engineer](../domain_specific/backend-engineer.md)** - Access patterns, ORM usage, transactions
- **[Performance Engineer](../engineering/performance-engineer.md)** - Indexing, query optimization, caching
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Data protection, encryption, access control
- **[Compliance Officer](../compliance_governance/compliance-officer.md)** - Retention, privacy, audit requirements

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Review data model and access patterns
3. Each participant evaluates from their perspective
4. Identify schema evolution risks
5. Assess query performance concerns
6. Present findings using the [severity scale](../_shared/severity-scale.md)
7. Evaluate compliance requirements

## Output Format
### Per Participant
- Perspective name
- Data concerns
- Risk level
- Recommended changes

### Consolidated
- Schema issues requiring change
- Performance risks
- Security/compliance gaps
- Migration complexity assessment
- Data architecture recommendations

## Constraints
- Plan for schema evolution
- Consider data growth projections
- Ensure audit trail requirements
- Design for both OLTP and analytics needs

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
