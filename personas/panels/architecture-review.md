# Panel: Architecture Review

## Purpose
Evaluate system design decisions from multiple architectural perspectives.

## Participants
- **[Systems Architect](../architecture/systems-architect.md)** - Scalability, boundaries, state management
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Attack surface, auth model, data protection
- **[Failure Engineer](../operations_reliability/failure-engineer.md)** - Resilience, recovery, blast radius
- **[Infrastructure Engineer](../operations_reliability/infrastructure-engineer.md)** - Deployment, networking, operations
- **[API Designer](../architecture/api-designer.md)** - Contracts, versioning, consumer experience

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Present design context and constraints
3. Each participant evaluates from their lens
4. Surface cross-cutting concerns
5. Debate tradeoffs explicitly
6. Present findings using the [severity scale](../_shared/severity-scale.md)
7. Converge on recommendations

## Output Format
### Per Participant
- Perspective name
- Architectural concerns
- Risk assessment
- Recommended changes

### Consolidated
- Architectural strengths
- Critical risks
- Design modifications required
- Tradeoffs accepted (with rationale)
- Go/No-Go recommendation

## Constraints
- Consider both build and operate phases
- Identify hidden assumptions
- Prefer reversible decisions
- Document rejected alternatives

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
