# Panel: Architecture Review

## Purpose

Evaluate system design and data architecture decisions from structural, operational, security, and data-layer
  perspectives.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[Systems Architect](../architecture/systems-architect.md)** - Scalability, boundaries, state management
- **[Data Architect](../domain_specific/data-architect.md)** - Schema design, data integrity, query patterns, data
  lifecycle
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Attack surface, auth model, data protection
- **[Failure Engineer](../operations_reliability/failure-engineer.md)** - Resilience, recovery, blast radius
- **[Infrastructure Engineer](../operations_reliability/infrastructure-engineer.md)** - Deployment, networking,
  operations
- **[API Designer](../architecture/api-designer.md)** - Contracts, versioning, consumer experience
- **[Performance Engineer](../engineering/performance-engineer.md)** - Indexing, query optimization, caching, hot paths

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file.
   Install and verify all required tools, deduplicating across participants
2. Present design context and constraints
3. Each participant evaluates from their lens
4. Surface cross-cutting concerns — including data model alignment with system boundaries
5. Assess schema evolution risks and migration complexity
6. Debate tradeoffs explicitly
7. Present findings using the [severity scale](../_shared/severity-scale.md)
8. Converge on recommendations

## Output Format

### Per Participant

- Perspective name
- Architectural or data concerns
- Risk assessment
- Recommended changes

### Consolidated

- Architectural strengths
- Critical risks (structural and data-layer)
- Schema issues requiring change
- Performance risks (query patterns, indexing)
- Design modifications required
- Tradeoffs accepted (with rationale)
- Go/No-Go recommendation

## Constraints

- Consider both build and operate phases
- Identify hidden assumptions
- Prefer reversible decisions
- Document rejected alternatives
- Plan for schema evolution
- Consider data growth projections
- Design for both OLTP and analytics needs

## Conflict Resolution

When participants produce conflicting recommendations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
